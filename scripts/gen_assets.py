#!/usr/bin/env python3
"""
Gera todos os assets SVG da capa do perfil.

Rode:  python3 gen.py        # escreve em ./assets

Por que SVG proprio em vez de capsule-render / github-readme-stats:
  - Medido em 29/09/2026: github-readme-stats devolvia 503 e
    github-profile-trophy devolvia 402 (DEPLOYMENT_DISABLED).
    Servico externo cai e leva a capa junto.
  - GitHub remove <script> e CSS inline do README, mas renderiza SVG
    via <img>, incluindo <style> e SMIL dentro do proprio SVG.
    Toda animacao mora no arquivo.

Por que a fonte e a stack de sistema:
  Um SVG servido por <img> nao carrega webfont. Pedir "JetBrains Mono"
  ali nao resolve, so cai num fallback diferente em cada visitante.

Direcao visual: quase-preto, UM acento (ambar), hairlines. O gradiente
ciano->roxo->rosa que eu usei antes virou a assinatura visual de README
gerado por IA, entao aqui nao tem.
"""
import os, math

OUT = "assets"
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)

# DIM foi #807C74. Medido contra o fundo, dava 4.76:1 em opacidade cheia e
# 2.88:1 quando aplicado a 0.70 — ilegivel na pratica, e era o que deixava
# legendas e contagens apagadas. #A8A39A sobe para 7.89:1 e aguenta 0.85 (5.91:1).
BG, ACC, FG, DIM, BORDER = "#0A0A0B", "#F5A524", "#EDEAE4", "#A8A39A", "#26262A"
MONO = ("ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,"
        "'DejaVu Sans Mono','Liberation Mono',monospace")
SANS = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,"
        "Helvetica,Arial,sans-serif")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, n):
    """SVG nao quebra linha sozinho, entao quebro por palavra aqui."""
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def write(name, body):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"  {name:<36} {len(body)/1024:5.1f} KB")


def sigil(cx, cy, size=200, opacity=1.0):
    """Sigilo geometrico simetrico.

    Antes era uma grelha densa de tracinhos pseudo-aleatorios. Medi o
    efeito: lia como ruido/estatica, nao como desenho. Uma figura
    simetrica le como simbolo deliberado mesmo em tamanho pequeno, e
    simetria e o que separa "ornamento" de "sujeira de fundo".
    """
    SEGS = [
        ([(-1, 0), (0, -1), (1, 0), (0, 1), (-1, 0)], ACC, 1.6),          # losango externo
        ([(-0.55, 0), (0, -0.45), (0.55, 0), (0, 0.45), (-0.55, 0)], DIM, 1.0),  # losango interno
        ([(0, -1), (0, 1)], ACC, 1.1),                                     # espinha
        ([(-0.78, -0.34), (0, -0.72), (0.78, -0.34)], DIM, 1.0),           # chevron superior
        ([(-0.78, 0.34), (0, 0.72), (0.78, 0.34)], DIM, 1.0),              # chevron inferior
        ([(-1, 0), (-0.55, -0.45)], DIM, 1.0),
        ([(1, 0), (0.55, -0.45)], DIM, 1.0),
        ([(-1, 0), (-0.55, 0.45)], DIM, 1.0),
        ([(1, 0), (0.55, 0.45)], DIM, 1.0),
        ([(-0.55, -0.45), (-0.55, 0.45)], ACC, 0.9),                       # laterais
        ([(0.55, -0.45), (0.55, 0.45)], ACC, 0.9),
    ]
    k = size / 2.0
    out = []
    for pts, col, w in SEGS:
        pts_s = " ".join(f"{cx + x * k:.1f},{cy + y * k:.1f}" for x, y in pts)
        out.append(f'<polyline points="{pts_s}" fill="none" stroke="{col}" '
                   f'stroke-width="{w}" opacity="{opacity * 0.9:.2f}"/>')
    for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
        out.append(f'<circle cx="{cx + x * k:.1f}" cy="{cy + y * k:.1f}" r="2.3" '
                   f'fill="{ACC}" opacity="{opacity * 0.85:.2f}"/>')
    return "".join(out)


def tag_row(items, x, y, size=9.5):
    s, cx = [], x
    for i, t in enumerate(items):
        if i:
            s.append(f'<text x="{cx:.1f}" y="{y}" font-family="{MONO}" '
                     f'font-size="{size}" fill="{BORDER}">/</text>')
            cx += 10
        s.append(f'<text x="{cx:.1f}" y="{y}" font-family="{MONO}" font-size="{size}" '
                 f'fill="{DIM}" letter-spacing="0.6">{esc(t)}</text>')
        cx += len(t) * size * 0.62 + 10
    return "".join(s)


# ── header ───────────────────────────────────────────────────────────
def header():
    W, H = 880, 268
    roles = [
        "backend em FastAPI, async e event-driven",
        "arquitetura orientada a domínio, concorrência como invariante",
        "ferramentas para coding agents: JevGuard",
        "pesquisa aplicada: embeddings e recuperação",
    ]
    wipes, lines = [], []
    for i, r in enumerate(roles):
        wipes.append(f'''<clipPath id="w{i}"><rect x="0" y="0" width="0" height="24">
      <animate attributeName="width" from="0" to="640" begin="{0.7 + i*0.13:.2f}s"
               dur="0.45s" fill="freeze"/></rect></clipPath>''')
        t0 = 1.0 + i * 3.0
        lines.append(f'''<text x="52" y="196" font-family="{MONO}" font-size="14.5"
          fill="{DIM}" clip-path="url(#w{i})" opacity="0">{esc(r)}
      <set attributeName="opacity" to="1" begin="{t0}s" dur="0.2s" repeatCount="indefinite"/>
      <set attributeName="opacity" to="0" begin="{t0 + 2.3}s" dur="0.4s" repeatCount="indefinite"/>
    </text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Pablo Farina, backend, arquitetura de software e pesquisa">
  <defs>{''.join(wipes)}
    <linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{BG}" stop-opacity="1"/>
      <stop offset="52%" stop-color="{BG}" stop-opacity="0.98"/>
      <stop offset="64%" stop-color="{BG}" stop-opacity="0.70"/>
      <stop offset="70%" stop-color="{BG}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g>{sigil(706, 106, size=150, opacity=0.95)}</g>
  <rect width="{W}" height="{H}" fill="url(#veil)"/>
  <rect x="0" y="0" width="3" height="{H}" fill="{ACC}"/>
  <text x="52" y="92" font-family="{MONO}" font-size="12.5" fill="{ACC}"
        letter-spacing="2.4">BACKEND · ARQUITETURA</text>
  <text x="49" y="164" font-family="{SANS}" font-size="66" font-weight="700"
        fill="{FG}" letter-spacing="-2.6">Pablo Farina</text>
  {''.join(lines)}
  <rect x="52" y="185" width="9" height="15" fill="{ACC}">
    <animate attributeName="opacity" values="1;0;1" dur="1.15s" repeatCount="indefinite"/>
  </rect>
  <text x="52" y="242" font-family="{MONO}" font-size="11.5" fill="{DIM}"
        opacity="0.9">UNIRIO · Sistemas de Informação · Rio de Janeiro</text>
</svg>'''


# ── scope: numeros reais ─────────────────────────────────────────────
def scope():
    # Estatico de proposito: um <animate> filho direto do <svg> anima a
    # OPACIDADE DA RAIZ, nao do card. Foi o que deixou esta faixa presa em
    # ~5% e ilegivel (medido: pixel 27/255 onde o texto e #EDEAE4).
    W, H = 880, 158
    cw = (W - 3 * 20) / 3
    items = [
        ("200+", "lojas em produção", "sistemas internos na Bagaggio"),
        ("10+", "projetos entregues", "do requisito ao deploy monitorado"),
        ("605", "commits em 12 meses", "21 repositórios com contribuições"),
    ]
    cards = []
    for i, (big, label, sub) in enumerate(items):
        x = 20 + i * (cw + 20)
        cards.append(f'''
  <line x1="{x:.1f}" y1="24" x2="{x + cw:.1f}" y2="24" stroke="{ACC}" stroke-width="2" opacity="0.9"/>
  <line x1="{x:.1f}" y1="24" x2="{x:.1f}" y2="132" stroke="{DIM}" stroke-width="1" opacity="0.22"/>
  <line x1="{x:.1f}" y1="132" x2="{x + cw:.1f}" y2="132" stroke="{DIM}" stroke-width="1" opacity="0.22"/>
  <text x="{x + 18:.1f}" y="76" font-family="{SANS}" font-size="42" font-weight="700" fill="{FG}">{big}</text>
  <text x="{x + 18:.1f}" y="102" font-family="{MONO}" font-size="12" fill="{FG}" opacity="0.9">{label}</text>
  <text x="{x + 18:.1f}" y="121" font-family="{MONO}" font-size="10.5" fill="{DIM}">{sub}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="200+ lojas em produção, 10+ projetos entregues, 1,7 mil commits em 12 meses">
  {''.join(cards)}
</svg>'''


# ── manifesto: prosa, nao lista de titulo em negrito ─────────────────
PRINCIPLES = [
    "Concorrência só vira problema de verdade quando duas pessoas tentam comprar o "
    "último item ao mesmo tempo. Já vi isso acontecer o suficiente pra saber que a "
    "resposta não pode ser decidida depois: ou tem lock e transação explícita, ou o "
    "bug aparece em produção num sábado.",
    "Procuro manter cada regra de negócio perto de quem entende dela. Espalhada pelo "
    "controller, a regra vira algo que ninguém consegue explicar, nem eu. Mensageria "
    "entra pelo mesmo motivo: quem publica um evento não precisa conhecer quem escuta.",
    "Agora estou preso em verificação. Agente escreve mais rápido do que eu consigo "
    "revisar, e prompt melhor não resolve isso. Foi por isso que o JevGuard começou.",
]

def principles():
    W = 880
    PAD, SIZE, LH, GAP = 34, 13.5, 21, 15
    chars = 92
    blocks = [wrap(p, chars) for p in PRINCIPLES]
    H = 70 + sum(len(b) * LH for b in blocks) + GAP * (len(blocks) - 1) + 26
    y = 74
    out = []
    for b in blocks:
        for i, line in enumerate(b):
            out.append(f'<text x="{PAD}" y="{y:.1f}" font-family="{SANS}" '
                       f'font-size="{SIZE}" fill="{FG if i == 0 else DIM}">{esc(line)}</text>')
            y += LH
        y += GAP
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H:.0f}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Como eu penso: concorrência, fronteira de domínio e verificação de agentes">
  <text x="{PAD}" y="34" font-family="{MONO}" font-size="12.5" fill="{ACC}">&gt; como eu penso</text>
  <line x1="{PAD}" y1="46" x2="{W-PAD}" y2="46" stroke="{BORDER}" stroke-width="1"/>
  {''.join(out)}
</svg>'''


# ── cards de projeto ─────────────────────────────────────────────────
def half(title, idx, desc, stack):
    W, H, PAD = 432, 204, 26
    body = "".join(
        f'<text x="{PAD}" y="{104 + i*17}" font-family="{SANS}" font-size="12.5" '
        f'fill="{DIM}">{esc(l)}</text>' for i, l in enumerate(wrap(desc, 56)[:4]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(title)}">
  <rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{BORDER}"/>
  <rect x="0" y="0" width="{W}" height="2" fill="{ACC}"/>
  <text x="{W-PAD}" y="42" font-family="{MONO}" font-size="11" fill="{ACC}"
        text-anchor="end" opacity="0.85">{idx}</text>
  <text x="{PAD}" y="66" font-family="{SANS}" font-size="20" font-weight="700"
        fill="{FG}" letter-spacing="-0.4">{esc(title)}</text>
  {body}
  {tag_row(stack, PAD, 182)}
</svg>'''


def feature(title, sub, idx, desc, flow, stack):
    W, H, PAD = 880, 236, 34
    body = "".join(
        f'<text x="{PAD}" y="{112 + i*18}" font-family="{SANS}" font-size="13" '
        f'fill="{DIM}">{esc(l)}</text>' for i, l in enumerate(wrap(desc, 96)[:2]))
    n, bw, gap, by = len(flow), 138, 26, 168
    boxes = []
    for i, label in enumerate(flow):
        x = PAD + i * (bw + gap)
        cx = x + bw / 2
        verdict = i == n - 1
        col = ACC if verdict else DIM
        op = 0.85 if verdict else 0.42
        boxes.append(f'<rect x="{x:.1f}" y="{by}" width="{bw}" height="34" rx="6" '
                     f'fill="none" stroke="{col}" stroke-width="1" opacity="{op}"/>')
        boxes.append(f'<text x="{cx:.1f}" y="{by+21.5}" font-family="{MONO}" font-size="9.5" '
                     f'fill="{col}" text-anchor="middle">{esc(label)}</text>')
        if i < n - 1:
            ax = x + bw
            boxes.append(f'<line x1="{ax+5:.1f}" y1="{by+17}" x2="{ax+gap-6:.1f}" y2="{by+17}" '
                         f'stroke="{BORDER}" stroke-width="1.5"/>'
                         f'<path d="M{ax+gap-9:.1f},{by+13.5} L{ax+gap-4:.1f},{by+17} '
                         f'L{ax+gap-9:.1f},{by+20.5} Z" fill="{BORDER}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(title)}">
  <rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{BORDER}"/>
  <rect x="0" y="0" width="{W}" height="2" fill="{ACC}"/>
  <text x="{W-PAD}" y="46" font-family="{MONO}" font-size="11.5" fill="{ACC}"
        text-anchor="end" opacity="0.85">{idx}</text>
  <text x="{PAD}" y="72" font-family="{SANS}" font-size="27" font-weight="700"
        fill="{FG}" letter-spacing="-0.7">{esc(title)}</text>
  <text x="{PAD}" y="93" font-family="{MONO}" font-size="11" fill="{ACC}"
        opacity="0.9">{esc(sub)}</text>
  {body}
  {''.join(boxes)}
  {tag_row(stack, PAD, 224)}
</svg>'''


def thin(title, idx, desc, stack):
    W, H, PAD = 880, 108, 34
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(title)}">
  <rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{BORDER}"/>
  <rect x="0" y="0" width="{W}" height="2" fill="{ACC}"/>
  <text x="{W-PAD}" y="38" font-family="{MONO}" font-size="11" fill="{ACC}"
        text-anchor="end" opacity="0.85">{idx}</text>
  <text x="{PAD}" y="46" font-family="{SANS}" font-size="19" font-weight="700"
        fill="{FG}" letter-spacing="-0.3">{esc(title)}</text>
  <text x="{PAD}" y="70" font-family="{SANS}" font-size="12.5" fill="{DIM}">{esc(desc)}</text>
  {tag_row(stack, PAD, 92)}
</svg>'''


# ── linguagens: bytes reais da API ───────────────────────────────────
# Dados de repositorios PUBLICOS e nao-fork apenas (42 no total, 4,60 MB).
# A primeira medicao misturava repositorios privados e inflava Java e o total.
LANGS = [("TypeScript", 49.8, 12), ("Python", 20.7, 17), ("Java", 8.4, 10),
         ("HTML", 6.6, 11), ("SCSS", 5.6, 6), ("JavaScript", 4.3, 9),
         ("CSS", 3.7, 12)]

def languages():
    W, row, top = 880, 30, 58
    H = top + row * len(LANGS) + 36
    bx, bmax, mx = 160, 360, LANGS[0][1]
    rows = []
    for i, (name, pct, n) in enumerate(LANGS):
        y = top + i * row
        op = 1.0 if i == 0 else 0.6
        rows.append(f'''
  <text x="30" y="{y+15}" font-family="{MONO}" font-size="13" fill="{FG}" opacity="{op}">{name}</text>
  <text x="132" y="{y+15}" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end">{pct}%</text>
  <rect x="{bx}" y="{y+4}" width="{bmax}" height="12" rx="6" fill="{DIM}" opacity="0.14"/>
  <rect x="{bx}" y="{y+4}" width="0" height="12" rx="6" fill="{ACC}" opacity="{op}">
    <animate attributeName="width" from="0" to="{bmax*pct/mx:.1f}" begin="{0.2 + i*0.09:.2f}s"
             dur="0.75s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1"/>
  </rect>
  <text x="{bx + bmax + 16}" y="{y+15}" font-family="{MONO}" font-size="10.5" fill="{DIM}" opacity="0.85">{n}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Linguagens por volume de codigo nos 42 repositorios publicos">
  <text x="30" y="30" font-family="{MONO}" font-size="12.5" fill="{ACC}">&gt; por volume de código</text>
  <text x="{W-30}" y="30" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end">42 repositórios públicos, sem forks</text>
  <text x="{bx + bmax + 16}" y="30" font-family="{MONO}" font-size="10.5" fill="{DIM}" opacity="0.85">repos</text>
  <line x1="30" y1="44" x2="{W-30}" y2="44" stroke="{DIM}" stroke-width="1" opacity="0.25"/>
  {''.join(rows)}
  <text x="30" y="{H-14}" font-family="{MONO}" font-size="10" fill="{DIM}"
        opacity="0.85">cada repositório pode ter mais de uma linguagem, então as contagens passam de 42</text>
</svg>'''


def footer():
    W, H = 880, 72
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="xMidYMid meet" role="img" aria-label="Fim">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g>{sigil(W/2, 34, size=46, opacity=0.7)}</g>
  <rect x="0" y="{H-2}" width="{W}" height="2" fill="{ACC}"/>
</svg>'''


def divider():
    W, H = 880, 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}"
     preserveAspectRatio="none" role="presentation" aria-hidden="true">
  <line x1="0" y1="7" x2="{W}" y2="7" stroke="{BORDER}" stroke-width="1"/>
  <line x1="0" y1="7" x2="88" y2="7" stroke="{ACC}" stroke-width="1"/>
</svg>'''


if __name__ == "__main__":
    print("gerando assets:")
    write("header.svg", header())
    write("scope.svg", scope())
    write("principles.svg", principles())
    write("languages.svg", languages())
    write("footer.svg", footer())
    write("divider.svg", divider())
    print("  -- cards de projeto --")
    write("projects/jevguard.svg", feature(
        "JevGuard", "motor de política semântica para coding agents", "01",
        "Verifica o diff que um agente acabou de produzir contra as políticas do "
        "repositório. Cada regra recebe um julgamento semântico e um gate determinístico "
        "local devolve o veredito.",
        ["agente termina o turno", "diff + regras locais", "julgamento por regra",
         "gate determinístico", "PASS · WARN · FAIL"],
        ["TypeScript", "CLI", "policy engine"]))
    write("projects/prisma.svg", half(
        "PRISMA", "02",
        "Plataforma da UNIRIO para projetos acadêmicos importados do SIE. Auth institucional "
        "via Google, sessões com access e refresh token em Redis, e recomendação semântica "
        "sobre a busca.",
        ["Python", "FastAPI", "Redis", "RAG"]))
    write("projects/self-checkout.svg", half(
        "self-checkout-monolith", "03",
        "Carrinho anônimo por mesa em Redis, checkout Stripe idempotente, reset de senha "
        "assíncrono com RabbitMQ e worker SMTP, catálogo com cache por produto.",
        ["FastAPI", "Redis", "RabbitMQ", "Stripe"]))
    write("projects/subscription.svg", half(
        "subscription-monolith", "04",
        "Gestão de assinaturas com regras separadas por domínio, persistência relacional e "
        "comunicação assíncrona entre os serviços.",
        ["FastAPI", "PostgreSQL", "RabbitMQ"]))
    write("projects/fastapi-template.svg", half(
        "FastAPI-Template", "05",
        "Template de API em padrão de produção. Organização modular, configuração por "
        "ambiente e docker-compose pronto pra subir.",
        ["FastAPI", "Docker", "PostgreSQL"]))
    print("ok")
