"""Monta o EDL da previa: corta erros, comprime silencios, ordena pelos blocos.

Regras que o usuario pediu:
  - erros fora (no Clesio a frase da Marina tem tres tentativas; vale a ultima)
  - silencio longo comprimido, sem picotar a leitura
  - Ana (bloco 2 do video) e Arthur entram como cartela de 5s

Toda borda de corte cai em fronteira de palavra vinda do Scribe, e leva padding
para absorver a deriva de 50 a 100ms dos timestamps.
"""
import json, pathlib

EDIT = pathlib.Path(__file__).resolve().parent
NORM = EDIT / "normalizado"

GAP_MAX  = 0.70   # silencio acima disso e ar morto
PAD_IN   = 0.15   # antes da primeira palavra do segmento
PAD_OUT  = 0.20   # depois da ultima -> sobra ~0.35s de ar no lugar do silencio
EDGE_IN  = 0.06   # bordas de um trecho mantido (inicio/fim ou corte de erro)
EDGE_OUT = 0.12

# Trechos a manter por fonte. O que fica de fora e erro ou ar morto de ponta.
MANTER = {
    "marina-bloco1": [(1.10, 163.70)],                       # fim corta a palma
    "marina-bloco4": [(0.84, 92.92)],                        # fim corta a batida
    "clesio-bloco5": [(3.82, 58.68),                         # ate "validacao metodologica"
                      (92.72, 121.74),                       # ultima versao da frase da Marina
                      (124.02, 134.20)],                     # tira a gagueira "Nosso obje--"
    "marina-bloco6": [(0.82, 93.06)],
}

def palavras(fonte):
    d = json.load(open(EDIT / "transcripts" / f"{fonte}.json"))
    return [w for w in d["words"] if w.get("type") == "word"]

def segmentos(fonte):
    """Quebra cada trecho mantido nos silencios longos e devolve os cortes."""
    ws, out = palavras(fonte), []
    for a, b in MANTER[fonte]:
        dentro = [w for w in ws if w["start"] >= a - 0.01 and w["end"] <= b + 0.01]
        if not dentro:
            continue
        ini = dentro[0]["start"] - EDGE_IN
        for i, w in enumerate(dentro[:-1]):
            gap = dentro[i + 1]["start"] - w["end"]
            if gap > GAP_MAX:
                out.append((ini, w["end"] + PAD_OUT))
                ini = dentro[i + 1]["start"] - PAD_IN
        out.append((ini, dentro[-1]["end"] + EDGE_OUT))
    return out

BLOCOS = [
    (1, "Marina", "marina-bloco1"),
    (2, "Arthur", None),
    (3, "Ana",    None),
    (4, "Marina", "marina-bloco4"),
    (5, "Clésio", "clesio-bloco5"),
    (6, "Marina", "marina-bloco6"),
]

ranges, fontes, total = [], {}, 0.0
print(f'{"bloco":22s} {"segs":>5s} {"bruto":>9s} {"cortado":>9s}')
for n, quem, fonte in BLOCOS:
    if fonte is None:
        ranges.append({"source": f"ph{n}", "start": 0.0, "end": 5.0,
                       "beat": f"BLOCO {n} - {quem}", "quote": "(cartela 5s)",
                       "reason": "bruto ainda nao gravado"})
        fontes[f"ph{n}"] = str(EDIT / "placeholders" / f"bloco{n}.mp4")
        total += 5.0
        print(f'{f"{n}. {quem} (cartela)":22s} {1:5d} {"-":>9s} {"5.0s":>9s}')
        continue
    segs = segmentos(fonte)
    bruto = sum(b - a for a, b in MANTER[fonte])
    corte = sum(b - a for a, b in segs)
    for a, b in segs:
        ranges.append({"source": fonte, "start": round(a, 2), "end": round(b, 2),
                       "beat": f"BLOCO {n} - {quem}", "quote": "", "reason": ""})
    fontes[fonte] = str(NORM / f"{fonte}.mp4")
    total += corte
    print(f'{f"{n}. {quem}":22s} {len(segs):5d} {bruto:8.1f}s {corte:8.1f}s')

edl = {"version": 1, "sources": fontes, "ranges": ranges,
       "grade": None, "total_duration_s": round(total, 2)}
(EDIT / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=2))
m, s = divmod(total, 60)
print(f'\n{len(ranges)} segmentos, previa = {int(m)}min{s:04.1f}s')
