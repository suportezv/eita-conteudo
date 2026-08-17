# Revisão do render v1 (Claude Design, 2026-08-17)

Fonte revisada: `render-v1/Carrossel Culpa do Descanso.dc.html` (export do projeto do Claude Design; os slides são HTML parametrizado, não PNG).

## O que ficou bom

- **Copy 100% fiel** ao `SLIDES.md`, sem paráfrase. Zero travessões em todo o HTML (verificado por grep).
- **Estrutura correta**: 9 slides de 1080x1350, numeração 01/09, blocos de destaque ancorados no pé, comparativo em duas colunas com a coluna "sem função" como protagonista (borda verde e sombra), passos numerados com círculos.
- **Guarda-corpos presentes**: credencial completa da Ana no slide 9, "não substitui terapia" e CVV 188 no rodapé do fechamento.
- **Uso inteligente da plataforma**: CTA com duas variantes parametrizadas (escuro/acqua) e textura de fundo desligável via props; dá para alternar sem reeditar.
- **Ilustração própria** da cena do sofá na capa (gerada, não banco de imagem).
- Bom respiro geral, hierarquia clara, um destaque por slide.

## O que melhorar

1. **Cores fora do token da marca** (parecidas, mas nenhuma bate): fundo #F6F9F9 em vez de #F5F7F6, tinta #0E1416 em vez de #17202A, verdes #1FBE87/#48EBAD em vez de #00EFA9/#0A7757, verde-suave #ECFCF5 em vez de #D6F7EB. Isoladas passam; em lote produzem uma marca "quase igual", e no feed a diferença do verde é visível contra o site e o avatar da EITA.
2. **Tipografia fora do sistema**: títulos em Clash Display (fonte da Fontshare que o site não usa) e o JetBrains Mono sumiu por completo. Os eyebrows, créditos e numeração estão em League Spartan espaçada. O mono é justamente a assinatura mais reconhecível do site; sem ele, o post não "rima" com o blog.
3. **Sem sinal de editoria**: nada indica que o post nasce de um texto do blog (pedido novo, resolvido na proposta abaixo).
4. **Zona segura do Instagram**: numeração e rodapés a 44px da borda inferior; a UI do carrossel cobre essa faixa. Subir para pelo menos 96px.
5. **Capa densa**: eyebrow + título 88px + parágrafo + indicador + ilustração full-bleed. Com o selo de editoria entrando, o parágrafo de apoio pode encurtar ou a ilustração virar faixa menor.
6. **Ilustração em JPEG** (sem alfa): o fundo da imagem pode não casar exatamente com o fundo do slide. Pedir PNG com fundo transparente ou com o fundo exato #F5F7F6.
7. **Operacional**: o export .dc.html só abre dentro do Claude Design (runtime próprio; renderizei localmente e a página monta em branco). Para agendar no Metricool preciso dos **9 PNGs exportados** de 1080x1350.

## Identidade de editoria "Do Blog" (proposta)

Objetivo: qualquer pessoa que já viu o site reconhecer em meio segundo que o post é um texto novo do blog. Quatro elementos fixos, todos emprestados do próprio site, que passam a valer para TODO carrossel desta editoria:

1. **Selo NOVO NO BLOG**: pílula branca com borda fina #DFE8EB, ponto verde "vivo" (#1EC46C, o pulse-dot do site) e o texto NOVO NO BLOG em JetBrains Mono, caps, tracking largo. Sempre no topo esquerdo da capa. É o análogo do selo "Central de conhecimento" do cabeçalho do site.
2. **Barra de endereço no rodapé de todos os slides**: `mentoravirtual.com.br/blog` em JetBrains Mono pequeno, com a numeração integrada na mesma linha (ex.: `mentoravirtual.com.br/blog · 03/09`). Vira o chassi da editoria: viu a barra, é post de blog. Também resolve a numeração dentro da zona segura.
3. **Byline da autora na capa**, espelhando o cabeçalho do artigo no site: avatar redondo da Ana, "Anaclaudia Zani" e, embaixo, "Neurocientista criadora do método EITA". Sinaliza artigo com autoria, não meme de feed.
4. **Chip de leitura na capa**: `LEITURA · 10 MIN` em mono, copiando o valor do badge do card do post no blog (nunca estimar: o site é a fonte).

Complementos: eyebrow de categoria no formato do site (traço curto + texto mono em verde profundo #0A7757), abrindo espaço para codificar categorias por cor no futuro; e uma linha discreta no slide final, "O texto completo está no blog", acima do rodapé do CVV (o CTA principal continua sendo "Conversa com a EITA. Link na bio.").

O prompt de iteração pronto para colar no Claude Design está em `ITERACAO-EDITORIA.md`.
