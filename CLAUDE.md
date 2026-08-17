# EITA Conteúdo Studio (memória persistente do projeto)

Este repositório é o **EITA Conteúdo Studio**: edição e agendamento de conteúdo para as redes da **EITA Mentora Virtual** (produto de mentoria emocional por WhatsApp da Anaclaudia Zani). Projeto irmão do `ana-conteudo` (perfil pessoal @anaclaudia.eita); a infraestrutura é idêntica, o posicionamento é o do produto.

**Antes de editar qualquer vídeo ou escrever qualquer caption, leia `FRAMEWORK.md`** (posicionamento, regras inegociáveis, formatos, assinaturas de edição e todos os gotchas técnicos).

## Regras que valem em qualquer resposta pública

- Nunca usar travessão em texto público (caption, lettering, legenda): reescrever a frase.
- Quando citar a criadora: sempre "Neurocientista criadora do método EITA".
- A EITA fala como a personagem (acolhedora, leve, direta); nunca como "IA genérica".

## Working dirs

- Estúdio: este repo (symlink `~/eita-conteudo` aponta para cá). Projetos em `projects/<nome>/`.
- Ferramentas: `video-use` e `hyperframes` clonados em `/workspace/browser-use/` e `/workspace/heygen-com/` (Linux/cloud) ou `~/video-editor/` (Mac). Skills registradas em `~/.claude/skills/`.
- Ambiente novo (container limpo): rode `bash scripts/setup.sh` e depois `bash scripts/validate.sh`.

## Estado do ambiente (última verificação: 2026-08-17, sessão cloud)

Toolchain instalado e validado num container limpo pelo `scripts/setup.sh` (leva ~2 min):

| Item | Estado |
|---|---|
| ffmpeg | 6.1.1 do apt, com `subtitles` e `zscale` (3 filtros) |
| fonts-liberation | 12 fontes (fallback do lettering no Linux) |
| video-use | clone `92c2b34`, `.venv` via `uv sync`, patch `is_portrait_source` aplicado |
| hyperframes + media-use | 9 skills registradas em `~/.claude/skills/` |
| PIL / numpy | pillow 12.3.0 / numpy 2.4.6 |

**Rede: liberada desde 2026-08-17 (tarde).** `drive.google.com` (302), `drive.usercontent.google.com` e `api.elevenlabs.io` respondem HTTP normal (404 na raiz é o esperado). A troca de policy valeu para o container em execução, ao contrário do que se supunha de manhã. Se algum domínio voltar a dar 000/403: `curl -sS "$HTTPS_PROXY/__agentproxy/status"` lista as negativas recentes em `recentRelayFailures`.

## IDs e contas

- Instagram do produto: **@eita.mentoravirtual** (confirmado pela equipe em 2026-08-17; não é mais hipótese da planilha). O perfil pessoal da Anaclaudia é @anaclaudia.eita: nunca confundir os dois.
- Metricool: conta da agência suporte@mentoravirtual.com.br. **Marca da EITA conectada em 2026-08-17: "eita.mentoravirtual", blog_id 6735014** (userId 5161049, timezone America/Sao_Paulo), com Instagram `eita.mentoravirtual`, Facebook, LinkedIn, Pinterest, TikTok e YouTube. Conteúdo do produto agenda-se SEMPRE nela; a marca "anaclaudia.eita" (blog_id 6707687) é o perfil pessoal. Existe ainda uma terceira marca na conta, "normalyze.ai" (6735045), de outro projeto: ignorar.
- Kairogen: conta suporte@zavi.ag, plano Essential (`veo3-1-lite` para vídeo). Verificado em 2026-08-17: 286 créditos, crédito a R$ 0,175, renovação 2026-09-11, concorrência máxima 4 gerações (2 imagem + 2 vídeo). Para lote de vídeos, gerar em ondas de 2.
- ElevenLabs: chave em `.env` na raiz do video-use (transcrição Scribe + SFX/trilha + TTS). Voz clonada da **Anaclaudia**: voice_id `XsU4z9JE7JPZzkVPg4GW` (`eleven_multilingual_v2`, stability 0.5, similarity 0.8). A voz da **personagem EITA** dos áudios do WhatsApp é outra: **PENDENTE mapear voice_id com a equipe**.
- Drive (brutos): pasta do projeto **PENDENTE: criar/apontar** (padrão: pasta com "qualquer pessoa com o link: leitor" para download direto).

## Pendências que dependem da equipe (checar no início de cada sessão)

Das três pendências de 2026-08-17 de manhã, duas fecharam no mesmo dia (marca eita.mentoravirtual no Metricool, blog_id 6735014; rede liberada no container). Resta uma que trava transcrição, trilha e SFX:

1. **`ELEVENLABS_API_KEY` ainda é o key ID, não a chave.** Em 2026-08-17 a equipe configurou a env var, mas com o valor errado pela segunda vez: 64 caracteres hex (prefixo `329...`), e a API respondeu `api_key_id_used_as_api_key`. A chave certa começa com `sk_` e tem 51 caracteres; ela só aparece na hora em que a key é criada ou rotacionada em elevenlabs.io/app/settings/api-keys. Se não foi copiada na hora, rotacionar e copiar o `sk_` novo. Ao corrigir: atualizar a env var do environment e gravar em `/workspace/browser-use/video-use/.env`.

Ainda em aberto, sem bloquear o começo: `voice_id` da personagem EITA (a dos áudios do WhatsApp, diferente da voz clonada da Anaclaudia) e a pasta de brutos no Drive.

## Gotchas essenciais (herdados do ana-conteudo, todos validados)

- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez antes de editar (filtro `colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc`).
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG sequence + qtrle (ou PNG estático com fade de alpha).
- Zoom animado com `zoompan`, não `crop` (crop não aceita `t` em w/h).
- video-use precisa do patch `patches/video-use-is-portrait-source.patch` (senão vertical vira paisagem).
- Metricool MCP: sem delete (cancelar = update draft:true; update devolve id novo); mídia por URL pública (o Metricool copia para o CDN dele na hora).
- Mac: usar ffmpeg-full keg-only com PATH explícito. Linux: ffmpeg do apt já serve.
- Cloud, brutos do Drive: usar o environment com network Custom e `drive.google.com` + `drive.usercontent.google.com` + `api.elevenlabs.io` liberados (o environment "ana-conteudo" já está assim; pode ser reutilizado ou duplicado). Download direto de arquivo público, qualquer tamanho: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`. O conector MCP do Drive serve para busca e metadados; download por ele só até ~4 MB. Fallback para arquivo público pequeno: Kairogen `download_audio_from_url`.
- Cloud, mídia pública para o Metricool: commit temporário do render na branch (repo público, raw.githubusercontent.com passa no proxy), agendar e remover o arquivo em seguida. Exige `git add -f` (o .gitignore barra mídia) com autorização do usuário. **Por isso este repo deve ser público.**
- Cloud: a env var `ELEVENLABS_API_KEY` de environment antigo continha um key ID (64 hex); a chave real é `sk_...` de 51 caracteres.
- Trilhas/SFX: ElevenLabs sound-generation (`/v1/sound-generation`, máx ~22s) gera beds e SFX ótimos; para trilha maior, gerar build+drop e costurar com acrossfade. Detecção de BPM/batidas: script próprio com numpy (fluxo de energia + autocorrelação), ver `ana-conteudo/projects/teste-02-interlagos/edit/beats.py`.
