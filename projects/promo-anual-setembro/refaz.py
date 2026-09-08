#!/usr/bin/env python3
"""Regera blocos com defeito, validando cada tentativa por transcricao Scribe."""
import json, os, re, subprocess, urllib.request

KEY = [l.strip().split("=", 1)[1] for l in open("/workspace/browser-use/video-use/.env")
       if l.startswith("ELEVENLABS_API_KEY=")][0]
VOICE = "XsU4z9JE7JPZzkVPg4GW"
TTS = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128"
STT = "https://api.elevenlabs.io/v1/speech-to-text"
OUT = os.path.dirname(os.path.abspath(__file__))

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

# palavras que precisam aparecer, e quantas vezes o nome Eita deve aparecer
EXIGE = {
    "hook": (["impossível", "alguém do seu lado"], 0),
    "b1":   (["acalmar", "no impulso", "clareza", "sozinha", "aperta"], 0),
    "b2":   (["setembro amarelo", "promoção", "desconto", "whatsapp", "preço do ano"], 2),
    "b3":   (["escuta", "organiza", "pensamentos", "piloto automático", "melhor caminho",
              "ritmo", "anônimo"], 1),
    "b4":   (["por mês", "só agora", "volta ao normal", "link na bio"], 0),
}
PROIBIDO = ["email", "e-mail"]

CFG = {
    "A": {"model_id": "eleven_v3",
          "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": True}},
    "B": {"model_id": "eleven_v3",
          "voice_settings": {"stability": 0.0, "similarity_boost": 0.8, "use_speaker_boost": True}},
    "C": {"model_id": "eleven_multilingual_v2",
          "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.55,
                             "use_speaker_boost": True, "speed": 1.0}},
}


def transcreve(wav):
    boundary = "----eita"
    with open(wav, "rb") as f:
        data = f.read()
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\n"
        f"Content-Type: audio/wav\r\n\r\n"
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        STT, data=body,
        headers={"xi-api-key": KEY, "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read()).get("text", "")


def valida(bid, txt):
    t = txt.lower()
    faltando = [k for k in EXIGE[bid][0] if k not in t]
    if faltando:
        return False, f"faltou {faltando}"
    achou = [p for p in PROIBIDO if p in t]
    if achou:
        return False, f"palavra estranha {achou}"
    nome_ok = len(re.findall(r"\beita\b", t))
    if nome_ok != EXIGE[bid][1]:
        errado = re.findall(r"\b(eta|ita|aita|eitcha)\b", t)
        return False, f"nome saiu {nome_ok}x (esperado {EXIGE[bid][1]}); ruido {errado}"
    if re.search(r"\b(\w+)[- ]\1\b", t):
        return False, "gagueira"
    return True, "ok"


def gera(var, bid, tent=5):
    for n in range(1, tent + 1):
        payload = {"text": TEXTOS[bid], **CFG[var]}
        req = urllib.request.Request(
            TTS, data=json.dumps(payload).encode(),
            headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        mp3, wav = os.path.join(OUT, f"{var}-{bid}.mp3"), os.path.join(OUT, f"{var}-{bid}.wav")
        with urllib.request.urlopen(req, timeout=240) as r, open(mp3, "wb") as f:
            f.write(r.read())
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
             "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse",
             "-ar", "44100", "-ac", "1", wav], check=True)
        ok, motivo = valida(bid, transcreve(wav))
        print(f"  {var}-{bid} tentativa {n}: {motivo}")
        if ok:
            return True
    return False


if __name__ == "__main__":
    import sys
    alvos = [a.split("-") for a in sys.argv[1:]]
    for var, bid in alvos:
        gera(var, bid)
