#!/usr/bin/env python3
"""Regera blocos gravando a pilula inteira numa tomada continua e recortando depois.

Motivo: bloco curto (os LIP tem so duas frases) nao da embalo pra voz. A tomada
sai robotica, gagueja e as vezes ganha um som fantasma na entrada. Gravando a
pilula toda de uma vez a prosodia flui, e o corte por marcacao de palavras
devolve os arquivos separados que o roteiro pede.

Uso:  python3 continuo.py 06            -> refaz todos os blocos da pilula 06
      python3 continuo.py 05:LIP        -> refaz so o LIP, aproveitando a tomada
      python3 continuo.py 07:VO 11:LIP  -> varios de uma vez
"""
import json, os, re, subprocess, sys, time, unicodedata, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import PILULAS
from gera import KEY, RECEITA, STT, TTS, RUIDO, normaliza, palavras, post, transcreve, valida

RAIZ = os.path.dirname(os.path.abspath(__file__))
AUDIOS = os.path.join(RAIZ, "audios")
TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")


def transcreve_palavras(path):
    """Transcricao com marcacao de tempo por palavra."""
    b = "----eita"
    data = open(path, "rb").read()
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\n"
            f"Content-Type: audio/mpeg\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode()
    raw = post(STT, body, {"xi-api-key": KEY,
                           "Content-Type": f"multipart/form-data; boundary={b}"})
    d = json.loads(raw)
    ws = [w for w in d.get("words", []) if w.get("type") == "word"]
    return d.get("text", ""), ws


def limpa(w):
    t = unicodedata.normalize("NFKD", w.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", t)


def acha_inicio(ws, alvo, desde):
    """Onde o bloco 'alvo' comeca na sequencia de palavras ouvidas."""
    chave = [limpa(x) for x in alvo.split()[:4] if limpa(x)]
    ouvidas = [limpa(w["text"]) for w in ws]
    melhor, pontos = None, 0
    for i in range(desde, len(ouvidas) - len(chave) + 1):
        p = sum(1 for k, c in enumerate(chave) if ouvidas[i + k] == c)
        if p > pontos:
            melhor, pontos = i, p
        if p == len(chave):
            break
    if pontos < max(2, len(chave) - 1):
        return None
    return melhor


def grava_pilula(pid, quais, tent=6):
    blocos = PILULAS[pid]
    texto = " ".join(t for _, t in blocos)
    bruto = os.path.join(AUDIOS, f".tomada-{pid}.mp3")
    for n in range(1, tent + 1):
        raw = post(TTS, json.dumps(dict(RECEITA, text=texto)).encode(),
                   {"xi-api-key": KEY, "Content-Type": "application/json"})
        with open(bruto, "wb") as f:
            f.write(raw)
        ouvido, ws = transcreve_palavras(bruto)

        # a tomada inteira precisa bater com o roteiro
        ok, motivo = valida(texto, ouvido)
        if not ok:
            print(f"  {pid} tomada {n}: {motivo}", flush=True)
            continue
        # nada de som fantasma antes da primeira palavra
        primeira = [limpa(x) for x in blocos[0][1].split() if limpa(x)][0]
        if ws and limpa(ws[0]["text"]) != primeira:
            print(f"  {pid} tomada {n}: entrada fantasma \"{ws[0]['text']}\"", flush=True)
            continue

        # onde cada bloco comeca
        cortes, pos, falhou = [], 0, False
        for rot, t in blocos:
            i = acha_inicio(ws, t, pos)
            if i is None:
                falhou = True
                break
            cortes.append(i)
            pos = i + 1
        if falhou:
            print(f"  {pid} tomada {n}: nao localizei as fronteiras", flush=True)
            continue

        # corta no meio do silencio entre um bloco e o proximo
        limites = []
        for k, i in enumerate(cortes):
            ini = 0.0 if k == 0 else (ws[i - 1]["end"] + ws[i]["start"]) / 2
            fim = None if k == len(cortes) - 1 else None
            limites.append(ini)
        limites.append(None)

        recortes, problema = {}, None
        for k, (rot, t) in enumerate(blocos):
            destino = os.path.join(AUDIOS, f".novo-{pid}-{rot}.mp3")
            cmd = ["ffmpeg", "-v", "error", "-y", "-i", bruto, "-ss", f"{limites[k]:.3f}"]
            if limites[k + 1] is not None:
                cmd += ["-to", f"{limites[k + 1]:.3f}"]
            cmd += ["-af", TRIM, "-ar", "44100", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "192k", destino]
            subprocess.run(cmd, check=True)
            if rot in quais:  # so valido o que vou usar
                ok2, m2 = valida(t, transcreve(destino))
                if ok2 and "eita" in normaliza(t):
                    ok2, m2 = valida(t, transcreve(destino))
                if not ok2:
                    problema = f"{rot}: {m2}"
                    break
            recortes[rot] = destino
        if problema:
            print(f"  {pid} tomada {n}: recorte {problema}", flush=True)
            continue

        for rot in quais:
            final = os.path.join(AUDIOS, f"{pid}-{rot}.mp3")
            os.replace(recortes[rot], final)
            d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "default=nw=1:nk=1", final],
                               capture_output=True, text=True).stdout.strip()
            print(f"  {pid}-{rot}: refeito, {float(d):.1f}s", flush=True)
        for f in list(recortes.values()) + [bruto]:
            if os.path.exists(f):
                os.remove(f)
        return True
    print(f"  {pid}: NAO consegui em {tent} tomadas", flush=True)
    return False


def main():
    pedidos = {}
    for arg in sys.argv[1:]:
        if ":" in arg:
            pid, rot = arg.split(":", 1)
            pedidos.setdefault(pid, []).append(rot)
        else:
            pedidos[arg] = [r for r, _ in PILULAS[arg]]
    for pid, quais in pedidos.items():
        print(f"Pilula {pid} (refazendo {', '.join(quais)})", flush=True)
        grava_pilula(pid, quais)


if __name__ == "__main__":
    main()
