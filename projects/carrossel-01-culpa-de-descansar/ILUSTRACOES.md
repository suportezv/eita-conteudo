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

## Set do carrossel-01 (cenas propostas, uma por slide vazio)

1. **Slide 2** (a conta que não fecha): calendário de férias evaporando ou copo furado sendo enchido; a água escoa por baixo.
2. **Slide 4** (a parte incômoda): pessoa tentando colar uma etiqueta verde de "produtivo" numa rede de descanso, e a etiqueta descolando.
3. **Slide 5** (pedágio): JÁ GERADA no teste (pessoa no sofá com balão de checklist). Usar a do nano-banana-pro.
4. **Slide 7** (modo padrão): cabeça de perfil com constelação de pontos verdes conectados acendendo por dentro.
5. **Slide 9** (fechamento): a EITA (avatar existente) sentada no sofá ao lado da pessoa; alternativa: usar só o avatar oficial já presente.

Slides 3, 6 e 8 já têm estrutura visual própria (bullets, colunas, passos numerados); não precisam de ilustração, no máximo mais respiro.

Custo estimado do set restante: 4 imagens x 6 créditos = ~24 créditos (sobram ~254 na conta). Concorrência do plano: 2 imagens por vez; gerar em ondas de 2.

## Regra de diagramação derivada (para o prompt de iteração no Claude Design)

Cada slide de conteúdo deve ter no máximo 40% de área "vazia" contínua; onde a copy é curta (slides 2, 4, 5 e 7), a ilustração ocupa o terço central ou o canto oposto ao bloco de destaque, sempre com a mesma largura relativa (~60% do slide) para ritmo visual.

## Pendência de environment

Adicionar `cdn.kairogen.ai` à allowlist do environment permitiria baixar as imagens direto no estúdio (e automatizar o handoff para o Claude Design e para o Metricool).
