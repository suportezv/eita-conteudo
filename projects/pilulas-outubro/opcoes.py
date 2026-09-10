#!/usr/bin/env python3
"""Gera varias tomadas do MESMO bloco, com temperos diferentes, para a equipe escolher.

Existe porque a validacao automatica so garante as palavras: entrega (robotico,
gagueira, entonacao) so ouvido humano julga. Em vez de tentar adivinhar de novo,
entrega opcoes lado a lado.

Uso: python3 opcoes.py 05:LIP 07:VO
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import PILULAS
from gera import KEY, TTS, normaliza, post, transcreve, valida

RAIZ = os.path.dirname(os.path.abspath(__file__))
OPCOES = os.path.join(RAIZ, "opcoes")
TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")

# temperos deliberadamente diferentes entre si, para as opcoes nao saírem iguais
TEMPEROS = [
    ("A", "mais solta",        {"stability": 0.30, "style": 0.60}),
    ("B", "receita padrão",    {"stability": 0.45, "style": 0.55}),
    ("C", "firme e expressiva",{"stability": 0.60, "style": 0.70}),
    ("D", "mais contida",      {"stability": 0.50, "style": 0.40}),
]


def gera(pid, rot, tent=5):
    blocos = PILULAS[pid]
    i = [r for r, _ in blocos].index(rot)
    texto = dict(blocos)[rot]
    prev = blocos[i - 1][1] if i > 0 else None
    nxt = blocos[i + 1][1] if i < len(blocos) - 1 else None
    os.makedirs(OPCOES, exist_ok=True)
    feitas = []
    for letra, apelido, ajuste in TEMPEROS:
        destino = os.path.join(OPCOES, f"{pid}-{rot}-{letra}.mp3")
        for n in range(1, tent + 1):
            vs = {"similarity_boost": 0.8, "use_speaker_boost": True, "speed": 1.0, **ajuste}
            payload = {"text": texto, "model_id": "eleven_multilingual_v2", "voice_settings": vs}
            if prev:
                payload["previous_text"] = prev
            if nxt:
                payload["next_text"] = nxt
            raw = post(TTS, json.dumps(payload).encode(),
                       {"xi-api-key": KEY, "Content-Type": "application/json"})
            with open("/tmp/.op.mp3", "wb") as f:
                f.write(raw)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/.op.mp3", "-af", TRIM,
                            "-ar", "44100", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "192k",
                            destino], check=True)
            ok, motivo = valida(texto, transcreve(destino))
            if ok and "eita" in normaliza(texto):
                ok, motivo = valida(texto, transcreve(destino))
            if ok:
                d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "default=nw=1:nk=1", destino],
                                   capture_output=True, text=True).stdout.strip()
                print(f"  {pid}-{rot} opcao {letra} ({apelido}): ok, {float(d):.1f}s", flush=True)
                feitas.append((letra, apelido, destino))
                break
            print(f"  {pid}-{rot} opcao {letra} t{n}: {motivo}", flush=True)
        else:
            print(f"  {pid}-{rot} opcao {letra}: nao passou", flush=True)
    return feitas


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        pid, rot = arg.split(":", 1)
        print(f"Bloco {pid}-{rot}", flush=True)
        gera(pid, rot)
