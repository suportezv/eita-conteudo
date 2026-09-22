import sys, subprocess, io, pathlib
sys.path.insert(0, '.')
from PIL import Image, ImageDraw
import pecas
from motion import W, H
ALVOS = sys.argv[1:]
mapa = {n: (i, d, f) for n, i, d, f in pecas.PECAS}
saidas = []
for nome in ALVOS:
    ini, dur, fab = mapa[nome]
    t = float(dur) * 0.72          # perto do fim: tudo ja revelado
    raw = subprocess.run(["ffmpeg","-v","error","-ss",str(ini+t),"-i","../renders/previa-v1.mp4",
                          "-frames:v","1","-f","image2pipe","-vcodec","png","-"],
                         capture_output=True).stdout
    base = Image.open(io.BytesIO(raw)).convert("RGBA")
    cam = Image.new("RGBA", (W, H), (0,0,0,0))
    fab()(cam, ImageDraw.Draw(cam), t)
    p = f"verify/espia-{nome}.png"
    Image.alpha_composite(base, cam).convert("RGB").save(p)
    saidas.append(p)
print(" ".join(saidas))
