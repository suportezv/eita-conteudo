# EITA Conteúdo Studio

Estúdio de edição e agendamento de conteúdo para as redes da **EITA Mentora Virtual**. Projeto irmão do [`ana-conteudo`](https://github.com/suportezv/ana-conteudo) (perfil pessoal da Anaclaudia); mesma infraestrutura, posicionamento do produto.

- **`FRAMEWORK.md`**: persona, regras, pilares, assinaturas de edição e fluxo por vídeo.
- **`CLAUDE.md`**: memória persistente do projeto (IDs, contas, gotchas).
- **`projects/`**: um subdiretório por vídeo (briefing, transcrição, scripts de edição, caption). Comece copiando `projects/_template/`.
- **`scripts/`**: setup e validação do ambiente (Linux/cloud).
- **`patches/`**: correções necessárias nas ferramentas.

## Primeiro uso (cloud)

```bash
bash scripts/setup.sh
bash scripts/validate.sh
```

Depois: coloque o bruto no Drive (pasta pública) ou anexe na conversa, escreva o briefing em `projects/<nome>/` e peça a edição.

| Serviço | Uso | Configuração |
|---|---|---|
| Google Drive | Brutos | Conector oficial + domínios liberados no environment |
| Metricool | Agendamento | Conectar a marca da EITA (pendente) |
| ElevenLabs | Transcrição, trilha, SFX, TTS | Chave `sk_...` no `.env` do video-use |
| Kairogen | B-roll por IA | Conta suporte@zavi.ag (Essential) |
