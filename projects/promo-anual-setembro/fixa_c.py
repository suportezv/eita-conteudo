#!/usr/bin/env python3
"""Regera os blocos da voz C que contem o nome, com dupla validacao de pronuncia."""
import json, os, re, subprocess, sys, urllib.request

KEY = [l.strip().split("=", 1)[1] for l in open("/workspace/browser-use/video-use/.env")
       if l.startswith("ELEVENLABS_API_KEY=")][0]
TTS = "https://api.elevenlabs.io/v1/text-to-speech/XsU4z9JE7JPZzkVPg4GW?output_format=mp3_44100_128"
STT = "https://api.elevenlabs.io/v1/speech-to-text"

TEXTOS = {
    "hook": "Você não precisa esperar o dia ficar impossível para ter alguém do seu lado.",
    "b1": "Para se acalmar antes de responder no impulso. Para enxergar a situação com mais clareza. "
          "Para não se sentir sozinha quando tudo aperta.",
    "b2": "Neste Setembro Amarelo, acontece a única promoção do ano da Eita. "
          "Plano anual com cinquenta por cento de desconto. "
          "Doze meses com a Eita no seu WhatsApp pelo menor preço do ano.",
    "b3": "A Eita te escuta, organiza seus pensamentos e te ajuda a sair do piloto automático "
          "e a encontrar seu melhor caminho. Vinte e quatro horas. No seu ritmo. Anônimo.",
    "b4": "Menos de treze reais por mês. Só agora. Depois de setembro, o valor volta ao normal. "
          "Link na bio e garante o seu.",
}
ORDEM = ["hook", "b1", "b2", "b3", "b4"]
NOMES = {"hook": 0, "b1": 0, "b2": 2, "b3": 1, "b4": 0}
RUIDO = re.compile(r"\b(eta|aeta|aita|ita|aeita|reita|rita|eitcha)\b")


def transcreve(path):
    b = "----eita"
    data = open(path, "rb").read()
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\n"
            f"Content-Type: audio/wav\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(
        STT, data=body,
        headers={"xi-api-key": KEY, "Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(urllib.request.urlopen(req, timeout=180).read()).get("text", "").lower()


def checa_nome(bid, t):
    n = len(re.findall(r"\beita\b", t))
    ruido = RUIDO.findall(t)
    if n != NOMES[bid] or ruido:
        return False, f"nome {n}/{NOMES[bid]} ruido={ruido}"
    return True, "ok"


def gera(bid, stability, style, tent=8):
    i = ORDEM.index(bid)
    for n in range(1, tent + 1):
        payload = {
            "text": TEXTOS[bid], "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": stability, "similarity_boost": 0.8,
                               "style": style, "use_speaker_boost": True, "speed": 1.0},
        }
        if i > 0:
            payload["previous_text"] = TEXTOS[ORDEM[i - 1]]
        if i < len(ORDEM) - 1:
            payload["next_text"] = TEXTOS[ORDEM[i + 1]]
        req = urllib.request.Request(
            TTS, data=json.dumps(payload).encode(),
            headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        mp3, wav = f"C-{bid}.mp3", f"C-{bid}.wav"
        with urllib.request.urlopen(req, timeout=240) as r, open(mp3, "wb") as f:
            f.write(r.read())
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
             "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse",
             "-ar", "44100", "-ac", "1", wav], check=True)
        ok1, m1 = checa_nome(bid, transcreve(wav))
        if not ok1:
            print(f"  C-{bid} t{n}: {m1}")
            continue
        ok2, m2 = checa_nome(bid, transcreve(wav))
        print(f"  C-{bid} t{n}: leitura1 ok / leitura2 {m2}")
        if ok2:
            return True
    return False


if __name__ == "__main__":
    stab = float(sys.argv[1]) if len(sys.argv) > 1 else 0.45
    for bid in sys.argv[2:] or ["b2", "b3"]:
        if not gera(bid, stab, 0.55):
            print(f"  C-{bid}: NAO passou em {stab}")
