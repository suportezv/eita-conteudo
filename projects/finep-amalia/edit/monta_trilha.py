"""Costura os leitos de 22s numa trilha continua de 444s, bloco a bloco.

A API do ElevenLabs entrega no maximo ~22s, entao a trilha e montada com
acrossfade entre leitos. A ordem nao e aleatoria: cada bloco recebe uma
progressao que acompanha o que esta sendo dito, e os leitos compartilham
instrumento e tonalidade para o conjunto soar como uma peca so.
"""
import subprocess, pathlib, json

EDIT = pathlib.Path(__file__).resolve().parent
AUD = EDIT / "audio"
XF = 3.0          # duracao do acrossfade entre leitos
PASSO = 22.0 - XF  # quanto cada leito adiciona ao total

# Por bloco: (inicio na saida, fim, sequencia de leitos)
# bloco 1 abre minimo e ganha corpo; as cartelas ficam suspensas; o 5 tem o
# pulso dos dados; o 6 resolve.
# Sem as cartelas de Arthur e Ana, tudo depois de 161.55 anda 10s para tras.
BLOCOS = [
    ("b1", 0.00,   161.55, ["a","a","b","b","c","b","b","d","b"]),
    ("b4", 161.55, 252.89, ["b","b","c","b","d","b"]),
    ("b5", 252.89, 343.77, ["c","c","b","c","c","b"]),
    ("b6", 343.77, 433.81, ["b","d","d","b","d","d"]),
]

def costura(seq, destino):
    ent, filtros, rotulo = [], [], None
    for i, s in enumerate(seq):
        ent += ["-i", str(AUD / f"leito-{s}.wav")]
    for i in range(len(seq)):
        filtros.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo[s{i}]")
    rotulo = "[s0]"
    for i in range(1, len(seq)):
        novo = f"[x{i}]"
        filtros.append(f"{rotulo}[s{i}]acrossfade=d={XF}:c1=tri:c2=tri{novo}")
        rotulo = novo
    filtros.append(f"{rotulo}anull[out]")
    subprocess.run(["ffmpeg", "-v", "error", *ent,
                    "-filter_complex", ";".join(filtros), "-map", "[out]",
                    "-c:a", "pcm_s16le", "-y", str(destino)], check=True)

partes = []
for nome, ini, fim, seq in BLOCOS:
    dur = fim - ini
    precisa = int(-(-(dur - 22.0) // PASSO)) + 1 if dur > 22 else 1
    seq = (seq * ((precisa // len(seq)) + 1))[:max(precisa, 1)]
    bruto = AUD / f"_bloco-{nome}-bruto.wav"
    costura(seq, bruto)
    # Corta no tamanho exato do bloco, com respiro nas pontas.
    destino = AUD / f"bloco-{nome}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(bruto), "-t", f"{dur:.3f}",
                    "-af", f"afade=t=in:st=0:d=1.6,afade=t=out:st={max(0,dur-1.8):.3f}:d=1.8",
                    "-c:a", "pcm_s16le", "-y", str(destino)], check=True)
    bruto.unlink()
    real = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                                 "-of","csv=p=0",str(destino)],capture_output=True,text=True).stdout)
    print(f"  {nome:9s} {ini:7.2f}-{fim:7.2f} ({dur:6.2f}s)  {len(seq)} leitos -> {real:.2f}s")
    partes.append((destino, ini, dur))

# Junta os blocos na linha do tempo cheia.
ent, filtros = [], []
for i, (p, ini, dur) in enumerate(partes):
    ent += ["-i", str(p)]
    filtros.append(f"[{i}:a]adelay={int(ini*1000)}|{int(ini*1000)}[d{i}]")
mix = "".join(f"[d{i}]" for i in range(len(partes)))
filtros.append(f"{mix}amix=inputs={len(partes)}:duration=longest:normalize=0[out]")
subprocess.run(["ffmpeg", "-v", "error", *ent, "-filter_complex", ";".join(filtros),
                "-map", "[out]", "-t", "433.81", "-c:a", "pcm_s16le",
                "-y", str(AUD / "trilha.wav")], check=True)
print("trilha.wav:", subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
      "-of","csv=p=0",str(AUD/"trilha.wav")],capture_output=True,text=True).stdout.strip())
