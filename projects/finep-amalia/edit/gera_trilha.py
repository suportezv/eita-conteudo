"""Gera os leitos da trilha no ElevenLabs sound-generation.

A direcao e "institucional contido": piano e pad, pulso suave, quase sem
percussao. Todos os prompts compartilham instrumento, andamento e tonalidade
para que os leitos conversem entre si; o que muda e a textura e a intensidade,
que e o que faz cada bloco acompanhar o que esta sendo dito.

A API entrega no maximo ~22s por chamada, entao os blocos sao montados depois
costurando estes leitos com acrossfade.
"""
import os, pathlib, sys, urllib.request, json, time

SAIDA = pathlib.Path(__file__).resolve().parent / "audio"
SAIDA.mkdir(exist_ok=True)
CHAVE = os.environ["ELEVENLABS_API_KEY"]

BASE = ("solo felt piano and sustained warm string pad, A minor, 68 bpm, "
        "no drums, no percussion hits, institutional documentary underscore, "
        "restrained and spacious, clean studio recording, loopable")

LEITOS = {
    "leito-a": f"{BASE}, very sparse, single piano notes with long silence between them, introspective opening",
    "leito-b": f"{BASE}, gentle repeating four note piano motif over soft pad, steady and calm",
    "leito-c": f"{BASE}, same piano motif with a subtle low synth pulse underneath, quiet forward momentum",
    "leito-d": f"{BASE}, fuller warm strings joining the piano, hopeful resolving harmony",
    "leito-e": f"{BASE}, suspended pad swell with light shimmer, transitional, unresolved",
}
EFEITOS = {
    "sfx-entra":  "very short soft airy whoosh transition, subtle, clean, no music, 1 second",
    "sfx-marca":  "single soft muted marimba note, warm and short, no reverb tail, no music",
    "sfx-conta":  "very soft high digital tick, minimal UI sound, short, no music",
}

def gera(nome, prompt, seg, influencia=0.45):
    destino = SAIDA / f"{nome}.mp3"
    if destino.exists() and destino.stat().st_size > 5000:
        print(f"  ja existe: {nome}"); return
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/sound-generation",
        data=json.dumps({"text": prompt, "duration_seconds": seg,
                         "prompt_influence": influencia}).encode(),
        headers={"xi-api-key": CHAVE, "Content-Type": "application/json"})
    for tentativa in range(3):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                destino.write_bytes(r.read())
            print(f"  {nome}: {destino.stat().st_size//1024} KB"); return
        except Exception as e:
            print(f"  {nome} falhou ({e}), tentativa {tentativa+1}"); time.sleep(4)
    print(f"  ERRO: {nome} nao gerado")

def nivela(nome, alvo=-18.0):
    """Iguala o leito em -18 LUFS.

    O gerador nao entrega nivel consistente: na primeira leva o leito-d saiu em
    -10.8 LUFS contra -18.9 do leito-b, e na costura isso virava um salto de 6 dB
    aos 6min18 do video. Nivelar antes de costurar resolve na origem.
    """
    import subprocess, json
    src = SAIDA / f"{nome}.mp3"
    dst = SAIDA / f"{nome}.wav"
    med = subprocess.run(["ffmpeg", "-v", "info", "-i", str(src),
                          "-af", f"loudnorm=I={alvo}:TP=-2:LRA=11:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    d = json.loads(med[med.rindex("{"):med.rindex("}")+1])
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-af",
                    f"loudnorm=I={alvo}:TP=-2:LRA=11:measured_I={d['input_i']}:"
                    f"measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:"
                    f"measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true,"
                    f"aformat=sample_rates=44100:channel_layouts=stereo",
                    "-c:a", "pcm_s16le", "-y", str(dst)], check=True)
    print(f"  {nome}: {d['input_i']} -> {alvo} LUFS")

alvo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
if alvo in ("tudo", "leitos"):
    for n, p in LEITOS.items(): gera(n, p, 22)
if alvo in ("tudo", "sfx"):
    for n, p in EFEITOS.items(): gera(n, p, 2, influencia=0.6)
if alvo in ("tudo", "leitos", "nivela"):
    print("nivelando os leitos:")
    for n in LEITOS: nivela(n)
