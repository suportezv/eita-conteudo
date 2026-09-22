"""Converte tempo de fonte -> tempo de saida, e acha a palavra na saida."""
import json, pathlib, sys
EDIT = pathlib.Path(__file__).resolve().parent
EDL = json.load(open(EDIT / "edl.json"))

def mapa():
    m, desloc = [], 0.0
    for r in EDL["ranges"]:
        d = r["end"] - r["start"]
        m.append((r["source"], r["start"], r["end"], desloc))
        desloc += d
    return m

def para_saida(src, t):
    for s, a, b, off in mapa():
        if s == src and a - 1e-6 <= t <= b + 1e-6:
            return t - a + off
    return None

def acha(src, frase):
    """Primeira ocorrencia de `frase` na transcricao; devolve (ini,fim) na saida."""
    d = json.load(open(EDIT / "transcripts" / f"{src}.json"))
    ws = [w for w in d["words"] if w.get("type") == "word"]
    alvo = frase.lower().split()
    for i in range(len(ws) - len(alvo) + 1):
        if [ws[i+j]["text"].strip(" ,.?!").lower() for j in range(len(alvo))] == alvo:
            a, b = para_saida(src, ws[i]["start"]), para_saida(src, ws[i+len(alvo)-1]["end"])
            if a is not None and b is not None:
                return round(a, 2), round(b, 2)
    return None

if __name__ == "__main__":
    ALVOS = [
        ("marina-bloco1", "tentar entender um filme"),
        ("marina-bloco1", "elevar a inteligência pelo treino da autopercepção"),
        ("marina-bloco1", "trinta e cinco mil usuários"),
        ("marina-bloco1", "mil e duzentos usuários"),
        ("marina-bloco1", "primeira aplicação internacional"),
        ("marina-bloco1", "daí que nasce"),
        ("marina-bloco4", "memória longitudinal"),
        ("clesio-bloco5", "setenta e cinco por cento"),
        ("clesio-bloco5", "duzentas mensagens por mês"),
        ("clesio-bloco5", "vinte e quatro meses"),
        ("clesio-bloco5", "o artur lidera"),
        ("clesio-bloco5", "a ana atua"),
        ("clesio-bloco5", "a marina conecta"),
        ("clesio-bloco5", "eu atuo na gestão"),
        ("marina-bloco6", "linha um"),
        ("marina-bloco6", "sem a gente substituir"),
    ]
    for src, frase in ALVOS:
        r = acha(src, frase)
        print(f'{src:16s} "{frase[:38]:38s}" -> {r}')
