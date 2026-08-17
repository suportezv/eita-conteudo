# Revisão do render v2 (Claude Design, 2026-08-17)

Fonte: `render-v2/Carrossel Culpa do Descanso.dc.html`. Veredicto: **aprovada com um ajuste obrigatório** (numeração dos slides, abaixo).

## Conferido item a item contra o pedido de iteração

| Item | Estado |
|---|---|
| Tokens de cor (fundo, tinta, os três verdes, bordas) | Todos exatos: #F5F7F6, #17202A, #00EFA9, #0A7757, #D6F7EB com borda #B8E8D2, #DFE8EB |
| Clash Display removida, títulos em League Spartan 800 | OK |
| JetBrains Mono em eyebrows, créditos, chips, barra e numerais dos passos | OK |
| Eyebrow no formato do site (traço 18px + mono verde profundo) | OK |
| Selo NOVO NO BLOG com pulse-dot #1EC46C | OK (brilho estático via sombra, correto para imagem) |
| Chip LEITURA · 10 MIN | OK, valor do badge do blog |
| Byline da Ana na capa (avatar + credencial completa em mono) | OK, com foto real em `assets/ana-zani.png` |
| Barra de endereço em todos os 9 slides, a 96px do fundo | OK |
| "O texto completo está no blog." no slide 9 | OK |
| Ilustração em PNG com alfa (sem retângulo de fundo) | OK, RGBA |
| Zero travessões | OK (grep no HTML) |
| Copy intacta | OK |

## Ajuste obrigatório antes de exportar

- **A numeração dos slides sumiu.** O pedido era a barra com numeração integrada (`mentoravirtual.com.br/blog · 03/09`) e a v2 trouxe a barra sem o número em todos os slides. Numeração importa em carrossel (retenção e senso de progresso). Pedir no Claude Design: "adicione ' · NN/09' ao final da barra de endereço de cada slide, com o número do slide em dois dígitos".

## Conferir no preview da plataforma (possível, não certo)

- Na capa, a ilustração (830px de largura, ~463px de altura) pode encostar na linha da barra de endereço dependendo da quebra do título. Se sobrepor, reduzir a ilustração para ~760px ou tirar 2 linhas do parágrafo de apoio.

## Depois do ajuste

Exportar os 9 PNGs em 1080x1350 e enviar na conversa para agendamento no Metricool (marca eita.mentoravirtual, blog_id 6735014), caption pronta em `CAPTION.md`.
