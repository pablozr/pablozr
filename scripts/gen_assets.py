#!/usr/bin/env python3
"""
Gera todos os assets SVG do perfil.

Rode:  python3 scripts/gen_assets.py     # escreve em ./assets

Conceito: "Calçadão". O perfil é um catálogo de exposição impresso em
papel e tinta. A capa usa a onda da calçada de Copacabana; os princípios
viram Estudos, cada um com uma figura que desenha o problema; os projetos
viram Obras, com etiqueta de museu.

Restrições que continuam valendo:
  - SVG servido por <img> no GitHub não carrega webfont, então a tipografia
    é a stack de sistema (Georgia / Times / Liberation Serif para o serifado).
  - GitHub remove <script>, mas renderiza <style>, filtros e SMIL dentro do
    SVG. Toda animação mora no arquivo.
  - Nada de serviço externo: github-readme-stats e afins caem e levam a capa.
"""
import os, math

OUT = "assets"
os.makedirs(os.path.join(OUT, "works"), exist_ok=True)
os.makedirs(os.path.join(OUT, "sections"), exist_ok=True)

PAPER, INK, RED, DIM, RULE = "#EFE8DA", "#17150F", "#D8432A", "#6A6255", "#CFC6B4"
SERIF = "Georgia,'Times New Roman','Liberation Serif',serif"
MONO = ("ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,"
        "'DejaVu Sans Mono','Liberation Mono',monospace")
W = 880


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"  {name:<32} {len(body)/1024:5.1f} KB")


def svg(h, body, label, grain=True, bg=True):
    """Moldura comum: papel + granulação de impressão."""
    g = ""
    if grain:
        g = f'''<filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/>
      <feColorMatrix values="0 0 0 0 0.09  0 0 0 0 0.08  0 0 0 0 0.06  0 0 0 0.10 0"/>
    </filter>'''
    back = f'<rect width="{W}" height="{h}" fill="{PAPER}"/>' if bg else ""
    over = f'<rect width="{W}" height="{h}" filter="url(#grain)"/>' if grain else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {h}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(label)}">
  <defs>{g}</defs>
  {back}
  {body}
  {over}
</svg>'''


# ── a onda de Copacabana ─────────────────────────────────────────────
def wave_path(x0, x1, y, amp, period, phase=0.0, step=6):
    pts = []
    x = x0
    while x <= x1 + step:
        pts.append((x, y + amp * math.sin(2 * math.pi * (x / period) + phase)))
        x += step
    return pts


def calcadao(x0, x1, y0, y1, band=18, amp=11, period=120, color=INK, step=8):
    """Faixas alternadas preenchidas entre senoides paralelas.

    Na calçada as ondas são pedra preta e branca do mesmo tamanho; aqui cada
    faixa preta é o espaço entre duas senoides deslocadas de `band`.
    """
    out = []
    y = y0 - band * 2
    while y < y1 + band:
        top = wave_path(x0, x1, y, amp, period, step=step)
        bot = wave_path(x0, x1, y + band, amp, period, step=step)
        d = "M" + " ".join(f"{a:.0f},{b:.1f}" for a, b in top)
        d += " " + " ".join(f"{a:.0f},{b:.1f}" for a, b in reversed(bot)) + "Z"
        out.append(f'<path d="{d}" fill="{color}"/>')
        y += band * 2
    return "".join(out)


# ── capa ─────────────────────────────────────────────────────────────
def header():
    H = 400
    period = 140
    # a onda anda um período inteiro e volta ao começo: loop sem emenda
    waves = calcadao(470 - period * 2, W + 8, 0, H, band=17, amp=13, period=period)
    roles = [
        "backend · FastAPI, async, event-driven",
        "arquitetura · concorrência como invariante",
        "coding agents · JevGuard",
        "pesquisa · embeddings e recuperação",
    ]
    cycle = 3.2 * len(roles)
    e = 0.025
    lines = []
    for i, r in enumerate(roles):
        a, b = i / len(roles), (i + 1) / len(roles)
        pts = [(0, 0), (a, 0), (a + e, 1), (b - e, 1), (b, 0), (1, 0)]
        if i == 0:
            pts = [(0, 1), (b - e, 1), (b, 0), (1 - e, 0), (1, 1)]
        kt = ";".join(f"{t:.3f}" for t, _ in pts)
        vals = ";".join(str(v) for _, v in pts)
        lines.append(f'''<text x="0" y="0" font-family="{MONO}" font-size="14" fill="{INK}" opacity="{1 if i == 0 else 0}">{esc(r)}
      <animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>
    </text>''')
    body = f'''
  <clipPath id="field"><rect x="470" y="0" width="{W-470}" height="{H}"/></clipPath>
  <g clip-path="url(#field)">
    <g>
      {waves}
      <animateTransform attributeName="transform" type="translate" from="0 0" to="{period} 0"
                        dur="14s" repeatCount="indefinite"/>
    </g>
  </g>
  <line x1="470" y1="0" x2="470" y2="{H}" stroke="{INK}" stroke-width="1.5"/>

  <text x="40" y="52" font-family="{MONO}" font-size="11" fill="{DIM}" letter-spacing="2">CATÁLOGO · Nº 01 · 2026</text>
  <text x="430" y="52" font-family="{MONO}" font-size="11" fill="{DIM}" letter-spacing="2" text-anchor="end">RJ</text>
  <line x1="40" y1="66" x2="430" y2="66" stroke="{INK}" stroke-width="1"/>

  <text x="36" y="168" font-family="{SERIF}" font-size="92" fill="{INK}" letter-spacing="-3">Pablo</text>
  <text x="36" y="252" font-family="{SERIF}" font-size="92" font-style="italic" fill="{INK}" letter-spacing="-3">Farina<tspan fill="{RED}">.</tspan></text>

  <g transform="translate(40 300)">{''.join(lines)}</g>
  <rect x="40" y="316" width="28" height="3" fill="{RED}">
    <animate attributeName="width" values="28;120;28" dur="{cycle/len(roles)}s" repeatCount="indefinite"/>
  </rect>

  <line x1="40" y1="352" x2="430" y2="352" stroke="{INK}" stroke-width="1"/>
  <text x="40" y="374" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1">UNIRIO · SISTEMAS DE INFORMAÇÃO</text>
  <text x="430" y="374" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1" text-anchor="end">22°54′S 43°12′W</text>

  <circle cx="{W-64}" cy="{H-64}" r="34" fill="{RED}"/>
  <text x="{W-64}" y="{H-59}" font-family="{MONO}" font-size="11" fill="{PAPER}" text-anchor="middle" letter-spacing="1.5">RIO</text>
'''
    return svg(H, body, "Pablo Farina. Backend, arquitetura, coding agents e pesquisa. UNIRIO, Rio de Janeiro.")


# ── links: bilhetes ──────────────────────────────────────────────────
def ticket(label, value):
    w, h = 250, 56
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}: {esc(value)}">
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>
  <line x1="78" y1="8" x2="78" y2="{h-8}" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>
  <circle cx="78" cy="1" r="6" fill="{INK}"/><circle cx="78" cy="{h-1}" r="6" fill="{INK}"/>
  <text x="40" y="{h/2+4}" font-family="{MONO}" font-size="10.5" fill="{RED}" text-anchor="middle" letter-spacing="1.5">{esc(label.upper())}</text>
  <text x="96" y="{h/2+6}" font-family="{SERIF}" font-size="18" font-style="italic" fill="{INK}">{esc(value)}</text>
  <text x="{w-16}" y="{h/2+5}" font-family="{SERIF}" font-size="16" fill="{INK}" text-anchor="end">→</text>
</svg>'''


# ── título de seção ──────────────────────────────────────────────────
def section(num, title, note):
    H = 100
    body = f'''
  <text x="28" y="62" font-family="{SERIF}" font-size="46" font-style="italic" fill="{RED}">{num}</text>
  <text x="{56 + len(num)*18}" y="62" font-family="{SERIF}" font-size="40" fill="{INK}" letter-spacing="-1">{esc(title)}</text>
  <text x="{W-28}" y="60" font-family="{MONO}" font-size="11" fill="{DIM}" text-anchor="end" letter-spacing="1">{esc(note)}</text>
  <line x1="28" y1="78" x2="{W-28}" y2="78" stroke="{INK}" stroke-width="1.5"/>
  <line x1="28" y1="83" x2="{W-28}" y2="83" stroke="{INK}" stroke-width="0.6"/>'''
    return svg(H, body, f"{num}. {title}")


# ── ficha técnica: números reais ─────────────────────────────────────
def figures():
    H = 160
    items = [
        ("200+", "lojas em produção", "sistemas internos na Bagaggio"),
        ("10+", "projetos entregues", "do requisito ao deploy monitorado"),
        ("605", "commits em 12 meses", "21 repositórios com contribuições"),
    ]
    cw = (W - 56) / 3
    out = []
    for i, (big, label, sub) in enumerate(items):
        x = 28 + i * cw
        if i:
            out.append(f'<line x1="{x:.1f}" y1="26" x2="{x:.1f}" y2="{H-20}" stroke="{INK}" stroke-width="1"/>')
        px = x + (28 if i else 0)
        out.append(f'''
  <text x="{px:.1f}" y="40" font-family="{MONO}" font-size="10.5" fill="{RED}" letter-spacing="1.5">FIG. {i+1}</text>
  <text x="{px - 3:.1f}" y="96" font-family="{SERIF}" font-size="58" fill="{INK}" letter-spacing="-2">{big}</text>
  <text x="{px:.1f}" y="118" font-family="{SERIF}" font-size="15" font-style="italic" fill="{INK}">{esc(label)}</text>
  <text x="{px:.1f}" y="136" font-family="{MONO}" font-size="10.5" fill="{DIM}">{esc(sub)}</text>''')
    body = "".join(out)
    return svg(H, body, "200+ lojas em produção, 10+ projetos entregues, 605 commits em 12 meses")


# ── estudos: cada princípio com uma figura que desenha o problema ────
def study_frame(num, title, text, figure):
    H = 250
    lines = wrap(text, 60)
    txt = "".join(
        f'<text x="330" y="{118 + i*22}" font-family="{SERIF}" font-size="15.5" fill="{INK}">{esc(l)}</text>'
        for i, l in enumerate(lines))
    body = f'''
  <rect x="20" y="20" width="270" height="{H-40}" fill="none" stroke="{INK}" stroke-width="1"/>
  {figure}
  <text x="330" y="52" font-family="{MONO}" font-size="10.5" fill="{RED}" letter-spacing="2">ESTUDO {num}</text>
  <text x="330" y="86" font-family="{SERIF}" font-size="27" font-style="italic" fill="{INK}" letter-spacing="-0.5">{esc(title)}</text>
  {txt}'''
    return svg(H, body, f"Estudo {num}: {title}. {text}")


def study_race():
    """Duas requisições, um item. Uma pega o lock, a outra espera e volta."""
    D = 5.0
    item = (155, 125)
    fig = f'''
  <text x="36" y="46" font-family="{MONO}" font-size="9.5" fill="{DIM}" letter-spacing="1">req A</text>
  <text x="36" y="214" font-family="{MONO}" font-size="9.5" fill="{DIM}" letter-spacing="1">req B</text>
  <path d="M40 58 C 90 58, 110 125, {item[0]-18} {item[1]}" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M40 192 C 90 192, 110 125, {item[0]-18} {item[1]}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="3 4"/>
  <rect x="{item[0]-16}" y="{item[1]-16}" width="32" height="32" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>
  <text x="{item[0]}" y="{item[1]+4}" font-family="{MONO}" font-size="11" fill="{INK}" text-anchor="middle">1</text>
  <text x="{item[0]}" y="{item[1]+34}" font-family="{MONO}" font-size="9" fill="{DIM}" text-anchor="middle">último item</text>
  <path d="M{item[0]+16} {item[1]} H 262" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <text x="262" y="{item[1]-10}" font-family="{MONO}" font-size="9" fill="{DIM}" text-anchor="end">commit</text>

  <circle r="6" fill="{RED}">
    <animateMotion dur="{D}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.4;1"
                   path="M40 58 C 90 58, 110 125, {item[0]-18} {item[1]} H 262" calcMode="linear"/>
  </circle>
  <circle r="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.5">
    <animateMotion dur="{D}s" repeatCount="indefinite" keyPoints="0;0.92;0.92;0" keyTimes="0;0.38;0.8;1"
                   path="M40 192 C 90 192, 110 125, {item[0]-18} {item[1]}" calcMode="linear"/>
  </circle>
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.3;0.34;0.8;1" dur="{D}s" repeatCount="indefinite"/>
    <rect x="{item[0]-7}" y="{item[1]-34}" width="14" height="11" fill="{RED}"/>
    <path d="M{item[0]-4} {item[1]-34} v-4 a4 4 0 0 1 8 0 v4" fill="none" stroke="{RED}" stroke-width="2"/>
    <text x="{item[0]+12}" y="{item[1]-26}" font-family="{MONO}" font-size="9" fill="{RED}">lock</text>
  </g>'''
    return fig


def study_domain():
    """Três domínios fechados; eventos atravessam o barramento sem conhecer quem escuta."""
    D = 6.0
    nodes = [(95, 85, "pedido"), (215, 85, "estoque"), (155, 185, "cobrança")]
    fig = [f'<line x1="36" y1="135" x2="274" y2="135" stroke="{INK}" stroke-width="1" stroke-dasharray="2 4"/>',
           f'<text x="270" y="128" font-family="{MONO}" font-size="9" fill="{DIM}" text-anchor="end">eventos</text>']
    for x, y, name in nodes:
        fig.append(f'<circle cx="{x}" cy="{y}" r="34" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
        fig.append(f'<circle cx="{x}" cy="{y}" r="27" fill="none" stroke="{INK}" stroke-width="0.6" stroke-dasharray="2 3"/>')
        fig.append(f'<text x="{x}" y="{y+4}" font-family="{SERIF}" font-size="13" font-style="italic" fill="{INK}" text-anchor="middle">{name}</text>')
    fig.append(f'<line x1="95" y1="119" x2="95" y2="135" stroke="{INK}" stroke-width="1"/>')
    fig.append(f'<line x1="215" y1="119" x2="215" y2="135" stroke="{INK}" stroke-width="1"/>')
    fig.append(f'<line x1="155" y1="135" x2="155" y2="151" stroke="{INK}" stroke-width="1"/>')
    # evento sai de "pedido", corre o barramento e é consumido pelos outros dois
    fig.append(f'''<circle r="5" fill="{RED}">
    <animateMotion dur="{D}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.5;1"
                   path="M95 119 V135 H215 V119"/>
  </circle>
  <circle r="5" fill="{RED}" opacity="0.9">
    <animateMotion dur="{D}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;0.25;0.55;1"
                   path="M95 135 H155 V151"/>
  </circle>''')
    return "".join(fig)


def study_gate():
    """Um diff passa linha por linha pelo gate; uma linha sai do escopo e é barrada."""
    D = 7.0
    rows = [(52, 150, "+"), (70, 120, "+"), (88, 170, "-"), (106, 90, "+"), (124, 140, "+"),
            (142, 110, "!"), (160, 160, "+"), (178, 130, "-")]
    fig = []
    for i, (y, w, s) in enumerate(rows):
        bad = s == "!"
        col = RED if bad else INK
        fig.append(f'<text x="38" y="{y+4}" font-family="{MONO}" font-size="10" fill="{col}">{"+" if bad else s}</text>')
        fig.append(f'<rect x="52" y="{y-3}" width="{w}" height="6" fill="{col}" opacity="{0.9 if bad else 0.75}"/>')
    fig.append(f'''<g>
    <line x1="30" y1="0" x2="238" y2="0" stroke="{RED}" stroke-width="1.5"/>
    <animateTransform attributeName="transform" type="translate" values="0 40;0 190;0 190" keyTimes="0;0.7;1"
                      dur="{D}s" repeatCount="indefinite"/>
  </g>
  <rect x="238" y="40" width="34" height="150" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <text x="255" y="110" font-family="{MONO}" font-size="9" fill="{INK}" text-anchor="middle" transform="rotate(-90 255 110)">gate</text>
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.5;0.53;0.95;1" dur="{D}s" repeatCount="indefinite"/>
    <text x="155" y="214" font-family="{MONO}" font-size="11" fill="{RED}" text-anchor="middle" letter-spacing="2">FAIL · fora do escopo</text>
  </g>''')
    return "".join(fig)


STUDIES = [
    ("I", "duas requisições, um item",
     "Concorrência só vira problema de verdade quando duas pessoas tentam comprar o "
     "último item ao mesmo tempo. A resposta não pode ser decidida depois: ou tem lock "
     "e transação explícita, ou o bug aparece em produção num sábado.", study_race),
    ("II", "cada regra na sua casa",
     "Procuro manter cada regra de negócio perto de quem entende dela. Espalhada pelo "
     "controller, vira algo que ninguém consegue explicar, nem eu. Mensageria entra pelo "
     "mesmo motivo: quem publica um evento não precisa conhecer quem escuta.", study_domain),
    ("III", "o agente escreve, alguém verifica",
     "Agora estou preso em verificação. Agente escreve mais rápido do que eu consigo "
     "revisar, e prompt melhor não resolve isso. Foi por isso que o JevGuard começou.", study_gate),
]


# ── obras: etiqueta de museu ─────────────────────────────────────────
def seeded(seed):
    h = 0
    for ch in seed:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    while True:
        h = (h * 1103515245 + 12345) & 0xFFFFFFFF
        yield (h >> 8) & 0xFFFF


def print_art(seed, x, y, w, h, uid):
    """Série Calçadão: cada obra é uma gravura da mesma onda, com parâmetros
    derivados do nome. Mesma família, nenhuma igual."""
    r = seeded(seed)
    band = 7 + next(r) % 8
    amp = 4 + next(r) % 12
    period = 60 + next(r) % 90
    angle = [0, 90, -35, 35, 20][next(r) % 5]
    mx, my = x + w * (0.2 + (next(r) % 60) / 100), y + h * (0.25 + (next(r) % 50) / 100)
    rad = min(w, h) * (0.12 + (next(r) % 10) / 100)
    cx, cy = x + w / 2, y + h / 2
    span = math.hypot(w, h) / 2 + band * 2
    waves = calcadao(cx - span, cx + span, cy - span, cy + span, band=band, amp=amp, period=period)
    return f'''<clipPath id="{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>
  <g clip-path="url(#{uid})">
    <g transform="rotate({angle} {cx:.1f} {cy:.1f})">{waves}</g>
    <circle cx="{mx:.1f}" cy="{my:.1f}" r="{rad + 7:.1f}" fill="{PAPER}"/>
    <circle cx="{mx:.1f}" cy="{my:.1f}" r="{rad:.1f}" fill="{RED}"/>
  </g>'''


def work(num, title, subtitle, technique, desc, width=W, featured=False):
    ww = width
    H = 300 if featured else 372
    ax, ay = 24, 24
    art_w = 300 if featured else ww - 48
    art_h = H - 48 if featured else 110
    uid = "art" + "".join(c for c in title.lower() if c.isalnum())
    art = print_art(title, ax, ay, art_w, art_h, uid)
    if featured:
        tx, ty, chars = ax + art_w + 36, 60, 60
    else:
        tx, ty, chars = 24, ay + art_h + 36, 50
    body = "".join(
        f'<text x="{tx}" y="{ty + 90 + i*20}" font-family="{SERIF}" font-size="14" fill="{INK}">{esc(l)}</text>'
        for i, l in enumerate(wrap(desc, chars)))
    content = f'''
  <rect x="0.75" y="0.75" width="{ww-1.5}" height="{H-1.5}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>
  {art}
  <rect x="{ax}" y="{ay}" width="{art_w}" height="{art_h}" fill="none" stroke="{INK}" stroke-width="1"/>
  <text x="{tx}" y="{ty}" font-family="{MONO}" font-size="10.5" fill="{RED}" letter-spacing="2">OBRA {num}</text>
  <text x="{tx}" y="{ty + 34}" font-family="{SERIF}" font-size="{30 if featured else 23}" font-style="italic" fill="{INK}" letter-spacing="-0.6">{esc(title)}</text>
  <text x="{tx}" y="{ty + 58}" font-family="{MONO}" font-size="10.5" fill="{DIM}">{esc(subtitle)}</text>
  {body}
  <line x1="{tx}" y1="{H-50}" x2="{ww-24}" y2="{H-50}" stroke="{INK}" stroke-width="0.8"/>
  <text x="{tx}" y="{H-28}" font-family="{MONO}" font-size="10" fill="{DIM}" letter-spacing="0.5">técnica mista · {esc(technique)}</text>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {ww} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(title)}: {esc(desc)}">
  {content}
</svg>'''


# ── materiais: linguagens como faixa de cor ──────────────────────────
# Repositórios PÚBLICOS e não-fork (42 no total). Mesma medição da versão anterior.
LANGS = [("TypeScript", 49.8, 12), ("Python", 20.7, 17), ("Java", 8.4, 10),
         ("HTML", 6.6, 11), ("SCSS", 5.6, 6), ("JavaScript", 4.3, 9),
         ("CSS", 3.7, 12)]

STACK = [
    ("backend", ["Python", "FastAPI", "Java", "Spring Boot", "Go"]),
    ("frontend", ["Angular", "TypeScript", "React", "Next.js", "Vite"]),
    ("dados e infra", ["PostgreSQL", "MongoDB", "Redis", "RabbitMQ", "Docker"]),
]


def pattern_defs():
    return f'''
    <pattern id="p0" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="{INK}"/></pattern>
    <pattern id="p1" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="{RED}"/></pattern>
    <pattern id="p2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="{PAPER}"/><rect width="3" height="6" fill="{INK}"/></pattern>
    <pattern id="p3" width="7" height="7" patternUnits="userSpaceOnUse"><rect width="7" height="7" fill="{PAPER}"/><circle cx="3.5" cy="3.5" r="1.8" fill="{INK}"/></pattern>
    <pattern id="p4" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="{PAPER}"/><rect width="6" height="2.5" fill="{RED}"/></pattern>
    <pattern id="p5" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="6" height="6" fill="{PAPER}"/><rect width="1.5" height="6" fill="{INK}"/></pattern>
    <pattern id="p6" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="{PAPER}"/><path d="M0 4 H8 M4 0 V8" stroke="{INK}" stroke-width="1"/></pattern>'''


def materials():
    H = 462
    bx, bw, by, bh = 28, W - 56, 52, 96
    x = bx
    total = sum(p for _, p, _ in LANGS)
    segs, legend = [], []
    for i, (name, pct, n) in enumerate(LANGS):
        w = bw * pct / total
        segs.append(f'<rect x="{x:.1f}" y="{by}" width="{w:.1f}" height="{bh}" fill="url(#p{i})" stroke="{INK}" stroke-width="1"/>')
        col, row = i % 4, i // 4
        lx, ly = 28 + col * ((W - 56) / 4), by + bh + 36 + row * 44
        legend.append(f'''<rect x="{lx:.1f}" y="{ly-11}" width="14" height="14" fill="url(#p{i})" stroke="{INK}" stroke-width="1"/>
  <text x="{lx+24:.1f}" y="{ly+1}" font-family="{SERIF}" font-size="15" font-style="italic" fill="{INK}">{name}</text>
  <text x="{lx+24:.1f}" y="{ly+18}" font-family="{MONO}" font-size="10" fill="{DIM}">{str(pct).replace(".", ",")}% · {n} repos</text>''')
        x += w
    stack_y = 306
    cols = []
    for i, (group, items) in enumerate(STACK):
        cx = 28 + i * ((W - 56) / 3)
        cols.append(f'<text x="{cx:.1f}" y="{stack_y}" font-family="{MONO}" font-size="10.5" fill="{RED}" letter-spacing="2">{esc(group.upper())}</text>')
        cols.append(f'<line x1="{cx:.1f}" y1="{stack_y+10}" x2="{cx + W/3 - 28:.1f}" y2="{stack_y+10}" stroke="{INK}" stroke-width="0.8"/>')
        for j, it in enumerate(items):
            cols.append(f'<text x="{cx:.1f}" y="{stack_y + 34 + j*20}" font-family="{SERIF}" font-size="15" fill="{INK}">{esc(it)}</text>')
    body = f'''<defs>{pattern_defs()}</defs>
  <text x="28" y="34" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1">COMPOSIÇÃO · por volume de código · 42 repositórios públicos, sem forks</text>
  {''.join(segs)}
  {''.join(legend)}
  {''.join(cols)}'''
    return svg(H, body, "Linguagens por volume de código: " +
               ", ".join(f"{n} {p}%" for n, p, _ in LANGS) + ". Stack: " +
               "; ".join(f"{g}: {', '.join(it)}" for g, it in STACK))


def footer():
    H = 120
    waves = calcadao(-120, W + 120, 0, 80, band=10, amp=7, period=120)
    body = f'''
  <clipPath id="strip"><rect x="0" y="0" width="{W}" height="80"/></clipPath>
  <g clip-path="url(#strip)"><g>{waves}
    <animateTransform attributeName="transform" type="translate" from="0 0" to="-120 0" dur="12s" repeatCount="indefinite"/>
  </g></g>
  <line x1="0" y1="80" x2="{W}" y2="80" stroke="{INK}" stroke-width="1.5"/>
  <text x="24" y="106" font-family="{MONO}" font-size="10" fill="{DIM}" letter-spacing="1">DESENHADO À MÃO EM SVG · SEM SERVIÇO EXTERNO</text>
  <text x="{W-24}" y="106" font-family="{SERIF}" font-size="14" font-style="italic" fill="{INK}" text-anchor="end">fim do catálogo<tspan fill="{RED}">.</tspan></text>'''
    return svg(H, body, "Fim")


if __name__ == "__main__":
    print("gerando assets:")
    write("header.svg", header())
    write("figures.svg", figures())
    write("materials.svg", materials())
    write("footer.svg", footer())
    write("ticket-linkedin.svg", ticket("linkedin", "pablozr"))
    write("ticket-email.svg", ticket("email", "me escreva"))
    write("ticket-github.svg", ticket("github", "pablozr"))
    for num, title, note in [("I", "Nota de abertura", "quem escreve"),
                             ("II", "Estudos", "como eu penso"),
                             ("III", "Obras", "o que eu construí"),
                             ("IV", "Materiais", "com o que eu construo")]:
        write(f"sections/{num.lower()}.svg", section(num, title, note))
    for num, title, text, fig in STUDIES:
        write(f"study-{num.lower()}.svg", study_frame(num, title, text, fig()))
    print("  -- obras --")
    write("works/jevguard.svg", work(
        "01", "JevGuard", "motor de política semântica para coding agents", "TypeScript, CLI, policy engine",
        "Verifica o diff que um agente acabou de produzir contra as políticas do repositório. "
        "Cada regra recebe um julgamento semântico e um gate determinístico local devolve o "
        "veredito: PASS, WARN ou FAIL.", featured=True))
    halves = [
        ("02", "PRISMA", "plataforma acadêmica da UNIRIO", "Python, FastAPI, Redis, RAG",
         "Projetos acadêmicos importados do SIE. Auth institucional via Google, access e "
         "refresh token em Redis e recomendação semântica sobre a busca."),
        ("03", "self-checkout-monolith", "autoatendimento por mesa", "FastAPI, Redis, RabbitMQ, Stripe",
         "Carrinho anônimo por mesa em Redis, checkout Stripe idempotente, reset de senha "
         "assíncrono com worker SMTP e cache por produto."),
        ("04", "subscription-monolith", "gestão de assinaturas", "FastAPI, PostgreSQL, RabbitMQ",
         "Regras separadas por domínio, persistência relacional e comunicação assíncrona "
         "entre os serviços."),
        ("05", "FastAPI-Template", "base de API para produção", "FastAPI, Docker, PostgreSQL",
         "Organização modular, configuração por ambiente e docker-compose pronto pra subir."),
    ]
    slugs = ["prisma", "self-checkout", "subscription", "fastapi-template"]
    for slug, (n, t, s, tech, d) in zip(slugs, halves):
        write(f"works/{slug}.svg", work(n, t, s, tech, d, width=432))
    print("ok")
