# Plano de ilustração do carrossel (Kairogen)

Diagnóstico da equipe sobre a v2: diagramação com espaços vazios e poucos elementos ilustrando. O Claude Design não gera imagens; quem gera é o **Kairogen**, aqui do estúdio. Fluxo: gero as ilustrações aqui, a equipe baixa pelo widget da conversa (o proxy bloqueia cdn.kairogen.ai, então não consigo baixar localmente) e sobe como assets no projeto do Claude Design.

## Teste de estilo (2026-08-17, mesmos prompt e paleta nos dois motores)

| Motor | Custo | Resultado |
|---|---|---|
| **nano-banana-pro** (gen `6a8303d67adf5e35b028474f`) | 6 créditos | Fundo frio correto (#F5F7F6), verdes da marca, checklist sem texto real, linha consistente. **Recomendado.** |
| seedream-v4-5 (gen `6a8303ff7adf5e35b0284925`) | 2 créditos | Composição bonita, mas fundo bege com textura (criaria retângulo visível sobre o slide) e teal fora da paleta. |

## Prompt base (usar como prefixo de todas as gerações da editoria)

> Flat vector-style editorial spot illustration for a mental health blog. [CENA]. Solid pale background exactly #F5F7F6. Limited brand palette only: dark ink #17202A for lines and main shapes, vivid mint green #00EFA9 as the single accent color, deep green #0A7757 for small details, soft pale green #D6F7EB for secondary fills. Thick consistent line weight, soft rounded geometric forms, generous negative space, modern minimal editorial illustration. Absolutely no text, no letters, no numbers, no watermark, no photorealism, no gradients.

**Consistência entre imagens**: a partir da segunda geração, passar a imagem aprovada do teste como `reference_image_urls` (o nano-banana-pro aceita 1 referência). Personagem recorrente: mesma pessoa de cabelo escuro ondulado do teste.

## Set do carrossel-01: GERADO E COMPLETO (2026-08-17, estilo aprovado pela equipe)

Todas em nano-banana-pro, 1:1, com a imagem do teste como referência de estilo/personagem. Baixar pelo widget da conversa ou pela galeria do Kairogen (arquivos `.png` em nome do gen id abaixo).

| Slide | Cena | generation_id | Arquivo no CDN |
|---|---|---|---|
| 2 (conta que não fecha) | Copo com rachadura sendo enchido, água vazando | `6a8304e1314f9a54dbe06f40` | `bf81bbb7-...png` |
| 4 (parte incômoda) | Etiqueta verde que não cola na rede | `6a83057e0362cba60bf16315` | `6b2e13ea-...png` |
| 5 (pedágio) | Pessoa no sofá com balão de checklist (a do teste) | `6a8303d67adf5e35b028474f` | `d23b3601-...png` |
| 7 (modo padrão) | Cabeça de perfil com constelação verde | `6a8305cb7adf5e35b02855ca` | `41669f01-...png` |
| 9 (fechamento) | Pessoa relaxada com celular de brilho verde e balão de conversa | `6a8305cf314f9a54dbe07623` | `a832f5e1-...png` |

Slides 3, 6 e 8 já têm estrutura visual própria (bullets, colunas, passos numerados); não levam ilustração.

Custo real do projeto: 32 créditos (5 x 6 do nano-banana-pro + 2 do teste seedream). Saldo restante: ~254.

**Operacional aprendido**: com `wait_for_completion=true` o cliente MCP estoura em 60s; gerar sempre assíncrono (`false`) e poll com `get_generation`. O limite de 2 imagens simultâneas conta gerações que acabaram de completar; se der `GENERATION_LIMIT_REACHED`, aguardar a fila e reenviar.

## Regra de diagramação derivada (para o prompt de iteração no Claude Design)

Cada slide de conteúdo deve ter no máximo 40% de área "vazia" contínua; onde a copy é curta (slides 2, 4, 5 e 7), a ilustração ocupa o terço central ou o canto oposto ao bloco de destaque, sempre com a mesma largura relativa (~60% do slide) para ritmo visual.

## Pendência de environment

Adicionar `cdn.kairogen.ai` à allowlist do environment permitiria baixar as imagens direto no estúdio (e automatizar o handoff para o Claude Design e para o Metricool).
