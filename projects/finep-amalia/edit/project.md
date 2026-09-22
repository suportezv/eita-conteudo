# FINEP / AMALIA — memória do projeto

## Sessão 1 — 2026-09-22

**Estratégia:** primeira prévia do vídeo institucional FINEP. Só quatro dos seis
blocos estão gravados (Marina x3, Clésio x1); Arthur e Ana entram como cartela de
5s para a prévia manter a ordem do roteiro. Cortar erros e silêncios, equalizar a
cor entre as duas câmeras, montar na ordem do roteiro.

**Fontes (brutos em `../brutos/`, fora do git):**

| arquivo | bloco | formato | duração |
|---|---|---|---|
| marina-bloco1.MOV | 1 | 1080x1920 rotation -90, 8 bits bt709, 30fps | 2:47 |
| marina-bloco4.MOV | 4 | idem | 1:36 |
| marina-bloco6.MOV | 6 | idem | 1:36 |
| clesio-bloco5.mov | 5 | 2710x1524 HLG 10 bits (arib-std-b67), 30fps | 2:16 |

**Decisões:**

- *Normalização antes do EDL.* As duas câmeras não batem em nada: resolução,
  rotação, profundidade de bits e curva. Além disso o `render.py` do video-use
  aplica uma cor só para o EDL inteiro. Gravar a cor num master por fonte
  (`normalizado/*.mp4`, 1920x1080 bt709 CRF 16) resolve os dois de uma vez.
- *Cor equalizada por medição, não no olho.* Medido com `signalstats` (YAVG/UAVG/VAVG).
  Partida: Marina Y 84 / U 139 / V 139 (escura e magenta); Clésio Y 143 / U 113 / V 145
  (clara e amarela). Chegada: ambos U 128 / V 133; Marina Y 109, Clésio Y 125.
  A diferença de luma que sobrou é a diferença real entre uma sala escura e uma
  cozinha clara, e forçar além disso deixaria a Marina artificial.
- *Erros.* Marina veio limpa nos três blocos. O Clésio tem três tentativas da frase
  da Marina (54.0, 74.2 e 92.7); vale a última, como o usuário pediu. Fora isso,
  a gagueira "Nosso obje--" em 121.7 sai e a frase recomeça em "nosso objetivo".
- *Silêncios.* Corte conservador: só vão fora as pausas acima de 0.70s, e ainda
  sobram ~0.35s de ar no lugar. É leitura de teleprompter institucional, não corte
  de rede social; picotar demais deixaria o ritmo nervoso.
- *Slips mantidos por falta de take melhor:* "pri-privacidade" (bloco 1, 88.1s) e
  "pode muito além" sem o "ir" (bloco 6, 63.8s).

- *Nivelamento de audio.* Medido com ebur128: Clesio -11.8 LUFS contra Marina
  -18.6 / -18.6 / -20.2. Quase 7 dB de diferenca dao um tranco de volume a cada
  troca de locutor, e o loudnorm final do render.py nao resolve porque normaliza o
  programa inteiro de uma vez, nao cada locutor. `nivela_audio.sh` baixa o Clesio
  em 6.7 dB e levanta o bloco 6 em 1.7 dB (com limitador, porque o pico ja estava
  em -0.5 dBFS). Depois disso os quatro ficam entre -17.7 e -18.6 LUFS.

**Verificacao do render (previa-v1):**

- Duracao 444.13s contra 443.81s previstos no EDL.
- Emenda dos takes do Clesio (316.62s na saida) sem estalo e sem palavra cortada.
- Troca Marina/Clesio (262.89s) com niveis casados e sem salto de cor.
- Cartelas com silencio limpo nos dois lados.
- Cor no render final: U entre 126.2 e 128.1, V entre 132.7 e 133.5 do inicio ao
  fim, ou seja o ajuste sobreviveu a extracao por segmento e ao concat.

## Sessão 2 — 2026-09-22 (retorno do cliente)

**Sombra dos motions.** Saiu o retangulo escuro atras do texto. A borda dele caia
em algum lugar da cena e lia como painel mal posicionado; agora a sombra e o alfa
do proprio desenho borrado, que acompanha a forma da letra.

**Legenda.** Contorno opaco (no ASS o primeiro byte da cor e alfa invertido, e o
&HC8 deixava a borda 78% transparente), contorno fino, e chunker reescrito para
quebrar por frase em vez de por estouro de linha. Gaguejo, hesitacao e ruido nao
entram. Legenda nao divide a tela com motion de tela cheia, mas divide com o GC
de credito, que e discreto.

**Trilha.** Leitos nivelados em -18 LUFS antes da costura: o gerador entregava
-10.8 num e -18.9 noutro, e isso virava um salto de 6 dB no meio do bloco 6.

**Movimento de camera.** Oito punch-ins de 7.5% nos pontos de enfase, com meio
cosseno nas pontas, via zoompan.

**Identificacao das fotos** (confirmada pelo cliente): 1 Marina, 2 Clesio,
3 Arthur, 4 Anaclaudia. O Clesio foi identificado comparando a foto com o
proprio video, nao pela ordem dos anexos.

**Gotcha das logos.** Os PNGs das marcas ja chegam com alfa correto. Tentar
"remover o fundo branco" calculando min(RGB) transforma o fundo transparente
(onde RGB e 0) em preto opaco, e a sombra amplifica isso num retangulo preto.
Usar o alfa do arquivo.

**Pendente:**

- Gravar blocos 2 (Arthur) e 3 (Ana).
- Artes de tela previstas no roteiro (GCs dos blocos 1, 3, 5 e 6; animação do 2).
- Enquadramento: a Marina está num plano bem mais aberto que o Clésio. Dá para
  aproximar com punch-in de ~1.3x, ao custo de um upscale. Não feito, não foi pedido.
