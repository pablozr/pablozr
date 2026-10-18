#!/usr/bin/env python3
"""
Generates every SVG used by the profile README, in a dark and a light variant.

Run:  python3 scripts/gen_assets.py     # writes to ./assets

The README picks the variant with <picture> and prefers-color-scheme, so each
image follows the viewer's GitHub theme. Everything is self-hosted: no stats
service, no badge service, nothing that can go down or rate-limit.

Constraints:
  - An SVG served through <img> cannot load webfonts: system font stacks only.
  - GitHub strips <script> but keeps <style>, so animation is CSS inside the
    file. Elements are visible by default and only animate *from* hidden, so a
    viewer without animation still shows everything.
  - Brand icons come from simple-icons (CC0), vendored in scripts/icons.json.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
ICONS = json.load(open(os.path.join(ROOT, "scripts", "icons.json"), encoding="utf-8"))

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(
        bg="#0d1117", card="#161b22", border="#30363d", fg="#e6edf3", muted="#8b949e",
        faint="#21262d", dot="#21262d", code="#0b0f14", a1="#8b5cf6", a2="#22d3ee",
        kw="#ff7b72", str="#a5d6ff", com="#8b949e", fn="#d2a8ff", num="#79c0ff",
        dark_icon="#e6edf3",
    ),
    "light": dict(
        bg="#ffffff", card="#f6f8fa", border="#d0d7de", fg="#1f2328", muted="#59636e",
        faint="#eaeef2", dot="#d8dee4", code="#ffffff", a1="#7c3aed", a2="#0891b2",
        kw="#cf222e", str="#0a3069", com="#6e7781", fn="#8250df", num="#0550ae",
        dark_icon="#1f2328",
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, n):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def defs(t, extra=""):
    return f"""<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/>
  </linearGradient>
  <linearGradient id="accentV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/>
  </linearGradient>
  {extra}
</defs>"""


STYLE = """<style>
  .sans { font-family: %s; }
  .mono { font-family: %s; }
  .in { animation: in .7s cubic-bezier(.2,.7,.2,1) backwards; }
  .blink { animation: blink 1.1s steps(1) infinite; }
  .pulse { animation: pulse 6s ease-in-out infinite; }
  @keyframes in { from { opacity: 0; transform: translateY(6px); } }
  @keyframes blink { 50%% { opacity: 0; } }
  @keyframes pulse { 0%%, 100%% { opacity: .55; } 50%% { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) { .in, .blink, .pulse { animation: none; } }
</style>""" % (SANS, MONO)


def svg(w, h, body, t, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="none">\n{STYLE}\n{defs(t, extra_defs)}\n{body}\n</svg>\n'
    )


def icon(name, x, y, size, t, color=None):
    ic = ICONS[name]
    fill = color or "#" + ic["hex"]
    if fill.lower() in ("#000000", "#0f0f11", "#181717"):
        fill = t["dark_icon"]
    s = size / 24
    return f'<path transform="translate({x} {y}) scale({s})" fill="{fill}" d="{ic["path"]}"/>'


def delay(i, base=0.0, step=0.12):
    return f'style="animation-delay:{base + i * step:.2f}s"'


# ---------------------------------------------------------------- header
def header(t):
    w, h = 1000, 300
    tx, ty, tw, th = 548, 38, 412, 224
    term = [
        ("$ ", "cat focus.yml", True),
        ("backend:      ", "FastAPI · async · event-driven", False),
        ("architecture: ", "concurrency as an invariant", False),
        ("agents:       ", "JevGuard · diff verification", False),
        ("research:     ", "embeddings &amp; retrieval", False),
    ]
    lines = []
    for i, (k, v, cmd) in enumerate(term):
        y = ty + 76 + i * 27
        kc = t["a2"] if cmd else t["fn"]
        vc = t["fg"] if cmd else t["muted"]
        lines.append(
            f'<text class="mono in" {delay(i, .5, .25)} x="{tx + 22}" y="{y}" font-size="13.5">'
            f'<tspan fill="{kc}">{esc(k) if cmd else k}</tspan><tspan fill="{vc}">{v}</tspan></text>'
        )
    cy = ty + 76 + len(term) * 27
    lines.append(
        f'<text class="mono in" {delay(len(term), .5, .25)} x="{tx + 22}" y="{cy}" font-size="13.5" '
        f'fill="{t["a2"]}">$ <tspan class="blink" fill="{t["fg"]}">▍</tspan></text>'
    )
    body = f"""
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t['bg']}" stroke="{t['border']}"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#dots)"/>
<circle class="pulse" cx="760" cy="40" r="260" fill="url(#glow)" clip-path="url(#frame)"/>
<rect x="1" y="1" width="{w - 2}" height="3" rx="1.5" fill="url(#accent)"/>

<text class="mono in" x="48" y="92" font-size="15" fill="{t['muted']}">// hello, world. I'm</text>
<text class="sans in" style="animation-delay:.1s" x="46" y="152" font-size="56" font-weight="700" fill="{t['fg']}" letter-spacing="-1.5">Pablo Farina</text>
<text class="sans in" style="animation-delay:.2s" x="48" y="194" font-size="24" font-weight="600" fill="url(#accent)">Backend Engineer</text>
<text class="sans in" style="animation-delay:.3s" x="48" y="230" font-size="15.5" fill="{t['muted']}">Concurrency · Architecture · Coding-agent verification</text>
<text class="mono in" style="animation-delay:.4s" x="48" y="264" font-size="13" fill="{t['muted']}">
  <tspan fill="{t['a2']}">◆</tspan> Rio de Janeiro, Brazil  <tspan fill="{t['a2']}">◆</tspan> Information Systems @ UNIRIO</text>

<g class="in" style="animation-delay:.3s">
  <rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{t['code']}" stroke="{t['border']}"/>
  <path d="M{tx} {ty + 12}a12 12 0 0 1 12-12h{tw - 24}a12 12 0 0 1 12 12v24h-{tw}z" fill="{t['card']}"/>
  <line x1="{tx}" y1="{ty + 36}" x2="{tx + tw}" y2="{ty + 36}" stroke="{t['border']}"/>
  <circle cx="{tx + 20}" cy="{ty + 18}" r="5.5" fill="#ff5f57"/>
  <circle cx="{tx + 38}" cy="{ty + 18}" r="5.5" fill="#febc2e"/>
  <circle cx="{tx + 56}" cy="{ty + 18}" r="5.5" fill="#28c840"/>
  <text class="mono" x="{tx + tw / 2}" y="{ty + 23}" font-size="12" fill="{t['muted']}" text-anchor="middle">pablo@rio: ~</text>
</g>
{chr(10).join(lines)}
"""
    extra = f"""
  <clipPath id="frame"><rect x="1" y="1" width="998" height="298" rx="16"/></clipPath>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{t['dot']}"/>
  </pattern>
  <radialGradient id="glow">
    <stop offset="0" stop-color="{t['a1']}" stop-opacity=".20"/>
    <stop offset=".5" stop-color="{t['a2']}" stop-opacity=".06"/>
    <stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/>
  </radialGradient>"""
    return svg(w, h, body, t, extra)


# ---------------------------------------------------------------- contact
def contact(kind, t):
    label = {"linkedin": "LinkedIn", "email": "pablo.farina28@outlook.com", "github": "GitHub"}[kind]
    w = 64 + int(len(label) * (7.9 if kind == "email" else 8.6))
    h = 44
    if kind == "email":
        ic = (
            f'<g transform="translate(18 12)" stroke="{t["fg"]}" stroke-width="1.8" '
            f'stroke-linejoin="round" stroke-linecap="round" fill="none">'
            f'<rect x="1" y="3" width="18" height="14" rx="2.5"/><path d="M2 5l8 6 8-6"/></g>'
        )
    else:
        ic = icon(kind, 18, 12, 20, t)
    body = f"""
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="22" fill="{t['card']}" stroke="{t['border']}"/>
{ic}
<text class="sans" x="48" y="27.5" font-size="14.5" font-weight="600" fill="{t['fg']}">{esc(label)}</text>
"""
    return svg(w, h, body, t)


# ---------------------------------------------------------------- stats
def stats(t):
    w, h = 1000, 150
    tiles = [
        ("200+", "stores in production", "internal systems at Bagaggio"),
        ("10+", "projects shipped", "from requirements to monitored deploy"),
        ("605", "commits in 12 months", "across 21 repositories"),
    ]
    tw, gap = 316, 26
    parts = []
    for i, (num, label, sub) in enumerate(tiles):
        x = i * (tw + gap)
        parts.append(f"""
<g class="in" {delay(i, 0, .15)}>
  <rect x="{x + .5}" y=".5" width="{tw - 1}" height="{h - 1}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
  <rect x="{x + 24}" y="28" width="28" height="3" rx="1.5" fill="url(#accent)"/>
  <text class="sans" x="{x + 24}" y="82" font-size="44" font-weight="700" fill="url(#accent)" letter-spacing="-1">{num}</text>
  <text class="sans" x="{x + 24}" y="110" font-size="16" font-weight="600" fill="{t['fg']}">{label}</text>
  <text class="sans" x="{x + 24}" y="130" font-size="13.5" fill="{t['muted']}">{sub}</text>
</g>""")
    return svg(w, h, "".join(parts), t)


# ---------------------------------------------------------------- principles
def code_line(tokens, t):
    out = []
    for txt, kind in tokens:
        color = {"kw": t["kw"], "str": t["str"], "com": t["com"], "fn": t["fn"],
                 "num": t["num"], "": t["fg"]}[kind]
        out.append(f'<tspan fill="{color}">{esc(txt)}</tspan>')
    return "".join(out)


def principles(t):
    rows = [
        ("01", "Concurrency",
         "Concurrency only gets real when two people try to buy the last item at the same "
         "time. That can't be decided later: either there is an explicit lock and transaction, "
         "or the bug shows up in production on a Saturday.",
         [[("UPDATE ", "kw"), ("stock ", ""), ("SET ", "kw"), ("qty = qty - ", ""), ("1", "num")],
          [("WHERE ", "kw"), ("sku = $1 ", ""), ("AND ", "kw"), ("qty > ", ""), ("0", "num"), (";", "")],
          [("-- 0 rows: sold out", "com")]]),
        ("02", "Domain",
         "I keep each business rule close to whoever understands it. Scattered across "
         "controllers, it turns into something nobody can explain, me included. Messaging "
         "follows the same logic: whoever publishes an event doesn't need to know who listens.",
         [[("await ", "kw"), ("bus.", ""), ("publish", "fn"), ("(", "")],
          [("    ", ""), ('"order.created"', "str"), (", event)", "")],
          [("# who listens is not my problem", "com")]]),
        ("03", "Verification",
         "Agents write code faster than I can review it, and better prompts don't fix that. "
         "That's why I started JevGuard.",
         [[("verdict ", ""), ("= ", "kw"), ("gate", "fn"), ("(diff, rules)", "")],
          [("# PASS · WARN · FAIL, decided locally", "com")]]),
    ]
    w = 1000
    y = 0
    parts = []
    for i, (num, title, text, code) in enumerate(rows):
        tl = wrap(text, 62)
        rh = max(118, 44 + len(tl) * 22)
        cbh = 22 + len(code) * 21
        parts.append(f"""
<g class="in" {delay(i, 0, .15)}>
  <rect x=".5" y="{y + .5}" width="{w - 1}" height="{rh - 1}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
  <rect x=".5" y="{y + 18}" width="3" height="{rh - 36}" rx="1.5" fill="url(#accentV)"/>
  <text class="mono" x="32" y="{y + 44}" font-size="13" fill="{t['a2']}">{num}</text>
  <text class="sans" x="32" y="{y + 72}" font-size="21" font-weight="700" fill="{t['fg']}">{title}</text>
  {''.join(f'<text class="sans" x="212" y="{y + 40 + j * 22}" font-size="14.5" fill="{t["muted"]}">{esc(l)}</text>' for j, l in enumerate(tl))}
  <rect x="660" y="{y + (rh - cbh) / 2}" width="316" height="{cbh}" rx="10" fill="{t['code']}" stroke="{t['border']}"/>
  {''.join(f'<text class="mono" x="678" y="{y + (rh - cbh) / 2 + 26 + j * 21}" font-size="13" xml:space="preserve">{code_line(c, t)}</text>' for j, c in enumerate(code))}
</g>""")
        y += rh + 14
    return svg(w, y - 14, "".join(parts), t)


# ---------------------------------------------------------------- project cards
LANG = {"TypeScript": "#3178c6", "Rust": "#dea584", "Python": "#3572A5"}
REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 "
             "0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 "
             "0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a"
             ".25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z")

PROJECTS = [
    ("jevguard", "JevGuard", "Semantic policy engine for coding agents",
     "Checks the diff a coding agent just produced against your repository's policies. Each "
     "rule gets a semantic judgment, and a local deterministic gate returns PASS, WARN or FAIL.",
     ["typescript", "cli", "policy-engine"], "TypeScript"),
    ("xemnas", "xemnas", "Engineering-decision memory for coding agents",
     "Local desktop app that turns the decisions made in agent sessions into a versioned, "
     "evidence-backed project memory, and feeds it back to the agent as context.",
     ["rust", "gpui", "sqlite", "mcp"], "Rust"),
    ("prisma", "PRISMA", "Academic platform for UNIRIO",
     "Academic projects imported from SIE, institutional sign-in with Google, access and "
     "refresh tokens in Redis, and semantic recommendations on top of search.",
     ["python", "fastapi", "redis", "rag"], "Python"),
    ("self-checkout", "self-checkout-monolith", "Table-side self-checkout",
     "Anonymous per-table cart in Redis, idempotent Stripe checkout, async password reset "
     "with an SMTP worker, and per-product caching.",
     ["fastapi", "redis", "rabbitmq", "stripe"], "Python"),
    ("subscription", "subscription-monolith", "Subscription management",
     "Business rules split by domain, relational persistence and asynchronous communication "
     "between services.",
     ["fastapi", "postgresql", "rabbitmq"], "Python"),
    ("fastapi-template", "FastAPI-Template", "Production-ready API starter",
     "Modular structure, per-environment configuration and a docker-compose setup ready "
     "to run.",
     ["fastapi", "docker", "postgresql"], "Python"),
]


def card(p, t):
    _, name, tagline, desc, tags, lang = p
    w, h = 490, 230
    dl = wrap(desc, 62)[:3]
    tag_svg, x = [], 28
    for tag in tags:
        tw = 18 + len(tag) * 7.4
        tag_svg.append(
            f'<rect x="{x}" y="186" width="{tw:.0f}" height="24" rx="12" fill="{t["faint"]}"/>'
            f'<text class="mono" x="{x + tw / 2:.0f}" y="202" font-size="12" fill="{t["fg"]}" '
            f'text-anchor="middle">{tag}</text>'
        )
        x += tw + 8
    body = f"""
<g class="in">
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
<rect x=".5" y="20" width="3" height="{h - 40}" rx="1.5" fill="url(#accentV)"/>
<path transform="translate(28 24)" fill="{t['muted']}" d="{REPO_ICON}"/>
<text class="mono" x="52" y="37" font-size="13" fill="{t['muted']}">pablozr / <tspan fill="{t['fg']}">{name}</tspan></text>
<circle cx="{w - 28 - len(lang) * 7.3 - 12}" cy="32" r="6" fill="{LANG[lang]}"/>
<text class="sans" x="{w - 28}" y="37" font-size="13" fill="{t['muted']}" text-anchor="end">{lang}</text>
<text class="sans" x="28" y="80" font-size="23" font-weight="700" fill="{t['fg']}" letter-spacing="-.4">{esc(name)}</text>
<text class="sans" x="28" y="106" font-size="14.5" font-weight="600" fill="url(#accent)">{esc(tagline)}</text>
{''.join(f'<text class="sans" x="28" y="{134 + i * 19}" font-size="13.5" fill="{t["muted"]}">{esc(l)}</text>' for i, l in enumerate(dl))}
{''.join(tag_svg)}
</g>"""
    return svg(w, h, body, t)


# ---------------------------------------------------------------- stack
STACK = [
    ("backend/", ["python", "fastapi", "java", "spring", "go", "rust"]),
    ("frontend/", ["typescript", "angular", "react", "nextjs", "vite", "javascript"]),
    ("data &amp; infra/", ["postgresql", "mongodb", "redis", "rabbitmq", "docker", "bun"]),
]
TITLES = {"java": "Java"}


def stack(t):
    w = 1000
    rows = len(STACK) + 1
    h = 30 + rows * 58
    parts = []
    for r, (label, items) in enumerate(STACK):
        y = 26 + r * 58
        parts.append(f'<text class="mono in" {delay(r)} x="28" y="{y + 26}" font-size="14" fill="{t["a2"]}">{label}</text>')
        x = 200
        for i, k in enumerate(items):
            title = TITLES.get(k, ICONS[k]["title"])
            cw = 56 + len(title) * 8.6
            parts.append(f"""
<g class="in" {delay(r * 6 + i, .1, .04)}>
  <rect x="{x}" y="{y}" width="{cw:.0f}" height="40" rx="10" fill="{t['card']}" stroke="{t['border']}"/>
  {icon(k, x + 14, y + 10, 20, t)}
  <text class="sans" x="{x + 44}" y="{y + 25.5}" font-size="14" font-weight="500" fill="{t['fg']}">{title}</text>
</g>""")
            x += cw + 10
    y = 26 + len(STACK) * 58
    parts.append(f'<text class="mono in" {delay(3)} x="28" y="{y + 26}" font-size="14" fill="{t["a2"]}">also/</text>')
    x = 200
    for item in ["REST APIs", "ERP integration", "WebRTC", "SSO", "Server Actions", "Phaser", "Bun tests"]:
        cw = 26 + len(item) * 7.6
        parts.append(
            f'<g class="in" {delay(3, .2)}><rect x="{x}" y="{y + 6}" width="{cw:.0f}" height="28" rx="14" '
            f'fill="{t["faint"]}"/><text class="sans" x="{x + cw / 2:.0f}" y="{y + 25}" font-size="13" '
            f'fill="{t["fg"]}" text-anchor="middle">{item}</text></g>'
        )
        x += cw + 8
    return svg(w, h, "".join(parts), t)


# ---------------------------------------------------------------- languages
LANGS = [
    ("TypeScript", 49.8, "#3178c6"), ("Python", 20.7, "#3572A5"), ("Java", 8.4, "#b07219"),
    ("HTML", 6.6, "#e34c26"), ("SCSS", 5.6, "#c6538c"), ("JavaScript", 4.3, "#f1e05a"),
    ("CSS", 3.7, "#663399"),
]


def languages(t):
    w, h = 1000, 140
    total = sum(p for _, p, _ in LANGS)
    other = round(100 - total, 1)
    bx, bw = 28, w - 56
    segs, x = [], bx
    for _, p, c in LANGS + [("Other", other, t["muted"])]:
        sw = bw * p / 100
        segs.append(f'<rect x="{x:.1f}" y="62" width="{max(sw - 2, 1):.1f}" height="10" fill="{c}"/>')
        x += sw
    legend, x = [], 28
    for name, p, c in LANGS + [("Other", other, t["muted"])]:
        legend.append(
            f'<circle cx="{x + 5}" cy="104" r="5" fill="{c}"/>'
            f'<text class="sans" x="{x + 16}" y="109" font-size="13.5" fill="{t["fg"]}">{name} '
            f'<tspan fill="{t["muted"]}">{p:.1f}%</tspan></text>'
        )
        x += 30 + len(f"{name} {p:.1f}%") * 7.6
    body = f"""
<g class="in">
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
<text class="mono" x="28" y="38" font-size="13.5" fill="{t['a2']}">$ linguist --public --no-forks <tspan fill="{t['muted']}"># code volume across 42 public repositories</tspan></text>
<clipPath id="bar"><rect x="{bx}" y="62" width="{bw}" height="10" rx="5"/></clipPath>
<g clip-path="url(#bar)">{''.join(segs)}</g>
{''.join(legend)}
</g>"""
    return svg(w, h, body, t)


# ---------------------------------------------------------------- footer
def footer(t):
    w, h = 1000, 90
    body = f"""
<rect x="200" y="20" width="600" height="1.5" fill="url(#fade)"/>
<text class="mono in" x="{w / 2}" y="62" font-size="14" fill="{t['muted']}" text-anchor="middle" letter-spacing="2">close the world, open the n<tspan fill="url(#accent)" font-weight="700">E</tspan>xt</text>
"""
    extra = f"""
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['a1']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{t['a1']}"/>
    <stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/>
  </linearGradient>"""
    return svg(w, h, body, t, extra)


def main():
    os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "contact"), exist_ok=True)
    for mode, t in THEMES.items():
        files = {
            f"header-{mode}.svg": header(t),
            f"stats-{mode}.svg": stats(t),
            f"principles-{mode}.svg": principles(t),
            f"stack-{mode}.svg": stack(t),
            f"languages-{mode}.svg": languages(t),
            f"footer-{mode}.svg": footer(t),
        }
        for kind in ("linkedin", "email", "github"):
            files[f"contact/{kind}-{mode}.svg"] = contact(kind, t)
        for p in PROJECTS:
            files[f"projects/{p[0]}-{mode}.svg"] = card(p, t)
        for path, content in files.items():
            with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
                f.write(content)
    print("assets written to", OUT)


if __name__ == "__main__":
    main()
