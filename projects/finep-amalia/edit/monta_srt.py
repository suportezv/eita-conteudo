"""Monta o master.srt na linha do tempo de saida, frase a frase.

O build_master_srt do video-use quebra em blocos de 2 palavras e joga tudo em
caixa alta, que e estilo de rede social. Aqui o video e institucional: legenda
frase a frase, caixa natural, para acompanhar a leitura sem competir com ela.

Tempo de saida = palavra.inicio - inicio_do_segmento + deslocamento_do_segmento,
senao a legenda desalinha depois da concatenacao dos segmentos.
"""
import json, pathlib

EDIT = pathlib.Path(__file__).resolve().parent
MAX_CHARS = 42      # por linha
MAX_LINHAS = 2
FIM_FRASE = ".?!"
PAUSA = 0.45        # silencio que tambem quebra a legenda

def palavras_em(src, a, b):
    d = json.load(open(EDIT / "transcripts" / f"{src}.json"))
    return [w for w in d["words"]
            if w.get("type") == "word" and w["start"] >= a - 0.01 and w["end"] <= b + 0.01]

def ts(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000)
    return f"{h:02d}:{m:02d}:{ms//1000:02d},{ms%1000:03d}"

def quebra(txt, largura):
    linhas, atual = [], ""
    for p in txt.split():
        if atual and len(atual) + 1 + len(p) > largura:
            linhas.append(atual); atual = p
        else:
            atual = f"{atual} {p}".strip()
    if atual: linhas.append(atual)
    return linhas

def monta():
    edl = json.load(open(EDIT / "edl.json"))
    entradas, desloc = [], 0.0
    for r in edl["ranges"]:
        src, ini, fim = r["source"], float(r["start"]), float(r["end"])
        dur = fim - ini
        if not (EDIT / "transcripts" / f"{src}.json").exists():
            desloc += dur; continue                      # cartelas nao tem fala
        grupo = []
        for w in palavras_em(src, ini, fim):
            grupo.append(w)
            txt = " ".join(x["text"].strip() for x in grupo)
            prox_pausa = False
            fecha = w["text"].strip()[-1:] in FIM_FRASE
            # Cabe em duas linhas? Se passar, fecha aqui.
            estourou = len(quebra(txt, MAX_CHARS)) > MAX_LINHAS
            if estourou:
                grupo.pop()
                # Recua ate a ultima virgula: quebrar em "quando uma / organizacao"
                # atrapalha a leitura, quebrar depois da virgula nao.
                corte = len(grupo)
                for i in range(len(grupo) - 1, max(0, len(grupo) - 5), -1):
                    if grupo[i-1]["text"].strip()[-1:] in ",;:":
                        corte = i; break
                entradas.append((grupo[:corte], ini, desloc))
                grupo = grupo[corte:] + [w]
            elif fecha:
                entradas.append((grupo, ini, desloc)); grupo = []
        if grupo:
            entradas.append((grupo, ini, desloc))
        desloc += dur

    # Quebra tambem em pausas longas dentro de uma frase comprida.
    saida, n = [], 0
    for grupo, ini, desloc in entradas:
        if not grupo: continue
        sub, partes = [], []
        for i, w in enumerate(grupo):
            sub.append(w)
            if i + 1 < len(grupo) and grupo[i+1]["start"] - w["end"] > PAUSA and len(sub) >= 3:
                partes.append(sub); sub = []
        if sub: partes.append(sub)
        for parte in partes:
            a = parte[0]["start"] - ini + desloc
            b = parte[-1]["end"] - ini + desloc + 0.18   # respiro para leitura
            txt = " ".join(x["text"].strip() for x in parte)
            saida.append([a, b, txt])

    # O respiro de 0.18s no fim pode invadir a legenda seguinte, e libass
    # desenha as duas ao mesmo tempo. Limita cada fim ao inicio da proxima.
    saida.sort(key=lambda e: e[0])
    for i in range(len(saida) - 1):
        saida[i][1] = min(saida[i][1], saida[i+1][0] - 0.02)
    saida = [e for e in saida if e[1] > e[0] + 0.15]

    linhas = []
    for n, (a, b, txt) in enumerate(saida, 1):
        linhas.append(f"{n}\n{ts(a)} --> {ts(b)}\n" + "\n".join(quebra(txt, MAX_CHARS)) + "\n")
    (EDIT / "master.srt").write_text("\n".join(linhas), encoding="utf-8")
    return len(saida)

n = monta()
print(f"master.srt: {n} legendas")
import subprocess
print(subprocess.run(["head","-14",str(EDIT/"master.srt")],capture_output=True,text=True).stdout)
