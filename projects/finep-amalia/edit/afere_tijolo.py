"""Mede a inclinacao localizando a MESMA linha de argamassa em varias colunas.

Em vez de pontuar a imagem inteira (que nao deu sinal: o pico ficava 1.1x acima
da media), aqui rastreamos uma borda horizontal concreta. Em cada coluna estreita
somamos o gradiente vertical e pegamos o y de maior resposta dentro de uma janela
de busca; a reta ajustada por esses pontos da o angulo. Positivo = a linha desce
para a direita.
"""
import subprocess, sys, io
import numpy as np
from PIL import Image

def quadro(video, t):
    raw = subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",video,"-frames:v","1",
                          "-f","image2pipe","-vcodec","png","-"], capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert("L")

def rastreia(a, x0, x1, y0, y1, n=12, larg=24):
    """y da borda horizontal mais forte em n colunas entre x0 e x1."""
    pts = []
    for xc in np.linspace(x0, x1 - larg, n).astype(int):
        faixa = a[y0:y1, xc:xc+larg].astype(np.float64)
        perfil = np.abs(np.diff(faixa, axis=0)).sum(axis=1)
        if perfil.max() < perfil.mean() * 2.0:   # sem borda clara nesta coluna
            continue
        pts.append((xc + larg/2, y0 + int(np.argmax(perfil))))
    return np.array(pts, dtype=float)

def angulo(pts):
    if len(pts) < 4: return None, None, 0
    x, y = pts[:,0], pts[:,1]
    # Ajuste robusto: descarta os 25% piores residuos antes de refazer a reta.
    for _ in range(3):
        c = np.polyfit(x, y, 1)
        r = np.abs(y - np.polyval(c, x))
        keep = r <= np.quantile(r, 0.75) + 1e-9
        if keep.sum() < 4: break
        x, y = x[keep], y[keep]
    c = np.polyfit(x, y, 1)
    resid = float(np.std(y - np.polyval(c, x)))
    return float(np.degrees(np.arctan(c[0]))), resid, len(x)

if __name__ == "__main__":
    video = sys.argv[1]; x0,x1,y0,y1 = map(int, sys.argv[2:6])
    tempos = [float(t) for t in sys.argv[6:]] or [20,45,70,95,120]
    print("== validacao (giro conhecido):")
    im = quadro(video, tempos[0])
    for v in (0.0, 1.0, -1.5):
        g = np.asarray(im.rotate(v, resample=Image.BICUBIC, center=((x0+x1)/2,(y0+y1)/2)))
        a, r, n = angulo(rastreia(g, x0, x1, y0, y1))
        # rotate() gira no sentido anti-horario, entao o esperado troca de sinal.
        print(f"   injetado {-v:+.2f} -> medido {a:+.2f}  (residuo {r:.1f}px, {n} pts)" if a else "   sem borda")
    print("== medicao real:")
    vals = []
    for t in tempos:
        a, r, n = angulo(rastreia(np.asarray(quadro(video, t)), x0, x1, y0, y1))
        if a is None: print(f"   t={t}s sem borda clara"); continue
        vals.append(a); print(f"   t={t:5.0f}s  {a:+.2f} graus  (residuo {r:.1f}px, {n} pts)")
    if vals: print(f"   MEDIANA: {np.median(vals):+.2f} graus")
