"""Mede a inclinacao do horizonte de um video.

Linhas horizontais da cena viram picos no gradiente vertical. Para achar o angulo,
somamos o gradiente ao longo de retas de varias inclinacoes: o angulo certo e o
que concentra a energia em poucas linhas. O deslocamento e feito por cisalhamento
com shift inteiro por coluna, nao por rotacao, porque rotacionar interpola, borra
o gradiente e enviesa o resultado para zero (a primeira versao disto media +0.00
em tudo justamente por isso).

Mede em varios quadros e tira a mediana, para nao depender de um instante em que
a pessoa se mexeu na frente da cena.
"""
import subprocess, sys, io
import numpy as np
from PIL import Image

def quadro(video, t, larg=960):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1",
         "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True).stdout
    im = Image.open(io.BytesIO(raw)).convert("L")
    return im.resize((larg, int(im.height * larg / im.width)))

def foco(grad, ang, margem):
    """Energia concentrada por linha depois de cisalhar por `ang` graus.

    `margem` e fixa para toda a varredura: se cada angulo usasse a sua, os
    angulos maiores somariam menos linhas e pareceriam mais concentrados so por
    isso (era o que fazia a medicao encostar sempre no limite da faixa).
    """
    h, w = grad.shape
    desl = np.round(np.arange(w) * np.tan(np.radians(ang))).astype(int)
    col = np.arange(w)
    # Cada coluna sobe/desce um numero inteiro de pixels; nada e interpolado.
    idx = np.arange(margem, h - margem)[:, None] + desl[None, :]
    somas = grad[idx, col[None, :]].sum(axis=1)
    n = len(somas)
    return float(n * (somas ** 2).sum() / (somas.sum() ** 2 + 1e-9))

def angulo(grad, faixa=4.0, passo=0.05):
    h, w = grad.shape
    margem = int(np.ceil(w * np.tan(np.radians(faixa)))) + 1
    if margem >= h // 2:
        return 0.0
    angs = np.arange(-faixa, faixa + passo / 2, passo)
    pontos = [foco(grad, a, margem) for a in angs]
    return float(angs[int(np.argmax(pontos))])

def grad_de(im):
    a = np.asarray(im, dtype=np.float64)
    return np.abs(np.diff(a, axis=0))

def mede(video, tempos):
    return [angulo(grad_de(quadro(video, t))) for t in tempos]

if sys.argv[1] == "--teste":
    # Ferramenta so vale se acertar um angulo conhecido: gira 1.5 graus de proposito.
    im = quadro(sys.argv[2], 30)
    for verdade in (0.0, 1.5, -2.0):
        girada = im.rotate(verdade, resample=Image.BICUBIC)
        m = int(min(girada.size) * 0.15)
        rec = angulo(grad_de(girada.crop((m, m, girada.width - m, girada.height - m))))
        print(f"  injetado {verdade:+.2f}  ->  medido {rec:+.2f}  (erro {rec - verdade:+.2f})")
    sys.exit()

for video in sys.argv[1:]:
    r = mede(video, [20, 45, 70, 95])
    print(f"{video.split('/')[-1]:22s} quadros={[f'{x:+.2f}' for x in r]}  mediana={np.median(r):+.2f} graus")
