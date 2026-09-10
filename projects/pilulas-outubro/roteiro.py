#!/usr/bin/env python3
"""Roteiro das 12 pilulas de outubro, dividido em blocos VO e LIP.

Fonte: Google Doc "Cliente: EITA / Formato: Pilulas Outubro" (prazo 11-09).
O nome da marca vai escrito "Eita" em caixa mista: e a unica grafia que o
multilingual_v2 le com o ditongo certo (ver CLAUDE.md).
"""

ASSINATURA = "Sou sua mentora e companheira emocional no seu WhatsApp."

# Cada pilula e uma lista ordenada de (rotulo, texto).
# O rotulo vira o nome do arquivo: 01-VO.mp3, 03-LIP-1.mp3, etc.
PILULAS = {
    "01": [
        ("VO", "Às vezes a desistência não é fraqueza. É esconderijo. "
               "Enquanto você não tenta de verdade, dá pra viver com o \"e se\". "
               "Tentar é aceitar descobrir a resposta."),
        ("LIP", "A Eita te ajuda a encarar a pergunta que você evita. " + ASSINATURA),
    ],
    "02": [
        ("VO", "Mais um curso, mais um vídeo, mais um post salvo. E a sua vida exatamente igual. "
               "Consumir conteúdo dá sensação de progresso. "
               "Mas sem executar, é água em balde furado: entra de um lado, vaza do outro."),
        ("LIP", "A Eita te ajuda a tampar o furo. " + ASSINATURA),
    ],
    "03": [
        ("LIP-1", "A régua dos outros mede a distância que eles andaram."),
        ("VO", "Aplicada em você, só produz um número sem sentido. "
               "Você não está atrasado só porque alguém chegou antes. "
               "Cada pessoa tem seu tempo e seu caminho."),
        ("LIP-2", "A Eita te ajuda a trocar a cobrança pela pergunta certa. " + ASSINATURA),
    ],
    "04": [
        ("LIP-1", "O que você não fala não some."),
        ("VO", "Muda de endereço. "
               "Vira resposta curta, vira distância, vira explosão por bobeira. "
               "E quando finalmente transborda, você ainda ouve que é drama."),
        ("LIP-2", "Se você vive assim pra manter todo mundo confortável, a Eita pode te ajudar. "
                  + ASSINATURA),
    ],
    "05": [
        ("VO", "Respira fundo, bebe água, se distrai. Meia hora depois, o aperto volta. "
               "Silenciar o alarme não apaga o incêndio. "
               "Enquanto o fogo continua lá, ele vai tocar de novo."),
        ("LIP", "A Eita te ajuda a achar onde o seu começa. " + ASSINATURA),
    ],
    "06": [
        ("VO", "Firmeza não vem antes da estrada. Vem dela."),
        ("LIP", "A Eita te ajuda a continuar depois dos tombos que ninguém vê. " + ASSINATURA),
    ],
    "07": [
        ("VO", "Você ensaia desgraça. A demissão que não veio, o diagnóstico que não existe, "
               "a briga que ninguém começou. "
               "Parece preparo. Mas a dor não dá desconto pra quem chega adiantado. "
               "Você paga duas vezes: uma na imaginação, outra se acontecer. "
               "Quase sempre, só a primeira."),
        ("LIP", "Se sua mente vive nesse ensaio do que nem existe, a Eita pode te ajudar. "
                + ASSINATURA),
    ],
    "08": [
        ("VO", "Tem barreira que some quando você chega perto. Ela só existia na distância. "
               "Só que você decide tudo de longe. E de longe, qualquer sombra vira muro."),
        ("LIP", "A Eita te ajuda a conferir de perto, uma por uma. " + ASSINATURA),
    ],
    "09": [
        ("LIP-1", "Amanhã eu resolvo."),
        ("VO", "O amanhã chega, e quem tá lá é você de novo. "
               "Com a mesma pendência, só que maior."),
        ("LIP-2", "A Eita te ajuda a entender por que justo essa você não encara. " + ASSINATURA),
    ],
    "10": [
        ("VO", "Retrovisor existe pra uma olhada de vez em quando. "
               "Mas você dirige com os olhos grudados nele. "
               "Enquanto sua atenção fica no que passou, você perde de vista o caminho à frente."),
        ("LIP", "A Eita te ajuda a voltar os olhos pra pista. " + ASSINATURA),
    ],
    "11": [
        ("VO", "A pessoa mais segura que você conhece também treme por dentro. Só não mostra. "
               "A diferença entre vocês não tá no que sentem. Tá em quem age tremendo."),
        ("LIP", "A Eita te ajuda a dar esse passo. " + ASSINATURA),
    ],
    "12": [
        ("LIP-1", "Atrasado em relação a quê?"),
        ("VO", "Colega promovido, amigo casando, alguém mais novo comprando apê. "
               "Aí o seu dia, que tava bom, vira atraso. "
               "Essa sensação não nasce da sua vida. Nasce da vida dos outros."),
        ("LIP-2", "Se toda conquista alheia soa como cobrança pra você, a Eita pode te ajudar. "
                  + ASSINATURA),
    ],
}

if __name__ == "__main__":
    total = sum(len(b) for b in PILULAS.values())
    chars = sum(len(t) for b in PILULAS.values() for _, t in b)
    print(f"{len(PILULAS)} pilulas, {total} blocos, {chars} caracteres")
    for pid, blocos in PILULAS.items():
        print(f"  {pid}: {', '.join(r for r, _ in blocos)}")
