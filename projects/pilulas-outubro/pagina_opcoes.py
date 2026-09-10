#!/usr/bin/env python3
"""Pagina enxuta para a equipe escolher entre tomadas do mesmo bloco."""
import base64, html, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import PILULAS

RAIZ = os.path.dirname(os.path.abspath(__file__))


def b64(p):
    leve = "/tmp/.leve.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ar", "44100", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "96k", leve], check=True)
    return base64.b64encode(open(leve, "rb").read()).decode()


def dur(p):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", p],
                             capture_output=True, text=True).stdout.strip())
    return f"{int(d) // 60}:{int(d) % 60:02d}"


APELIDOS = {"A": "mais solta", "B": "receita padrão", "C": "firme e expressiva",
            "D": "mais contida", "ATUAL": "a que está no pacote"}

GRUPOS = [
    ("05-LIP", "Pílula 05 · fala da Eita",
     "As duas versões anteriores foram reprovadas. Nenhuma destas é a que você já ouviu.",
     [("A", "opcoes/05-LIP-A.mp3"), ("B", "opcoes/05-LIP-B.mp3"),
      ("C", "opcoes/05-LIP-C.mp3"), ("D", "opcoes/05-LIP-D.mp3")]),
    ("07-VO", "Pílula 07 · narração",
     "A primeira da lista é a que você aprovou como quase perfeita, devolvida ao pacote. "
     "As outras quatro são tentativas de acertar a última frase sem perder o resto.",
     [("ATUAL", "audios/07-VO.mp3"), ("A", "opcoes/07-VO-A.mp3"), ("B", "opcoes/07-VO-B.mp3"),
      ("C", "opcoes/07-VO-C.mp3"), ("D", "opcoes/07-VO-D.mp3")]),
]

CSS = """<title>Escolha das Tomadas</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap">
<style>
:root{--papel:#F5F7F6;--tinta:#17202A;--apoio:#3A4754;--mudo:#65727F;--verde:#00EFA9;
--verde-prof:#0A7757;--verde-suave:#D6F7EB;--borda:#DFE8EB;--card:#FFFFFF;
--sombra:0 2px 12px rgba(23,32,42,.06);--aviso:#8A5A00;--aviso-bg:#FFF3D6;--aviso-bd:#F0DCA8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
--papel:#101820;--tinta:#E8EEEC;--apoio:#B7C2C4;--mudo:#7E8C90;--verde:#00EFA9;
--verde-prof:#39D9A4;--verde-suave:#123D31;--borda:#243038;--card:#18222B;
--sombra:0 2px 12px rgba(0,0,0,.3);--aviso:#F0C979;--aviso-bg:#2E2411;--aviso-bd:#4A3A18}}
:root[data-theme="dark"]{--papel:#101820;--tinta:#E8EEEC;--apoio:#B7C2C4;--mudo:#7E8C90;
--verde:#00EFA9;--verde-prof:#39D9A4;--verde-suave:#123D31;--borda:#243038;--card:#18222B;
--sombra:0 2px 12px rgba(0,0,0,.3);--aviso:#F0C979;--aviso-bg:#2E2411;--aviso-bd:#4A3A18}
*{box-sizing:border-box}
body{background:var(--papel);color:var(--tinta);font-family:system-ui,-apple-system,sans-serif;margin:0;padding:40px 20px 90px}
.wrap{max-width:660px;margin:0 auto}
.eyebrow{display:flex;align-items:center;gap:10px;font-family:"JetBrains Mono",monospace;font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--verde-prof)}
.eyebrow::before{content:"";width:18px;height:3px;background:var(--verde-prof)}
h1{font-family:"League Spartan",system-ui,sans-serif;font-weight:800;font-size:clamp(30px,6vw,40px);letter-spacing:-.02em;line-height:1.06;margin:14px 0 10px;text-wrap:balance}
.sub{color:var(--apoio);font-size:16px;line-height:1.55;margin:0 0 30px;max-width:60ch}
.grupo{background:var(--card);border:1px solid var(--borda);border-radius:16px;padding:22px;box-shadow:var(--sombra);margin-bottom:18px}
.cab{margin-bottom:6px}
.num{font-family:"JetBrains Mono",monospace;font-weight:700;font-size:12px;letter-spacing:.1em;color:var(--verde-prof)}
h2{font-family:"League Spartan",system-ui,sans-serif;font-weight:700;font-size:20px;letter-spacing:-.01em;margin:4px 0 8px}
.nota{color:var(--mudo);font-size:14px;line-height:1.55;margin:0 0 14px}
.fala{font-size:15.5px;line-height:1.55;color:var(--tinta);background:var(--verde-suave);border-radius:10px;padding:12px 14px;margin:0 0 18px}
.ops{display:flex;flex-direction:column;gap:12px}
.op{display:grid;grid-template-columns:auto 1fr;gap:13px;align-items:center}
.btn{width:44px;height:44px;border-radius:50%;border:none;background:var(--verde);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .12s}
.btn:hover{transform:scale(1.06)}
.btn:focus-visible{outline:3px solid var(--verde-prof);outline-offset:3px}
.btn svg{width:18px;height:18px;fill:#17202A}
.col{min-width:0}
.top{display:flex;align-items:baseline;gap:9px;margin-bottom:6px;flex-wrap:wrap}
.letra{font-family:"JetBrains Mono",monospace;font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--verde-prof)}
.apelido{font-size:14px;color:var(--apoio)}
.tempo{font-family:"JetBrains Mono",monospace;font-size:11.5px;color:var(--mudo);margin-left:auto}
.bar{height:6px;border-radius:999px;background:var(--verde-suave);cursor:pointer}
.fill{height:100%;width:0%;border-radius:999px;background:var(--verde-prof);pointer-events:none}
.aviso{display:block;margin:26px 0 0;padding:14px 16px;background:var(--aviso-bg);border:1px solid var(--aviso-bd);border-radius:10px;color:var(--aviso);font-size:14px;line-height:1.6}
.foot{margin-top:34px;padding-top:16px;border-top:1px solid var(--borda);font-family:"JetBrains Mono",monospace;font-size:12px;line-height:1.8;color:var(--mudo)}
@media (prefers-reduced-motion: reduce){.btn{transition:none}}
</style>"""


def main():
    corpo, dados, n = [], [], 0
    for chave, titulo, nota, itens in GRUPOS:
        pid, rot = chave.split("-", 1)
        texto = dict(PILULAS[pid])[rot]
        corpo.append(f'<div class="grupo"><div class="cab"><span class="num">{chave}</span>'
                     f'<h2>{html.escape(titulo)}</h2></div>'
                     f'<p class="nota">{html.escape(nota)}</p>'
                     f'<p class="fala">{html.escape(texto)}</p><div class="ops">')
        for letra, caminho in itens:
            p = os.path.join(RAIZ, caminho)
            if not os.path.exists(p):
                continue
            bid = f"o{n}"; n += 1
            dados.append(f'{bid}: "{b64(p)}"')
            corpo.append(
                f'<div class="op" data-id="{bid}">'
                f'<button class="btn" aria-label="Tocar opção {letra} de {chave}">'
                f'<svg class="ic-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
                f'<svg class="ic-pause" viewBox="0 0 24 24" hidden><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
                f'</button><div class="col"><div class="top"><span class="letra">{letra}</span>'
                f'<span class="apelido">{APELIDOS.get(letra, "")}</span>'
                f'<span class="tempo">{dur(p)}</span></div>'
                f'<div class="bar"><div class="fill"></div></div></div></div>')
        corpo.append("</div></div>")

    pagina = f"""{CSS}<div class="wrap">
  <div class="eyebrow">Bancada de Voz</div>
  <h1>Escolha das tomadas</h1>
  <p class="sub">Dois blocos ainda não acertaram. Como só ouvido humano julga entrega, aqui estão tomadas diferentes do mesmo texto para você apontar a boa. Me diga a letra e eu coloco no pacote.</p>
  {''.join(corpo)}
  <div class="aviso">Se nenhuma das opções da pílula 05 servir, o problema pode ser a própria frase: "achar onde o seu começa" fica sem sujeito para a voz apoiar a ênfase, e é o único LIP do pacote com essa construção. Você me disse para não mexer no texto, e não mexi. Mas se quiser, uma palavra a mais ali resolveria de vez.</div>
  <p class="foot">Todas as tomadas passaram pela conferência de texto e de pronúncia do nome antes de entrar aqui.<br>O que muda entre elas é a firmeza e a expressividade da voz, não o texto.<br>Medi melodia e ênfase das tomadas aprovadas e reprovadas: os números não separam as duas, por isso a escolha é sua.</p>
</div>
<script>
const AUDIOS = {{{','.join(dados)}}};
document.querySelectorAll(".op").forEach(op => {{
  const audio = new Audio("data:audio/mpeg;base64," + AUDIOS[op.dataset.id]);
  const btn = op.querySelector(".btn"), p = op.querySelector(".ic-play"), q = op.querySelector(".ic-pause");
  const bar = op.querySelector(".bar"), fill = op.querySelector(".fill");
  btn.addEventListener("click", () => {{
    document.querySelectorAll(".op").forEach(o => {{ if (o !== op && o._a && !o._a.paused) o._a.pause(); }});
    audio.paused ? audio.play() : audio.pause();
  }});
  audio.addEventListener("play",  () => {{ p.hidden = true;  q.hidden = false; }});
  audio.addEventListener("pause", () => {{ p.hidden = false; q.hidden = true; }});
  audio.addEventListener("ended", () => {{ p.hidden = false; q.hidden = true; }});
  audio.addEventListener("timeupdate", () => {{
    if (audio.duration) fill.style.width = (audio.currentTime / audio.duration * 100) + "%";
  }});
  bar.addEventListener("click", e => {{
    const r = bar.getBoundingClientRect();
    if (audio.duration) audio.currentTime = (e.clientX - r.left) / r.width * audio.duration;
  }});
  op._a = audio;
}});
</script>"""
    destino = os.path.join(RAIZ, "bancada-opcoes.html")
    with open(destino, "w") as f:
        f.write(pagina)
    print("ok", os.path.getsize(destino), "bytes,", n, "opcoes")


if __name__ == "__main__":
    main()
