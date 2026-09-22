#!/usr/bin/env bash
# Normaliza cada bruto para um master 1920x1080 bt709 com a cor ja equalizada.
#
# Precisa existir porque as duas cameras nao batem em nada: a Marina gravou
# 1080x1920 com rotation=-90 (paisagem so depois do autorotate) em 8 bits SDR,
# e o Clesio gravou 2710x1524 HLG 10 bits. Alem disso o render.py do video-use
# aplica UMA cor para o EDL inteiro, e aqui cada fonte precisa da sua. Gravar a
# cor no master resolve os dois problemas de uma vez.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# HLG -> SDR bt709. npl=100 e o nivel de pico; hable segura os altos sem chapar.
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
# Marina: cena escura e magenta. Gamma levanta os medios sem estourar o preto,
# o lutyuv tira o excesso de azul (U) e de vermelho (V).
GM="eq=contrast=1.06:gamma=1.32:brightness=0.02:saturation=0.96,lutyuv=u='clip(val-10,0,255)':v='clip(val-5,0,255)'"
# Clesio: cena clara e amarela. Gamma abaixa os medios, lutyuv devolve azul.
GC="$TM,eq=contrast=1.08:gamma=0.78:saturation=0.96,lutyuv=u='clip(val+15,0,255)':v='clip(val-11,0,255)'"

norm() { # entrada saida filtro
  [ -s "$2" ] && { echo "ja existe: $2"; return 0; }
  ffmpeg -v error -stats -i "$1" \
    -vf "$3,scale=1920:1080:flags=lanczos,setsar=1" \
    -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p \
    -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
    -c:a copy -y "$2"
  echo "OK $2"
}
norm brutos/marina-bloco1.MOV edit/normalizado/marina-bloco1.mp4 "$GM"
norm brutos/marina-bloco4.MOV edit/normalizado/marina-bloco4.mp4 "$GM"
norm brutos/marina-bloco6.MOV edit/normalizado/marina-bloco6.mp4 "$GM"
norm brutos/clesio-bloco5.mov edit/normalizado/clesio-bloco5.mp4 "$GC"
