"""Todas as pecas de motion da previa, com o tempo de cada uma na saida.

Sistema visual do manual da marca: acqua #48EBAD como fio condutor, azul de
apoio, League Spartan unica familia, "sem excessos". Nada revela dois elementos
novos ao mesmo tempo: o olho nao acompanha dois, entao tudo entra em cascata.
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from motion import *

FOTOS = pathlib.Path(__file__).resolve().parent / "fotos"

# ---------------------------------------------------------------- GC credito
def gc(nome, cargo, dur):
    X, Y = 148, 838
    f_nome, f_cargo = fonte(600, 56), fonte(400, 32)
    def desenha(img, d, t):
        _, a = janela(t, 0, 1, saida=dur)
        scrim(img, 0, Y - 150, X + 980, H, forca=175, alfa=a)
        p1 = out_cubic(t / 0.45)
        regua(d, X - 26, Y + 96 - 96 * p1, 5, 96 * p1, ACQUA, a)
        p2 = out_cubic((t - 0.22) / 0.55)
        if p2 > 0: texto(d, (X - 30 * (1 - p2), Y), nome.upper(), f_nome, BRANCO, p2 * a)
        p3 = out_cubic((t - 0.5) / 0.5)
        if p3 > 0: texto(d, (X, Y + 74), cargo, f_cargo, ACQUA, p3 * a)
    return desenha

# ------------------------------------------------------------- numeros grandes
def numeros(itens, dur, y=286):
    """itens = [(valor, rotulo, apoio, atraso)]. Cada um entra no seu tempo."""
    X = 168
    f_num, f_rot, f_ap = fonte(700, 142), fonte(600, 38), fonte(400, 28)
    def desenha(img, d, t):
        _, a = janela(t, 0, 1, saida=dur)
        alt = 250 * len(itens)
        scrim(img, 0, y - 190, X + 780, y + alt + 150, forca=180, alfa=a)
        for i, (valor, rot, ap, atraso) in enumerate(itens):
            yy = y + i * 250
            tl = t - atraso
            if tl <= 0: continue
            p = out_cubic(tl / 0.9)
            txt = valor if isinstance(valor, str) else f"{int(round(valor * p)):,}".replace(",", ".")
            texto(d, (X, yy), txt, f_num, ACQUA, min(1.0, tl / 0.25) * a)
            regua(d, X, yy + 164, 240 * out_cubic((tl - 0.35) / 0.6), 4, AZUL, a)
            p2 = out_cubic((tl - 0.45) / 0.55)
            if p2 > 0: texto(d, (X, yy + 186), rot.upper(), f_rot, BRANCO, p2 * a)
            if ap:
                p3 = out_cubic((tl - 0.7) / 0.5)
                if p3 > 0: texto(d, (X, yy + 230), ap, f_ap, CINZA, p3 * a)
    return desenha

# ------------------------------------------------------------------- chip/tag
def chip(titulo, linhas, dur, y=760):
    X = 148
    f_tit, f_lin = fonte(600, 42), fonte(400, 32)
    def desenha(img, d, t):
        _, a = janela(t, 0, 1, saida=dur)
        scrim(img, 0, y - 140, X + 1080, y + 90 + 52 * len(linhas), forca=175, alfa=a)
        p1 = out_cubic(t / 0.5)
        regua(d, X, y - 18, 110 * p1, 4, ACQUA, a)
        p2 = out_cubic((t - 0.2) / 0.55)
        if p2 > 0: texto(d, (X, y + 12 * (1 - p2)), titulo.upper(), f_tit, BRANCO, p2 * a)
        for i, ln in enumerate(linhas):
            p = out_cubic((t - 0.5 - i * 0.28) / 0.5)
            if p <= 0: continue
            texto(d, (X + 34, y + 62 + i * 50), ln, f_lin, CINZA, p * a)
            d.ellipse([X + 8, y + 76 + i * 50, X + 20, y + 88 + i * 50],
                      fill=(*ACQUA, int(255 * p * a)))
    return desenha

# ------------------------------------------------------------------ lettering
def sigla(dur):
    """EITA: cada inicial acende junto com a palavra que ela representa."""
    palavras = [("E", "levar a"), ("I", "nteligência pelo"), ("T", "reino da"), ("A", "utopercepção")]
    f_ini, f_resto = fonte(700, 96), fonte(400, 52)
    X, Y = 168, 380
    def desenha(img, d, t):
        _, a = janela(t, 0, 1, saida=dur)
        scrim(img, 0, Y - 170, 1420, Y + 480, forca=185, alfa=a)
        for i, (ini, resto) in enumerate(palavras):
            p = out_cubic((t - 0.35 - i * 0.42) / 0.55)
            if p <= 0: continue
            yy = Y + i * 104
            texto(d, (X, yy), ini, f_ini, ACQUA, p * a)
            texto(d, (X + 78, yy + 34), resto, f_resto, BRANCO, p * a)
    return desenha

def titulo(txt, sub, dur, y=400):
    f_t, f_s = fonte(700, 190), fonte(400, 40)
    def desenha(img, d, t):
        _, a = janela(t, 0, 1, saida=dur)
        scrim(img, 0, y - 220, W, y + 420, forca=200, alfa=a)
        p = out_cubic(t / 0.8)
        lg = largura(d, txt.upper(), f_t)
        texto(d, (W/2, y + 24 * (1 - p)), txt.upper(), f_t, ACQUA, p * a, ancora="ma")
        regua(d, W/2 - lg/2, y + 218, lg * out_cubic((t - 0.5) / 0.7), 5, AZUL, a)
        p2 = out_cubic((t - 0.75) / 0.6)
        if p2 > 0: texto(d, (W/2, y + 252), sub, f_s, BRANCO, p2 * a, ancora="ma")
    return desenha

# --------------------------------------------------------------- ilustracoes
def ilu_filme(dur):
    """Tres fotos soltas contra uma tira de filme continua.

    E a metafora literal da fala: fotografias avulsas nao contam o filme.
    """
    f_leg, f_rot = fonte(400, 36), fonte(600, 32)
    X, yA, yB = 300, 300, 660
    def desenha(img, d, t):
        a = veu(img, t, dur)
        if a <= 0: return
        texto(d, (X, yA - 74), "HOJE", f_rot, CINZA, out_cubic(t/0.4) * a)
        # 3 fotos esparsas, cinza: informacao pontual
        for i in range(3):
            p = out_cubic((t - 0.3 - i * 0.22) / 0.5)
            if p <= 0: continue
            x = X + i * 420
            d.rounded_rectangle([x, yA, x + 230, yA + 168], 8,
                                outline=(*CINZA, int(230 * p * a)), width=3)
            d.line([x + 28, yA + 132, x + 88, yA + 78, x + 140, yA + 132], width=4,
                   fill=(*CINZA, int(200 * p * a)))
        p = out_cubic((t - 1.0) / 0.5)
        if p > 0: texto(d, (X, yA + 202), "pesquisas e avaliações pontuais", f_leg, CINZA, p * a)
        # tira de filme: continuidade
        texto(d, (X, yB - 74), "LONGITUDINAL", f_rot, ACQUA, out_cubic((t-1.5)/0.4) * a)
        p2 = out_cubic((t - 1.8) / 1.5)
        if p2 > 0:
            n = 16
            for i in range(n):
                if i / n > p2: break
                x = X + i * 82
                d.rounded_rectangle([x, yB, x + 70, yB + 168], 5,
                                    outline=(*ACQUA, int(235 * a)), width=3)
                for k in (yB + 10, yB + 146):   # perfuracoes da pelicula
                    d.rectangle([x + 10, k, x + 22, k + 12], fill=(*ACQUA, int(150 * a)))
        p3 = out_cubic((t - 3.2) / 0.6)
        if p3 > 0: texto(d, (X, yB + 202), "mudança observada ao longo do tempo", f_leg, BRANCO, p3 * a)
    return desenha

def ilu_longitudinal(dur):
    """Um ponto isolado nao diz nada; a serie no tempo revela o padrao."""
    f_leg, f_rot = fonte(400, 36), fonte(600, 32)
    X0, X1, Y = 300, 1620, 660
    pts = [(0.00, 0.35), (0.12, 0.30), (0.24, 0.52), (0.36, 0.44), (0.48, 0.68),
           (0.60, 0.58), (0.72, 0.82), (0.84, 0.74), (1.00, 0.95)]
    def desenha(img, d, t):
        a = veu(img, t, dur)
        if a <= 0: return
        texto(d, (X0, 300), "UMA INTERAÇÃO ISOLADA NÃO EXPLICA UMA PESSOA", f_rot, CINZA,
              out_cubic(t/0.4) * a)
        # eixo
        p0 = out_cubic((t - 0.3) / 0.8)
        regua(d, X0, Y + 4, (X1 - X0) * p0, 3, (90, 100, 108), a)
        # ponto solto
        p1 = out_cubic((t - 0.6) / 0.4)
        if p1 > 0:
            cy = Y - 0.35 * 260
            d.ellipse([X0 + 330 - 13, cy - 13, X0 + 330 + 13, cy + 13], fill=(*CINZA, int(255*p1*a)))
        # serie completa
        p2 = out_cubic((t - 1.6) / 2.0)
        if p2 > 0:
            ant = None
            for fx, fy in pts:
                if fx > p2: break
                x, y = X0 + (X1 - X0) * fx, Y - fy * 260
                if ant: d.line([*ant, x, y], fill=(*ACQUA, int(220 * a)), width=4)
                ant = (x, y)
                d.ellipse([x-11, y-11, x+11, y+11], fill=(*ACQUA, int(255 * a)))
        p3 = out_cubic((t - 3.4) / 0.6)
        if p3 > 0:
            texto(d, (X0, Y + 56), "o padrão aparece na repetição e na mudança ao longo do tempo", f_leg, BRANCO, p3 * a)
    return desenha

def ilu_camada(dur):
    """Modelos de terceiros embaixo, camada AMALIA no meio, aplicacoes em cima."""
    f_cx, f_rot, f_leg = fonte(600, 30), fonte(700, 46), fonte(400, 28)
    X, LARG, Y = 300, 1320, 300
    def caixa(d, y, h, txt, f, cor, p, a, preenche=False):
        if p <= 0: return
        al = int(255 * p * a)
        if preenche:
            # Fundo escuro, nao acqua translucido: com fill claro o tijolo da cena
            # atravessa e o nome do projeto deixa de ler.
            d.rounded_rectangle([X, y, X + LARG, y + h], 10, fill=(6, 14, 12, int(238 * p * a)),
                                outline=(*cor, al), width=3)
        else:
            d.rounded_rectangle([X, y, X + LARG, y + h], 10, outline=(*cor, al), width=3)
        texto(d, (X + LARG/2, y + h/2), txt, f, cor if preenche else BRANCO, p * a, ancora="mm")
    def desenha(img, d, t):
        a = veu(img, t, dur)
        if a <= 0: return
        # 1. modelos de terceiros
        for i, m in enumerate(["LLM A", "LLM B", "LLM C", "LLM D"]):
            p = out_cubic((t - 0.2 - i * 0.14) / 0.45)
            if p <= 0: continue
            x = X + i * (LARG / 4)
            d.rounded_rectangle([x + 8, Y + 320, x + LARG/4 - 8, Y + 392], 8,
                                outline=(*CINZA, int(220 * p * a)), width=3)
            texto(d, (x + LARG/8, Y + 356), m, f_cx, CINZA, p * a, ancora="mm")
        p = out_cubic((t - 1.0) / 0.5)
        if p > 0: texto(d, (X, Y + 414), "modelos de terceiros, substituíveis", f_leg, CINZA, p * a)
        # 2. setas subindo
        p2 = out_cubic((t - 1.4) / 0.5)
        for i in range(4):
            if p2 <= 0: break
            x = X + i * (LARG/4) + LARG/8
            d.line([x, Y + 318, x, Y + 318 - 46 * p2], fill=(*AZUL, int(220 * a)), width=3)
        # 3. camada AMALIA: o nucleo proprietario
        caixa(d, Y + 180, 92, "AMALIA · camada proprietária brasileira", f_rot, ACQUA,
              out_cubic((t - 1.9) / 0.6), a, preenche=True)
        # 4. aplicacoes
        p3 = out_cubic((t - 2.7) / 0.5)
        for i in range(4):
            if p3 <= 0: break
            x = X + i * (LARG/4) + LARG/8
            d.line([x, Y + 178, x, Y + 178 - 46 * p3], fill=(*AZUL, int(220 * a)), width=3)
        caixa(d, Y + 40, 78, "aplicações", fonte(600, 38), BRANCO, out_cubic((t - 3.1) / 0.6), a)
    return desenha

# ------------------------------------------------------------------- socios
SOCIOS = [("Arthur Luiz", "Tecnologia", "AL", 0.0),
          ("Anaclaudia Zani", "Metodologia", "AZ", 4.4),
          ("Marina Marzotto", "Produto", "MM", 9.3),
          ("Clésio Souza", "Operação e marketing", "CS", 17.8)]

def socios(dur):
    """Um avatar por socio, entrando quando o Clesio cita cada um.

    Se a foto existir em edit/fotos/<iniciais>.png ela e usada; senao entra o
    monograma. As fotos estao no Drive mas ainda nao foram compartilhadas.
    """
    f_nome, f_cargo, f_mono = fonte(600, 34), fonte(400, 26), fonte(700, 52)
    R, Y = 72, 300
    cache = {}
    def foto(ini):
        if ini in cache: return cache[ini]
        p = FOTOS / f"{ini}.png"
        im = None
        if p.exists():
            im = Image.open(p).convert("RGBA").resize((R*2, R*2), Image.LANCZOS)
            mask = Image.new("L", (R*2, R*2), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, R*2-1, R*2-1], fill=255)
            im.putalpha(mask)
        cache[ini] = im
        return im
    def desenha(img, d, t):
        _, a = janela(t, 0, 1, saida=dur)
        scrim(img, 0, Y - 170, 560, Y + 4 * 190 + 60, forca=180, alfa=a)
        for i, (nome, cargo, ini, atraso) in enumerate(SOCIOS):
            p = out_cubic((t - atraso) / 0.6)
            if p <= 0: continue
            yy = Y + i * 190
            cx = 210 + 14 * (1 - p)
            al = int(255 * p * a)
            im = foto(ini)
            if im is not None:
                img.alpha_composite(Image.blend(Image.new("RGBA", im.size, (0,0,0,0)), im, p * a),
                                    (int(cx - R), int(yy - R)))
            else:
                d.ellipse([cx-R, yy-R, cx+R, yy+R], fill=(*AZUL, int(70 * p * a)),
                          outline=(*ACQUA, al), width=3)
                texto(d, (cx, yy), ini, f_mono, ACQUA, p * a, ancora="mm")
            texto(d, (cx + R + 34, yy - 26), nome.upper(), f_nome, BRANCO, p * a)
            texto(d, (cx + R + 34, yy + 16), cargo, f_cargo, ACQUA, p * a)
    return desenha

# ------------------------------------------------------------------ manifesto
PECAS = [
    ("gc-marina",        2.00,  5.0, lambda: gc("Marina Marzotto", "Produto", 5.0)),
    ("ilu-filme",       33.20,  7.0, lambda: ilu_filme(7.0)),
    ("eita-sigla",      68.00,  6.5, lambda: sigla(6.5)),
    ("num-usuarios",   122.80,  8.5, lambda: numeros(
        [(35000, "usuários no B2C", "aplicações em produção", 0.0),
         (1200,  "usuários no B2B", "empresas e projetos-piloto", 3.6)], 8.5)),
    ("chip-colombia",  134.80,  5.0, lambda: chip("1ª aplicação internacional",
        ["Colômbia, 2026", "acolhimento a pessoas afetadas por desastre"], 5.0)),
    ("titulo-amalia",  158.60,  5.2, lambda: titulo("AMALIA",
        "Arquitetura Multiagente de IA", 5.2)),
    ("bullets-desafios", 219.60, 7.5, lambda: chip("O que o AMALIA precisa resolver",
        ["memória longitudinal", "segurança e confiabilidade",
         "privacidade e governança"], 7.5, y=620)),
    ("ilu-longitudinal", 250.40, 7.0, lambda: ilu_longitudinal(7.0)),
    ("gc-clesio",      264.90,  5.0, lambda: gc("Clésio Souza", "Operação e marketing", 5.0)),
    ("num-retencao",   281.80, 11.5, lambda: numeros(
        [("75%", "dos usuários retornam", "para falar novamente", 0.0),
         (200,   "mensagens por mês", "média por usuário", 7.2)], 11.5)),
    ("chip-24meses",   295.40,  4.5, lambda: chip("24 meses de projeto",
        ["equipe multidisciplinar", "tecnologia, psicologia, neurociência e gestão"], 4.5)),
    ("socios",         306.60, 26.0, lambda: socios(26.0)),
    ("chip-finep",     360.40,  6.0, lambda: chip("FINEP · Tecnologias Digitais",
        ["Linha 1, subtema 1.1",
         "Plataformas Nacionais para Operação e Escala de Sistemas de IA"], 6.0)),
    ("ilu-camada",     383.00,  7.5, lambda: ilu_camada(7.5)),
    ("cartela-final",  438.30,  5.5, lambda: titulo("AMALIA", "EITA Mental Tech", 5.5)),
]

if __name__ == "__main__":
    import json
    alvo = sys.argv[1] if len(sys.argv) > 1 else None
    for nome, ini, dur, fab in PECAS:
        if alvo and alvo != nome: continue
        render(nome, dur, fab())
        print(f"  {nome:18s} {ini:7.2f}s +{dur:4.1f}s")
    json.dump([{"file": f"animacoes/{n}.mov", "start_in_output": i, "duration": d}
               for n, i, d, _ in PECAS],
              open("overlays.json", "w"), indent=2)
    print(f"{len(PECAS)} pecas -> overlays.json")
