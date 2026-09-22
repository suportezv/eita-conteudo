"""Motor dos overlays: desenha quadro a quadro em RGBA e sai em qtrle com alfa.

Sistema visual vem do manual da marca EITA: verde-acqua #48EBAD como fio
condutor (tem que aparecer em toda peca), azul #477EA1 de apoio, League Spartan
como unica familia. O manual pede "seriedade sem rigidez" e "sem excessos",
entao nada de caixa colorida cheia: regua de acento, tipografia e respiro.

Easing sempre cubico. Linear parece robo.
"""
import subprocess, shutil, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

_medidor = ImageDraw.Draw(Image.new("RGBA", (4, 4)))

def larg(txt, f):
    """Largura de um texto, para dimensionar a sombra ao conteudo."""
    x0, _, x1, _ = _medidor.textbbox((0, 0), txt, font=f)
    return x1 - x0

def scrim(img, x0, y0, x1, y1, forca=190, alfa=1.0, fade=210,
          fade_l=None, fade_r=None, fade_t=None, fade_b=None):
    """Sombra atras do texto: cheia sobre a caixa, esmaecendo `fade` px para fora.

    A caixa e o conteudo, nao um retangulo arbitrario. As primeiras versoes
    usavam medidas fixas muito maiores que o texto, e a borda do degrade caia no
    meio da cena (entre o lettering e a pessoa), lendo como um painel cinza mal
    posicionado em vez de sombra. Dimensionando pelo texto e deixando o degrade
    acontecer fora dele, a sombra vira contorno do conteudo.

    Quem encosta na borda do quadro passa fade_l=0 para nao criar aresta ali.
    """
    fl = fade if fade_l is None else fade_l
    fr = fade if fade_r is None else fade_r
    ft = fade if fade_t is None else fade_t
    fb = fade if fade_b is None else fade_b
    X0, Y0 = int(max(0, x0 - fl)), int(max(0, y0 - ft))
    X1, Y1 = int(min(W, x1 + fr)), int(min(H, y1 + fb))
    w, h = X1 - X0, Y1 - Y0
    if w <= 0 or h <= 0 or alfa <= 0.003: return
    xs = np.arange(X0, X1)[None, :].astype(np.float64)
    ys = np.arange(Y0, Y1)[:, None].astype(np.float64)
    def rampa(v, lo, hi, f_lo, f_hi):
        a = np.ones_like(v)
        if f_lo > 0: a = np.minimum(a, np.clip((v - (lo - f_lo)) / f_lo, 0, 1))
        if f_hi > 0: a = np.minimum(a, np.clip(((hi + f_hi) - v) / f_hi, 0, 1))
        return a
    m = rampa(xs, x0, x1, fl, fr) * rampa(ys, y0, y1, ft, fb)
    m = (m ** 1.4 * forca * alfa).astype(np.uint8)
    faixa = Image.fromarray(np.dstack([np.zeros_like(m)] * 3 + [m]), "RGBA")
    img.alpha_composite(faixa, (X0, Y0))

# -------- render -------------------------------------------------------------
def sombra_do_conteudo(camada, raio=16, ganho=2.6):
    """Sombra tirada do proprio desenho, nao de uma caixa atras dele.

    Toda versao anterior punha um retangulo escuro atras do texto. Por mais que
    se ajustasse tamanho e posicao, a borda do retangulo caia em algum lugar da
    cena e lia como um painel cinza mal colocado. Borrando o alfa do proprio
    conteudo a sombra vira contorno do texto: acompanha a forma, nao tem aresta
    e some sozinha onde nao ha desenho.
    """
    alfa = camada.getchannel("A").filter(ImageFilter.GaussianBlur(raio))
    alfa = alfa.point(lambda v: min(255, int(v * ganho)))
    s = Image.new("RGBA", camada.size, (0, 0, 0, 0))
    s.putalpha(alfa)
    return Image.alpha_composite(s, camada)

def render(nome, dur, desenha, fps=FPS, sombra=True):
    """desenha(img, draw, t) -> None, para t em segundos.

    sombra=False para as pecas que ja escurecem o quadro inteiro (`veu`): ali a
    sombra sairia do veu e cobriria tudo.
    """
    tmp = SAIDA / f".{nome}"
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    n = int(round(dur * fps))
    for i in range(n):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        desenha(img, ImageDraw.Draw(img), i / fps)
        if sombra:
            img = sombra_do_conteudo(img)
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
