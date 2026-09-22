"""Localiza o rosto de cada locutor no quadro, para o zoom mirar nele.

Amostra varios instantes de cada master e tira a mediana das deteccoes. Os dois
ficam sentados e quase parados, entao um centro por fonte e mais estavel que
seguir o rosto quadro a quadro, que produziria tremor.
"""
import subprocess, io, json, pathlib, sys
import numpy as np, cv2
from PIL import Image

EDIT = pathlib.Path(__file__).resolve().parent
CASCATA = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def quadro(v, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(v),
                          "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True).stdout
    return np.asarray(Image.open(io.BytesIO(raw)).convert("RGB"))

def acha(v, tempos):
    achados = []
    for t in tempos:
        img = quadro(v, t)
        cinza = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = CASCATA.detectMultiScale(cinza, 1.1, 6, minSize=(90, 90))
        if len(faces) == 0: continue
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])   # a maior = o locutor
        achados.append((x + w/2, y + h/2, w))
    if not achados: return None
    a = np.array(achados)
    return dict(cx=float(np.median(a[:,0])), cy=float(np.median(a[:,1])),
                largura=float(np.median(a[:,2])), n=len(achados))

if __name__ == "__main__":
    saida = {}
    for f in sorted((EDIT / "normalizado").glob("*.mp4")):
        dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                                    "-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
        tempos = list(np.linspace(dur*0.08, dur*0.92, 14))
        r = acha(f, tempos)
        saida[f.stem] = r
        print(f"  {f.stem:16s} {r}")
    json.dump(saida, open(EDIT / "rostos.json", "w"), indent=2)
