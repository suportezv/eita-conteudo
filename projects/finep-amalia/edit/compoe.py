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

# Contorno opaco: no ASS o primeiro byte da cor e alfa INVERTIDO, entao o
# &HC8... de antes deixava a borda 78% transparente e o texto sumia sobre
# fundo claro. &H00 e preto solido.
# Borda fina: Outline=2 no espaco de 288 do libass da ~7.5px em 1080p, que o
# cliente apontou como grossa demais. Com 1 fica ~3.7px, so o contorno de leitura.
# Sem PlayRes no SRT o libass assume 384x288 e TODAS as medidas de estilo vivem
# nesse espaco, nao em pixels. FontSize 13 da ~49px em 1080p: pequena, como
# pedido. As margens tambem: 180 de cada lado (a primeira tentativa) sobrava 24
# de 384 de largura util e cada palavra virava uma linha. 40 deixa ~79% do
# quadro, que e onde a quebra de 42 caracteres do monta_srt.py cabe.
ESTILO = ("FontName=League Spartan,FontSize=13,Bold=0,"
          "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,"
          "BorderStyle=1,Outline=1,Shadow=0,Spacing=0.4,"
          "Alignment=2,MarginV=52,MarginL=40,MarginR=40")

# Punch-ins discretos nos pontos de enfase. Ficam fora das janelas de motion de
# tela cheia, senao o zoom mexeria numa imagem que esta escurecida de qualquer
# forma. zoompan e nao crop: crop nao aceita `t` em w/h.
ENFASE = [76.0, 103.5, 150.5, 175.0, 232.0, 272.0, 337.0, 420.0]
AMP, SUBIDA, SUSTENTA, DESCIDA = 0.075, 0.95, 1.5, 1.15

def expressao_zoom(fps=30):
    """z(t) = 1 + soma de pulsos suaves. Meio cosseno na subida e na descida:
    rampa linear em movimento de camera denuncia que e sintetico."""
    T = f"(on/{fps})"
    termos = []
    for t0 in ENFASE:
        t1, t2, t3 = t0 + SUBIDA, t0 + SUBIDA + SUSTENTA, t0 + SUBIDA + SUSTENTA + DESCIDA
        sobe = f"(0.5-0.5*cos(PI*({T}-{t0})/{SUBIDA:.3f}))"
        desce = f"(0.5-0.5*cos(PI*({t3:.3f}-{T})/{DESCIDA:.3f}))"
        termos.append(
            f"if(between({T},{t0:.3f},{t1:.3f}),{AMP}*{sobe},"
            f"if(between({T},{t1:.3f},{t2:.3f}),{AMP},"
            f"if(between({T},{t2:.3f},{t3:.3f}),{AMP}*{desce},0)))")
    return "1+" + "+".join(termos)

# Centro do zoom puxado para a direita e para cima: nos dois enquadramentos a
# pessoa esta a direita do centro e o rosto fica na metade de cima.
ZOOM = (f"zoompan=z='{expressao_zoom()}':d=1:"
        "x='iw*0.55-(iw/zoom/2)':y='ih*0.42-(ih/zoom/2)':s=1920x1080:fps=30")

ent = ["-i", str(BASE)]
filtros = [f"[0:v]{ZOOM}[base]"]
for i, (nome, ini, dur, _) in enumerate(PECAS, start=1):
    ent += ["-i", str(EDIT / "animacoes" / f"{nome}.mov")]
    filtros.append(f"[{i}:v]setpts=PTS-STARTPTS+{ini}/TB[a{i}]")

atual = "[base]"
for i, (nome, ini, dur, _) in enumerate(PECAS, start=1):
    prox = f"[v{i}]"
    # eof_action=pass e repeatlast=0 sao obrigatorios: sem eles o framesync do
    # overlay segura o quadro principal enquanto espera uma entrada que so comeca
    # la na frente, duplica quadros e empurra o fim do video. A primeira versao
    # fez exatamente isso: aos 442s aparecia o Clesio no lugar da Marina.
    filtros.append(f"{atual}[a{i}]overlay=enable='between(t,{ini:.3f},{ini+dur:.3f})'"
                   f":eof_action=pass:repeatlast=0{prox}")
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
