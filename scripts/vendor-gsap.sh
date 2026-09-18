#!/usr/bin/env bash
# Vendoriza o GSAP dentro de um projeto hyperframes.
#
# Por que isso existe: o template do `hyperframes init` carrega o GSAP de
# cdn.jsdelivr.net, e esse host esta fora da allowlist do environment (403 no
# CONNECT do agent proxy). O Chrome do render nao baixa o script, o
# hyperframes aborta com `sub_timeline_script_failure` e nenhum MP4 sai.
# registry.npmjs.org passa, entao a copia local resolve de vez.
#
# Uso: bash scripts/vendor-gsap.sh <dir-do-projeto>   copia para o projeto
#      bash scripts/vendor-gsap.sh                     so garante o cache do repo
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJ="${1:-}"
GSAP_CACHE="$REPO_ROOT/assets/vendor/gsap.min.js"

# A copia versionada no repo e a fonte preferida: nao depende de rede nenhuma.
# Se ela sumir, o npm ainda serve de fallback.
if [ ! -f "$GSAP_CACHE" ]; then
  echo "assets/vendor/gsap.min.js ausente; baixando do npm"
  tmp="$(mktemp -d)"
  ( cd "$tmp" && npm pack gsap@3.14.2 --silent >/dev/null \
      && tar -xzf gsap-3.14.2.tgz package/dist/gsap.min.js ) \
    || { echo "ERRO: npm pack gsap falhou"; rm -rf "$tmp"; exit 1; }
  mkdir -p "$(dirname "$GSAP_CACHE")"
  cp "$tmp/package/dist/gsap.min.js" "$GSAP_CACHE"
  rm -rf "$tmp"
fi

# Sem argumento o trabalho acaba aqui: o setup.sh so quer o cache preenchido.
if [ -z "$PROJ" ]; then
  echo "GSAP em cache: $GSAP_CACHE"
  exit 0
fi

[ -d "$PROJ" ] || { echo "ERRO: $PROJ nao existe"; exit 1; }

mkdir -p "$PROJ/vendor"
cp "$GSAP_CACHE" "$PROJ/vendor/gsap.min.js"

# Reescreve qualquer <script src> de GSAP em CDN para o caminho local. O template
# fixa a versao na URL, mas outras podem aparecer, entao o padrao e amplo.
n=0
while IFS= read -r -d '' html; do
  if grep -q 'cdn\.jsdelivr\.net.*gsap' "$html"; then
    sed -i -E 's#https?://cdn\.jsdelivr\.net/npm/gsap[^"'"'"']*#vendor/gsap.min.js#g' "$html"
    n=$((n+1))
  fi
done < <(find "$PROJ" -maxdepth 2 -name '*.html' -not -path '*/node_modules/*' -print0)

echo "GSAP local em $PROJ/vendor/gsap.min.js ($n arquivo(s) HTML reescrito(s))"
