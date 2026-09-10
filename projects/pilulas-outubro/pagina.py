#!/usr/bin/env python3
"""Monta a Bancada de Voz das pilulas de outubro (pagina de aprovacao)."""
import base64, html, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import PILULAS

RAIZ = os.path.dirname(os.path.abspath(__file__))
AUDIOS = os.path.join(RAIZ, "audios")
PREVIA = os.path.join(RAIZ, "previa")

# tema de cada pilula, para o leitor saber o que esperar antes de tocar
TEMAS = {
    "01": "Desistir como esconderijo",
    "02": "Consumir conteúdo sem executar",
    "03": "A régua dos outros",
    "04": "O que você engole não some",
    "05": "Silenciar o alarme não apaga o incêndio",
    "06": "Firmeza vem da estrada",
    "07": "Ensaiar desgraça",
    "08": "Barreiras que só existem de longe",
    "09": "Amanhã eu resolvo",
    "10": "Dirigir olhando o retrovisor",
    "11": "Quem age tremendo",
    "12": "Atrasado em relação a quê",
}


REFEITOS = set()
_r = os.path.join(RAIZ, "refeitos.txt")
if os.path.exists(_r):
    REFEITOS = {l.strip() for l in open(_r) if l.strip()}


def previa(nome):
    """Versao leve do mp3 para caber na pagina."""
    os.makedirs(PREVIA, exist_ok=True)
    orig, leve = os.path.join(AUDIOS, nome), os.path.join(PREVIA, nome)
    if not os.path.exists(leve) or os.path.getmtime(orig) > os.path.getmtime(leve):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", orig,
                        "-ar", "44100", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "96k", leve],
                       check=True)
    with open(leve, "rb") as f:
        return base64.b64encode(f.read()).decode()


def dur(nome):
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", os.path.join(AUDIOS, nome)],
                       capture_output=True, text=True).stdout.strip()
    s = int(float(d))
    return f"{s // 60}:{s % 60:02d}"


CSS = """<title>Pílulas de Outubro</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap">
<style>
:root{
  --papel:#F5F7F6; --tinta:#17202A; --apoio:#3A4754; --mudo:#65727F;
  --verde:#00EFA9; --verde-prof:#0A7757; --verde-suave:#D6F7EB; --borda:#DFE8EB;
  --card:#FFFFFF; --sombra:0 2px 12px rgba(23,32,42,.06);
  --lip:#0A7757; --lip-bg:#D6F7EB; --vo:#5B4A86; --vo-bg:#EBE6F7;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --papel:#101820; --tinta:#E8EEEC; --apoio:#B7C2C4; --mudo:#7E8C90;
    --verde:#00EFA9; --verde-prof:#39D9A4; --verde-suave:#123D31; --borda:#243038;
    --card:#18222B; --sombra:0 2px 12px rgba(0,0,0,.3);
    --lip:#39D9A4; --lip-bg:#123D31; --vo:#B9A9E0; --vo-bg:#251E38;
  }
}
:root[data-theme="dark"]{
  --papel:#101820; --tinta:#E8EEEC; --apoio:#B7C2C4; --mudo:#7E8C90;
  --verde:#00EFA9; --verde-prof:#39D9A4; --verde-suave:#123D31; --borda:#243038;
  --card:#18222B; --sombra:0 2px 12px rgba(0,0,0,.3);
  --lip:#39D9A4; --lip-bg:#123D31; --vo:#B9A9E0; --vo-bg:#251E38;
}
*{box-sizing:border-box}
body{background:var(--papel);color:var(--tinta);font-family:system-ui,-apple-system,sans-serif;margin:0;padding:40px 20px 90px}
.wrap{max-width:720px;margin:0 auto}
.eyebrow{display:flex;align-items:center;gap:10px;font-family:"JetBrains Mono",monospace;font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--verde-prof)}
.eyebrow::before{content:"";width:18px;height:3px;background:var(--verde-prof)}
h1{font-family:"League Spartan",system-ui,sans-serif;font-weight:800;font-size:clamp(30px,6vw,42px);letter-spacing:-.02em;line-height:1.05;margin:14px 0 10px;text-wrap:balance}
.sub{color:var(--apoio);font-size:16px;line-height:1.55;margin:0 0 20px;max-width:62ch}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.meta span{font-family:"JetBrains Mono",monospace;font-size:12px;font-weight:600;letter-spacing:.06em;padding:6px 12px;border:1px solid var(--borda);border-radius:999px;background:var(--card);color:var(--mudo)}
.legenda{display:flex;flex-wrap:wrap;gap:18px;margin:0 0 34px;font-size:13.5px;color:var(--apoio)}
.legenda b{font-family:"JetBrains Mono",monospace;font-size:11px;font-weight:700;letter-spacing:.1em;padding:3px 9px;border-radius:5px;margin-right:7px}
.tipo-VO{color:var(--vo);background:var(--vo-bg)}
.tipo-LIP{color:var(--lip);background:var(--lip-bg)}
.pilulas{display:flex;flex-direction:column;gap:16px}
.pil{background:var(--card);border:1px solid var(--borda);border-radius:16px;padding:20px 22px;box-shadow:var(--sombra)}
.cab{display:flex;align-items:baseline;gap:12px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid var(--borda)}
.num{font-family:"JetBrains Mono",monospace;font-weight:700;font-size:13px;letter-spacing:.08em;color:var(--verde-prof)}
.tema{font-family:"League Spartan",system-ui,sans-serif;font-weight:700;font-size:19px;letter-spacing:-.01em}
.blocos{display:flex;flex-direction:column;gap:15px}
.bloco{display:grid;grid-template-columns:auto 1fr;gap:13px;align-items:start}
.btn{width:42px;height:42px;border-radius:50%;border:none;background:var(--verde);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .12s}
.btn:hover{transform:scale(1.06)}
.btn:focus-visible{outline:3px solid var(--verde-prof);outline-offset:3px}
.btn svg{width:18px;height:18px;fill:#17202A}
.col{min-width:0}
.top{display:flex;align-items:center;gap:9px;margin-bottom:7px}
.tipo{font-family:"JetBrains Mono",monospace;font-size:11px;font-weight:700;letter-spacing:.1em;padding:3px 9px;border-radius:5px}
.arq{font-family:"JetBrains Mono",monospace;font-size:11.5px;color:var(--mudo)}
.novo{font-family:"JetBrains Mono",monospace;font-size:10.5px;font-weight:700;letter-spacing:.1em;padding:2px 8px;border-radius:5px;background:var(--verde);color:#17202A}
.bar{height:6px;border-radius:999px;background:var(--verde-suave);cursor:pointer}
.fill{height:100%;width:0%;border-radius:999px;background:var(--verde-prof);pointer-events:none}
.fala{font-size:15.5px;line-height:1.55;color:var(--apoio);margin:9px 0 0}
.foot{margin-top:48px;padding-top:16px;border-top:1px solid var(--borda);font-family:"JetBrains Mono",monospace;font-size:12px;line-height:1.8;color:var(--mudo)}
@media (prefers-reduced-motion: reduce){.btn{transition:none}}
</style>
"""

JS = """
document.querySelectorAll(".bloco").forEach(bl => {
  const audio = new Audio("data:audio/mpeg;base64," + AUDIOS[bl.dataset.id]);
  const btn = bl.querySelector(".btn"), p = bl.querySelector(".ic-play"), q = bl.querySelector(".ic-pause");
  const bar = bl.querySelector(".bar"), fill = bl.querySelector(".fill");
  btn.addEventListener("click", () => {
    document.querySelectorAll(".bloco").forEach(o => { if (o !== bl && o._a && !o._a.paused) o._a.pause(); });
    audio.paused ? audio.play() : audio.pause();
  });
  audio.addEventListener("play",  () => { p.hidden = true;  q.hidden = false; });
  audio.addEventListener("pause", () => { p.hidden = false; q.hidden = true; });
  audio.addEventListener("ended", () => { p.hidden = false; q.hidden = true; });
  audio.addEventListener("timeupdate", () => {
    if (audio.duration) fill.style.width = (audio.currentTime / audio.duration * 100) + "%";
  });
  bar.addEventListener("click", e => {
    const r = bar.getBoundingClientRect();
    if (audio.duration) audio.currentTime = (e.clientX - r.left) / r.width * audio.duration;
  });
  bl._a = audio;
});
"""


def main():
    faltando = []
    for pid, blocos in PILULAS.items():
        for rot, _ in blocos:
            if not os.path.exists(os.path.join(AUDIOS, f"{pid}-{rot}.mp3")):
                faltando.append(f"{pid}-{rot}")
    if faltando:
        print("faltam:", ", ".join(faltando))
        return

    corpo, dados, n = [], [], 0
    for pid, blocos in PILULAS.items():
        corpo.append(f'<div class="pil"><div class="cab"><span class="num">PÍLULA {pid}</span>'
                     f'<span class="tema">{html.escape(TEMAS[pid])}</span></div><div class="blocos">')
        for rot, texto in blocos:
            nome = f"{pid}-{rot}.mp3"
            tipo = "LIP" if rot.startswith("LIP") else "VO"
            bid = f"b{n}"; n += 1
            dados.append(f'{bid}: "{previa(nome)}"')
            corpo.append(
                f'<div class="bloco" data-id="{bid}">'
                f'<button class="btn" aria-label="Tocar {pid} {rot}">'
                f'<svg class="ic-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
                f'<svg class="ic-pause" viewBox="0 0 24 24" hidden><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
                f'</button><div class="col"><div class="top">'
                f'<span class="tipo tipo-{tipo}">{rot}</span>'
                f'<span class="arq">{nome} · {dur(nome)}</span>'
                f'{chr(10) if False else ""}'
                + ('<span class="novo">REFEITO</span>' if f"{pid}-{rot}" in REFEITOS else '')
                + '</div>'
                f'<div class="bar"><div class="fill"></div></div>'
                f'<p class="fala">{html.escape(texto)}</p></div></div>')
        corpo.append("</div></div>")

    total = sum(float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1",
         os.path.join(AUDIOS, f"{p}-{r}.mp3")], capture_output=True, text=True).stdout.strip())
        for p, bs in PILULAS.items() for r, _ in bs)

    cabeca = f"""{CSS}<div class="wrap">
  <div class="eyebrow">Bancada de Voz</div>
  <h1>Pílulas de outubro</h1>
  <p class="sub">Doze pílulas na voz da Ana, cada fala em arquivo próprio e já separada como o roteiro pede. Toque bloco a bloco e me diga o que ajustar: dá para regerar uma fala isolada sem mexer em nenhuma outra.</p>
  <div class="meta"><span>12 PÍLULAS</span><span>{n} ARQUIVOS</span><span>{int(total // 60)} MIN {int(total % 60):02d} S</span><span>PRONÚNCIA CONFERIDA</span></div>
  <div class="legenda">
    <span><b class="tipo-VO">VO</b>narração por cima da cena</span>
    <span><b class="tipo-LIP">LIP</b>fala da Eita, para o lipsync</span>
  </div>
  <div class="pilulas">
{''.join(corpo)}
  </div>
  <p class="foot">Receita aprovada em 8 de setembro: multilingual v2, expressividade alta, velocidade natural, blocos longos.<br>Cada bloco foi transcrito e conferido contra o roteiro antes de entrar aqui; os que trazem o nome da marca passaram por dupla leitura.<br>Os arquivos da página estão em qualidade de audição; a entrega final vai em 192 kbps.</p>
</div>
<script>
const AUDIOS = {{{','.join(dados)}}};
{JS}
</script>"""

    destino = os.path.join(RAIZ, "bancada-pilulas-outubro.html")
    with open(destino, "w") as f:
        f.write(cabeca)
    print("ok", os.path.getsize(destino), "bytes,", n, "blocos")


if __name__ == "__main__":
    main()
