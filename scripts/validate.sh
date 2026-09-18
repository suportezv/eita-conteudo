#!/usr/bin/env bash
# Validação do EITA Conteúdo Studio. Itens de MCP (Metricool, Kairogen) validam-se
# dentro da sessão do Claude, não aqui.
set -uo pipefail

TOOLS_DIR="${TOOLS_DIR:-/workspace}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTION="$TOOLS_DIR/remotion-studio"
VIDEO_USE="$TOOLS_DIR/browser-use/video-use"
[ -d "$VIDEO_USE" ] || VIDEO_USE="$HOME/video-editor/video-use"
FF_PATH="/opt/homebrew/opt/ffmpeg-full/bin"
[ -d "$FF_PATH" ] && export PATH="$FF_PATH:$PATH"

echo "== 1. ffmpeg: subtitles + zscale =="
N=$(ffmpeg -filters 2>/dev/null | grep -cE "subtitles|zscale")
if [ "${N:-0}" -ge 2 ]; then echo "OK ($N filtros)"; else echo "FALHOU (esperado >=2, obtido ${N:-0})"; fi

echo "== 2. video-use helpers =="
if (cd "$VIDEO_USE" && { [ -d .venv ] && .venv/bin/python helpers/timeline_view.py --help >/dev/null 2>&1 || python3 helpers/timeline_view.py --help >/dev/null 2>&1; }); then
  echo "OK (helpers importam)"
else
  echo "FALHOU (helpers não rodam em $VIDEO_USE)"
fi
if grep -q 'if f\]' "$VIDEO_USE/helpers/render.py" 2>/dev/null; then
  echo "OK (patch is_portrait_source presente)"
else
  echo "PENDENTE: patch is_portrait_source não aplicado"
fi

echo "== 3. ElevenLabs =="
if grep -q '^ELEVENLABS_API_KEY=sk_' "$VIDEO_USE/.env" 2>/dev/null; then
  echo "OK (chave sk_ presente; transcrição real gasta créditos, rodar sob demanda)"
else
  echo "PENDENTE: ELEVENLABS_API_KEY sk_ ausente no .env do video-use"
fi

echo "== 4. Skills registradas =="
[ -e ~/.claude/skills/video-use/SKILL.md ] && echo "OK video-use" || echo "PENDENTE video-use"
ls ~/.claude/skills 2>/dev/null | grep -q hyperframes && echo "OK hyperframes" || echo "verifique skills do hyperframes (npx hyperframes skills update)"

echo "== 5. Motores de render =="
# O que importa nao e o binario existir, e o render achar um Chrome. Os dois
# motores dependem do mesmo, baixado por `npx hyperframes browser ensure`.
if ls /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell >/dev/null 2>&1 \
   || ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell >/dev/null 2>&1; then
  echo "OK chrome headless"
else
  echo "PENDENTE: chrome headless ausente (npx hyperframes browser ensure)"
fi
[ -f "$REPO_ROOT/assets/vendor/gsap.min.js" ] \
  && echo "OK gsap em cache (cdn.jsdelivr.net e bloqueado; use scripts/vendor-gsap.sh)" \
  || echo "PENDENTE: gsap nao cacheado (bash scripts/vendor-gsap.sh)"
if [ -d "$REMOTION/node_modules/remotion" ]; then
  echo "OK remotion $(node -p "require('$REMOTION/node_modules/remotion/package.json').version" 2>/dev/null)"
else
  echo "PENDENTE: remotion nao instalado em $REMOTION (rode scripts/setup.sh)"
fi

echo "== 6. Na sessão do Claude, validar ainda: =="
echo " - Rede: curl a drive.google.com deve responder HTTP (environment com domínios liberados)"
echo " - Metricool: getBrandSettings deve listar a marca da EITA com Instagram conectado (PENDENTE conectar)"
echo " - Kairogen: get_me_context mostra plano Essential+ e créditos"
