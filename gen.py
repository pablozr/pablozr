#!/usr/bin/env python3
"""
Capa GitHub — Pablo Farina.

v3: mata a moldura de terminal (bolinhas de janela, ~/path, "$ cat whoami").
Isso e o formato mais replicado de README de dev — e o proprio renderizador
avaliou a v2 como "template generico de terminal". Trocado por um SIGIL
GEOMETRICO DETERMINISTICO, derivado do nome: grelha de runas onde cada celula
receve um travo dependente do hash do caractere. Ninguem mais tem esse glifo.

Restricao de verdade: SVG servido por <img> no GitHub nao carrega webfont.
Entao o nome usa a stack de SISTEMA (nunca "Fira Code", que cai feio).
"""
import sys, os, html

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
THEME = sys.argv[2] if len(sys.argv) > 2 else "amber"
os.makedirs(OUT, exist_ok=True)

MONO = ("ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,"
        "'DejaVu Sans Mono','Liberation Mono',monospace")
SANS = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,"
        "Helvetica,Arial,sans-serif")

THEMES = {
    "amber": ("#0A0A0B", "#F5A524", "#EDEAE4", "#807C74"),
    "red":   ("#0A0A0B", "#FF3B2F", "#EDEAE4", "#807C74"),
    "lime":  ("#0A0A0B", "#B4F03A", "#EDEAE4", "#807C74"),
    "bone":  ("#0A0A0B", "#E4E0D8", "#EDEAE4", "#807C74"),
    "void":  ("#0A0A0B", "#6E6A63", "#EDEAE4", "#807C74"),
}
BG, ACC, FG, DIM = THEMES[THEME]

SEED = "PabloFarina"


def sigil(cx, cy, cols, rows, cell, opacity=1.0):
    """Grelha de runas deterministica: cada celula derivada do hash do nome."""
    h = 0
    for ch in SEED:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    out = []
    w = cols * cell
    top = cy - (rows * cell) / 2
    for r in range(rows):
        for c in range(cols):
            h = (h * 1103515245 + 12345) & 0xFFFFFFFF
            v = (h >> 16) & 0xF
            x = cx - w / 2 + c * cell
            y = top + r * cell
            m = cell * 0.26
            x1, y1, x2, y2 = x + m, y + m, x + cell - m, y + cell - m
            paths = [
                f'M{x1} {y1} H{x2}',                       # horizontal
                f'M{x1} {y1} V{y2}',                       # vertical
                f'M{x1} {y1} L{x2} {y2}',                  # diagonal
                f'M{x2} {y1} L{x1} {y2}',                  # anti-diagonal
                f'M{x1} {y1} H{x2} V{y2}',                # elbow
                f'M{x1} {y1} V{y2} H{x2}',                # elbow invertido
                f'M{x1} {y1} H{(x1+x2)/2} M{(x1+x2)/2} {y1} V{y2} H{x2}',
                f'M{(x1+x2)/2} {y1} V{y2}',               # centro vertical
                f'M{x1} {(y1+y2)/2} H{x2}',               # centro horizontal
            ]
            stroke = ACC if (v % 4 == 0) else DIM
            op = opacity * (0.85 if (v % 4 == 0) else 0.30 + (v % 5) * 0.08)
            out.append(f'<path d="{paths[v % len(paths)]}" fill="none" '
                       f'stroke="{stroke}" stroke-width="1.1" opacity="{op:.2f}"/>')
    return "".join(out)


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"  {name}  {len(body)/1024:.1f} KB")


def header():
    W, H = 880, 268
    roles = [
        "backend — FastAPI · async · event-driven",
        "arquitetura — domain-driven · concorrência como invariante",
        "ferramentas para coding agents — JevGuard",
        "pesquisa — TCC · embeddings · recuperação",
    ]
    wipes, lines = [], []
    for i, r in enumerate(roles):
        wipes.append(f'''<clipPath id="w{i}"><rect x="0" y="0" width="0" height="24">
      <animate attributeName="width" from="0" to="640" begin="{0.7 + i*0.13:.2f}s"
               dur="0.45s" fill="freeze"/></rect></clipPath>''')
        t0 = 1.0 + i * 3.0
        lines.append(f'''<text x="52" y="196" font-family="{MONO}" font-size="14.5"
          fill="{DIM}" clip-path="url(#w{i})" opacity="0">{html.escape(r)}
      <set attributeName="opacity" to="1" begin="{t0}s" dur="0.2s" repeatCount="indefinite"/>
      <set attributeName="opacity" to="0" begin="{t0 + 2.3}s" dur="0.4s" repeatCount="indefinite"/>
    </text>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Pablo Farina — backend, arquitetura de software e pesquisa">
  <defs>{''.join(wipes)}
    <linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{BG}" stop-opacity="1"/>
      <stop offset="58%" stop-color="{BG}" stop-opacity="0.97"/>
      <stop offset="78%" stop-color="{BG}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{BG}" stop-opacity="0.15"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>

  <!-- sigil a direita -->
  <g>{sigil(700, 134, 11, 9, 17, opacity=0.95)}</g>
  <!-- veu: dissolve o sigil sob o texto, sem caixa, sem gradiente decorativo -->
  <rect width="{W}" height="{H}" fill="url(#veil)"/>

  <rect x="0" y="0" width="3" height="{H}" fill="{ACC}"/>

  <!-- eyebrow -->
  <text x="52" y="92" font-family="{MONO}" font-size="12.5" fill="{ACC}"
        letter-spacing="2.4">BACKEND · ARQUITETURA</text>

  <!-- o nome -->
  <text x="49" y="164" font-family="{SANS}" font-size="66" font-weight="700"
        fill="{FG}" letter-spacing="-2.6">Pablo Farina</text>

  {''.join(lines)}
  <rect x="52" y="185" width="9" height="15" fill="{ACC}">
    <animate attributeName="opacity" values="1;0;1" dur="1.15s"
             repeatCount="indefinite"/>
  </rect>

  <!-- rodape enxuto -->
  <text x="52" y="242" font-family="{MONO}" font-size="11.5" fill="{DIM}"
        opacity="0.8">UNIRIO · Sistemas de Informação · Rio de Janeiro</text>
</svg>'''


def scope():
    W, H = 880, 158
    cw = (W - 3 * 20) / 3
    items = [
        ("200+", "lojas em produção", "sistemas internos na Bagaggio"),
        ("10+", "projetos entregues", "do requisito ao deploy monitorado"),
        ("1,7k", "commits em 12 meses", "50 repositórios públicos"),
    ]
    cards = []
    for i, (big, label, sub) in enumerate(items):
        x = 20 + i * (cw + 20)
        cards.append(f'''
    <line x1="{x:.1f}" y1="24" x2="{x + cw:.1f}" y2="24" stroke="{ACC}"
          stroke-width="2" opacity="0.9"/>
    <line x1="{x:.1f}" y1="24" x2="{x + cw:.1f}" y2="132" stroke="{DIM}"
          stroke-width="1" opacity="0.22"/>
    <line x1="{x:.1f}" y1="132" x2="{x + cw:.1f}" y2="132" stroke="{DIM}"
          stroke-width="1" opacity="0.22"/>
    <text x="{x + 18:.1f}" y="76" font-family="{SANS}" font-size="42"
          font-weight="700" fill="{FG}">{big}</text>
    <text x="{x + 18:.1f}" y="102" font-family="{MONO}" font-size="12"
          fill="{FG}" opacity="0.9">{label}</text>
    <text x="{x + 18:.1f}" y="121" font-family="{MONO}" font-size="10.5"
          fill="{DIM}">{sub}</text>
    <animate attributeName="opacity" values="0;1" begin="{0.15 + i*0.13:.2f}s"
             dur="0.5s" fill="freeze"/>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Escopo: 200+ lojas, 10+ projetos, 1,7k commits em 12 meses">
  {''.join(cards)}
</svg>'''


LANGS = [("TypeScript", 48.8, 15), ("Java", 19.5, 12), ("Python", 14.2, 17),
         ("HTML", 4.8, 14), ("CSS", 4.2, 16), ("JavaScript", 3.9, 12),
         ("SCSS", 3.8, 6)]

def langs():
    W = 880
    row, top = 30, 58
    H = top + row * len(LANGS) + 36
    bx, bmax, mx = 160, 360, LANGS[0][1]
    rows = []
    for i, (name, pct, n) in enumerate(LANGS):
        y = top + i * row
        op = 1.0 if i == 0 else 0.6
        rows.append(f'''
    <text x="30" y="{y+15}" font-family="{MONO}" font-size="13" fill="{FG}"
          opacity="{op}">{name}</text>
    <text x="132" y="{y+15}" font-family="{MONO}" font-size="10.5" fill="{DIM}"
          text-anchor="end">{pct}%</text>
    <rect x="{bx}" y="{y+4}" width="{bmax}" height="12" rx="6" fill="{DIM}"
          opacity="0.14"/>
    <rect x="{bx}" y="{y+4}" width="0" height="12" rx="6" fill="{ACC}"
          opacity="{op}">
      <animate attributeName="width" from="0" to="{bmax*pct/mx:.1f}" begin="{0.2 + i*0.09:.2f}s"
               dur="0.75s" fill="freeze" calcMode="spline"
               keySplines="0.16 1 0.3 1" keyTimes="0;1"/>
    </rect>
    <text x="{bx + bmax + 16}" y="{y+15}" font-family="{MONO}" font-size="10.5"
          fill="{DIM}" opacity="0.7">{n}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Linguagens por volume de codigo">
  <text x="30" y="30" font-family="{MONO}" font-size="12.5" fill="{ACC}">&gt; por volume de código</text>
  <text x="{W-30}" y="30" font-family="{MONO}" font-size="10.5" fill="{DIM}"
        text-anchor="end">bytes reais · 7,06 MB · 50 repositórios</text>
  <line x1="30" y1="44" x2="{W-30}" y2="44" stroke="{DIM}" stroke-width="1" opacity="0.25"/>
  {''.join(rows)}
</svg>'''


def footer():
    W, H = 880, 72
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="Fim">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g opacity="0.85">{sigil(W/2, 36, 33, 1, 26, opacity=0.5)}</g>
  <rect x="0" y="{H-2}" width="{W}" height="2" fill="{ACC}"/>
</svg>'''


if __name__ == "__main__":
    print(f"tema={THEME} -> {OUT}")
    write("header.svg", header())
    write("scope.svg", scope())
    write("languages.svg", langs())
    write("footer.svg", footer())
