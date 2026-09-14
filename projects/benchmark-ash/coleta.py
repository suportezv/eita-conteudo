#!/usr/bin/env python3
"""Baixa os criativos dos anuncios da Ash (top 30 por impressoes), extrai frames e transcreve.

Pre-requisito: *.fbcdn.net liberado no environment (o proxy bloqueia por padrao).
Entrada:  ads-top30.json (extraido da Biblioteca de Anuncios)
Saida:    media/<id>.mp4, media/<id>_c<i>.jpg, frames/<id>/f01..f06.jpg, transcricoes.json
Uso:      python3 coleta.py            # tudo
          python3 coleta.py --so-video # pula imagens
"""
import json, os, subprocess, sys, time, urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
ADS = json.load(open(os.path.join(RAIZ, "ads-top30.json")))
MEDIA, FRAMES = os.path.join(RAIZ, "media"), os.path.join(RAIZ, "frames")
os.makedirs(MEDIA, exist_ok=True); os.makedirs(FRAMES, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
KEY = [l.strip().split("=", 1)[1] for l in open("/workspace/browser-use/video-use/.env")
       if l.startswith("ELEVENLABS_API_KEY=")][0]


def baixa(url, destino):
    if os.path.exists(destino) and os.path.getsize(destino) > 10_000:
        return True
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "180", "-A", UA, "-o", destino,
                        "-w", "%{http_code}", url], capture_output=True, text=True)
    ok = r.stdout.strip().startswith("200") and os.path.getsize(destino) > 10_000
    if not ok:
        print("  FALHA", destino, r.stdout.strip(), r.stderr.strip()[:100], flush=True)
    return ok


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=nw=1:nk=1", p], capture_output=True, text=True).stdout or 0)


def frames(vid, pasta, n=6):
    os.makedirs(pasta, exist_ok=True)
    d = dur(vid)
    for i in range(n):
        t = max(0.2, d * (i + 0.5) / n)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", vid, "-frames:v", "1",
                        "-vf", "scale=540:-2", os.path.join(pasta, f"f{i+1:02d}.jpg")], check=False)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.1", "-i", vid, "-frames:v", "1",
                    "-vf", "scale=540:-2", os.path.join(pasta, "f00_abertura.jpg")], check=False)
    return d


def transcreve(vid):
    mp3 = vid[:-4] + ".mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-vn", "-ac", "1", "-ar", "44100",
                    "-c:a", "libmp3lame", "-b:a", "96k", mp3], check=True)
    b = "----ash"
    data = open(mp3, "rb").read()
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\n"
            f"Content-Type: audio/mpeg\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
                                 headers={"xi-api-key": KEY, "Content-Type": f"multipart/form-data; boundary={b}"})
    d = json.loads(urllib.request.urlopen(req, timeout=240).read())
    return {"texto": d.get("text", ""), "idioma": d.get("language_code"),
            "palavras": [{"t": round(w["start"], 2), "w": w["text"]} for w in d.get("words", []) if w.get("type") == "word"]}


def main():
    so_video = "--so-video" in sys.argv
    saida = os.path.join(RAIZ, "transcricoes.json")
    res = json.load(open(saida)) if os.path.exists(saida) else {}
    for a in ADS:
        aid = a["id"]
        if a.get("video_hd") or a.get("video_sd"):
            vid = os.path.join(MEDIA, f"{aid}.mp4")
            print(f"[{aid}] video", flush=True)
            if baixa(a.get("video_hd") or a["video_sd"], vid):
                d = frames(vid, os.path.join(FRAMES, aid))
                if aid not in res:
                    try:
                        res[aid] = {"dur": round(d, 1), **transcreve(vid)}
                        print(f"   {d:.1f}s | {res[aid]['texto'][:110]}", flush=True)
                    except Exception as e:
                        print("   transcricao falhou:", e, flush=True)
                json.dump(res, open(saida, "w"), ensure_ascii=False, indent=1)
            if a.get("video_preview"):
                baixa(a["video_preview"], os.path.join(MEDIA, f"{aid}_preview.jpg"))
        if not so_video:
            for i, c in enumerate(a.get("cards", [])):
                if c.get("image"):
                    baixa(c["image"], os.path.join(MEDIA, f"{aid}_c{i}.jpg"))
                if c.get("video"):
                    vid = os.path.join(MEDIA, f"{aid}_c{i}.mp4")
                    if baixa(c["video"], vid):
                        frames(vid, os.path.join(FRAMES, f"{aid}_c{i}"))
    print("\nfeito:", len(res), "videos transcritos;", len(os.listdir(MEDIA)), "arquivos em media/")


if __name__ == "__main__":
    main()
