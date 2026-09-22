# FINEP / AMALIA — master v7 (CRF 16, 1080p30, 449 MB)

O GitHub recusa arquivos acima de 100 MB, entao o master foi dividido em 5 partes.

## Como juntar no Mac

Baixe as 5 partes para a mesma pasta (ex: Downloads) e rode no Terminal:

    cd ~/Downloads && cat finep-amalia-v7.mp4.part-* > finep-amalia-v7.mp4

Para conferir que ficou integro:

    shasum -a 256 finep-amalia-v7.mp4

O resultado tem que bater com o conteudo de CHECKSUM-sha256.txt.

## Especificacoes

- Duracao: 7min14s (434,09s)
- Video: H.264 1920x1080 @30fps, CRF 16, 8,7 Mbps
- Audio: AAC 256k, -16,0 LUFS integrado, LRA 4,8

## Alternativa em arquivo unico

`finep-amalia-v7-1080p.mp4` — 95 MB, 1080p30, dois passes a 1,7 Mbps.
Mesmo corte e mesma duracao, um clique, sem precisar juntar partes.
Mais comprimido que o master, mas adequado para submissao e visualizacao.
