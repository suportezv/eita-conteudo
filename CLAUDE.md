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

## IDs e contas

- Instagram do produto: **confirmar handle com a equipe** (planilha de mídia usa "@eita.mentoravirtual").
- Metricool: conta da agência suporte@mentoravirtual.com.br. **PENDENTE: conectar a marca da EITA no painel do Metricool** (hoje só existe "anaclaudia.eita", blog_id 6707687). Timezone America/Sao_Paulo.
- Kairogen: conta suporte@zavi.ag, plano Essential (`veo3-1-lite` para vídeo).
- ElevenLabs: chave em `.env` na raiz do video-use (transcrição Scribe + SFX/trilha + TTS; chave atual tem voices_read). Voz clonada da **Anaclaudia**: voice_id `XsU4z9JE7JPZzkVPg4GW` (`eleven_multilingual_v2`, stability 0.5, similarity 0.8). A voz da **personagem EITA** dos áudios do WhatsApp: **PENDENTE confirmar com a equipe qual é**. Não há voz chamada "EITA" na conta; candidatas femininas pt-BR: Ana Alice `ORgG8rwdAiMYRug8RJwR`, Raquel `GDzHdQOi6jjf8zaXhCYD`, Bia `Eyspt3SYhZzXd1Jd3J8O`, Katiuscia `wXwzHFLHnXex5h3JPBXA`, Slany `x8udhExu0uJxUn4Tf9Az`, Horseway `mPDAoQyGzxBSkE0OAOKw`, Lucinda `fs3nd19KF2GO2hLTzkBm`.
- Drive (brutos): pasta do projeto **PENDENTE: criar/apontar** (padrão: pasta com "qualquer pessoa com o link: leitor" para download direto).

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
