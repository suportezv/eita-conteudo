# EITA Conteúdo Studio: FRAMEWORK

Estúdio de edição e agendamento para as redes da **EITA Mentora Virtual**, o produto de mentoria emocional por WhatsApp criado pela Anaclaudia Zani (Neurocientista criadora do método EITA). Espelho do framework do `ana-conteudo`, adaptado do perfil pessoal para o perfil do produto.

## Persona e voz do perfil

- Quem fala é a **EITA**: a mentora ruiva ilustrada, acolhedora, leve e direta. Proximidade sem clichê de autoajuda e sem cara de "chatbot".
- A Anaclaudia aparece como criadora e autoridade (sempre com a credencial "Neurocientista criadora do método EITA").
- CTA padrão do produto: **"Conversa com a EITA. Link na bio."**
- Bordões herdados do ecossistema ("Meus Anjos", "Conta pra titia") pertencem à Anaclaudia; usar no perfil da EITA apenas quando ela assina o conteúdo.

### REGRAS INEGOCIÁVEIS

1. **Nunca usar travessão em texto público.** Reescrever a frase.
2. Credencial da criadora sempre completa: **"Neurocientista criadora do método EITA"**.
3. A EITA nunca promete tratamento ou substitui terapia; ela acolhe, ensina técnicas e acompanha.

## Pilares de conteúdo (hipóteses iniciais, validar com desempenho)

| Pilar | Formato | Referência |
|---|---|---|
| A | Demo de produto: conversa real no WhatsApp virando reel (estilo "ataque de ansiedade às 3h") | teste-01 do ana-conteudo |
| B | Técnica guiada: a EITA ensinando exercício (respiração, ancoragem) com a voz dos áudios | áudios do produto |
| C | Prova social: depoimentos e reações de usuários (bipar/anonimizar dados) | a coletar |
| D | Criadora: cortes da Anaclaudia explicando a neurociência por trás do método | brutos do ana-conteudo |

Sempre que o material permitir, **hibridizar acolhimento com leveza** (a EITA pode ser engraçada sem perder o cuidado).

## Assinaturas de edição

Herdadas do estúdio ana-conteudo (validadas nos testes 01 e 02 e na leva @luxosobrerodas):

- Hook verbal ou visual + título na tela nos **2 primeiros segundos**.
- Lettering condensado caps branco com sombra dura; acento **amarelo #FFE234** nas ênfases (fonte: Helvetica Neue Condensed Black no Mac; Liberation Sans Bold como fallback Linux).
- Legendas frase a frase em branco (não karaokê), terço inferior, SEMPRE por último no filter chain.
- Cortes secos; punch-ins de zoom 1.10 a 1.22x; freeze frames P&B com card para punchlines; cutaways como payoff de piada.
- Palavrão não corta: **bipa** (sine 1000 Hz curto, voz mutada no trecho).
- Trilha discreta (vol ~0.12 a 0.15) gerada via ElevenLabs sound-generation; SFX (whoosh, impact, riser, scratch) sincronizados aos cortes.
- Duração alvo: **20 a 60s**. Loudness final: **-14 LUFS**.

## Editoria "Do Blog" (carrosséis derivados de posts do blog)

Sistema visual fixo definido no carrossel-01 (detalhes em `projects/carrossel-01-culpa-de-descansar/ITERACAO-EDITORIA.md`): selo NOVO NO BLOG com pulse-dot, barra `mentoravirtual.com.br/blog · NN/NN` no rodapé de todos os slides, byline da autora na capa e chip de tempo de leitura.

- **Tempo de leitura: SEMPRE o valor do badge do post no blog.** Nunca estimar. O badge fica no card do post no índice `/blog` (via MCP da Vercel: `web_fetch_vercel_url` em `eita-teste.vercel.app/blog`).
- **NUNCA numerar os slides** (nem 01/09, nem integrado à barra de endereço). Decisão da equipe em 2026-08-17, vale para todo carrossel.

## Fórmula da caption (produto)

1. Hook em 1 linha (dor ou cena concreta, sem travessão)
2. 2 a 3 parágrafos curtos (o que aconteceu na demo / a técnica / o porquê neurocientífico)
3. CTA: "Conversa com a EITA. Link na bio."
4. Pergunta de engajamento

## Fluxo por vídeo

1. Bruto (Drive público ou anexo na conversa) + briefing (`projects/_template/BRIEFING.md` copiado para `projects/<nome>/`)
2. Proxy SDR (se HLG) + transcrição Scribe (timestamps por palavra)
3. Decupagem/cortes (mapear falas de impacto e picos de áudio)
4. Cor
5. Lettering/motion (PIL, PNGs com fade de alpha)
6. **Legendas por último**
7. Trilha + SFX (sound-generation; batidas detectadas por script)
8. Preview 720p+ para aprovação na conversa
9. Caption
10. Agendamento no Metricool (marca da EITA, blog_id 6735014; melhor horário via `getBestTimeToPostByNetwork`). **Todos os canais conectados, exceto YouTube horizontal** (YouTube entra só para vídeo vertical/Shorts); redes que não aceitam o formato ficam de fora naturalmente.

## Gotchas técnicos

Ver a seção "Gotchas essenciais" do `CLAUDE.md` deste repo (herdados e validados no ana-conteudo). Detalhes completos e histórico: repo `suportezv/ana-conteudo`.
