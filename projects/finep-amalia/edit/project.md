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

**Pendente:**

- Gravar blocos 2 (Arthur) e 3 (Ana).
- Artes de tela previstas no roteiro (GCs dos blocos 1, 3, 5 e 6; animação do 2).
- Enquadramento: a Marina está num plano bem mais aberto que o Clésio. Dá para
  aproximar com punch-in de ~1.3x, ao custo de um upscale. Não feito, não foi pedido.
