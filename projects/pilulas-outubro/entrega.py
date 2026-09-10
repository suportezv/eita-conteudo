#!/usr/bin/env python3
"""Empacota os audios aprovados no zip de entrega, espelhando a estrutura do roteiro."""
import os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import PILULAS

RAIZ = os.path.dirname(os.path.abspath(__file__))
AUDIOS = os.path.join(RAIZ, "audios")
PACOTE = os.path.join(RAIZ, "PILULAS-OUTUBRO")


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
        capture_output=True, text=True).stdout.strip())


def main():
    if os.path.exists(PACOTE):
        shutil.rmtree(PACOTE)
    linhas = ["PILULAS DE OUTUBRO - AUDIOS", "",
              "Voz da Ana (clone ElevenLabs). Cada fala em arquivo proprio, na ordem do roteiro.",
              "VO  = narracao por cima da cena.",
              "LIP = fala da Eita, para o lipsync.",
              "Quando a pilula tem LIP no comeco e no fim, os arquivos vem numerados: LIP-1 e LIP-2.",
              "", "=" * 62, ""]
    total = 0.0
    for pid, blocos in PILULAS.items():
        pasta = os.path.join(PACOTE, pid)
        os.makedirs(pasta, exist_ok=True)
        linhas.append(f"PILULA {pid}")
        for rot, texto in blocos:
            nome = f"{pid}-{rot}.mp3"
            origem = os.path.join(AUDIOS, nome)
            if not os.path.exists(origem):
                print(f"FALTA {nome}")
                return 1
            shutil.copy2(origem, os.path.join(pasta, nome))
            d = dur(origem)
            total += d
            linhas.append(f"  {nome}  ({d:.1f}s)")
            linhas.append(f"    {texto}")
        linhas.append("")
    linhas.append("=" * 62)
    linhas.append(f"Total: {sum(len(b) for b in PILULAS.values())} arquivos, "
                  f"{int(total // 60)} min {int(total % 60):02d} s de audio.")
    with open(os.path.join(PACOTE, "ROTEIRO.txt"), "w") as f:
        f.write("\n".join(linhas) + "\n")

    zip_path = os.path.join(RAIZ, "PILULAS-OUTUBRO.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    subprocess.run(["zip", "-r", "-q", zip_path, "PILULAS-OUTUBRO"], cwd=RAIZ, check=True)
    mb = os.path.getsize(zip_path) / 1e6
    print(f"{zip_path} ({mb:.1f} MB) - {sum(len(b) for b in PILULAS.values())} audios, "
          f"{int(total // 60)}min{int(total % 60):02d}s")
    if mb > 30:
        print("AVISO: passa do limite de 30 MB do envio pela conversa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
