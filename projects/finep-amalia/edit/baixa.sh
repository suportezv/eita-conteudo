#!/usr/bin/env bash
# Baixa os brutos publicos do Drive. Arquivo grande exige o confirm=t do
# drive.usercontent.google.com; o conector MCP so serve ate ~4 MB.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../brutos"
baixa() { # id destino
  [ -s "$2" ] && { echo "ja existe: $2"; return 0; }
  curl -L --fail --retry 4 --retry-delay 2 --max-time 1800 \
    -o "$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t" \
    && echo "OK $2 ($(du -h "$2" | cut -f1))" || echo "FALHOU $2"
}
baixa 1VW22rqG5g4tLP6zp_ClJ9PN3P4bhjEw0 marina-bloco1.MOV
baixa 15cQzOi9ddZ96O_muAbz-92c_MTnEot3T marina-bloco4.MOV
baixa 1xxOYc7yWZjcSJYRDXGcEFgaoEUnGhyXS marina-bloco6.MOV
baixa 1tZ9EmFVk_7CVOmHKNJP12ke1BIO3niPk clesio-bloco5.mov
