#!/usr/bin/env python3
"""Mede acusticamente se uma tomada soa viva ou robotica.

A validacao por transcricao so garante que as palavras estao certas. Ela nao ve
entrega. Estas medidas veem:

  melodia   variacao da altura da voz (em semitons). Fala robotica e plana.
  enfase    variacao de volume entre as silabas. Fala robotica e uniforme.
  respiro   quantidade e tamanho das pausas internas.
  ritmo     variacao da duracao das palavras (fala humana acelera e desacelera).

Calibrado contra tomadas que a equipe aprovou e tomadas que a equipe reprovou.
"""
import json, os, subprocess, sys, wave
import numpy as np

SR = 16000


def carrega(path):
    wav = "/tmp/.q.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", str(SR), "-ac", "1",
                    "-c:a", "pcm_s16le", wav], check=True)
    with wave.open(wav) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return x


def f0_frames(x, win=0.040, hop=0.010, fmin=70, fmax=350):
    """Altura da voz quadro a quadro, por autocorrelacao."""
    n, h = int(win * SR), int(hop * SR)
    lo, hi = int(SR / fmax), int(SR / fmin)
    saida = []
    for i in range(0, len(x) - n, h):
        q = x[i:i + n] * np.hanning(n)
        e = np.sqrt(np.mean(q ** 2))
        if e < 0.008:
            saida.append(0.0)
            continue
        q = q - q.mean()
        ac = np.correlate(q, q, "full")[n - 1:]
        if ac[0] <= 0:
            saida.append(0.0)
            continue
        ac = ac / ac[0]
        seg = ac[lo:hi]
        if len(seg) == 0:
            saida.append(0.0)
            continue
        k = int(np.argmax(seg))
        saida.append(SR / (lo + k) if seg[k] > 0.3 else 0.0)
    return np.array(saida)


def energia_db(x, win=0.030, hop=0.010):
    n, h = int(win * SR), int(hop * SR)
    e = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, h)])
    return 20 * np.log10(np.maximum(e, 1e-6))


def medidas(path, palavras=None):
    x = carrega(path)
    f0 = f0_frames(x)
    voz = f0[f0 > 0]
    m = {}
    if len(voz) > 20:
        st = 12 * np.log2(voz / np.median(voz))
        m["melodia"] = float(np.percentile(st, 92) - np.percentile(st, 8))
        m["melodia_dp"] = float(np.std(st))
    else:
        m["melodia"] = m["melodia_dp"] = 0.0
    db = energia_db(x)
    ativo = db[db > db.max() - 35]
    m["enfase"] = float(np.std(ativo)) if len(ativo) else 0.0
    # respiros: trechos abaixo de -35 dB do pico, com pelo menos 120 ms
    baixo = db <= db.max() - 35
    respiros, corrida = [], 0
    for b in baixo:
        corrida = corrida + 1 if b else 0
        if not b and corrida:
            respiros.append(corrida * 0.010)
            corrida = 0
    respiros = [r for r in respiros if r >= 0.12]
    m["respiros"] = len(respiros)
    m["dur"] = len(x) / SR
    m["respiros_por_min"] = len(respiros) / (m["dur"] / 60) if m["dur"] else 0
    if palavras and len(palavras) > 3:
        d = np.array([w["end"] - w["start"] for w in palavras])
        d = d[d > 0]
        m["ritmo"] = float(np.std(d) / np.mean(d)) if len(d) else 0.0
        m["palavras_por_min"] = len(palavras) / (m["dur"] / 60)
    return m


def linha(rot, m):
    return (f"{rot:22} melodia {m['melodia']:5.1f}st  dp {m['melodia_dp']:4.1f}  "
            f"enfase {m['enfase']:4.1f}dB  respiros {m['respiros']:2d}"
            + (f"  ritmo {m['ritmo']:.2f}" if "ritmo" in m else ""))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    for p in sys.argv[1:]:
        print(linha(os.path.basename(p), medidas(p)))
