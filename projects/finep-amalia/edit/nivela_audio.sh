#!/usr/bin/env bash
# Nivela o audio entre os locutores nos masters normalizados.
#
# Medido com ebur128 (amostra de 60s): Clesio -11.8 LUFS, Marina -18.6 / -18.6 /
# -20.2. Sem isso o volume salta a cada troca de locutor. O alvo e -18.5 LUFS,
# o nivel natural da Marina; o loudnorm final do render.py leva o programa
# inteiro para -14. Video passa intacto com -c:v copy.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/normalizado"

ajusta() { # arquivo filtro-de-audio
  [ -f "$1.bak" ] && { echo "ja ajustado: $1"; return 0; }
  cp "$1" "$1.bak"
  ffmpeg -v error -i "$1.bak" -c:v copy -af "$2" -c:a aac -b:a 192k -y "$1"
  echo "OK $1  ($2)"
}
# Clesio: so abaixar, sem risco de clipe.
ajusta clesio-bloco5.mp4 "volume=-6.7dB"
# Bloco 6: levantar 1.7dB estouraria (pico em -0.5 dBFS), entao entra limitador.
ajusta marina-bloco6.mp4 "volume=1.7dB,alimiter=limit=0.9"
# Blocos 1 e 4 ja estao no alvo; mexer neles so adicionaria geracao de perda.
echo "blocos 1 e 4: sem ajuste (-18.6 LUFS, ja no alvo)"
