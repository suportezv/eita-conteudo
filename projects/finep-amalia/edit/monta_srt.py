"""Monta o master.srt na linha do tempo de saida.

Regras que o video pede:
  - legenda fiel ao que foi dito, sem gaguejo nem marcacao de ruido
  - quebra por frase, nunca no meio de um sintagma: a versao anterior partia
    quando estourava a segunda linha e produzia coisas como "olhando pra /
    tras." ou "colocou ela no mundo / real."
  - legenda e motion nunca dividem a tela, com uma excecao: o GC de credito,
    que e discreto e nao rouba a leitura

Tempo de saida = palavra.inicio - inicio_do_segmento + deslocamento_do_segmento.
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

EDIT = pathlib.Path(__file__).resolve().parent
MAX_CHARS, MAX_LINHAS = 42, 2
PAUSA_FRASE = 0.9          # silencio longo tambem fecha legenda
RESP_MOTION = 0.25
MIN_DUR, RESPIRO = 0.85, 0.20

# Nomes proprios que o Scribe erra.
NOMES = {"Aita": "EITA", "Aíta": "EITA", "Artur": "Arthur",
         "Normalize": "Normalyze", "Amália": "AMALIA", "Amalia": "AMALIA",
         "Amalía": "AMALIA"}
# Gagueira: legenda o que a pessoa quis dizer, nao o tropeco.
GAGUEIRA = {"pri-privacidade": "privacidade", "obje--": "", "de--": ""}

def limpa(tok):
    nucleo = tok.strip()
    pont = ""
    m = re.match(r"^(.*?)([,.;:!?]*)$", nucleo)
    if m: nucleo, pont = m.group(1), m.group(2)
    if nucleo.lower() in GAGUEIRA:
        nucleo = GAGUEIRA[nucleo.lower()]
        if not nucleo: return ""
    for errado, certo in NOMES.items():
        if nucleo == errado: nucleo = certo
    return nucleo + pont

def palavras_na_saida():
    """Todas as palavras do corte, ja com tempo na linha de tempo final."""
    edl = json.load(open(EDIT / "edl.json"))
    fora, desloc = [], 0.0
    for r in edl["ranges"]:
        src, ini, fim = r["source"], float(r["start"]), float(r["end"])
        tr = EDIT / "transcripts" / f"{src}.json"
        if tr.exists():
            for w in json.load(open(tr))["words"]:
                if w.get("type") != "word": continue         # (palma), (batida)
                if not (ini - 0.01 <= w["start"] and w["end"] <= fim + 0.01): continue
                txt = limpa(w["text"])
                if txt:
                    fora.append({"t": w["start"] - ini + desloc,
                                 "f": w["end"] - ini + desloc, "txt": txt})
        desloc += fim - ini
    return fora

FILLER = {"é", "eh", "ah", "então"}

def tira_filler(fr):
    """Remove hesitacao no comeco da frase ("E, pesquisas periodicas...").

    E marcacao de fala, nao conteudo: legendar isso so atrapalha a leitura.
    """
    while (len(fr) > 3 and fr[0]["txt"].lower().rstrip(",") in FILLER
           and fr[0]["txt"].endswith(",")):
        fr = fr[1:]
    return fr

def frases(ws):
    """Agrupa em frases: fecha em . ? ! ou em silencio longo."""
    out, atual = [], []
    for i, w in enumerate(ws):
        atual.append(w)
        fecha = w["txt"][-1:] in ".?!"
        pausa = i + 1 < len(ws) and ws[i+1]["t"] - w["f"] > PAUSA_FRASE
        if fecha or pausa:
            out.append(tira_filler(atual)); atual = []
    if atual: out.append(tira_filler(atual))
    return out

def linhas(txt):
    ls, cur = [], ""
    for p in txt.split():
        if cur and len(cur) + 1 + len(p) > MAX_CHARS: ls.append(cur); cur = p
        else: cur = f"{cur} {p}".strip()
    if cur: ls.append(cur)
    return ls

def cabe(ws):
    return len(linhas(" ".join(w["txt"] for w in ws))) <= MAX_LINHAS

def parte(ws):
    """Divide a frase em legendas, preferindo cortar depois de pontuacao.

    Divide sempre ao meio da parte que ainda nao cabe, procurando o respiro mais
    proximo do meio. Assim as duas metades ficam parecidas, em vez de uma cheia
    e uma com duas palavras.
    """
    if cabe(ws): return [ws]
    meio = len(ws) // 2
    RESPIRO_TOK = (",", ";", ":")
    candidatos = sorted(range(1, len(ws)), key=lambda i: abs(i - meio))
    corte = next((i for i in candidatos if ws[i-1]["txt"][-1:] in RESPIRO_TOK), None)
    if corte is None:
        CONJ = {"e", "mas", "que", "porque", "ou", "para", "pra", "com", "como", "quando"}
        corte = next((i for i in candidatos if ws[i]["txt"].lower() in CONJ), meio)
    return parte(ws[:corte]) + parte(ws[corte:])

CAUDA = {"e", "ou", "mas", "que", "de", "da", "do", "a", "o", "em", "com",
         "para", "pra", "por", "no", "na", "ao", "se", "the"}

def ajeita(chunks):
    """Duas correcoes depois da divisao.

    1. Conjuncao ou preposicao pendurada no fim ("percebe o risco psicossocial
       ou") passa para a legenda seguinte, que e onde ela pertence.
    2. Legenda curta demais vira orfa na tela; junta com a vizinha se couber.
    """
    for _ in range(3):
        mudou = False
        for i in range(len(chunks) - 1):
            while (len(chunks[i]) > 1
                   and chunks[i][-1]["txt"].strip(",.;:").lower() in CAUDA
                   and cabe([chunks[i][-1]] + chunks[i+1])):
                chunks[i+1].insert(0, chunks[i].pop()); mudou = True
        juntos, i = [], 0
        while i < len(chunks):
            if (i + 1 < len(chunks)
                    and len(" ".join(w["txt"] for w in chunks[i])) < 22
                    and cabe(chunks[i] + chunks[i+1])):
                juntos.append(chunks[i] + chunks[i+1]); i += 2; mudou = True
            else:
                juntos.append(chunks[i]); i += 1
        chunks = juntos
        if not mudou: break
    return chunks

def janelas_sem_legenda():
    """Motion que toma a tela. O GC de credito fica de fora: e discreto e o
    cliente pediu legenda durante os creditos."""
    from pecas import PECAS
    return [(i, i + d) for n, i, d, _f in PECAS if not n.startswith("gc-")]

def ts(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000)
    return f"{h:02d}:{m:02d}:{ms//1000:02d},{ms%1000:03d}"

def monta():
    itens = []
    for fr in frases(palavras_na_saida()):
        for ch in ajeita(parte(fr)):
            itens.append([ch[0]["t"], ch[-1]["f"] + RESPIRO,
                          " ".join(w["txt"] for w in ch)])

    # Fora o que cai sobre um motion; o resto e aparado nas bordas.
    recortado = []
    for a, b, txt in itens:
        pedacos = [(a, b)]
        for ja, jb in janelas_sem_legenda():
            ja, jb = ja - RESP_MOTION, jb + RESP_MOTION
            novos = []
            for x, y in pedacos:
                if y <= ja or x >= jb: novos.append((x, y)); continue
                if x < ja: novos.append((x, ja))
                if y > jb: novos.append((jb, y))
            pedacos = novos
        for x, y in pedacos:
            if y - x >= MIN_DUR: recortado.append([x, y, txt])

    recortado.sort(key=lambda e: e[0])
    for i in range(len(recortado) - 1):
        recortado[i][1] = min(recortado[i][1], recortado[i+1][0] - 0.02)
    recortado = [e for e in recortado if e[1] - e[0] >= 0.4]

    saida = []
    for n, (a, b, txt) in enumerate(recortado, 1):
        saida.append(f"{n}\n{ts(a)} --> {ts(b)}\n" + "\n".join(linhas(txt)) + "\n")
    (EDIT / "master.srt").write_text("\n".join(saida), encoding="utf-8")
    return len(saida)

print(f"master.srt: {monta()} legendas")
