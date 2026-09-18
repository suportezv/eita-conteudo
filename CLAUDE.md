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

- Instagram do produto: **@eita.mentoravirtual** (confirmado; a marca também tem Facebook, LinkedIn, Pinterest, TikTok e YouTube conectados).
- Metricool: conta da agência suporte@mentoravirtual.com.br, marca "eita.mentoravirtual", **blog_id 6735014**, timezone America/Sao_Paulo. Melhor horário de publicação: medir com a marca nova (getBestTimeToPostByNetwork).
- **Regra de agendamento (todas as marcas da agência)**: sempre incluir TODOS os canais conectados da marca no post, exceto YouTube horizontal. YouTube entra como **Short** (`youtubeData: {type: "short", title, madeForKids: false}`); Instagram como REEL; Facebook como REEL; TikTok, LinkedIn e Pinterest com networkData padrão. Nunca publicar vídeo vertical como YouTube horizontal comum.
- Kairogen: conta suporte@zavi.ag, plano Essential (`veo3-1-lite` para vídeo).
- ElevenLabs: chave em `.env` na raiz do video-use (transcrição Scribe + SFX/trilha + TTS; chave atual tem voices_read). **A voz da EITA é a voz clonada da Anaclaudia** (confirmado pela equipe em ago/2026): voice_id `XsU4z9JE7JPZzkVPg4GW`, modelo `eleven_multilingual_v2`, stability 0.5, similarity 0.8. Amostra de referência aprovada: `ana-conteudo/assets/voz/amostra-voz-clonada.mp3`. Toda narração da EITA (pilar B) usa essa voz.
- Drive (brutos): pasta do projeto **PENDENTE: criar/apontar** (padrão: pasta com "qualquer pessoa com o link: leitor" para download direto).

## Rede do environment

Network **Custom**. Hosts que este cinto de ferramentas exige:

| Host | Para quê |
|---|---|
| `drive.google.com`, `drive.usercontent.google.com` | baixar brutos |
| `api.elevenlabs.io` | TTS, transcrição Scribe, SFX |
| `api.openai.com` | geração de imagem por GPT |
| `generativelanguage.googleapis.com` | geração de imagem por Gemini |
| `www.googleapis.com` | upload para o Drive |
| `pypi.org`, `files.pythonhosted.org` | dependências Python |
| `registry.npmjs.org` | Remotion e `npx` |
| `api.github.com` + GitHub Releases | ffmpeg estático e clones |

`raw.githubusercontent.com` **não** precisa ser liberado: o `setup.sh` registra as skills do hyperframes a partir do clone local quando o `npx ... skills update` falha.

**Gotcha central**: `pypi.org`, `files.pythonhosted.org` e `registry.npmjs.org` vêm na variável `no_proxy` do container. Por isso contornam o agent proxy e batem direto no firewall de egresso, que responde **403 "Host not in allowlist"** mesmo estando na allowlist. Roteando pelo agent proxy respondem 200. O contorno está embutido no `scripts/setup.sh`.

Diagnóstico de qualquer host em um comando: `curl -sv https://host/ 2>&1 | grep CONNECT`. Se aparecer `HTTP/1.1 403` no CONNECT, é allowlist; qualquer outra resposta significa que a rede passou e o problema é outro (chave, quota, rota).

## Chaves de API (todas por variável de ambiente, nenhuma no repo)

| Variável | Para quê | Como conferir o escopo |
|---|---|---|
| `ELEVENLABS_API_KEY` | TTS, Scribe e `sound-generation` | chamar o endpoint com parâmetro inválido: `401 missing_permissions` = escopo ausente; `400`/`404` = escopo presente |
| `OPENAI_API_KEY` | `scripts/gera_imagem.py` | `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"` |
| `GEMINI_API_KEY` | `scripts/gera_imagem.py` | `curl https://generativelanguage.googleapis.com/v1beta/models -H "x-goog-api-key: $GEMINI_API_KEY"` |

Três armadilhas já pagas com tempo nos estúdios irmãos:

1. **Variável de ambiente entra na criação do container.** Cadastrar no environment com uma sessão já aberta não faz a sessão enxergar: é preciso sessão nova. Conferir com `printenv | grep -c API_KEY` antes de acusar o script.
2. **Chave válida não significa quota.** No Gemini, listar modelos funciona no tier gratuito, mas gerar imagem devolve `429` com `limit: 0`. Se o erro cita `quotaId: ...-FreeTier`, o projeto da chave não está no faturamento, e vincular meio de pagamento à conta não basta: tem que estar vinculado **ao projeto daquela chave**.
3. **Nem toda chave da ElevenLabs tem todos os escopos.** Sem `user_read` não dá para checar saldo antes de gerar lote. Verificar antes de planejar lote grande.

## Scripts do estúdio (`scripts/`)

| Script | O que faz |
|---|---|
| `decupar.py` | Decupa vídeo por **âncoras de texto** ("de tal frase até tal frase") casadas contra transcrição com timestamp por palavra. Junta trechos, gira, aplica LUT, normaliza áudio |
| `relatorio_decupagem.py` | Retranscreve as peças finais e monta o relatório do que ficou e do que caiu |
| `gera_lut_slog2.py` | Gera LUT 3D de S-Log2/S-Gamut para Rec.709 a partir das transferências da `colour-science` |
| `zip_index_remoto.py` | Lista e extrai arquivos de um ZIP gigante no Drive por *range request*, sem baixar o ZIP |
| `gera_imagem.py` | Gera imagem pela OpenAI ou pelo Gemini, mesma interface, chaves só do ambiente |
| `sobe_para_drive.py` | Sobe arquivos para uma pasta do Drive com token de acesso |
| `setup.sh` / `validate.sh` | Boot do container e validação por comportamento |

O `validate.sh` **testa comportamento, não presença de arquivo**: roda filtros reais no ffmpeg, gera retrato/paisagem/paisagem girada e confere se `is_portrait_source` acerta os três, renderiza 1 frame de verdade no Remotion e bate os hosts liberados. Se um passo do `setup.sh` avisar, ele não derruba o boot (é intencional), então **ler a saída, não só o código de retorno**.

## Gotchas essenciais (herdados dos estúdios irmãos, todos validados)

### Captação e cor

- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez antes de editar (filtro `colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc`).
- **Brutos de Sony em S-Log2 (A7 III): converter, não "filtrar".** O XML lateral de cada clipe (`C00xxM01.XML`) declara `CaptureGammaEquation` e `CaptureColorPrimaries`; quando diz `s-log2`/`s-gamut`, a imagem chega chapada e precisa de conversão para Rec.709. `scripts/gera_lut_slog2.py` gera a LUT com a `colour-science`. Dois cuidados que a prática impôs: **exposição -0,5 stop e joelho em 0,65**, senão o branco estoura; e conferir que o ffmpeg aplica a `lut3d` **em RGB, não em YUV** (ele auto-insere `yuvj420p -> rgb24`; verificar com `-v verbose`). Saída sempre com `out_range=tv` e `-color_range tv`.
- **Câmera pode gravar na vertical sem gravar a flag de rotação.** O arquivo vem 3840x2160 deitado e o ffprobe não mostra rotação nenhuma; só olhando um frame se descobre. Corrigir com `transpose=1` antes de escalar. Vale checar um frame de qualquer lote novo antes de planejar o corte.

### Edição

- **Decupagem por âncora de texto, não por timecode.** `scripts/decupar.py` recebe um `edl.json` onde cada trecho é "de tal frase até tal frase"; ele casa as âncoras contra a transcrição com timestamp por palavra do Scribe e resolve os tempos. Revisar um corte vira editar uma frase. O campo `apos` empurra o cursor quando a mesma frase aparece antes.
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG sequence + qtrle (ou PNG estático com fade de alpha).
- Zoom animado com `zoompan`, não `crop` (crop não aceita `t` em w/h).
- **O patch `video-use-is-portrait-source` foi aposentado (18/set/2026).** O upstream reescreveu `is_portrait_source` para ler também o `rotation` do side data, o que cobre mais casos que o patch cobria. O `validate.sh` agora testa **comportamento** (retrato, paisagem e paisagem com matriz de rotação 90) em vez de procurar o patch no código.
- Trilhas/SFX: ElevenLabs `sound-generation` (`/v1/sound-generation`, máx ~22s, `duration_seconds` entre 0.5 e 30) gera beds e SFX ótimos; para trilha maior, gerar build+drop e costurar com `acrossfade`. Detecção de BPM/batidas: script próprio com numpy (fluxo de energia + autocorrelação), ver `ana-conteudo/projects/teste-02-interlagos/edit/beats.py`.
- Testar escopo de chave da ElevenLabs sem gastar crédito: chamar o endpoint com parâmetro inválido. `401 missing_permissions` = escopo ausente; `400`/`404` de validação = escopo presente.

### Motion (Remotion e HyperFrames)

- **Remotion renderiza com o `headless_shell`, não com o Chromium do Playwright.** O `chromium-1194` removeu o headless antigo que o Remotion pede e o launch morre com "Old Headless mode has been removed". O binário certo é `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, fixado em `remotion/remotion.config.ts`. Baixar o browser próprio do Remotion não é opção: está fora da allowlist.
- **Remotion e HyperFrames resolvem o mesmo problema.** O HyperFrames se declara "default output framework" e só oferece caminho de mão única `remotion-to-hyperframes`; não existe o inverso. Manter os dois é escolha deliberada: HyperFrames para o fluxo com skills, Remotion para composição React feita à mão. Ao começar peça nova, escolher um e dizer qual (ver `FRAMEWORK.md`).
- **Licença do Remotion não é MIT.** `LICENSE.md` do pacote: grátis para indivíduo, organização sem fins lucrativos, empresa **de até 3 funcionários** e avaliação; acima disso exige Company License paga (remotion.pro). **Confirmar o enquadramento antes de usar em produção.**
- **Sem rede de fontes no render.** Google Fonts está fora da allowlist, então o headless cai para a sans do sistema. Para usar a fonte da marca, embutir o arquivo como asset local.
- **A paleta vive em `remotion/src/marca.ts`.** `Aurora.tsx` e `CartaoTitulo.tsx` leem daqui e são idênticos aos dos estúdios irmãos, por isso os **nomes** das chaves são herdados e neutros: ler `rosaVivo` como "acento principal". Se a paleta da marca mudar, atualizar Remotion e HyperFrames nos dois lados.
- **Skills do hyperframes sem rede**: `npx hyperframes skills update` falha quando `raw.githubusercontent.com` está fora da allowlist, porque confere um manifesto lá. Não é preciso liberar o domínio: o clone em `/workspace/heygen-com/hyperframes/skills/<nome>/SKILL.md` já traz todas. O `scripts/setup.sh` as registra automaticamente quando o `npx` falha.

### Ambiente e rede

- **O setup do environment falha por caminho relativo.** O campo de setup script traz `bash scripts/setup.sh`, um caminho **relativo**, e o boot roda com o diretório de trabalho no **pai** do repo: `No such file or directory`, exit 127, e a sessão nasce sem `/workspace` e sem skills. Resolver com caminho absoluto (`bash /home/user/eita-conteudo/scripts/setup.sh`) ou com a versão à prova de diretório:
  ```bash
  for p in ./scripts/setup.sh ./*/scripts/setup.sh; do [ -f "$p" ] && exec bash "$p"; done; p=$(find /home /workspace /repo /app /src -maxdepth 4 -type f -path "*/scripts/setup.sh" 2>/dev/null | head -1); [ -n "$p" ] && exec bash "$p"; echo "setup.sh nao encontrado no repo"; exit 1
  ```
  Enquanto o campo não for corrigido, em sessão nova **conferir `ls /workspace` antes de contar com video-use ou hyperframes**.
- **A URL do ffmpeg estático quebrou em 18/set/2026, e a diferença é de uma palavra.** `releases/download/latest/...` é a tag rolante do BtbN e **serve o arquivo**; `releases/latest/download/...` parece equivalente e **não é**: resolve para a autobuild do dia e devolve 404. O `setup.sh` tenta as duas em ordem e, principalmente, **confere a assinatura XZ (`fd377a585a00`) antes de extrair**, senão um 404 chega como corpo de texto e o `tar` reclama de "not a tar archive", escondendo a causa. Os 403 do apt são ruído conhecido e esperado.
- **Allowlist do environment não cobre subdomínio.** A entrada é literal: `www.googleapis.com` **não** cobre `generativelanguage.googleapis.com`. Para um site inteiro, usar `*.dominio.com` junto do apex.
- **Chromium não contorna a allowlist.** O headless usa o mesmo agent proxy e devolve `ERR_TUNNEL_CONNECTION_FAILED` no mesmo host que o `curl` recusa. Navegador só ajuda contra JS/SPA, nunca contra egresso bloqueado.
- **Processo em background com `nohup`/`setsid` é recolhido quando a tool call retorna.** Usar `run_in_background: true` da própria ferramenta Bash, que o harness rastreia. Em lote longo, `flock` num arquivo de lock evita a corrida de dois loops escrevendo o mesmo arquivo.
- **Ler o índice de um ZIP gigante no Drive sem baixar o arquivo.** `drive.usercontent.google.com` aceita `Range`, então dá para pegar os últimos ~64 KB, achar o EOCD (`PK\x05\x06`) e, em arquivo >4 GB, o ZIP64 EOCD via locator `PK\x06\x07`, ler o central directory e listar tudo. Com entradas `method=0` (stored), cada arquivo pode ser extraído sozinho por outro `Range`. Evita baixar 11 GB para pegar um vídeo de 90 MB. Script: `scripts/zip_index_remoto.py`.
- **Upload de vídeo para o Drive pode não sair deste container.** `www.googleapis.com` precisa estar na allowlist, e o conector MCP do Drive só aceita conteúdo via `base64Content` na própria chamada, inviável para vídeo. Criar pasta funciona. Entrega de vídeo sai por commit na branch ou pelo envio direto do arquivo na conversa.
- Mac: usar ffmpeg-full keg-only com PATH explícito. Linux: o build estático do `setup.sh` já serve.
- Cloud, brutos do Drive: download direto de arquivo público, qualquer tamanho, com `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`. O conector MCP do Drive serve para busca e metadados; download por ele só até ~4 MB. Fallback para arquivo público pequeno: Kairogen `download_audio_from_url`.
- Cloud: a env var `ELEVENLABS_API_KEY` de environment antigo continha um key ID (64 hex); a chave real é `sk_...` de 51 caracteres.

### Publicação

- Metricool MCP: sem delete (cancelar = update `draft:true`; update devolve id novo); mídia por URL pública (o Metricool copia para o CDN dele na hora).
- **Metricool, rascunho com data vencida não publica e não avisa.** Um post `draft:true` cuja data passa continua no calendário, aparecendo em `getScheduledPosts` como se estivesse agendado, mas nunca dispara. Regra: **quem agenda tira do rascunho na mesma sessão e confirma com `getScheduledPosts`**; nunca deixar o flip de `draft` para uma sessão seguinte. Tirar do rascunho com a data no passado também não resolve, é preciso data nova.
- Cloud, mídia pública para o Metricool: commit temporário do render na branch (repo público, `raw.githubusercontent.com` passa no proxy), agendar e remover o arquivo em seguida. Exige `git add -f` (o `.gitignore` barra mídia) com autorização do usuário. **Por isso este repo deve ser público.**
- **Instagram exige login, mesmo liberado na rede.** Ler perfil de forma anônima é impossível: `/<perfil>/` devolve 302 para `/accounts/login/`, a API `web_profile_info` devolve 401 `require_login: true`, e o embed devolve casca vazia. É política do Instagram, não é rede. Para analisar feed, as rotas viáveis são prints do usuário, o conector do Metricool (só para contas conectadas à marca) ou a Graph API da Meta com token.
