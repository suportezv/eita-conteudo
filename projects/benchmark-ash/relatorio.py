#!/usr/bin/env python3
"""Monta o relatorio de benchmark da Ash como pagina HTML (artifact) com as folhas de contato embutidas."""
import base64, io, os, json
from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
OUT = "/tmp/claude-0/-home-user-eita-conteudo/122ef73e-ceef-56ef-b427-e72dd6deefbc/scratchpad/bench-report/benchmark-ash.html"

def img(name, w=1400, q=72):
    p = os.path.join(RAIZ, "folhas", name)
    im = Image.open(p).convert("RGB")
    if im.width > w:
        im = im.resize((w, int(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def fig(name, legenda, w=1400):
    return f'<figure><img src="{img(name, w)}" alt="{legenda}" loading="lazy"><figcaption>{legenda}</figcaption></figure>'

tr = json.load(open(os.path.join(RAIZ, "transcricoes.json")))

CSS = """<title>Benchmark Ash</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;700;800&family=JetBrains+Mono:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
:root{--papel:#F5F7F6;--tinta:#17202A;--apoio:#3A4754;--mudo:#65727F;--verde:#00EFA9;--verde-prof:#0A7757;--verde-suave:#D6F7EB;--borda:#DFE8EB;--card:#FFFFFF;--ash:#C9BFE6;--ash-ink:#2E2650;--alerta-bg:#FFF3D6;--alerta-bd:#F0DCA8;--alerta:#7A4E00}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--papel:#101820;--tinta:#E8EEEC;--apoio:#B7C2C4;--mudo:#7E8C90;--verde-prof:#39D9A4;--verde-suave:#123D31;--borda:#243038;--card:#18222B;--ash:#3A3358;--ash-ink:#D9D2F0;--alerta-bg:#2E2411;--alerta-bd:#4A3A18;--alerta:#F0C979}}
:root[data-theme="dark"]{--papel:#101820;--tinta:#E8EEEC;--apoio:#B7C2C4;--mudo:#7E8C90;--verde-prof:#39D9A4;--verde-suave:#123D31;--borda:#243038;--card:#18222B;--ash:#3A3358;--ash-ink:#D9D2F0;--alerta-bg:#2E2411;--alerta-bd:#4A3A18;--alerta:#F0C979}
*{box-sizing:border-box}
body{background:var(--papel);color:var(--tinta);font-family:"Source Serif 4",Georgia,serif;margin:0;padding:44px 20px 100px;font-size:17px;line-height:1.6}
.wrap{max-width:880px;margin:0 auto}
.eyebrow{display:flex;align-items:center;gap:10px;font-family:"JetBrains Mono",monospace;font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--verde-prof)}
.eyebrow::before{content:"";width:18px;height:3px;background:var(--verde-prof)}
h1{font-family:"League Spartan",system-ui,sans-serif;font-weight:800;font-size:clamp(34px,6vw,50px);letter-spacing:-.02em;line-height:1.02;margin:14px 0 12px;text-wrap:balance}
.lede{font-size:20px;line-height:1.5;color:var(--apoio);max-width:64ch;margin:0 0 18px}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 44px}
.meta span{font-family:"JetBrains Mono",monospace;font-size:12px;font-weight:600;letter-spacing:.06em;padding:6px 12px;border:1px solid var(--borda);border-radius:999px;background:var(--card);color:var(--mudo)}
h2{font-family:"League Spartan",system-ui,sans-serif;font-weight:800;font-size:30px;letter-spacing:-.02em;line-height:1.08;margin:60px 0 14px;text-wrap:balance}
h3{font-family:"League Spartan",system-ui,sans-serif;font-weight:700;font-size:21px;letter-spacing:-.01em;margin:34px 0 8px}
p{max-width:66ch;margin:0 0 16px}
ul,ol{max-width:66ch;padding-left:22px;margin:0 0 18px}li{margin:0 0 8px}
strong{font-weight:600}
.num{font-family:"JetBrains Mono",monospace;font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--verde-prof)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:0 0 30px}
.kpi{background:var(--card);border:1px solid var(--borda);border-radius:12px;padding:16px 18px}
.kpi b{display:block;font-family:"League Spartan",system-ui,sans-serif;font-size:34px;font-weight:800;letter-spacing:-.02em;line-height:1;margin-bottom:6px}
.kpi span{font-size:13.5px;color:var(--mudo);line-height:1.4}
.tabela{overflow-x:auto;margin:0 0 26px;border:1px solid var(--borda);border-radius:12px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14.5px;font-family:system-ui,sans-serif}
th{text-align:left;font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mudo);padding:12px 14px;border-bottom:1px solid var(--borda);white-space:nowrap}
td{padding:11px 14px;border-bottom:1px solid var(--borda);vertical-align:top;line-height:1.45}
tr:last-child td{border-bottom:none}
td.pos{font-family:"JetBrains Mono",monospace;font-weight:700;color:var(--verde-prof);white-space:nowrap}
figure{margin:18px 0 26px;background:var(--card);border:1px solid var(--borda);border-radius:12px;padding:10px;overflow-x:auto}
figure img{display:block;width:100%;min-width:640px;border-radius:6px}
figcaption{font-family:"JetBrains Mono",monospace;font-size:12px;color:var(--mudo);padding:10px 4px 2px;line-height:1.5}
.anuncio{background:var(--card);border:1px solid var(--borda);border-radius:14px;padding:22px 24px;margin:0 0 18px}
.anuncio .top{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 14px;margin-bottom:8px}
.anuncio h3{margin:0}
.chip{font-family:"JetBrains Mono",monospace;font-size:11px;font-weight:700;letter-spacing:.08em;padding:3px 9px;border-radius:5px;background:var(--verde-suave);color:var(--verde-prof)}
.chip.ash{background:var(--ash);color:var(--ash-ink)}
blockquote{margin:14px 0;padding:14px 18px;border-left:3px solid var(--verde);background:var(--verde-suave);border-radius:0 10px 10px 0;font-style:italic;max-width:66ch}
blockquote p{margin:0}
.licao{display:grid;grid-template-columns:52px 1fr;gap:14px;padding:18px 0;border-top:1px solid var(--borda)}
.licao:last-of-type{border-bottom:1px solid var(--borda)}
.licao .n{font-family:"League Spartan",system-ui,sans-serif;font-weight:800;font-size:30px;line-height:1;color:var(--verde-prof)}
.licao h3{margin:2px 0 6px;font-size:19px}
.licao p{margin:0 0 6px;font-size:16px}
.ideia{background:var(--card);border:1px solid var(--borda);border-radius:14px;padding:22px 24px;margin:0 0 16px}
.ideia .rot{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
.ideia h3{margin:0 0 6px}
.ideia .gancho{font-family:"League Spartan",system-ui,sans-serif;font-weight:700;font-size:20px;letter-spacing:-.01em;line-height:1.25;margin:4px 0 12px;color:var(--tinta)}
.ideia dl{display:grid;grid-template-columns:110px 1fr;gap:6px 14px;margin:0;font-size:15.5px}
.ideia dt{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mudo);padding-top:4px}
.ideia dd{margin:0}
.aviso{margin:22px 0;padding:14px 18px;background:var(--alerta-bg);border:1px solid var(--alerta-bd);border-radius:10px;color:var(--alerta);font-size:15px;line-height:1.55;max-width:none}
details{margin:0 0 10px;border:1px solid var(--borda);border-radius:10px;background:var(--card)}
summary{cursor:pointer;padding:12px 16px;font-family:"JetBrains Mono",monospace;font-size:12.5px;font-weight:600}
details .corpo{padding:0 16px 14px;font-size:15px;color:var(--apoio)}
.foot{margin-top:60px;padding-top:16px;border-top:1px solid var(--borda);font-family:"JetBrains Mono",monospace;font-size:12px;line-height:1.8;color:var(--mudo)}
@media (max-width:640px){.ideia dl{grid-template-columns:1fr}.licao{grid-template-columns:40px 1fr}}
</style>"""

def anuncio(pos, titulo, chips, corpo, folha=None, legenda=""):
    ch = "".join(f'<span class="chip{" ash" if c.startswith("Ash") else ""}">{c}</span>' for c in chips)
    f = fig(folha, legenda) if folha else ""
    return f'<div class="anuncio"><div class="top"><span class="num">{pos}</span><h3>{titulo}</h3>{ch}</div>{corpo}{f}</div>'

def ideia(n, titulo, gancho, origem, formato, roteiro, twist, cuidado=None):
    c = f"<dt>Cuidado</dt><dd>{cuidado}</dd>" if cuidado else ""
    return (f'<div class="ideia"><div class="rot"><span class="num">IDEIA {n:02d}</span><span class="chip ash">vem de: {origem}</span>'
            f'<span class="chip">{formato}</span></div><h3>{titulo}</h3><p class="gancho">{gancho}</p>'
            f'<dl><dt>Estrutura</dt><dd>{roteiro}</dd><dt>Virada EITA</dt><dd>{twist}</dd>{c}</dl></div>')

H = []
H.append(CSS)
H.append('<div class="wrap">')
H.append('<div class="eyebrow">Benchmark de anúncios</div>')
H.append('<h1>O que a Ash está fazendo nos anúncios, e o que a EITA leva disso</h1>')
H.append('<p class="lede">Análise dos 30 anúncios mais veiculados da Ash, o app americano de "IA para saúde mental" da Slingshot AI, vistos vídeo a vídeo e copy a copy, com as lições que se transferem para a EITA e dez ideias de anúncio prontas para produzir.</p>')
H.append('<div class="meta"><span>BIBLIOTECA DE ANÚNCIOS META · EUA</span><span>30 DE 164 ATIVOS · POR IMPRESSÕES</span><span>19 VÍDEOS · 11 DINÂMICOS</span><span>14 DE SETEMBRO DE 2026</span></div>')

# ---------- resumo executivo ----------
H.append('<h2>O essencial em um minuto</h2>')
H.append('<div class="kpis">'
 '<div class="kpi"><b>9 de 11</b><span>dos anúncios mais vistos são o mesmo roteiro: "por que não usar o ChatGPT no meu término?"</span></div>'
 '<div class="kpi"><b>11</b><span>conceitos de vídeo distintos nos 19 vídeos; o resto é o mesmo arquivo duplicado por loja e canal</span></div>'
 '<div class="kpi"><b>1</b><span>única copy de texto para todos os 19 vídeos. A diferenciação está 100% dentro do vídeo</span></div>'
 '<div class="kpi"><b>10 a 31 s</b><span>duração dos vídeos; a maioria entre 15 e 21 segundos</span></div>'
 '</div>')
H.append('<p>A Ash não vende "IA para saúde mental". Ela vende uma <strong>comparação</strong>: o ChatGPT diz o que você quer ouvir, a Ash diz o que você precisa ouvir. Doze dos dezenove vídeos e a principal família de anúncios estáticos giram nessa mesma dobradiça. O inimigo escolhido não é a terapia nem o terapeuta, é a ferramenta genérica que o público já usa para desabafar. Isso resolve dois problemas de uma vez: explica o produto por contraste com algo conhecido e desarma a objeção "já tenho o ChatGPT para isso".</p>')
H.append('<p>Em formato, são dois sistemas que se repetem. O primeiro é o <strong>criador respondendo a um comentário</strong>, no estilo nativo do TikTok, com a pergunta de um seguidor na tela, corte para a gravação do app aos oito segundos e o ícone do produto no fim. O segundo é a <strong>esquete com atores rotulados</strong> "ChatGPT", "Claude" e "Ash", em que cada IA responde ao mesmo dilema e a Ash sempre fecha com uma única pergunta reflexiva. Nos dois, o produto aparece falando: a fala da Ash é o clímax do anúncio, não a promessa sobre ela.</p>')
H.append('<p>A parte mais transferível para a EITA não é nenhum anúncio específico. É o método: uma tese clara de posicionamento por contraste, um roteiro que prova a tese em vinte segundos deixando o produto dar a última palavra, três aberturas gravadas para o mesmo corpo, e duplicação sistemática do vencedor por loja e por canal. E a Ash deixa espaços abertos que a EITA ocupa com facilidade: zero atrito de instalação (é WhatsApp), voz e personagem próprios, preço declarado, criadora com credencial, e uma linha editorial que fala com mulheres brasileiras, público que os anúncios da Ash quase não representam.</p>')

# ---------- quem e a Ash ----------
H.append('<h2>Quem é a Ash</h2>')
H.append('<p><strong>Ash</strong> é o produto da <strong>Slingshot AI</strong> (Nova York), lançado em julho de 2025 como "a primeira IA desenhada para terapia" e hoje descrito no site como "IA para saúde mental", para maiores de 18 anos. A empresa levantou US$ 93 milhões (a16z, Radical Ventures, Forerunner, Felicis, Menlo) e é dirigida por Daniel Cahn (CEO, engenheiro de IA) e Neil Parikh (presidente, cofundador da Casper). Diz ter treinado um modelo próprio "para psicologia" com dados clínicos e mantém time clínico e conselho consultivo nomeados. Reporta mais de 150 mil usuários.</p>')
H.append('<p>Três fatos mudam a leitura dos anúncios. Primeiro, <strong>o app é gratuito</strong>, sem plano pago por enquanto, com assinatura prevista. Por isso a Ash nunca precisa vender preço e pode gastar toda a mensagem em posicionamento e em instalação. Segundo, o produto é <strong>app nativo</strong> (iOS e Android): todo anúncio termina em "Install now" ou "Download", e o funil paga o custo da instalação. Terceiro, a empresa carrega <strong>ruído de credibilidade</strong>: o estudo próprio de eficácia foi contestado por pesquisadores independentes ouvidos pela STAT, e em janeiro de 2026 a Ash saiu do Reino Unido por falta de caminho regulatório. Isso explica a insistência dos anúncios estáticos em "designed by mental health experts" e no selo "featured in and studied by researchers at NYU, The New York Times".</p>')
H.append('<h3>Como os dados foram obtidos</h3>')
H.append('<p>A Biblioteca de Anúncios da Meta, filtrada por anúncios ativos nos Estados Unidos e ordenada por impressões totais, lista 164 anúncios ativos da página "Ash - AI for Mental Health" (facebook.com/talktoashai). Esta análise cobre os 30 primeiros do ranking, ou seja, os mais veiculados. Para o mercado americano a biblioteca não publica número de impressões por anúncio, só a ordem. Os 19 vídeos foram baixados, transcritos com marcação de tempo e assistidos por frames; os 11 anúncios dinâmicos tiveram todos os cards de copy e imagem extraídos. Os arquivos ficam em <code>projects/benchmark-ash/</code> no repositório do estúdio.</p>')

# ---------- ranking ----------
H.append('<h2>O ranking, agrupado por conceito</h2>')
H.append('<p>Dos 19 vídeos, 11 são conceitos distintos. O resto é o mesmo arquivo, byte a byte, repetido para iOS, Android e o link universal, ou com uma abertura regravada. A tabela mostra onde cada conceito aparece no ranking dos 30.</p>')
H.append('<div class="tabela"><table><thead><tr><th>Posições</th><th>Conceito</th><th>Formato</th><th>Dura</th><th>O que faz</th></tr></thead><tbody>'
 '<tr><td class="pos">1 a 7, 10, 11</td><td><strong>Término vs ChatGPT</strong>, criador ruivo respondendo comentário</td><td>Vídeo, criador + app</td><td>19 a 21 s</td><td>O roteiro campeão. Três aberturas diferentes ("Why not just talk to ChatGPT about my breakup?", "Why can\'t I use ChatGPT when I\'m trying to move on?", "Why use Ash after a breakup when there\'s ChatGPT?") sobre o mesmo corpo, mais uma variante de corpo (posição 7). Duplicado por loja.</td></tr>'
 '<tr><td class="pos">8, 9</td><td><strong>"Your head is loud. Ash listens."</strong></td><td>Dinâmico, estático</td><td>·</td><td>Arte tipográfica em papel kraft: "They\'re living rent-free in your head. Evict them." Copy sobre a mensagem que você analisa demais e a pessoa que não sai da cabeça.</td></tr>'
 '<tr><td class="pos">12, 13, 14</td><td><strong>Esquete "people pleaser"</strong>, três atores</td><td>Vídeo, esquete</td><td>15,6 s</td><td>Título "How AI solves your toxic behaviors". ChatGPT dá um script, Claude dá uma definição, Ash pergunta "What would happen if you said no?"</td></tr>'
 '<tr><td class="pos">15</td><td><strong>Esquete "journaling"</strong>, banco de praça</td><td>Vídeo, esquete</td><td>11,9 s</td><td>Título "Getting AI advice to ease your mind". ChatGPT sugere um diário e um link de compra; Ash pergunta o que você evita ficando na cabeça em vez do corpo.</td></tr>'
 '<tr><td class="pos">16, 17</td><td><strong>Ponto de ônibus "need vs want"</strong></td><td>Dinâmico, mockup</td><td>·</td><td>Foto de abrigo de ônibus com o cartaz "An AI that tells you what you need to hear, not what you want to hear."</td></tr>'
 '<tr><td class="pos">18</td><td><strong>"ChatGPT will not help you get over your breakup"</strong>, criador de cabelo cacheado</td><td>Vídeo, criador + app</td><td>31,3 s</td><td>Versão mais longa e argumentativa do conceito 1, com o selo "input from mental health professionals".</td></tr>'
 '<tr><td class="pos">19, 21, 22, 23, 25, 27</td><td><strong>Família tipográfica lilás</strong></td><td>Dinâmico, estático</td><td>·</td><td>Quatro artes: "need to hear vs want to hear", "Ash is your space to... be you", "the job you built your identity around turned toxic", e a piada da gorjeta vs "would you still love me if I was a beetle".</td></tr>'
 '<tr><td class="pos">20</td><td><strong>"Can I use this to trauma dump?"</strong></td><td>Vídeo, criador podcast + app</td><td>18,8 s</td><td>Responde a objeção de uso com o argumento de disponibilidade: "available in the middle of the day, boom, whip it out, talk to Ash".</td></tr>'
 '<tr><td class="pos">24, 26</td><td><strong>Esquetes de ansiedade</strong>, banco de praça</td><td>Vídeo, esquete</td><td>11,7 e 13,5 s</td><td>"You ask AI if it\'s normal to feel anxious for no reason" e "When your email inbox triggers your fight/flight response". Ash fecha com "Let\'s talk about the root of this" e "What are you afraid of finding when you open it up?"</td></tr>'
 '<tr><td class="pos">28</td><td><strong>"Meet Ash. Your space."</strong></td><td>Dinâmico, estático</td><td>·</td><td>Nuvem de verbos manuscrita em rosa: "Speak the middle-of-the-night thoughts... Come as you are, leave clearer."</td></tr>'
 '<tr><td class="pos">29</td><td><strong>"Why shouldn\'t I use ChatGPT to get over my ex?"</strong></td><td>Vídeo, criador + onboarding</td><td>22,9 s</td><td>Mesmo criador da posição 18, mostrando as telas de onboarding ("What\'s weighing on you most right now?", "What strengths can you build on?").</td></tr>'
 '<tr><td class="pos">30</td><td><strong>Texto sobre B-roll</strong>, ponto de vista feminino</td><td>Vídeo, UGC de texto</td><td>9,4 s</td><td>"If your friends praise you for keeping your standards high but you\'re secretly terrified that you never make it past the third date..." O único anúncio com narradora mulher, e sem fala.</td></tr>'
 '</tbody></table></div>')
H.append(fig("previews.jpg", "Os 19 vídeos pelo frame de capa, na ordem do ranking. Da esquerda para a direita e de cima para baixo: o criador ruivo domina o topo; esquetes e outros criadores preenchem o meio; o UGC de texto fecha a lista.", 1400))

# ---------- anatomia dos videos ----------
H.append('<h2>Anatomia dos vídeos, um a um</h2>')
H.append('<p>Cada conceito abaixo tem a transcrição integral, o que o vídeo mostra na tela e o que a Ash está tentando provar com ele.</p>')

H.append(anuncio("POSIÇÕES 1 A 7, 10, 11", "Término vs ChatGPT, o roteiro campeão", ["Vídeo", "Criador + app", "19 a 21 s", "Ash fala no fim"],
 '<p>Um criador ruivo, de camisa xadrez, em casa, com microfone de lapela. Abre com o adesivo nativo do TikTok "Reply to Charles\'s comment: Why not just talk to ChatGPT about my breakup?". Aos 1,6 segundos aparece o logo do ChatGPT com um X vermelho. Legenda palavra por palavra. Aos oito segundos corta para a tela do app: a conversa de onboarding e a pergunta "Which voice do you prefer?". Volta ao criador e fecha com o ícone da Ash sobre a frase "start feeling clearer today".</p>'
 '<blockquote><p>"Why not just talk to ChatGPT about my breakup? The reality is ChatGPT doesn\'t tell you what you need to hear, it just tells you what you wanna hear. Ash actually helps you process what happened. It helps you notice patterns, reflect, and understand what you need to move forward. It\'s built for mental health, not giving advice. Download Ash and start feeling clearer today."</p></blockquote>'
 '<p><strong>Por que funciona.</strong> A pergunta do comentário é a objeção número um do público, dita pelo público. O corpo responde com uma frase que vira slogan ("need to hear, not want to hear") e, em vez de listar funções, descreve um processo ("notice patterns, reflect, understand"). O "not giving advice" é o diferencial disfarçado de limitação. Note as três aberturas gravadas para o mesmo corpo (Charles, John e James) e a variante da posição 7, que troca "processar" por "desacelerar": "Ash is built to slow everything down, let you reflect, and let you reconnect with yourself. It shares insights with you based on your conversations".</p>',
 "v-1076494364960665.jpg", "Posição 1. Adesivo de comentário, X sobre o ChatGPT, corte para a tela do app aos 8 s, ícone no fim."))
H.append(fig("v-1055480560546019.jpg", "Posição 11, mesma peça com outra abertura: \"Why use Ash after a breakup when there's ChatGPT?\" O ícone da Ash entra já no segundo 2, e a tela de voz aos 12 s.", 1400))
H.append(fig("v-1051453634336510.jpg", "Posição 7, a variante de corpo: mesmo gancho, argumento de \"desacelerar\" e mais tempo de tela do app (seletor de voz e conversa em texto).", 1400))

H.append(anuncio("POSIÇÕES 12, 13, 14", "Esquete: como a IA resolve seus comportamentos tóxicos", ["Vídeo", "Esquete com 3 atores", "15,6 s", "Ash fala por último"],
 '<p>Três atores sentados em um banco de escritório, parede de tijolo branco, cada um com uma etiqueta sobre a cabeça: ChatGPT, Claude, Ash. Título fixo no topo: "How AI solves your toxic behaviors". Um plano só, sem cortes. Termina no cartão preto "Ash. AI for mental health. Talk through it now."</p>'
 '<blockquote><p>ChatGPT: "There\'s nothing wrong with being a people pleaser. Here\'s a script for you to follow." · Claude: "Boundaries are personal, so I\'m going to give you the operative definition of what a boundary is." · Ash: "Saying yes is easy for you. What would happen if you said no?"</p></blockquote>'
 '<p><strong>Por que funciona.</strong> A esquete transforma o posicionamento em comédia de caracteres: o ChatGPT é o amigo que entrega um roteiro pronto, o Claude é o que teoriza sem responder, a Ash é a que faz a pergunta que dói. É barato (um plano, três pessoas, um banco), curtíssimo e memorável. E, de novo, a Ash não descreve o que faz: ela faz.</p>',
 "v-4576795639276788.jpg", "Posição 12. Um único plano, etiquetas coloridas por personagem, cartão final padrão."))

H.append(anuncio("POSIÇÕES 15, 24, 26", "Esquetes no banco de praça: diário, ansiedade e caixa de e-mail", ["Vídeo", "Esquete com 2 atores", "12 a 13,5 s", "Ash fala por último"],
 '<p>Dois atores em um banco de parque, etiquetas Ash (lilás) e ChatGPT (verde). Três títulos, três dilemas, um plano cada.</p>'
 '<blockquote><p>"Getting AI advice to ease your mind". ChatGPT: "Hmm, that\'s interesting. Have you tried journaling before bed? Here\'s a link to purchase one now." Ash: "What are you avoiding by staying in your head instead of your body?"</p></blockquote>'
 '<blockquote><p>"You ask AI if it\'s normal to feel anxious for no reason". ChatGPT: "Absolutely. And if you don\'t know the reason, I can make 10 guesses to make you feel even more anxious." Ash: "Anxiety rarely comes from nowhere. Let\'s talk about the root of this."</p></blockquote>'
 '<blockquote><p>"When your email inbox triggers your fight/flight response". ChatGPT: "Look at you, showing up for yourself just by thinking about it. Here\'s how to break this task into 19 smaller steps." Ash: "I hear you. Inbox anxiety is real. What are you afraid of finding when you open it up?"</p></blockquote>'
 '<p><strong>Por que funciona.</strong> A piada é sempre a mesma e sempre nova: o ChatGPT responde com produtividade, lista ou compra; a Ash responde com uma pergunta sobre a raiz. Cada esquete mira um gatilho cotidiano específico (dormir, ansiedade sem motivo, caixa de entrada), o que permite testar dezenas de dilemas com o mesmo elenco e o mesmo banco.</p>',
 "v-1063698926550292.jpg", "Posição 15, a esquete do diário. Repare no cartão final cortado (\"Talk through i\"): eles publicam sem polir, e não faz diferença no ranking."))
H.append(fig("v-1584040616524659.jpg", "Posição 26, a esquete da caixa de e-mail. Mesmo banco, mesmos atores, título diferente.", 1400))

H.append(anuncio("POSIÇÕES 18 E 29", "O criador cacheado: a versão longa e a versão com onboarding", ["Vídeo", "Criador + app", "31,3 s e 22,9 s", "Ash fala no fim"],
 '<p>Um segundo criador, cabelo cacheado, camisa polo preta, em um apartamento com pôsteres e halteres ao fundo, microfone de mesa. Mesmo adesivo de comentário ("Can ChatGPT get me through a break-up?" e "Why shouldn\'t I use ChatGPT to get over my ex?"). A versão longa é a mais argumentativa dos trinta anúncios; a curta mostra as telas de onboarding com os checkboxes "What\'s weighing on you most right now?" (work or studies, a relationship, friendships, family, my health) e "What strengths can you build on?".</p>'
 '<blockquote><p>"ChatGPT will not help you get over your breakup. ChatGPT\'s whole thing is agreeing with you, which feels good for five minutes, but then you\'re still lost. Ash helps you get honest with yourself, and not just vent, but actually notice where you\'re stuck so you can finally step out of it. It\'s built for emotional support with input from mental health professionals, not repurposed from a chatbot built to say anything about anything. Download Ash and actually start moving forward."</p></blockquote>'
 '<p><strong>O que muda aqui.</strong> Entra o argumento de autoridade ("input from mental health professionals", "built with real licensed therapists") e o ataque mais direto ("agreeing with you feels good for five minutes, but then you\'re still lost"). É o mesmo posicionamento com o volume mais alto, e fica atrás das versões curtas do criador ruivo no ranking.</p>',
 "v-1845874046587270.jpg", "Posição 18. Cortes de enquadramento a cada 4 segundos para segurar atenção em um vídeo de 31 s; cartão final e tela do seletor de voz."))
H.append(fig("v-2238847626963495.jpg", "Posição 29. As telas de onboarding com checkboxes são a demonstração mais concreta do produto em todo o conjunto.", 1400))

H.append(anuncio("POSIÇÃO 20", "\"Can I use this to trauma dump?\"", ["Vídeo", "Criador estilo podcast + app", "18,8 s"],
 '<p>Um terceiro criador, fundo lilás, microfone de podcast. Responde a objeção de uso com tom de conversa, cheio de "you know" e "I mean", e ancora no argumento de disponibilidade e de acesso.</p>'
 '<blockquote><p>"Can I use this to trauma dump? Yeah. I mean, you can talk to Ash about anything big or small. There\'s no judgment, there\'s no shame. The whole point is it\'s available for you anytime you need it, twenty four/seven. And, you know, unlike going to get traditional help where you have to go to insurance, this is actually available in the middle of the day. If something happens to you at work, boom, whip it out, talk to Ash."</p></blockquote>'
 '<p><strong>O que ensina.</strong> A naturalidade proposital (hesitações, gíria) faz parecer resposta de gente, não leitura de roteiro. E o contraste aqui não é com o ChatGPT, é com o sistema de saúde ("insurance"): disponibilidade no meio do dia como benefício central.</p>',
 "v-2521174485016532.jpg", "Posição 20. Fundo colorido, microfone à vista, corte para a conversa em texto no app."))

H.append(anuncio("POSIÇÃO 30", "Texto sobre B-roll, ponto de vista feminino", ["Vídeo", "UGC de texto", "9,4 s", "Sem fala"],
 '<p>Cenas genéricas (trilhos de trem, mulher no sofá com celular, corredor de metrô) sob um bloco de texto fixo. Trilha com voz cantada ao fundo. É o único anúncio dos trinta com narradora mulher, e o único sem fala.</p>'
 '<blockquote><p>"If your friends praise you for keeping your standards high but you\'re secretly terrified that you never make it past the third date because something is wrong with you, this is for you. Talking through it and being brutally honest with myself helped me get to the person I wanted to be."</p></blockquote>'
 '<p><strong>O que ensina.</strong> O gancho é uma frase longa de identificação, do tipo "se você é assim, isso é para você", seguida de um depoimento em primeira pessoa. É o formato mais barato do conjunto e o que mais se aproxima do tom das pílulas da EITA.</p>',
 "v-1748936549569977.jpg", "Posição 30. Bloco de texto fixo sobre B-roll, sem rosto, sem fala."))

# ---------- estaticos ----------
H.append('<h2>Os anúncios estáticos e dinâmicos</h2>')
H.append('<p>Os 11 anúncios dinâmicos (DCO) combinam até quatro cards de imagem com quatro famílias de copy. Todas as artes carregam a mesma barra de confiança no rodapé: "Designed by mental health experts, powered by AI" e "Featured in + studied by researchers at: New York University, The New York Times". É aqui, e não nos vídeos, que a Ash coloca credencial.</p>')
H.append(anuncio("POSIÇÕES 8 E 9", "\"They\'re living rent-free in your head. Evict them.\"", ["Dinâmico", "Tipografia em kraft", "Ash com voz própria"],
 '<p>Fundo cor de papel kraft, tipografia serifada grande, uma linha de humor sobre a pessoa que ocupa a cabeça. A copy que acompanha: "The text you\'re overanalyzing, the conversation you\'re rehearsing, the person you can\'t stop thinking about. Ash is here for all of it." Título: "Your head is loud. Ash listens."</p>'
 '<p><strong>O que ensina.</strong> O estático mais bem ranqueado é o que tem uma ideia só, dita com graça, sem foto de produto. A copy lista três micro-cenas reconhecíveis em vez de benefícios.</p>',
 "c-1473424221214363.jpg", "Cards das posições 8 e 9, em formato quadrado e vertical."))
H.append(anuncio("POSIÇÕES 16, 17 E 19", "\"An AI that tells you what you need to hear, not what you want to hear.\"", ["Dinâmico", "Mockup de ponto de ônibus", "Tipografia lilás"],
 '<p>A mesma frase em dois tratamentos: um cartaz dentro de um abrigo de ônibus fotografado em rua europeia, e a versão limpa em fundo lilás com "Figure out what\'s actually going on and get clear on how to move forward, with Ash. Talk through it, privately."</p>'
 '<p><strong>O que ensina.</strong> O mockup de mídia exterior dentro do feed empresta escala e seriedade a uma marca pequena. E a frase "need to hear, not want to hear" atravessa vídeo e estático como o slogan de fato da campanha.</p>',
 "c-1315949403751734.jpg", "Posições 16 e 17: o abrigo de ônibus."))
H.append(fig("c-1043379568695363.jpg", "Posição 19: a mesma tese em tipografia lilás, quatro proporções.", 1400))
H.append(anuncio("POSIÇÕES 21, 22, 23, 25, 27, 28", "As outras famílias tipográficas", ["Dinâmico", "Tipografia", "Humor e listas"],
 '<p><strong>"The job you built your identity around turned toxic. Ash helps you remember who you are without it."</strong> Fundo azul com flores botânicas recortadas; copy "Life not going to plan? Ash is here." e "You don\'t need to have it figured out."</p>'
 '<p><strong>"Ash is your space to... be you."</strong> Uma nuvem de verbos em negrito: speak the middle-of-the-night thoughts, vent about how your boss put you on the spot, admit that you\'re not okay, spiral about the thing you said three years ago, miss someone you aren\'t supposed to miss. Fecha com "Come as you are, leave clearer." A mesma peça existe em versão manuscrita rosa, "Meet Ash. Your space.", e uma copy longa: "Ash is there for the late-night spirals, the half-formed thoughts, the moments you just need space. No fixing. No pressure."</p>'
 '<p><strong>"One AI writes an essay when you ask what a 20% tip on a $100 bill is. Another helps you figure out what is behind the \'Would you still love me if I was a beetle?\' question to your boyfriend at dinner."</strong> A piada mais afiada do conjunto: contrasta o uso utilitário do ChatGPT com a pergunta absurda e emocional que a Ash sabe ler.</p>'
 '<p><strong>"You could get a dog as an emotional crutch to avoid dealing with your need for external validation... or you could talk to Ash."</strong> Em outdoor de tijolo, com o rodapé "Ash is a place for all your thoughts. It listens, remembers, and never judges."</p>',
 "c-1054833593819008.jpg", "Posições 22 e 23: a família azul botânica."))
H.append(fig("c-1440039337569284.jpg", "Posição 25: a nuvem de verbos \"be you\", em quatro proporções.", 1400))
H.append(fig("c-1007596909000100.jpg", "Posição 27: gorjeta vs besouro.", 1400))
H.append(fig("c-2133572367515319.jpg", "Posição 21: o outdoor do cachorro.", 1400))
H.append(fig("c-1767798247746321.jpg", "Posição 28: \"Meet Ash. Your space.\", a versão manuscrita.", 1400))

# ---------- copy e funil ----------
H.append('<h2>Copy, funil e estrutura de mídia</h2>')
H.append('<p><strong>A copy dos vídeos é uma só</strong>, para os dezenove: título "Talk to Ash now, 24/7, voice or text" e texto "Get help today with your mental health - try Ash, the AI built for emotional wellbeing." A Ash não gasta esforço no texto do anúncio em vídeo; o vídeo carrega tudo. O título entrega três coisas em oito palavras: ação (talk), disponibilidade (24/7) e modalidade (voice or text).</p>')
H.append('<p><strong>Os dinâmicos têm quatro famílias de copy</strong>, e a genérica ("Start your mental health journey today with Ash") é a que mais aparece, dezoito vezes. As outras três são micro-cenas, sempre em segunda pessoa: "the text you\'re overanalyzing, the conversation you\'re rehearsing", "you don\'t need to have it figured out", "the late-night spirals, the half-formed thoughts". Nada de "ansiedade", "bem-estar" ou "autocuidado" como palavra: a emoção aparece como cena.</p>')
H.append('<p><strong>Funil.</strong> Todo anúncio manda para instalação: nove para a App Store, dez para o Google Play, onze para o link universal (onelink) que decide a loja. O rótulo de site é sempre "talktoash.com". Os CTAs são "Download" (23) e "Install now" (7). Não há landing page, não há preço, não há teste gratuito a anunciar porque o app já é gratuito.</p>')
H.append('<p><strong>Estrutura de mídia.</strong> Os vídeos rodam em Facebook e Instagram sempre, Threads na maioria, e seis deles também em Audience Network e Messenger. O mesmo arquivo aparece até cinco vezes no ranking com destinos diferentes: isso é conjunto de anúncios separado por loja e por canal, não variação criativa. Todos os vídeos são 720 por 1280, 30 quadros por segundo, entre 9 e 31 segundos. Nenhum declara mídia gerada por IA. Todos os 30 começaram a rodar entre 27 de agosto e 12 de setembro: a Ash renova o estoque de criativos a cada duas semanas e mantém o vencedor no ar.</p>')

# ---------- licoes ----------
H.append('<h2>O que a EITA leva disso</h2>')
licoes = [
 ("Escolha um inimigo que o público já usa", "A Ash não briga com a terapia, briga com o ChatGPT. Para a EITA, o mesmo inimigo existe no Brasil, e ainda mais forte: muita gente já desabafa com o ChatGPT no celular. Posicionar a EITA por contraste (\"diz o que você precisa ouvir\") explica o produto sem precisar explicar o produto."),
 ("Deixe o produto dar a última palavra", "Em quase todo anúncio da Ash a fala do produto é o clímax: uma pergunta curta, reflexiva, que o espectador leva para casa. A EITA tem algo que a Ash não tem, uma personagem com voz. Cada anúncio pode terminar com a Eita fazendo a pergunta, na voz dela."),
 ("Um roteiro, três aberturas", "O campeão da Ash é um único corpo com três ganchos diferentes gravados. Custa quinze minutos a mais de gravação e multiplica as chances de acertar o gancho. Vale adotar como regra de produção das pílulas."),
 ("Formato nativo de resposta a comentário", "O adesivo \"respondendo ao comentário de fulano\" transforma a objeção do público em gancho e faz o anúncio parecer conteúdo. É gratuito e a EITA ainda não usa."),
 ("Esquete com etiquetas: barata, escalável, memorável", "Um banco, dois ou três atores, uma etiqueta sobre cada cabeça, um título no topo. O mesmo set rende dezenas de dilemas diferentes em uma tarde de gravação."),
 ("Emoção como cena, não como palavra", "As copies da Ash nunca dizem \"ansiedade\" ou \"bem-estar\": dizem \"a mensagem que você está analisando demais\", \"a conversa que você está ensaiando\". A EITA já escreve assim nas captions; vale levar para as artes e para os títulos dos anúncios."),
 ("Mostre a tela cedo", "Aos oito segundos o vídeo sempre corta para o app. Para a EITA, a tela é o WhatsApp, que todo mundo conhece: um print de conversa com a Eita vale mais que qualquer ilustração de benefício."),
 ("Credencial no estático, leveza no vídeo", "A Ash separa os registros: os vídeos são irreverentes e os estáticos carregam \"designed by mental health experts\" e os selos NYU e New York Times. A EITA tem uma credencial real para ocupar esse lugar, a Neurocientista criadora do método EITA."),
 ("Mockup de mídia exterior dentro do feed", "Um cartaz falso em ponto de ônibus custa uma foto de banco de imagens e faz a marca parecer maior do que é."),
 ("Duplicar o vencedor é estratégia, não preguiça", "Nove dos onze primeiros são o mesmo conceito. Quando um anúncio funciona, a Ash o repete por loja, por canal e com aberturas novas, em vez de trocar de ideia. Renova o estoque a cada duas semanas, mas não abandona o campeão."),
]
for i,(t,p) in enumerate(licoes,1):
    H.append(f'<div class="licao"><div class="n">{i:02d}</div><div><h3>{t}</h3><p>{p}</p></div></div>')

H.append('<h3>Onde a EITA ganha da Ash</h3>')
H.append('<ul>'
 '<li><strong>Zero atrito.</strong> Todo anúncio da Ash termina em "Install now". A EITA mora no WhatsApp: "não precisa baixar nada" é um gancho que a Ash não pode usar.</li>'
 '<li><strong>Personagem e voz.</strong> A Ash é um ícone lilás e uma tela escura. A EITA tem rosto, voz e jeito de falar. Os anúncios podem ter a Eita como protagonista, não só como destino.</li>'
 '<li><strong>Público feminino.</strong> Dos 30 anúncios da Ash, um único tem ponto de vista feminino. As pílulas da EITA já falam com mulheres e podem ocupar esse espaço com naturalidade.</li>'
 '<li><strong>Preço e oferta.</strong> A Ash não tem preço para anunciar. A EITA tem, e é baixo. A promoção anual é um argumento que o concorrente americano ainda não tem como copiar.</li>'
 '<li><strong>Criadora com credencial.</strong> A Ash cita "experts" sem rosto. A EITA tem a Anaclaudia, Neurocientista criadora do método EITA, com nome e cara.</li>'
 '<li><strong>Guarda-corpos como confiança.</strong> "Não é terapia" e o CVV 188 já fazem parte do padrão da EITA. Dito com clareza, isso vira credibilidade, exatamente onde a Ash apanha na imprensa.</li>'
 '</ul>')

# ---------- 10 ideias ----------
H.append('<h2>Dez ideias de anúncio para a EITA</h2>')
H.append('<p>Cada ideia diz de qual anúncio da Ash ela vem, o formato, a estrutura e a virada que a torna da EITA, não uma cópia. Todas respeitam as regras da casa: a Eita fala como personagem, a criadora aparece com a credencial completa, "não é terapia" e o CVV 188 entram onde couber, e nenhum texto público leva travessão.</p>')
H.append('<div class="aviso"><strong>Sobre citar o ChatGPT.</strong> No Brasil a publicidade comparativa é permitida pelo CONAR desde que seja verdadeira, objetiva e não denigra o concorrente. As ideias abaixo comparam comportamentos ("dá lista", "concorda com você"), não qualidade. Vale uma revisão de texto antes de veicular, e nunca usar o logo do ChatGPT com X vermelho como a Ash faz: prefira o nome escrito ou "a IA genérica".</div>')

ideias = [
 (1, "Por que não desabafar com o ChatGPT?", "\"Por que eu não posso só falar com o ChatGPT sobre o meu término?\"",
  "posições 1 a 7", "Vídeo 20 s · criador + WhatsApp",
  "Adesivo de comentário na tela com a pergunta. Criador ou criadora responde em casa, microfone de lapela, legenda palavra por palavra. Aos 8 s corta para um print real de conversa com a Eita no WhatsApp. Fecha com a Eita fazendo uma pergunta em áudio.",
  "O corpo é o mesmo argumento da Ash traduzido: o ChatGPT concorda com você, a Eita pergunta o que você está evitando. A virada é o fim: em vez de ícone de app, entra a voz da Eita com a pergunta. Gravar três aberturas: \"por que não o ChatGPT\", \"a IA não serve pra isso?\" e \"já tenho o ChatGPT\".",
  "Comparação de comportamento, não de qualidade. Sem logo do concorrente."),
 (2, "Quando a IA vira sua psicóloga", "\"Quando a IA vira sua psicóloga\"",
  "posições 12 a 14", "Esquete 15 s · três atrizes rotuladas",
  "Três pessoas em um banco, etiquetas \"IA genérica\", \"IA de produtividade\" e \"Eita\". Título fixo no topo. Dilema: \"não consigo dizer não pra minha mãe\". A primeira entrega um roteiro de sete passos, a segunda define o que é limite, a Eita pergunta: \"O que aconteceria se você dissesse não uma vez?\"",
  "A Eita da esquete pode ser dublada pela voz da Ana, ou a atriz usa a fala e a legenda leva o nome da Eita. Elenco feminino, dilema brasileiro (mãe, sogra, grupo da família). Um set rende dez esquetes.",
  "Se rotular \"ChatGPT\" pelo nome, manter o comportamento verossímil e sem deboche."),
 (3, "Pílula com contraste", "\"Você pergunta pra IA se é normal sentir ansiedade do nada\"",
  "posições 24 e 26", "Pílula 12 s · VO + LIP",
  "Aproveita o formato que a EITA já produz. VO: a resposta da IA genérica (\"Claro. E se você não sabe o motivo, eu dou dez palpites pra você ficar mais ansiosa\"). LIP: a Eita fecha: \"Ansiedade quase nunca vem do nada. Vamos falar de onde ela começa.\"",
  "É a esquete da Ash dentro da linguagem das pílulas: a personagem animada faz o papel da Ash, sem elenco. Os dilemas das pílulas de outubro já servem de matéria-prima.",
  None),
 (4, "O que você precisa ouvir, às três da manhã", "\"Quem te diz o que você precisa ouvir. Às três da manhã. Sem julgar.\"",
  "posições 16, 17 e 19", "Arte estática · série De Para",
  "Tipografia grande em papel #F5F7F6, verde da marca só na palavra-chave. Rodapé de confiança: \"Criada pela Neurocientista Anaclaudia Zani, criadora do método EITA. Não é terapia. Apoio do dia a dia.\"",
  "A frase-slogan da Ash vira uma frase da EITA com o diferencial que a Ash não tem, a hora e o WhatsApp. O rodapé faz o papel dos selos NYU e New York Times com uma credencial real.",
  None),
 (5, "Mora de graça na sua cabeça", "\"Tem gente morando de graça na sua cabeça. Hora de despejar.\"",
  "posições 8 e 9", "Arte estática · tipografia",
  "Fundo kraft ou papel da marca, uma linha de humor, e a copy em micro-cenas: \"A mensagem que você leu vinte vezes. A conversa que você ensaia no banho. A pessoa que não sai da sua cabeça.\"",
  "O humor da Ash com expressão brasileira. A copy nunca diz \"ansiedade\": diz a cena. Fecha com \"Conversa com a Eita. Link na bio.\"",
  None),
 (6, "O ponto de ônibus", "\"Uma IA que diz o que você precisa ouvir, não o que quer ouvir.\"",
  "posições 16 e 17", "Arte estática · mockup de mídia exterior",
  "Foto de abrigo de ônibus ou empena em São Paulo com o cartaz da EITA montado por cima. Uma frase, o logo, \"no seu WhatsApp\".",
  "Empresta escala. Pode virar série: relógio de rua, metrô, outdoor de estrada, cada um com uma frase da série De Para.",
  "Deixar claro em contexto que é arte, se a equipe achar necessário."),
 (7, "Isso aqui serve pra desabafar?", "\"Isso aqui serve pra desabafar?\" \"Serve. E pra mais coisa.\"",
  "posição 20", "Vídeo 20 s · série de objeções",
  "Adesivo de comentário com uma objeção real tirada dos comentários da EITA: \"é terapia?\", \"é robô?\", \"lê minhas mensagens?\", \"quanto custa?\", \"e se eu estiver muito mal?\". A Anaclaudia ou a Eita responde em tom de conversa, sem roteiro visível.",
  "A Ash responde só a objeção de uso. A EITA responde a objeção de confiança, com a credencial da criadora e os guarda-corpos (\"não é terapia\", CVV 188) como resposta, não como rodapé. Uma objeção por vídeo, cinco vídeos por gravação.",
  None),
 (8, "A Eita é o seu espaço pra", "\"A Eita é o seu espaço pra... ser você.\"",
  "posições 25 e 28", "Arte estática · nuvem de verbos",
  "Uma nuvem de verbos em negrito com cenas brasileiras: \"Falar o que você pensou às três da manhã. Reclamar do áudio de dez minutos da sua mãe. Admitir que não está bem. Ensaiar a conversa com o chefe. Sentir saudade de quem você não devia.\" Fecha com \"Chega como está, sai mais leve.\"",
  "As cenas são da vida da mulher brasileira, não da americana. Pode ser a peça de assinatura da marca, com versão manuscrita para stories.",
  None),
 (9, "Não precisa baixar nada", "\"Não precisa baixar nada. Já está no seu WhatsApp.\"",
  "toda a estratégia de instalação da Ash", "Vídeo 15 s · print de WhatsApp + voz da Eita",
  "Abre no que a Ash não pode dizer. Tela: o contato da Eita no WhatsApp, o primeiro áudio chegando. A voz da Eita entra: \"Oi. Não precisa criar conta, não precisa instalar. Me conta o que aconteceu.\"",
  "O atrito zero é o maior diferencial competitivo da EITA em relação a qualquer app americano. Este anúncio existe para dizer só isso, e fechar com o preço da promoção.",
  None),
 (10, "Gorjeta ou besouro", "\"Uma IA calcula a gorjeta. A outra entende por que você perguntou se ele ainda te amaria se você virasse uma barata.\"",
  "posição 27", "Arte estática ou vídeo 10 s",
  "Duas colunas, dois usos: o utilitário e o emocional. A piada com a pergunta absurda que todo casal já fez. Fecha com \"A Eita te ajuda a entender o que está por trás.\"",
  "Humor é o que mais falta ao gênero de saúde mental, e a EITA já é a personagem leve do ecossistema. A versão brasileira da pergunta (barata, não besouro) é o detalhe que faz rir aqui.",
  None),
]
for n,t,g,o,f,r,v,c in ideias:
    H.append(ideia(n,t,g,o,f,r,v,c))

H.append('<h3>Por onde começar</h3>')
H.append('<p>Se for uma gravação só, ela rende as ideias 1, 7 e 9 no mesmo dia: um criador ou a própria Anaclaudia, um microfone de lapela, três aberturas para cada corpo, e os prints de WhatsApp preparados antes. As ideias 4, 5 e 8 saem da mesa de arte com a identidade que já existe, sem gravação. As esquetes (2 e 3) pedem elenco ou a animação das pílulas e podem vir na segunda leva.</p>')

# ---------- anexo transcricoes ----------
H.append('<h2>Anexo: transcrições integrais</h2>')
ids_ordem = [a["id"] for a in json.load(open(os.path.join(RAIZ,"ads-top30.json")))]
pos = {i:k+1 for k,i in enumerate(ids_ordem)}
for i in ids_ordem:
    if i in tr:
        H.append(f'<details><summary>Posição {pos[i]:02d} · anúncio {i} · {tr[i]["dur"]} s</summary><div class="corpo">{tr[i]["texto"]}</div></details>')

H.append('<p class="foot">Fonte: Biblioteca de Anúncios da Meta, página "Ash - AI for Mental Health" (ID 352960604556563), anúncios ativos, Estados Unidos, ordenados por impressões totais, consultada em 14 de setembro de 2026.<br>Contexto da empresa: BusinessWire, STAT News, Forbes, Psychology.com, Choosing Therapy, HugoScore e o site da Slingshot AI.<br>Vídeos transcritos com ElevenLabs Scribe e assistidos por frames. Nenhuma métrica de resultado por anúncio é pública para o mercado americano; a ordem do ranking é o único sinal de desempenho disponível.</p>')
H.append('</div>')

open(OUT, "w").write("\n".join(H))
print("ok", os.path.getsize(OUT)//1024, "KB ->", OUT)
