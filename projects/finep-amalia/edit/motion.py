"""Motor dos overlays: desenha quadro a quadro em RGBA e sai em qtrle com alfa.

Sistema visual vem do manual da marca EITA: verde-acqua #48EBAD como fio
condutor (tem que aparecer em toda peca), azul #477EA1 de apoio, League Spartan
como unica familia. O manual pede "seriedade sem rigidez" e "sem excessos",
entao nada de caixa colorida cheia: regua de acento, tipografia e respiro.

Easing sempre cubico. Linear parece robo.
"""
import subprocess, shutil, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ   = pathlib.Path(__file__).resolve().parents[3]
FONTES = RAIZ / "assets" / "fonts"
SAIDA  = pathlib.Path(__file__).resolve().parent / "animacoes"
W, H, FPS = 1920, 1080, 30

ACQUA  = (0x48, 0xEB, 0xAD)
AZUL   = (0x47, 0x7E, 0xA1)
BRANCO = (0xFF, 0xFF, 0xFF)
CINZA  = (0xB8, 0xC2, 0xC6)
PRETO  = (0x00, 0x00, 0x00)

def fonte(peso, tam):
    return ImageFont.truetype(str(FONTES / f"LeagueSpartan-{peso}.ttf"), tam)

# -------- easing -------------------------------------------------------------
def out_cubic(t):    return 1 - (1 - max(0.0, min(1.0, t))) ** 3
def in_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 4*t**3 if t < 0.5 else 1 - (-2*t + 2)**3 / 2

def janela(t, ini, dur, saida=None, fade_out=0.45):
    """Progresso 0..1 de uma entrada, e alfa de saida no fim da peca."""
    p = out_cubic((t - ini) / dur) if dur > 0 else 1.0
    a = 1.0
    if saida is not None and t > saida - fade_out:
        a = max(0.0, 1 - (t - (saida - fade_out)) / fade_out)
    return p, a

# -------- primitivas ---------------------------------------------------------
def texto(d, xy, txt, f, cor, alfa=1.0, ancora="la"):
    if alfa <= 0.003: return
    d.text(xy, txt, font=f, fill=(*cor, int(255 * alfa)), anchor=ancora)

def largura(d, txt, f):
    x0, _, x1, _ = d.textbbox((0, 0), txt, font=f)
    return x1 - x0

def regua(d, x, y, comp, alt, cor, alfa=1.0):
    if alfa <= 0.003 or comp <= 0: return
    d.rectangle([x, y, x + comp, y + alt], fill=(*cor, int(255 * alfa)))

def scrim(img, x0, y0, x1, y1, forca=170, alfa=1.0, suave=0.26):
    """Degrade escuro atras do texto: garante leitura sobre qualquer imagem.

    A queda e nos dois eixos. A primeira versao caia so na vertical e deixava
    aresta reta nas laterais, o que aparecia como uma caixa cinza sobre a cena.
    `suave` e a fracao de cada lado gasta no degrade.
    """
    w, h = int(x1 - x0), int(y1 - y0)
    if w <= 0 or h <= 0 or alfa <= 0.003: return
    ys = np.linspace(0, 1, h)[:, None]
    xs = np.linspace(0, 1, w)[None, :]
    def queda(v):
        # 1 no miolo, 0 nas pontas, com joelho suave.
        d = np.minimum(v, 1 - v) / suave
        return np.clip(d, 0, 1) ** 1.5
    m = (queda(ys) * queda(xs) * forca * alfa).astype(np.uint8)
    faixa = Image.fromarray(np.dstack([np.zeros_like(m)] * 3 + [m]), "RGBA")
    img.alpha_composite(faixa, (int(x0), int(y0)))

# -------- render -------------------------------------------------------------
def render(nome, dur, desenha, fps=FPS):
    """desenha(img, draw, t) -> None, para t em segundos."""
    tmp = SAIDA / f".{nome}"
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    n = int(round(dur * fps))
    for i in range(n):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        desenha(img, ImageDraw.Draw(img), i / fps)
        img.save(tmp / f"{i:05d}.png")
    destino = SAIDA / f"{nome}.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-framerate", str(fps),
                    "-i", str(tmp / "%05d.png"),
                    "-c:v", "qtrle", "-pix_fmt", "argb", "-y", str(destino)], check=True)
    shutil.rmtree(tmp)
    return destino


def veu(img, t, dur, entrada=0.55, saida=0.55, forca=216):
    """Escurece o quadro inteiro para a ilustracao virar o assunto.

    Grafico fino por cima de cabeca falante nao le: a linha cruza o rosto e as
    duas coisas se estragam. Escurecendo tudo, a ilustracao vira um momento
    proprio enquanto a fala continua por baixo.
    """
    a = min(out_cubic(t / entrada), out_cubic((dur - t) / saida))
    if a <= 0.003: return 0.0
    img.alpha_composite(Image.new("RGBA", (W, H), (4, 8, 10, int(forca * a))))
    return a
