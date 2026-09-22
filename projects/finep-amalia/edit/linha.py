"""Remove as cartelas de Arthur e Ana e desloca a linha do tempo.

Os tempos de todas as pecas, da decupagem de zoom e da trilha foram escritos
contra a linha de tempo COM as cartelas. Em vez de reescrever dezenas de
constantes a mao, o corte e aplicado por uma funcao: o que vem depois do trecho
removido anda para tras, o que vem antes fica onde esta.
"""
import json, pathlib

EDIT = pathlib.Path(__file__).resolve().parent
# Trecho ocupado pelas duas cartelas na linha de tempo antiga.
CORTADOS = [(161.55, 171.55)]

def mapa(t):
    """Tempo antigo -> tempo novo."""
    novo = t
    for a, b in CORTADOS:
        if t >= b: novo -= (b - a)
        elif t > a: novo = a - sum(y - x for x, y in CORTADOS if y <= a)
    return round(novo, 3)

def desloca_pecas(pecas):
    return [(n, mapa(i), d, f) for n, i, d, f in pecas]

def desloca_plano(plano):
    return [(mapa(a), mapa(b), z0, z1) for a, b, z0, z1 in plano]

def edl_sem_cartelas(origem="edl.json", destino="edl-final.json"):
    """EDL sem os segmentos de cartela."""
    edl = json.load(open(EDIT / origem))
    edl["ranges"] = [r for r in edl["ranges"] if not r["source"].startswith("ph")]
    edl["sources"] = {k: v for k, v in edl["sources"].items() if not k.startswith("ph")}
    edl["total_duration_s"] = round(sum(r["end"] - r["start"] for r in edl["ranges"]), 2)
    json.dump(edl, open(EDIT / destino, "w"), ensure_ascii=False, indent=2)
    return edl["total_duration_s"]

if __name__ == "__main__":
    dur = edl_sem_cartelas()
    print(f"edl-final.json: {dur}s ({dur/60:.0f}min{dur%60:04.1f}s)")
    for t in (100.0, 161.0, 171.6, 262.89, 443.81):
        print(f"   {t:7.2f} -> {mapa(t):7.2f}")
