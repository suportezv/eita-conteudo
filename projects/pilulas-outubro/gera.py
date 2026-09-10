#!/usr/bin/env python3
"""Gera os audios das pilulas de outubro na receita aprovada, validando cada bloco.

Receita (CLAUDE.md, aprovada pela equipe em 2026-09-08):
  eleven_multilingual_v2, stability 0.45, similarity 0.8, style 0.55,
  use_speaker_boost, speed 1.0, blocos longos, mesmos parametros em toda a peca.

Validacao de cada tentativa por transcricao Scribe:
  1. o texto falado bate com o roteiro (cobertura de palavras);
  2. o nome "Eita" sai com o ditongo (dupla leitura nos blocos que o contem);
  3. sem gagueira.
"""
import json, os, re, subprocess, sys, time, unicodedata, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import PILULAS

KEY = [l.strip().split("=", 1)[1] for l in open("/workspace/browser-use/video-use/.env")
       if l.startswith("ELEVENLABS_API_KEY=")][0]
VOICE = "XsU4z9JE7JPZzkVPg4GW"
TTS = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128"
STT = "https://api.elevenlabs.io/v1/speech-to-text"

RECEITA = {
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.55,
                       "use_speaker_boost": True, "speed": 1.0},
}
RUIDO = re.compile(r"\b(eta|aeta|aita|ita|aeita|reita|rita|eitcha|aitya)\b")
COBERTURA_MIN = 0.85


def normaliza(txt):
    t = unicodedata.normalize("NFKD", txt.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", t)


def palavras(txt):
    return [w for w in normaliza(txt).split() if len(w) >= 4]


def post(url, data, headers, tent=4):
    for n in range(tent):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=240) as r:
                return r.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if n == tent - 1:
                raise
            time.sleep(2 ** n)


def transcreve(path):
    b = "----eita"
    data = open(path, "rb").read()
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\n"
            f"Content-Type: audio/wav\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode()
    raw = post(STT, body, {"xi-api-key": KEY,
                           "Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(raw).get("text", "")


def valida(texto, ouvido):
    t = normaliza(ouvido)
    esperadas = palavras(texto)
    achadas = sum(1 for w in esperadas if w in t)
    cob = achadas / len(esperadas) if esperadas else 1.0
    if cob < COBERTURA_MIN:
        faltando = [w for w in esperadas if w not in t][:6]
        return False, f"cobertura {cob:.0%} (faltou {faltando})"
    n_esp = len(re.findall(r"\beita\b", normaliza(texto)))
    n_ouv = len(re.findall(r"\beita\b", t))
    ruido = RUIDO.findall(t)
    if n_ouv != n_esp or ruido:
        return False, f"nome {n_ouv}/{n_esp} ruido={ruido}"
    if re.search(r"\b(\w+)[- ]\1\b", t):
        return False, "gagueira"
    return True, f"ok (cobertura {cob:.0%})"


def gera_bloco(pid, rotulo, texto, prev, nxt, outdir, tent=8):
    tem_nome = "eita" in normaliza(texto)
    base = os.path.join(outdir, f"{pid}-{rotulo}")
    for n in range(1, tent + 1):
        payload = dict(RECEITA, text=texto)
        if prev:
            payload["previous_text"] = prev
        if nxt:
            payload["next_text"] = nxt
        raw = post(TTS, json.dumps(payload).encode(),
                   {"xi-api-key": KEY, "Content-Type": "application/json"})
        with open(base + ".raw.mp3", "wb") as f:
            f.write(raw)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", base + ".raw.mp3", "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
             "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse",
             "-ar", "44100", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "192k", base + ".mp3"],
            check=True)
        ok, motivo = valida(texto, transcreve(base + ".mp3"))
        if ok and tem_nome:  # bloco com o nome pede confirmacao em segunda leitura
            ok, motivo = valida(texto, transcreve(base + ".mp3"))
            motivo = "2 leituras " + motivo
        print(f"  {pid}-{rotulo} t{n}: {motivo}", flush=True)
        if ok:
            os.remove(base + ".raw.mp3")
            d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "default=nw=1:nk=1", base + ".mp3"],
                               capture_output=True, text=True).stdout.strip()
            return float(d)
    return None


def main():
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
    os.makedirs(outdir, exist_ok=True)
    alvos = sys.argv[1:] or list(PILULAS)
    falhas, total = [], 0.0
    for pid in alvos:
        blocos = PILULAS[pid]
        print(f"Pilula {pid}", flush=True)
        for i, (rotulo, texto) in enumerate(blocos):
            destino = os.path.join(outdir, f"{pid}-{rotulo}.mp3")
            if os.path.exists(destino):
                print(f"  {pid}-{rotulo}: ja existe, pulando", flush=True)
                continue
            prev = blocos[i - 1][1] if i > 0 else None
            nxt = blocos[i + 1][1] if i < len(blocos) - 1 else None
            d = gera_bloco(pid, rotulo, texto, prev, nxt, outdir)
            if d is None:
                falhas.append(f"{pid}-{rotulo}")
            else:
                total += d
    print(f"\nTerminado. Duracao somada: {total:.1f}s", flush=True)
    if falhas:
        print("NAO passaram na validacao: " + ", ".join(falhas), flush=True)


if __name__ == "__main__":
    main()
