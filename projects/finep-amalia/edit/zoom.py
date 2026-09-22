"""Plano de zoom por frase, mirado no rosto de quem fala.

A versao anterior era um bump de 7.5% em oito instantes escolhidos a mao, com
centro fixo: nao mirava em ninguem e nao acompanhava o que estava sendo dito.

Aqui o enquadramento vai de 100% a 130% e obedece ao conteudo:
  - as informacoes principais entram em CORTE seco no zoom maximo, como em rede
    social, porque o corte marca a frase; a rampa suave dilui
  - o resto respira em movimento continuo entre 100% e ~115%
  - o centro e o rosto detectado em cada fonte (acha_rosto.py), com a cabeca a
    42% da altura da janela, que e onde o olho espera encontrar o rosto
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from monta_srt import palavras_na_saida, frases

EDIT = pathlib.Path(__file__).resolve().parent
FPS = 30
Z_MAX, Z_MEDIO, Z_LEVE, Z_ABERTO = 1.30, 1.18, 1.09, 1.00
ALTURA_ROSTO = 0.42     # posicao vertical do rosto dentro da janela

# Decupagem. Cada linha e (inicio, fim, z_inicial, z_final): quando os dois z
# sao iguais o movimento e um corte seco para aquele valor e segura; quando
# diferem, e um movimento continuo entre eles.
#
# A logica e de direcao, nao de regra: enumeracao e lista pedem plano aberto,
# porque o olho precisa correr os itens; tese, pergunta retorica e numero pedem
# plano fechado, porque a frase e uma so e o rosto carrega. Corte seco entra
# onde a frase vira a chave; movimento continuo onde ela constroi.
PLANO = [
    # --- bloco 1, Marina: o problema, a origem e a visao
    (  0.06,   4.58, 1.26, 1.30),   # tese de abertura, fecha enquanto fala
    (  5.10,  16.12, 1.00, 1.06),   # enumera cenarios: abre para o olho correr
    ( 16.47,  28.15, 1.06, 1.20),   # critica ao que existe hoje: fecha construindo
    ( 29.01,  32.91, 1.00, 1.00),   # corte: a lista de instrumentos, plano aberto
    ( 33.53,  38.93, 1.00, 1.00),   # ilustracao do filme toma a tela
    ( 39.61,  46.50, 1.14, 1.14),   # corte: de onde a EITA nasceu
    ( 46.50,  53.50, 1.14, 1.22),   # "com uma pergunta por tras"
    ( 53.50,  60.00, 1.22, 1.22),   # a pergunta se arma
    ( 60.00,  67.04, 1.22, 1.30),   # e fecha no ponto de interrogacao
    ( 67.39,  71.99, 1.00, 1.00),   # sigla EITA na tela: abre para o lettering
    ( 72.59,  78.11, 1.30, 1.30),   # CORTE: o que a EITA nao e. Frase-chave
    ( 78.61,  88.35, 1.30, 1.12),   # abre para as qualificacoes
    ( 88.93,  97.61, 1.12, 1.04),   # contexto de mercado, respira
    ( 98.61, 104.09, 1.30, 1.30),   # CORTE: a pergunta que justifica o projeto
    (104.61, 109.89, 1.08, 1.14),   # da tese ao mundo real
    (110.37, 116.40, 1.14, 1.14),   # arquitetura em producao
    (116.40, 121.69, 1.00, 1.00),   # corte: entram as marcas, abre para elas
    (122.23, 132.27, 1.12, 1.12),   # numeros a esquerda, plano medio
    (132.77, 146.27, 1.12, 1.22),   # Colombia: fecha ao longo da frase
    (146.83, 148.25, 1.30, 1.30),   # CORTE: "essa escala mostrou o que?"
    (148.27, 157.35, 1.30, 1.10),   # a resposta abre
    (157.89, 161.43, 1.00, 1.00),   # cartela AMALIA

    # --- bloco 4, Marina: por que saude emocional
    (171.61, 177.33, 1.26, 1.26),   # CORTE: abre o bloco declarando
    (177.85, 184.19, 1.26, 1.30),   # "milhares de pessoas": fecha no numero
    (184.69, 197.03, 1.00, 1.08),   # ambiente individual, abre e respira
    (197.55, 212.89, 1.08, 1.16),   # ambiente corporativo, fecha aos poucos
    (213.39, 226.27, 1.04, 1.10),   # bullets na tela, plano contido
    (226.69, 234.00, 1.30, 1.30),   # CORTE: onde esta o valor. Frase-chave
    (234.00, 241.81, 1.30, 1.18),   # abre listando a capacidade
    (242.16, 250.00, 1.18, 1.06),   # abre para a ilustracao longitudinal
    (250.00, 259.26, 1.00, 1.00),   # ilustracao na tela
    (259.61, 262.77, 1.30, 1.30),   # CORTE: "e esse ativo tecnologico"

    # --- bloco 5, Clesio: capacidade de execucao
    (262.95, 265.91, 1.14, 1.14),   # CORTE de troca de locutor, estabelece
    (266.47, 269.81, 1.30, 1.30),   # CORTE: nao estamos comecando do zero
    (270.35, 279.31, 1.06, 1.06),   # corte: lista o que ja existe
    (279.63, 282.33, 1.06, 1.20),   # "nao poderiam ser mais animadores"
    (282.75, 292.29, 1.26, 1.26),   # CORTE: os numeros de retencao
    (292.64, 306.50, 1.00, 1.00),   # abre: entra o painel dos socios
    (306.60, 333.63, 1.00, 1.00),   # painel na tela o tempo todo
    (334.05, 343.29, 1.30, 1.30),   # CORTE: nucleo tecnologico no Brasil
    (343.47, 353.65, 1.30, 1.22),   # objetivo do investimento

    # --- bloco 6, Marina: aderencia e fechamento
    (353.83, 364.54, 1.10, 1.10),   # CORTE: a chamada da FINEP, plano medio
    (364.89, 372.17, 1.10, 1.20),   # arquitetura ja em uso, fecha
    (372.65, 380.69, 1.00, 1.00),   # corte: a lista de desafios, abre
    (381.27, 390.60, 1.00, 1.00),   # ilustracao da camada
    (390.60, 395.74, 1.26, 1.26),   # CORTE: a ambicao, saindo da ilustracao
    (396.24, 397.04, 1.26, 1.26),   # "essa e a proposta"
    (397.68, 406.50, 1.10, 1.10),   # corte: por que comecar por aqui
    (406.95, 413.95, 1.10, 1.22),   # responsabilidade nao e opcional
    (414.45, 419.87, 1.30, 1.30),   # CORTE: pode ir muito alem
    (421.31, 430.00, 1.12, 1.12),   # corte: o resumo abre
    (430.00, 438.30, 1.12, 1.30),   # e fecha construindo ate o fim
    (438.30, 443.69, 1.00, 1.00),   # cartela final
]

def centro_por_segmento():
    """Rosto de cada trecho da linha do tempo de saida.

    Usa as mesmas fronteiras calibradas do valor do zoom. Enquanto isso vinha da
    soma bruta das duracoes, o centro trocava de rosto 110ms antes de a imagem
    cortar: o quadro ainda era de quem saia, ja reenquadrado para quem entrava, e
    a troca de locutor dava dois solavancos em vez de um corte.
    """
    rostos = json.load(open(EDIT / "rostos.json"))
    edl = json.load(open(EDIT / "edl-final.json"))
    cortes = cortes_de_imagem()
    fora = []
    for i, r in enumerate(edl["ranges"]):
        ro = rostos.get(r["source"])
        if ro: fora.append((cortes[i], cortes[i+1], ro["cx"], ro["cy"]))
    return fora

def cortes_de_imagem():
    """Onde a imagem realmente corta, em tempo de saida.

    Nao e a soma das duracoes do EDL: cada segmento e codificado num numero
    inteiro de quadros e o arredondamento acumula. Medido contra os cortes
    detectados no render, a soma simples errava 151ms no fim do video (quase
    cinco quadros) e a troca de enquadramento caia depois do corte, dando dois
    solavancos. Somando ceil(duracao*fps) o erro fica abaixo de um quadro.
    """
    import math
    edl = json.load(open(EDIT / "edl-final.json"))
    fora, quadros = [], 0
    for r in edl["ranges"]:
        # +1 medido: procurando o maior salto de luminancia em volta de cada
        # fronteira no proprio base_preview, o primeiro quadro do segmento novo
        # cai um quadro depois do que a soma dos ceil() preve, em sete de oito
        # fronteiras testadas. Sem esse quadro o enquadramento mudava um quadro
        # depois do corte e a troca aparecia como um solavanco.
        fora.append((quadros + 0) / float(FPS))
        quadros += math.ceil((r["end"] - r["start"]) * FPS)
    fora.append((quadros + 0) / float(FPS))
    return fora

def plano(fim_video=433.81):
    """(t_ini, t_fim, z_ini, z_fim, corte). Corte = z constante no trecho.

    Os vaos entre uma frase e a seguinte sao costurados: cada trecho se estica
    ate o inicio do proximo. Sem isso o enquadramento voltava ao aberto durante
    o silencio e piscava a cada respiracao de quem fala.
    """
    from linha import desloca_plano
    kf = [[a, b, z0, z1] for a, b, z0, z1 in desloca_plano(PLANO)]

    # Encaixa cada troca de enquadramento no corte de imagem mais proximo. As
    # frases comecam com padding, entao o trecho de zoom caia 60 a 250ms depois
    # do corte do EDL: davam dois solavancos seguidos em vez de um corte so. Foi
    # o que apareceu na virada do Clesio para a Marina. Mudando no mesmo quadro,
    # a troca de enquadramento ainda ajuda a esconder o corte.
    cortes = cortes_de_imagem()
    for b in kf:
        d, c = min((abs(b[0] - x), x) for x in cortes)
        if d < 0.55: b[0] = c   # meio segundo: acima disso sao dois eventos distintos
    kf[0][0] = 0.0
    for i in range(len(kf) - 1):
        kf[i][1] = kf[i+1][0]
    kf[-1][1] = max(kf[-1][1], fim_video)
    return [(a, b, z0, z1, abs(z1 - z0) < 1e-9) for a, b, z0, z1 in kf]

def dentro(_T, a, b):
    """Intervalo semiaberto [a, b), comparado em INDICE DE QUADRO.

    Duas armadilhas resolvidas aqui. A primeira: between() do ffmpeg e fechado
    nos dois lados, entao na fronteira os dois trechos vizinhos valiam 1 e os
    valores somavam, jogando o zoom para o teto por um quadro.

    A segunda: comparar em segundos com tres casas decimais nao funciona. O
    quadro 7889 vale 262.96666..., que arredondado vira 262.967, acima do tempo
    real do quadro. O gte falhava, o lt do trecho anterior passava, e o primeiro
    quadro depois do corte caia num vao onde nenhum trecho estava ativo: o zoom
    ia para o valor de fallback por exatamente um quadro. Era o solavanco que
    sobrava nas trocas de locutor. Em indice de quadro inteiro nao ha
    arredondamento possivel.
    """
    return f"gte(on,{int(round(a * FPS))})*lt(on,{int(round(b * FPS))})"

def expr_z(kfs):
    T = f"(on/{FPS})"
    termos = []
    for a, b, z0, z1, corte in kfs:
        if b - a < 0.05: continue
        if corte or abs(z1 - z0) < 1e-6:
            val = f"{z1:.4f}"
        else:
            k0, k1 = int(round(a * FPS)), int(round(b * FPS))
            u = f"((on-{k0})/{max(1, k1-k0)})"
            val = f"({z0:.4f}+{z1-z0:.4f}*(0.5-0.5*cos(PI*{u})))"
        termos.append(f"{dentro(T, a, b)}*{val}")
    # Com os intervalos semiabertos a soma tem exatamente um termo ativo por
    # quadro. Depois do ultimo trecho nao ha nenhum, dai o max com Z_ABERTO.
    return f"max({Z_ABERTO:.2f},min({Z_MAX:.2f},{'+'.join(termos)}))"

def expr_centro(segs, campo):
    T = f"(on/{FPS})"
    i = 2 if campo == "cx" else 3
    termos = [f"{dentro(T, s[0], s[1])}*{s[i]:.1f}" for s in segs]
    padrao = 960.0 if campo == "cx" else 420.0
    cobertura = "+".join(dentro(T, s[0], s[1]) for s in segs)
    return f"({'+'.join(termos)})+(1-min(1,{cobertura}))*{padrao}"

def filtro():
    kfs, segs = plano(), centro_por_segmento()
    z = expr_z(kfs)
    cx, cy = expr_centro(segs, "cx"), expr_centro(segs, "cy")
    # Janela presa dentro do quadro, senao abre borda preta.
    x = f"max(0,min(iw-iw/zoom,({cx})-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,({cy})-ih/zoom*{ALTURA_ROSTO}))"
    return f"zoompan=z='{z}':d=1:x='{x}':y='{y}':s=1920x1080:fps={FPS}"

if __name__ == "__main__":
    kfs = plano()
    n_max = sum(1 for k in kfs if abs(k[3]-Z_MAX) < 1e-6)
    n_corte = sum(1 for k in kfs if k[4])
    print(f"{len(kfs)} trechos | {n_max} no zoom maximo | {n_corte} em corte seco")
    f = filtro()
    print(f"expressao: {len(f)} caracteres")
    pathlib.Path(EDIT / "zoom_filtro.txt").write_text(f)
    for a, b, z0, z1, c in kfs[:12]:
        print(f"  {a:7.2f}-{b:7.2f}  {z0:.2f}->{z1:.2f}  {'CORTE' if c else 'continuo'}")
