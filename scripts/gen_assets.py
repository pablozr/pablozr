#!/usr/bin/env python3
"""
Gera todos os assets SVG do perfil.

Rode:  python3 scripts/gen_assets.py     # escreve em ./assets

Referência: Serial Experiments Lain. Não o "tema hacker" genérico, e sim o
que a série tem de próprio: céu pálido com dithering, postes e fios em
silhueta, sombras pretas com manchas vermelhas, tela de CRT e os títulos
"Layer:NN". O conteúdo é código de verdade, não decoração.

Restrições:
  - SVG servido por <img> no GitHub não carrega webfont: stack de sistema.
  - GitHub remove <script>, mas renderiza <style>, <pattern>, filtros e SMIL
    dentro do SVG. Toda animação mora no arquivo.
  - Nada de serviço externo.
"""
import os, math

OUT = "assets"
os.makedirs(os.path.join(OUT, "nodes"), exist_ok=True)
os.makedirs(os.path.join(OUT, "layers"), exist_ok=True)

BG, FG, DIM, RED, FAINT, PANEL = "#0A0A0A", "#E6E1D3", "#8C877C", "#C8102E", "#2A2825", "#121110"
MONO = ("ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,"
        "'DejaVu Sans Mono','Liberation Mono',monospace")
SANS = ("'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif")
JP = ("'Hiragino Sans','Yu Gothic','Meiryo','Noto Sans CJK JP',"
      "'WenQuanYi Zen Hei',sans-serif")
W = 880

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


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
    print(f"  {name:<28} {len(body)/1024:5.1f} KB")


# ── texturas ─────────────────────────────────────────────────────────
def dither(level, cell=3, color=FG, pid=None):
    """Pattern de dithering ordenado (Bayer 4x4). level 0..16 = pixels acesos."""
    pid = pid or f"d{level}"
    t = cell * 4
    px = "".join(
        f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}"/>'
        for r in range(4) for c in range(4) if BAYER[r][c] < level)
    return (f'<pattern id="{pid}" width="{t}" height="{t}" patternUnits="userSpaceOnUse">'
            f'<g fill="{color}">{px}</g></pattern>')


SCAN = f'''<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#000" opacity="0.35"/></pattern>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/>
      <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.06 0"/>
    </filter>'''


def screen(h, body, label, defs="", roll=True):
    """Tela de CRT: fundo, scanlines, grão e uma faixa de varredura lenta."""
    bar = ""
    if roll:
        bar = f'''<rect x="0" y="-40" width="{W}" height="40" fill="{FG}" opacity="0.035">
    <animate attributeName="y" from="-40" to="{h}" dur="7s" repeatCount="indefinite"/>
  </rect>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {h}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(label)}">
  <defs>{SCAN}{defs}</defs>
  <rect width="{W}" height="{h}" fill="{BG}"/>
  {body}
  {bar}
  <rect width="{W}" height="{h}" fill="url(#scan)"/>
  <rect width="{W}" height="{h}" filter="url(#grain)"/>
</svg>'''


def sky(y0, y1, lvl_top=13, lvl_bot=0, band=12):
    """Céu pálido que escurece em degraus de dithering até virar preto."""
    n = max(1, int((y1 - y0) / band))
    defs, rects = set(), []
    for i in range(n):
        lv = round(lvl_top + (lvl_bot - lvl_top) * i / (n - 1))
        defs.add(lv)
        rects.append(f'<rect x="0" y="{y0 + i*band}" width="{W}" height="{band}" fill="url(#d{lv})"/>')
    return "".join(dither(l) for l in sorted(defs) if l > 0), "".join(
        r for r in rects if 'url(#d0)' not in r)


def pole(x, top, bottom, s=1.0):
    """Poste de concreto com duas cruzetas e isoladores, em silhueta."""
    w = 9 * s
    arms = []
    for k, (ay, aw) in enumerate([(top + 18 * s, 92 * s), (top + 44 * s, 70 * s)]):
        arms.append(f'<rect x="{x - aw/2:.1f}" y="{ay:.1f}" width="{aw:.1f}" height="{5*s:.1f}"/>')
        for j in (-1, -0.45, 0.45, 1):
            ix = x + j * (aw / 2 - 6 * s)
            arms.append(f'<rect x="{ix - 2*s:.1f}" y="{ay - 7*s:.1f}" width="{4*s:.1f}" height="{7*s:.1f}"/>')
    brace = (f'<path d="M{x - 30*s:.1f} {top + 23*s:.1f} L{x:.1f} {top + 60*s:.1f} '
             f'L{x + 30*s:.1f} {top + 23*s:.1f}" fill="none" stroke="{BG}" stroke-width="{2*s:.1f}"/>')
    box = f'<rect x="{x - 11*s:.1f}" y="{top + 120*s:.1f}" width="{22*s:.1f}" height="{30*s:.1f}"/>'
    return (f'<g fill="{BG}"><path d="M{x - w/2*0.7:.1f} {top} L{x + w/2*0.7:.1f} {top} '
            f'L{x + w/2:.1f} {bottom} L{x - w/2:.1f} {bottom} Z"/>{"".join(arms)}{box}</g>{brace}')


def catenary(x0, y0, x1, y1, sag):
    mx = (x0 + x1) / 2
    my = (y0 + y1) / 2 + sag
    return f"M{x0:.1f} {y0:.1f} Q{mx:.1f} {my + sag*0.9:.1f} {x1:.1f} {y1:.1f}"


def wires(anchors, offsets, sag=34):
    """Fios entre as cruzetas de postes consecutivos."""
    out = []
    for dx, dy in offsets:
        for (xa, ya, sa), (xb, yb, sb) in zip(anchors, anchors[1:]):
            out.append(f'<path d="{catenary(xa + dx*sa, ya + dy*sa, xb + dx*sb, yb + dy*sb, sag)}" '
                       f'fill="none" stroke="{BG}" stroke-width="1.1"/>')
    return "".join(out)


def blots(cx, cy, n, spread, seed, rmax=7):
    """As manchas vermelhas nas sombras."""
    h = seed
    out = []
    for i in range(n):
        h = (h * 1103515245 + 12345) & 0x7FFFFFFF
        a = (h % 628) / 100
        d = spread * ((h >> 10) % 100) / 100
        r = 1.5 + ((h >> 17) % 100) / 100 * rmax
        x, y = cx + d * math.cos(a) * 1.6, cy + d * math.sin(a) * 0.5
        dur = 3 + (h >> 5) % 5
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{RED}">'
                   f'<animate attributeName="opacity" values="1;0.55;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def glitch(text, x, y, size, uid, period=9, family=SANS, spacing=2):
    """Cópia vermelha deslocada que aparece por um instante, recortada em faixa."""
    return f'''<clipPath id="{uid}"><rect x="0" y="{y - size}" width="{W}" height="{size*0.28:.0f}">
      <animate attributeName="y" values="{y-size};{y-size*0.55:.0f};{y-size*0.2:.0f};{y-size}" dur="{period}s" repeatCount="indefinite"/>
    </rect></clipPath>
  <text x="{x + 4}" y="{y}" font-family="{family}" font-size="{size}" fill="{RED}" letter-spacing="{spacing}"
        clip-path="url(#{uid})" opacity="0">{esc(text)}
    <animate attributeName="opacity" values="0;0;1;0;1;0;0" keyTimes="0;0.9;0.91;0.93;0.94;0.96;1"
             dur="{period}s" repeatCount="indefinite"/>
  </text>'''


# ── capa ─────────────────────────────────────────────────────────────
def header():
    H = 480
    sd, sr = sky(0, 288, lvl_top=15, lvl_bot=0)
    # postes: um perto, um longe, um cortado na borda
    p = [(640, 26, 1.45), (250, 140, 0.55), (868, 4, 1.7)]
    anchors = sorted([(x, t + 20 * s, s) for x, t, s in p])
    offs = [(-40, 0), (-18, -2), (18, -2), (40, 0), (-30, 26), (30, 26)]
    wire_lead = [(-12, 168, 0.3)] + anchors
    roles = [
        "backend       FastAPI · async · event-driven",
        "arquitetura   concorrência como invariante",
        "agentes       JevGuard, verificação de diff",
        "pesquisa      embeddings e recuperação",
    ]
    cycle, e = 3.4 * len(roles), 0.02
    lines = []
    for i, r in enumerate(roles):
        a, b = i / len(roles), (i + 1) / len(roles)
        pts = [(0, 0), (a, 0), (a + e, 1), (b - e, 1), (b, 0), (1, 0)]
        if i == 0:
            pts = [(0, 1), (b - e, 1), (b, 0), (1 - e, 0), (1, 1)]
        kt = ";".join(f"{t:.3f}" for t, _ in pts)
        vals = ";".join(str(v) for _, v in pts)
        lines.append(f'''<text x="40" y="408" font-family="{MONO}" font-size="13" fill="{DIM}" xml:space="preserve" opacity="{1 if i == 0 else 0}">{esc(r)}
      <animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>
    </text>''')
    kata = "パブロ・ファリナ"
    vert = "".join(f'<tspan x="846" dy="{0 if i == 0 else 17}">{c}</tspan>' for i, c in enumerate(kata))
    body = f'''
  {sr}
  <g>
    {wires(wire_lead, offs)}
    <animateTransform attributeName="transform" type="translate" values="0 0;0 0.8;0 0" dur="2.6s" repeatCount="indefinite"/>
  </g>
  {''.join(pole(x, t, H, s) for x, t, s in p)}
  {blots(660, 452, 13, 60, 11, rmax=5)}

  <text x="40" y="318" font-family="{MONO}" font-size="12" fill="{RED}" letter-spacing="3">LAYER:00</text>
  <text x="40" y="370" font-family="{SANS}" font-size="56" fill="{FG}" letter-spacing="3">Pablo Farina</text>
  {glitch("Pablo Farina", 40, 370, 56, "gx", period=8, spacing=3)}
  {''.join(lines)}
  <rect x="40" y="432" width="360" height="1" fill="{FAINT}"/>
  <text x="40" y="454" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1">unirio · sistemas de informação · rio de janeiro</text>
  <text x="846" y="326" font-family="{JP}" font-size="13" fill="{DIM}" text-anchor="middle">{vert}</text>
'''
    return screen(H, body, "Pablo Farina. Backend, arquitetura, verificação de coding agents e pesquisa. "
                  "UNIRIO, Rio de Janeiro.", defs=sd)


# ── título de camada ─────────────────────────────────────────────────
def layer(num, word, jp, note):
    H = 128
    # dithering horizontal: do preto ao cinza em degraus de 12px
    steps = list(range(0, 9))
    dd = "".join(dither(l) for l in steps if l)
    bw = 24
    fade = "".join(f'<rect x="{W - bw*(len(steps)-i)}" y="0" width="{bw}" height="{H}" fill="url(#d{l})"/>'
                   for i, l in enumerate(steps) if l)
    body = f'''
  {fade}
  <text x="40" y="44" font-family="{MONO}" font-size="12" fill="{RED}" letter-spacing="3">Layer:{num}<tspan fill="{DIM}" letter-spacing="1">   // {esc(note)}</tspan></text>
  <text x="36" y="98" font-family="{SANS}" font-size="46" fill="{FG}" letter-spacing="16">{esc(word)}
    <animate attributeName="opacity" values="1;1;0.2;1;0.4;1;1" keyTimes="0;0.8;0.81;0.83;0.84;0.86;1" dur="11s" repeatCount="indefinite"/>
  </text>
  {glitch(word, 36, 98, 46, "g" + num, period=11, spacing=16)}
  <text x="{W-236}" y="44" font-family="{JP}" font-size="13" fill="{DIM}" text-anchor="end">{jp}</text>'''
    return screen(H, body, f"Layer:{num} {word}, {note}", defs=dd, roll=False)


# ── leitura: números reais ───────────────────────────────────────────
def readout():
    H = 150
    items = [
        ("200+", "lojas_em_producao", "sistemas internos na Bagaggio"),
        ("10+", "projetos_entregues", "do requisito ao deploy monitorado"),
        ("605", "commits_12_meses", "21 repositórios com contribuições"),
    ]
    cw = (W - 80) / 3
    out = []
    for i, (v, k, c) in enumerate(items):
        x = 40 + i * cw
        out.append(f'''
  <text x="{x:.1f}" y="44" font-family="{MONO}" font-size="11" fill="{DIM}">{k}</text>
  <text x="{x - 2:.1f}" y="94" font-family="{SANS}" font-size="46" fill="{FG}">{v}</text>
  <text x="{x:.1f}" y="122" font-family="{MONO}" font-size="10.5" fill="{DIM}">// {esc(c)}</text>
  <rect x="{x:.1f}" y="30" width="6" height="6" fill="{RED}"/>''')
        out[-1] = out[-1].replace(f'<text x="{x:.1f}" y="44"', f'<text x="{x + 14:.1f}" y="36"', 1)
    return screen(H, "".join(out), "200+ lojas em produção, 10+ projetos entregues, 605 commits em 12 meses",
                  roll=False)


# ── psyche: cada princípio e a linha de código que ele vira ──────────
PSYCHE = [
    ("Concorrência só vira problema de verdade quando duas pessoas tentam comprar o "
     "último item ao mesmo tempo. A resposta não pode ser decidida depois: ou tem lock e "
     "transação explícita, ou o bug aparece em produção num sábado.",
     [("UPDATE", RED), (" estoque ", FG), ("SET", RED), (" qtd = qtd - 1 ", FG),
      ("WHERE", RED), (" sku = $1 ", FG), ("AND", RED), (" qtd > 0;", FG),
      ("  -- 0 linhas: acabou", DIM)]),
    ("Procuro manter cada regra de negócio perto de quem entende dela. Espalhada pelo "
     "controller, vira algo que ninguém consegue explicar, nem eu. Mensageria entra pelo "
     "mesmo motivo: quem publica um evento não precisa conhecer quem escuta.",
     [("await", RED), (" bus.publish(", FG), ('"pedido.criado"', DIM), (", evento)", FG),
      ("  # quem escuta não é problema meu", DIM)]),
    ("Agora estou preso em verificação. Agente escreve mais rápido do que eu consigo "
     "revisar, e prompt melhor não resolve isso. Foi por isso que o JevGuard começou.",
     [("veredito", FG), (" = ", DIM), ("gate", RED), ("(diff, regras)", FG),
      ("  # PASS · WARN · FAIL, decidido local", DIM)]),
]


def psyche():
    y = 34
    out = []
    for i, (prose, code) in enumerate(PSYCHE):
        out.append(f'<text x="40" y="{y + 14}" font-family="{MONO}" font-size="11" fill="{RED}">0{i+1}</text>')
        for j, l in enumerate(wrap(prose, 84)):
            out.append(f'<text x="84" y="{y + 14 + j*21}" font-family="{SANS}" font-size="14.5" '
                       f'fill="{FG}">{esc(l)}</text>')
        y += 14 + len(wrap(prose, 84)) * 21 + 6
        spans = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in code)
        out.append(f'<rect x="84" y="{y}" width="{W - 124}" height="32" fill="{PANEL}"/>'
                   f'<rect x="84" y="{y}" width="2" height="32" fill="{RED}"/>'
                   f'<text x="100" y="{y + 20.5}" font-family="{MONO}" font-size="12" xml:space="preserve">{spans}</text>')
        y += 32 + 34
    return screen(y, "".join(out), "Como eu penso. " + " ".join(p for p, _ in PSYCHE))


# ── protocol: projetos como nós da rede ──────────────────────────────
def trace(seed, x0, x1, y, amp):
    h = 0
    for ch in seed:
        h = (h * 131 + ord(ch)) & 0x7FFFFFFF
    pts, x = [], x0
    while x <= x1:
        h = (h * 1103515245 + 12345) & 0x7FFFFFFF
        spike = (h % 11 == 0)
        dy = (((h >> 8) % 100) / 100 - 0.5) * (amp * 2.4 if spike else amp * 0.35)
        pts.append(f"{x:.0f},{y + dy:.1f}")
        x += 6
    d = "M" + " L".join(pts)
    return (f'<path d="{d}" fill="none" stroke="{DIM}" stroke-width="1" opacity="0.7"/>'
            f'<circle r="3" fill="{RED}"><animateMotion dur="5s" repeatCount="indefinite" path="{d}"/></circle>')


def node(name, sub, desc, stack, width, featured=False):
    ww = width
    chars = 88 if featured else 52
    lines = wrap(desc, chars)
    H = (206 if featured else 216)
    tags = "  ".join(f"[{t}]" for t in stack)
    body = "".join(f'<text x="28" y="{118 + i*20}" font-family="{SANS}" font-size="13.5" fill="{FG}">{esc(l)}</text>'
                   for i, l in enumerate(lines))
    tr = trace(name, ww - (300 if featured else 150), ww - 28, 44, 14)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {ww} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(name)}: {esc(desc)}">
  <defs>{SCAN}</defs>
  <rect width="{ww}" height="{H}" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{ww-1}" height="{H-1}" fill="none" stroke="{FAINT}"/>
  <text x="28" y="34" font-family="{MONO}" font-size="10.5" fill="{DIM}">node://pablozr/{esc(name)}</text>
  {tr}
  <text x="26" y="76" font-family="{SANS}" font-size="{30 if featured else 22}" fill="{FG}" letter-spacing="1">{esc(name)}</text>
  <text x="28" y="96" font-family="{MONO}" font-size="11" fill="{RED}">{esc(sub)}</text>
  {body}
  <text x="28" y="{H - 22}" font-family="{MONO}" font-size="10.5" fill="{DIM}" xml:space="preserve">{esc(tags)}</text>
  <rect width="{ww}" height="{H}" fill="url(#scan)"/>
</svg>'''


# ── landscape: linguagens e stack ────────────────────────────────────
# Repositórios PÚBLICOS e não-fork (42 no total).
LANGS = [("TypeScript", 49.8, 12), ("Python", 20.7, 17), ("Java", 8.4, 10),
         ("HTML", 6.6, 11), ("SCSS", 5.6, 6), ("JavaScript", 4.3, 9),
         ("CSS", 3.7, 12)]

STACK = [
    ("backend", ["Python", "FastAPI", "Java", "Spring Boot", "Go"]),
    ("frontend", ["Angular", "TypeScript", "React", "Next.js", "Vite"]),
    ("dados_infra", ["PostgreSQL", "MongoDB", "Redis", "RabbitMQ", "Docker"]),
]


def landscape():
    top, row = 64, 28
    bx, bmax = 190, 520
    mx = LANGS[0][1]
    out = [f'<text x="40" y="38" font-family="{MONO}" font-size="11" fill="{DIM}">'
           f'$ linguist --public --no-forks   <tspan fill="{FAINT}">#</tspan> 42 repositórios</text>']
    for i, (name, pct, n) in enumerate(LANGS):
        y = top + i * row
        w = bmax * pct / mx
        out.append(f'''
  <text x="40" y="{y + 12}" font-family="{MONO}" font-size="12" fill="{FG}">{name}</text>
  <text x="{bx - 16}" y="{y + 12}" font-family="{MONO}" font-size="11" fill="{DIM}" text-anchor="end">{str(pct).replace('.', ',')}%</text>
  <rect x="{bx}" y="{y}" width="{bmax}" height="14" fill="url(#d1)"/>
  <rect x="{bx}" y="{y}" width="0" height="14" fill="url(#d{10 if i == 0 else 6})">
    <animate attributeName="width" from="0" to="{w:.1f}" begin="{0.2 + i*0.1:.1f}s" dur="0.9s" fill="freeze"/>
  </rect>
  <rect x="{bx}" y="{y}" width="2" height="14" fill="{RED}">
    <animate attributeName="x" from="{bx}" to="{bx + w - 2:.1f}" begin="{0.2 + i*0.1:.1f}s" dur="0.9s" fill="freeze"/>
  </rect>
  <text x="{bx + bmax + 20}" y="{y + 12}" font-family="{MONO}" font-size="11" fill="{DIM}">{n} repos</text>''')
    sy = top + len(LANGS) * row + 40
    cw = (W - 80) / 3
    for i, (g, items) in enumerate(STACK):
        x = 40 + i * cw
        out.append(f'<text x="{x:.1f}" y="{sy}" font-family="{MONO}" font-size="11" fill="{RED}">{g}/</text>')
        for j, it in enumerate(items):
            out.append(f'<text x="{x + 14:.1f}" y="{sy + 26 + j*21}" font-family="{MONO}" font-size="12.5" fill="{FG}">'
                       f'<tspan fill="{FAINT}">{"└─" if j == len(items) - 1 else "├─"} </tspan>{esc(it)}</text>')
    H = sy + 26 + 5 * 21 + 18
    return screen(H, "".join(out), "Linguagens por volume de código nos 42 repositórios públicos: " +
                  ", ".join(f"{n} {p}%" for n, p, _ in LANGS) + ". Stack: " +
                  "; ".join(f"{g}: {', '.join(it)}" for g, it in STACK),
                  defs=dither(1) + dither(6) + dither(10), roll=False)


def footer():
    H = 190
    sd, sr = sky(0, 140, lvl_top=11, lvl_bot=0, band=10)
    p = [(140, 20, 0.55), (520, 44, 0.42), (800, 60, 0.34)]
    anchors = [(x, t + 20 * s, s) for x, t, s in p]
    body = f'''
  {sr}
  {wires([(-10, 40, 0.5)] + anchors + [(890, 76, 0.3)], [(-40, 0), (40, 0), (-30, 26), (30, 26)], sag=22)}
  {''.join(pole(x, t, H, s) for x, t, s in p)}
  <text x="40" y="170" font-family="{MONO}" font-size="12" fill="{FG}" letter-spacing="2">close the world, open the nExt</text>
  <text x="{W-40}" y="170" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="2" text-anchor="end">txEn eht nepo ,dlrow eht esolc</text>'''
    return screen(H, body, "close the world, open the nExt", defs=sd)


if __name__ == "__main__":
    print("gerando assets:")
    write("header.svg", header())
    write("readout.svg", readout())
    write("psyche.svg", psyche())
    write("landscape.svg", landscape())
    write("footer.svg", footer())
    for num, word, jp, note in [("01", "EGO", "自我", "quem escreve"),
                                ("02", "PSYCHE", "精神", "como eu penso"),
                                ("03", "PROTOCOL", "プロトコル", "o que eu construí"),
                                ("04", "LANDSCAPE", "風景", "com o que eu construo")]:
        write(f"layers/{num}.svg", layer(num, word, jp, note))
    print("  -- nodes --")
    write("nodes/jevguard.svg", node(
        "JevGuard", "motor de política semântica para coding agents",
        "Verifica o diff que um agente acabou de produzir contra as políticas do repositório. "
        "Cada regra recebe um julgamento semântico e um gate determinístico local devolve o "
        "veredito: PASS, WARN ou FAIL.", ["typescript", "cli", "policy-engine"], W, featured=True))
    for slug, name, sub, desc, stack in [
        ("prisma", "PRISMA", "plataforma acadêmica da UNIRIO",
         "Projetos acadêmicos importados do SIE. Auth institucional via Google, access e "
         "refresh token em Redis e recomendação semântica sobre a busca.",
         ["python", "fastapi", "redis", "rag"]),
        ("self-checkout", "self-checkout-monolith", "autoatendimento por mesa",
         "Carrinho anônimo por mesa em Redis, checkout Stripe idempotente, reset de senha "
         "assíncrono com worker SMTP e cache por produto.",
         ["fastapi", "redis", "rabbitmq", "stripe"]),
        ("subscription", "subscription-monolith", "gestão de assinaturas",
         "Regras separadas por domínio, persistência relacional e comunicação assíncrona "
         "entre os serviços.", ["fastapi", "postgresql", "rabbitmq"]),
        ("fastapi-template", "FastAPI-Template", "base de API para produção",
         "Organização modular, configuração por ambiente e docker-compose pronto pra subir.",
         ["fastapi", "docker", "postgresql"]),
    ]:
        write(f"nodes/{slug}.svg", node(name, sub, desc, stack, 432))
    print("ok")
