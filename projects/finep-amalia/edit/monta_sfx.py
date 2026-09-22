"""Leito de efeitos: um som curto e discreto em cada entrada de motion.

"Sonorize levemente" e literal: o efeito marca a entrada do grafismo e some.
Se competir com a fala ele vira ruido, entao tudo entra bem abaixo e curto.
"""
import subprocess, pathlib, sys
sys.path.insert(0, '.')
from pecas import PECAS, SOCIOS

AUD = pathlib.Path(__file__).resolve().parent / "audio"
DUR = 433.81

eventos = []   # (tempo, arquivo, ganho_db)
for nome, ini, dur, _ in PECAS:
    if nome == "socios":
        # um toque por socio, no momento em que o Clesio cita cada um
        for _n, _c, _i, atraso in SOCIOS:
            eventos.append((ini + atraso, "sfx-marca", -20))
    elif nome.startswith("num-"):
        eventos.append((ini, "sfx-entra", -19))
        eventos.append((ini + 0.9, "sfx-conta", -24))
    elif nome.startswith("ilu-") or nome.startswith("titulo") or nome.startswith("cartela"):
        eventos.append((ini, "sfx-entra", -17))
    else:
        eventos.append((ini, "sfx-entra", -21))

ent, filtros = [], []
for i, (t, arq, db) in enumerate(eventos):
    ent += ["-i", str(AUD / f"{arq}.mp3")]
    filtros.append(f"[{i}:a]volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[e{i}]")
mix = "".join(f"[e{i}]" for i in range(len(eventos)))
filtros.append(f"{mix}amix=inputs={len(eventos)}:duration=longest:normalize=0,"
               f"aformat=sample_rates=44100:channel_layouts=stereo[out]")
subprocess.run(["ffmpeg", "-v", "error", *ent, "-filter_complex", ";".join(filtros),
                "-map", "[out]", "-t", f"{DUR}", "-c:a", "pcm_s16le",
                "-y", str(AUD / "sfx.wav")], check=True)
print(f"sfx.wav: {len(eventos)} eventos")
