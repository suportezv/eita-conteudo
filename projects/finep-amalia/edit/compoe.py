"""Composicao final: base -> overlays -> LEGENDA POR ULTIMO -> mix -> loudnorm.

A ordem e regra de producao, nao gosto: overlay depois da legenda esconde a
legenda. Cada overlay leva setpts=PTS-STARTPTS+T/TB para o quadro 0 dele cair
no inicio da janela, senao aparece o meio da animacao.

Audio: fala + trilha com ducking (sidechain pela propria fala) + leito de SFX.
"""
import subprocess, pathlib, sys, json
sys.path.insert(0, '.')
from pecas import PECAS

EDIT = pathlib.Path(__file__).resolve().parent
RAIZ = EDIT.parents[2]
BASE = EDIT / "base_preview.mp4"   # render.py sufixa o nome no modo preview
SAIDA = EDIT.parent / "renders" / "previa-v2.mp4"
SAIDA.parent.mkdir(exist_ok=True)

# Sem PlayRes no SRT o libass assume 384x288 e TODAS as medidas de estilo vivem
# nesse espaco, nao em pixels. FontSize 13 da ~49px em 1080p: pequena, como
# pedido. As margens tambem: 180 de cada lado (a primeira tentativa) sobrava 24
# de 384 de largura util e cada palavra virava uma linha. 40 deixa ~79% do
# quadro, que e onde a quebra de 42 caracteres do monta_srt.py cabe.
ESTILO = ("FontName=League Spartan,FontSize=13,Bold=0,"
          "PrimaryColour=&H00FFFFFF,OutlineColour=&HC8000000,BackColour=&H00000000,"
          "BorderStyle=1,Outline=2,Shadow=1,Spacing=0.4,"
          "Alignment=2,MarginV=52,MarginL=40,MarginR=40")

ent = ["-i", str(BASE)]
filtros = []
for i, (nome, ini, dur, _) in enumerate(PECAS, start=1):
    ent += ["-i", str(EDIT / "animacoes" / f"{nome}.mov")]
    filtros.append(f"[{i}:v]setpts=PTS-STARTPTS+{ini}/TB[a{i}]")

atual = "[0:v]"
for i, (nome, ini, dur, _) in enumerate(PECAS, start=1):
    prox = f"[v{i}]"
    filtros.append(f"{atual}[a{i}]overlay=enable='between(t,{ini:.3f},{ini+dur:.3f})'{prox}")
    atual = prox

srt = str(EDIT / "master.srt").replace("'", r"\'")
filtros.append(f"{atual}subtitles='{srt}':fontsdir='{RAIZ / 'assets' / 'fonts'}'"
               f":force_style='{ESTILO}'[outv]")

n_trilha = len(PECAS) + 1
n_sfx = len(PECAS) + 2
ent += ["-i", str(EDIT / "audio" / "trilha.wav"), "-i", str(EDIT / "audio" / "sfx.wav")]
filtros += [
    "[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[fala][chave]",
    # Trilha baixa e ainda abaixando quando alguem fala: em video institucional
    # de 7 minutos a musica sustenta, nao disputa.
    f"[{n_trilha}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=-21dB[mus]",
    "[mus][chave]sidechaincompress=threshold=0.02:ratio=7:attack=12:release=420:makeup=1[musd]",
    f"[{n_sfx}:a]aformat=sample_rates=44100:channel_layouts=stereo[sfx]",
    "[fala][musd][sfx]amix=inputs=3:duration=first:normalize=0[outa]",
]

tmp = EDIT / "_composto.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-stats", *ent,
                "-filter_complex", ";".join(filtros),
                "-map", "[outv]", "-map", "[outa]",
                "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
                "-c:a", "aac", "-b:a", "192k", "-y", str(tmp)], check=True)

# loudnorm em duas passagens: a primeira mede, a segunda aplica.
med = subprocess.run(["ffmpeg", "-v", "info", "-i", str(tmp),
                      "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
d = json.loads(med[med.rindex("{"):med.rindex("}")+1])
print("  medido:", {k: d[k] for k in ("input_i","input_tp","input_lra")})
subprocess.run(["ffmpeg", "-v", "error", "-stats", "-i", str(tmp),
                "-af", f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={d['input_i']}:"
                       f"measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:"
                       f"measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-y", str(SAIDA)], check=True)
tmp.unlink()
print("pronto:", SAIDA)
