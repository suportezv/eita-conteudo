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
- Metricool: conta da agência suporte@mentoravirtual.com.br. **Marca da EITA conectada em 2026-08-17: "eita.mentoravirtual", blog_id 6735014** (userId 5161049, timezone America/Sao_Paulo), com Instagram `eita.mentoravirtual`, Facebook, LinkedIn, Pinterest, TikTok e YouTube. Conteúdo do produto agenda-se SEMPRE nela; a marca "anaclaudia.eita" (blog_id 6707687) é o perfil pessoal. **Regra da equipe (2026-08-17): todo agendamento seleciona TODOS os canais conectados da marca, exceto YouTube horizontal.** Na prática: Instagram, Facebook, LinkedIn, Pinterest e TikTok sempre (`providers` com todas as redes que aceitam o formato); YouTube só quando o conteúdo for vídeo vertical (Shorts), nunca horizontal. Existe ainda uma terceira marca na conta, "normalyze.ai" (6735045), de outro projeto: ignorar.
- Kairogen: conta suporte@zavi.ag, plano Essential (`veo3-1-lite` para vídeo). Verificado em 2026-08-17: 286 créditos, crédito a R$ 0,175, renovação 2026-09-11, concorrência máxima 4 gerações (2 imagem + 2 vídeo). Para lote de vídeos, gerar em ondas de 2.
- ElevenLabs: chave em `.env` na raiz do video-use (transcrição Scribe + SFX/trilha + TTS). Voz clonada da **Anaclaudia**: voice_id `XsU4z9JE7JPZzkVPg4GW` (`eleven_multilingual_v2`, stability 0.5, similarity 0.8). A voz da **personagem EITA** é a mesma voz clonada da Ana (confirmado pela equipe em 2026-08-17): um único voice_id para tudo.
- Drive (brutos): pasta do projeto **PENDENTE: criar/apontar** (padrão: pasta com "qualquer pessoa com o link: leitor" para download direto).

## Pendências que dependem da equipe (checar no início de cada sessão)

As três pendências de 2026-08-17 de manhã fecharam no mesmo dia: marca eita.mentoravirtual no Metricool (blog_id 6735014), rede liberada no container, e chave `sk_` do ElevenLabs validada e gravada em `/workspace/browser-use/video-use/.env`. **O pipeline está 100% operacional.**

Sobre a chave do ElevenLabs (validada em 2026-08-17 à tarde):

- É uma chave de **permissões restritas**: `user_read` e `models_read` negados (irrelevantes para o estúdio); voices, TTS, speech-to-text (Scribe) e sound-generation **testados e funcionando**. A voz clonada da Anaclaudia (`XsU4z9JE7JPZzkVPg4GW`) aparece na conta.
- **Atenção em container novo:** a env var `ELEVENLABS_API_KEY` do environment ainda pode conter o key ID hex antigo (o valor visto pelo container congela no boot; nesta sessão a correção foi direto no `.env`). O `setup.sh` avisa quando a env var não começa com `sk_`; nesse caso, recuperar a chave com a equipe ou pedir para corrigirem a env var do environment.

Ainda em aberto, sem bloquear nada: a pasta de brutos no Drive. (A voz da personagem EITA foi confirmada em 2026-08-17: é a própria voz clonada da Ana, `XsU4z9JE7JPZzkVPg4GW`.)

## Gotchas essenciais (herdados do ana-conteudo, todos validados)

- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez antes de editar (filtro `colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc`).
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG sequence + qtrle (ou PNG estático com fade de alpha).
- Zoom animado com `zoompan`, não `crop` (crop não aceita `t` em w/h).
- video-use precisa do patch `patches/video-use-is-portrait-source.patch` (senão vertical vira paisagem).
- Metricool MCP: sem delete (cancelar = update draft:true; update devolve id novo); mídia por URL pública (o Metricool copia para o CDN dele na hora).
- Mac: usar ffmpeg-full keg-only com PATH explícito. Linux: ffmpeg do apt já serve.
- Cloud, brutos do Drive: usar o environment com network Custom e `drive.google.com` + `drive.usercontent.google.com` + `api.elevenlabs.io` liberados (o environment "ana-conteudo" já está assim; pode ser reutilizado ou duplicado). Download direto de arquivo público, qualquer tamanho: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`. O conector MCP do Drive serve para busca e metadados; download por ele só até ~4 MB. Fallback para arquivo público pequeno: Kairogen `download_audio_from_url`.
- Cloud, mídia pública para o Metricool (receita validada no carrossel-01, 2026-08-17): commit temporário da mídia numa branch SEM barra no nome (`midia-temp`), com `git add -f` (o .gitignore barra mídia) e autorização do usuário. **Por isso este repo deve ser público.** O normalizador do Metricool tem timeout curto por arquivo e desiste na primeira busca lenta, então: (1) montar URLs do jsDelivr fixadas no **SHA do commit** (`cdn.jsdelivr.net/gh/<owner>/<repo>@<sha40>/<path>`), nunca `@branch` (o jsDelivr congela a resolução da branch por horas e dá 404 para arquivo novo); (2) **aquecer cada URL antes** com o Kairogen `download_image_from_url` (fetch server-side, valida e cacheia na borda); (3) só então `createScheduledPost` com as 9 URLs quentes, que ele copia na hora para static.metricool.com; (4) remover a mídia. raw.githubusercontent leva rate-limit do GitHub em rajada de 9 e o backoff piora a cada retry; cdn.statically.io nunca passou. Deletar branch remota dá 403 no proxy; em vez disso, force-push da branch para o commit sem mídia.
- Cloud: a env var `ELEVENLABS_API_KEY` de environment antigo continha um key ID (64 hex); a chave real é `sk_...` de 51 caracteres.
- Site e blog do produto: `mentoravirtual.com.br` é o projeto **eita-site-prod** da Vercel (team suporte-3326s-projects). O proxy do environment BLOQUEIA o domínio público, mas o conteúdo sai inteiro pelo MCP da Vercel: `web_fetch_vercel_url` com `https://eita-teste.vercel.app/<path>` (domínio alternativo do mesmo projeto). O blog fica em `/blog`, posts em ordem do mais novo para o mais antigo no HTML do índice. Identidade visual do site (para artes do produto): papel #F5F7F6, tinta #17202A, verde #00EFA9, verde profundo #0A7757, verde suave #D6F7EB, League Spartan + JetBrains Mono.
- Trilhas/SFX: ElevenLabs sound-generation (`/v1/sound-generation`, máx ~22s) gera beds e SFX ótimos; para trilha maior, gerar build+drop e costurar com acrossfade. Detecção de BPM/batidas: script próprio com numpy (fluxo de energia + autocorrelação), ver `ana-conteudo/projects/teste-02-interlagos/edit/beats.py`.
