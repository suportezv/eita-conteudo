# Benchmark de anúncios: Ash (Slingshot AI) x EITA

Análise dos 30 anúncios mais veiculados da Ash na Biblioteca de Anúncios da Meta (EUA, ativos, ordenados por impressões; 164 ativos no total), feita em 14 de setembro de 2026. Relatório completo, com as folhas de contato dos vídeos e dos cards: ver o artifact "Benchmark Ash" https://claude.ai/artifact/86cqVwmR5f1LqhQaU4MY2g.

Arquivos: `ads-top30.json` (copy, formato, CTA, plataformas, URLs de mídia), `transcricoes.json` (19 vídeos com marcação de tempo), `coleta.py` (download, frames, transcrição), `relatorio.py` (gera a página). Mídia e frames ficam fora do git.

## Quem é a Ash

App gratuito de "IA para saúde mental" da Slingshot AI (Nova York). US$ 93 mi captados (a16z, Radical, Forerunner, Felicis, Menlo). Fundadores Daniel Cahn e Neil Parikh (Casper). Lançado em julho de 2025 como "a primeira IA desenhada para terapia"; mais de 150 mil usuários. Sem plano pago por enquanto. Pontos fracos públicos: estudo próprio de eficácia contestado (STAT) e saída do Reino Unido em janeiro de 2026 por falta de caminho regulatório.

## O que os anúncios fazem

- **Tese única:** o ChatGPT diz o que você quer ouvir; a Ash diz o que você precisa ouvir. 12 dos 19 vídeos e a principal família de estáticos giram nessa comparação. O inimigo é a ferramenta genérica, não a terapia.
- **Copy dos vídeos é uma só** para os 19: título "Talk to Ash now, 24/7, voice or text", texto "Get help today with your mental health - try Ash, the AI built for emotional wellbeing." A diferenciação está toda dentro do vídeo.
- **Formato 1, o campeão (posições 1 a 7, 10, 11):** criador respondendo a comentário (adesivo nativo do TikTok), microfone de lapela, legenda palavra a palavra, corte para a tela do app aos 8 s, ícone no fim. 19 a 21 s. Um corpo, três aberturas gravadas; o arquivo duplicado por loja e canal.
- **Formato 2, esquetes (posições 12 a 15, 24, 26):** dois ou três atores com etiquetas "ChatGPT", "Claude", "Ash", título fixo no topo, um plano só. Cada IA responde ao mesmo dilema; a Ash sempre fecha com uma pergunta ("What would happen if you said no?"). 10 a 16 s.
- **Estáticos (11 dinâmicos):** tipografia, sem foto de produto, humor ("They're living rent-free in your head. Evict them."), mockup de ponto de ônibus, nuvem de verbos ("Ash is your space to... be you. Come as you are, leave clearer."), e a barra de confiança "Designed by mental health experts, powered by AI · Featured in + studied by researchers at NYU, The New York Times".
- **Funil:** tudo para instalação (App Store, Google Play, onelink). CTAs "Download" (23) e "Install now" (7). Sem preço, sem landing page.
- **Mídia:** 720x1280, 30 fps, 9 a 31 s. Facebook e Instagram sempre, Threads na maioria, Audience Network e Messenger em 6. Todos começaram entre 27/08 e 12/09: renovação quinzenal mantendo o campeão.

## Dez lições

1. Escolha um inimigo que o público já usa (o ChatGPT), não a terapia.
2. Deixe o produto dar a última palavra: a fala da Eita como clímax, uma pergunta curta.
3. Um roteiro, três aberturas gravadas.
4. Formato nativo de "respondendo ao comentário": a objeção do público vira gancho.
5. Esquete com etiquetas: um banco, três atores, dezenas de dilemas por tarde.
6. Emoção como cena, não como palavra ("a mensagem que você leu vinte vezes", não "ansiedade").
7. Mostrar a tela cedo: print real de WhatsApp aos 8 s.
8. Credencial no estático, leveza no vídeo: a Neurocientista criadora do método EITA no rodapé das artes.
9. Mockup de mídia exterior no feed para emprestar escala.
10. Duplicar o vencedor por loja e canal é estratégia; renovar o estoque sem abandonar o campeão.

## Onde a EITA ganha

Zero atrito (WhatsApp, "não precisa baixar nada"); personagem com voz; público feminino (a Ash tem um único anúncio com ponto de vista de mulher em 30); preço e promoção; criadora com nome e credencial; guarda-corpos ("não é terapia", CVV 188) como confiança, justamente onde a Ash apanha na imprensa.

## Dez ideias (resumo)

1. "Por que não desabafar com o ChatGPT?" · vídeo 20 s, criador + print de WhatsApp, fecha com a voz da Eita. Três aberturas.
2. "Quando a IA vira sua psicóloga" · esquete 15 s, três atrizes rotuladas, dilema brasileiro, a Eita pergunta.
3. Pílula com contraste · VO com a resposta da IA genérica, LIP com a Eita fechando com a pergunta.
4. "O que você precisa ouvir, às três da manhã" · arte De Para com rodapé de credencial.
5. "Mora de graça na sua cabeça. Hora de despejar." · arte tipográfica com copy em micro-cenas.
6. O ponto de ônibus · mockup de mídia exterior em São Paulo com frases da série De Para.
7. "Isso aqui serve pra desabafar?" · série de objeções reais dos comentários, respondidas pela Anaclaudia ou pela Eita.
8. "A Eita é o seu espaço pra... ser você." · nuvem de verbos com cenas brasileiras; "Chega como está, sai mais leve."
9. "Não precisa baixar nada. Já está no seu WhatsApp." · o gancho que a Ash não pode usar; fecha com o preço.
10. "Gorjeta ou barata" · humor de duas colunas: o uso utilitário e o uso emocional da IA.

Cuidado com comparação nominal ao ChatGPT: o CONAR permite publicidade comparativa verdadeira e não denigratória. Comparar comportamento, nunca usar o logo do concorrente com X.

## Como reproduzir

1. Liberar `www.facebook.com` e `*.fbcdn.net` no environment.
2. Renderizar a URL da biblioteca em Chromium headless (`--dump-dom`); o JSON dos anúncios vem inline em `<script type="application/json">` sob `search_results_connection` (só a 1a página, 30 anúncios, ordenada pelo filtro da URL).
3. `python3 coleta.py` baixa mídia, extrai frames e transcreve; `python3 relatorio.py` monta a página.
