"""Gera as cartelas de 5s dos blocos ainda nao gravados (Arthur e Ana).

Sao marcadores de duracao, nao arte final: o objetivo e a previa manter a ordem
do roteiro e deixar obvio o que falta gravar.
"""
import subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

EDIT = pathlib.Path(__file__).resolve().parent
OUT  = EDIT / "placeholders"; OUT.mkdir(exist_ok=True)
W, H, FPS, DUR = 1920, 1080, 30, 5

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FUNDO, CLARO, MEIO, ACENTO = (18, 20, 26), (238, 240, 245), (130, 136, 150), (255, 190, 60)

CARTELAS = [
    (2, "ARTHUR", "Tecnologia atual e salto tecnológico", "1min50"),
    (3, "ANA",    "Saúde emocional, comportamento e rigor científico", "1min30"),
]

def centro(d, y, txt, fonte, cor):
    x0, y0, x1, y1 = d.textbbox((0, 0), txt, font=fonte)
    d.text(((W - (x1 - x0)) / 2 - x0, y), txt, font=fonte, fill=cor)
    return y1 - y0

for n, quem, titulo, alvo in CARTELAS:
    img = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(img)
    # Barra de acento: sinaliza "pendente" sem precisar de texto extra.
    d.rectangle([0, 0, W, 8], fill=ACENTO)
    centro(d, 355, f"BLOCO {n}", ImageFont.truetype(REG, 44), MEIO)
    centro(d, 425, quem, ImageFont.truetype(FONT, 150), CLARO)
    centro(d, 605, titulo, ImageFont.truetype(REG, 46), MEIO)
    centro(d, 700, f"a gravar  ·  duração prevista {alvo}", ImageFont.truetype(FONT, 40), ACENTO)
    png = OUT / f"bloco{n}.png"
    img.save(png)
    # Audio mudo com o mesmo formato dos brutos, senao o concat recusa o segmento.
    subprocess.run([
        "ffmpeg", "-v", "error", "-loop", "1", "-i", str(png),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-t", str(DUR), "-r", str(FPS),
        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-y", str(OUT / f"bloco{n}.mp4")], check=True)
    print(f"bloco{n}.mp4  {quem}")
