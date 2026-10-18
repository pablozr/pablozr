#!/usr/bin/env python3
"""
Generates every SVG used by the profile README, in a dark and a light variant.

Run:  python3 scripts/gen_assets.py     # writes to ./assets

Direction: a technical datasheet. Transparent backgrounds, 1px rules, mono
labels, one signal color used sparingly. Every image is drawn on a 1000px wide
canvas that GitHub scales down to about 830px, so font sizes here are set a
little above the size they should read at.

Constraints:
  - An SVG served through <img> cannot load webfonts: system font stacks only.
  - GitHub strips <script> but keeps <style>.
  - Brand icons come from simple-icons (CC0), vendored in scripts/icons.json,
    and are drawn in the text color, never in brand colors.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
ICONS = json.load(open(os.path.join(ROOT, "scripts", "icons.json"), encoding="utf-8"))

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
W = 1000

THEMES = {
    "dark": dict(fg="#e6e6e3", muted="#9aa0a8", faint="#646b75", rule="#30363d", signal="#ff6a3d"),
    "light": dict(fg="#16181d", muted="#555c66", faint="#8c939d", rule="#d0d7de", signal="#d9480f"),
}

STYLE = """<style>
  .s { font-family: %s; }
  .m { font-family: %s; }
</style>""" % (SANS, MONO)


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
    return lines + [cur] if cur else lines


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'fill="none">\n{STYLE}\n{body}\n</svg>\n'
    )


def text(x, y, s, t, size=13, color="fg", cls="s", anchor="start", weight=400, ls=0, raw=False):
    c = t.get(color, color)
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight != 400 else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{c}"{a}{w}{l}>{s if raw else esc(s)}</text>'


def hline(x1, x2, y, t, color="rule", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t[color]}" stroke-width="1"{d}/>'


def vline(x, y1, y2, t, color="rule"):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{t[color]}" stroke-width="1"/>'


def icon(name, x, y, size, color):
    s = size / 24
    return f'<path transform="translate({x} {y}) scale({s})" fill="{color}" d="{ICONS[name]["path"]}"/>'


def envelope(x, y, size, color):
    s = size / 24
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{color}" stroke-width="2" '
            f'stroke-linejoin="round" fill="none"><rect x="2" y="4.5" width="20" height="15" rx="1.5"/>'
            f'<path d="M3 6l9 7 9-7"/></g>')


# ---------------------------------------------------------------- header
def header(t):
    p = []
    p.append(text(0, 18, "PF-01 · PROFILE · REV. 2026.10", t, 13, "muted", "m", ls=1.5))
    p.append(text(W, 18, "RIO DE JANEIRO  22.9068°S  43.1729°W", t, 13, "muted", "m", "end", ls=1.5))
    p.append(hline(0, W, 34, t))
    p.append(text(-4, 122, "Pablo Farina", t, 74, "fg", "s", weight=600, ls=-3))
    p.append(text(0, 166, "Backend engineer.", t, 21, "fg", "s", weight=500))
    p.append(text(0, 196, "Concurrency, architecture and", t, 21, "muted", "s"))
    p.append(text(0, 224, "coding-agent verification.", t, 21, "muted", "s"))
    spec = [
        ("role", "backend engineer"),
        ("at", "bagaggio · dev intern"),
        ("school", "unirio · information systems"),
        ("shipped", "200+ stores · 10+ projects"),
        ("commits", "605 in 12 mo · 21 repos"),
    ]
    sx = 570
    for i, (k, v) in enumerate(spec):
        y = 82 + i * 34
        p.append(text(sx, y, k, t, 15, "muted", "m"))
        kw, vw = len(k) * 9.05, len(v) * 9.05
        p.append(hline(sx + kw + 10, W - vw - 10, y - 4, t, "faint", "1 4"))
        p.append(text(W, y, v, t, 15, "fg", "m", "end"))
    p.append(hline(0, W, 252, t))
    return svg(W, 256, "\n".join(p))


# ---------------------------------------------------------------- social buttons
SOCIAL = {
    "linkedin": ("LinkedIn", "in/pablo-de-araujo-farina"),
    "email": ("Email", "pablo.farina28@outlook.com"),
    "github": ("GitHub", "github.com/pablozr"),
}


def social(kind, t):
    w, h = 340, 76
    title, sub = SOCIAL[kind]
    ic = envelope(22, 25, 26, t["fg"]) if kind == "email" else icon(kind, 22, 25, 26, t["fg"])
    p = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="3" stroke="{t["rule"]}" stroke-width="1"/>',
         f'<rect x=".5" y=".5" width="3" height="{h - 1}" fill="{t["signal"]}"/>',
         ic,
         text(66, 34, title, t, 19, "fg", "s", weight=600),
         text(66, 56, sub, t, 13.5, "muted", "m"),
         text(w - 18, 45, "↗", t, 20, "signal", "m", "end")]
    return svg(w, h, "\n".join(p))


# ---------------------------------------------------------------- section heading
def heading(num, title, note, t):
    p = [text(0, 32, f"§{num:02d}", t, 15, "signal", "m", ls=1),
         text(56, 33, title, t, 25, "fg", "s", weight=600, ls=-.4),
         text(W, 32, note, t, 14, "muted", "m", "end", ls=.5),
         hline(0, W, 50, t)]
    return svg(W, 54, "\n".join(p))


# ---------------------------------------------------------------- principles
PRINCIPLES = [
    ("Concurrency",
     "Concurrency only gets real when two people try to buy the last item at the same time. "
     "That can't be decided later: either there is an explicit lock and transaction, or the "
     "bug shows up in production on a Saturday.",
     ["UPDATE stock SET qty = qty - 1", " WHERE sku = $1 AND qty > 0;", "-- 0 rows: sold out"]),
    ("Domain",
     "I keep each business rule close to whoever understands it. Scattered across "
     "controllers, it turns into something nobody can explain, me included. Messaging "
     "follows the same logic: whoever publishes an event doesn't need to know who listens.",
     ['bus.publish("order.created", e)', "# who listens is not my problem"]),
    ("Verification",
     "Agents write code faster than I can review it, and better prompts don't fix that. "
     "That's why I started JevGuard.",
     ["verdict = gate(diff, rules)", "# PASS | WARN | FAIL, local"]),
]


def principles(t):
    cw, gap = 300, 50
    texts = [wrap(d, 33) for _, d, _ in PRINCIPLES]
    lh = 27
    body_h = max(len(x) for x in texts) * lh
    code_y = 92 + body_h + 14
    h = code_y + 3 * 23 + 8
    p = []
    for i, ((title, _, code), lines) in enumerate(zip(PRINCIPLES, texts)):
        x = i * (cw + gap)
        if i:
            p.append(vline(x - gap / 2, 6, h - 6, t))
        p.append(text(x, 22, f"{i + 1:02d}", t, 14, "signal", "m", ls=1))
        p.append(text(x, 56, title, t, 22, "fg", "s", weight=600))
        for j, l in enumerate(lines):
            p.append(text(x, 92 + j * lh, l, t, 17.5, "muted", "s"))
        p.append(hline(x, x + cw, code_y - 20, t, "rule", "2 3"))
        for j, c in enumerate(code):
            color = "faint" if c.lstrip().startswith(("#", "--")) else "fg"
            p.append(f'<text class="m" x="{x}" y="{code_y + 6 + j * 23}" font-size="14.5" fill="{t[color]}" '
                     f'xml:space="preserve">{esc(c)}</text>')
    return svg(W, h, "\n".join(p))


# ---------------------------------------------------------------- project rows
PROJECTS = [
    ("jevguard", "JevGuard", "Semantic policy engine for coding agents. Checks the diff an agent "
     "just produced against the repository's policies; each rule gets a semantic judgment and a "
     "local deterministic gate returns PASS, WARN or FAIL.", "TypeScript", "cli · policy-engine"),
    ("xemnas", "xemnas", "Engineering-decision memory for coding agents. A local desktop app that "
     "turns the decisions made in agent sessions into a versioned, evidence-backed project memory "
     "and feeds it back to the agent as context.", "Rust", "gpui · sqlite · mcp"),
    ("prisma", "PRISMA", "Academic platform for UNIRIO. Projects imported from SIE, institutional "
     "sign-in with Google, access and refresh tokens in Redis, semantic recommendations on top of "
     "search.", "Python", "fastapi · redis · rag"),
    ("self-checkout", "self-checkout-monolith", "Table-side self-checkout. Anonymous per-table "
     "cart in Redis, idempotent Stripe checkout, async password reset with an SMTP worker, "
     "per-product caching.", "Python", "fastapi · redis · rabbitmq · stripe"),
    ("subscription", "subscription-monolith", "Subscription management. Business rules split by "
     "domain, relational persistence and asynchronous communication between services.",
     "Python", "fastapi · postgresql · rabbitmq"),
    ("fastapi-template", "FastAPI-Template", "Production-ready API starter. Modular structure, "
     "per-environment configuration and a docker-compose setup ready to run.",
     "Python", "fastapi · docker · postgresql"),
]


def project(i, proj, t, last):
    _, name, desc, lang, tags = proj
    lines = wrap(desc, 50)
    tags = tags.split(" · ")
    lh = 25
    h = max(40 + len(lines) * lh, 64 + len(tags) * 21) + 10
    p = [hline(0, W, .5, t)]
    p.append(text(0, 38, f"{i + 1:02d}", t, 14, "signal", "m", ls=1))
    p.append(text(44, 40, name, t, 23, "fg", "s", weight=600, ls=-.4))
    p.append(text(44, 66, f"pablozr/{name} <tspan fill=\"{t['signal']}\">↗</tspan>", t, 13, "faint", "m", raw=True))
    for j, l in enumerate(lines):
        p.append(text(350, 38 + j * lh, l, t, 17, "muted", "s"))
    p.append(text(W, 38, lang, t, 15, "fg", "m", "end"))
    for j, tag in enumerate(tags):
        p.append(text(W, 62 + j * 21, tag, t, 13.5, "faint", "m", "end"))
    if last:
        p.append(hline(0, W, h - .5, t))
    return svg(W, h, "\n".join(p))


# ---------------------------------------------------------------- stack + languages
STACK = [
    ("backend", ["python", "fastapi", "java", "spring", "go", "rust"]),
    ("frontend", ["typescript", "angular", "react", "nextjs", "vite", "javascript"]),
    ("data & infra", ["postgresql", "mongodb", "redis", "rabbitmq", "docker", "bun"]),
]
TITLES = {"java": "Java"}
ALSO = ["REST APIs", "ERP integration", "WebRTC", "SSO", "Server Actions", "Phaser",
        "unit tests with Bun"]
LANGS = [("TypeScript", 49.8), ("Python", 20.7), ("Java", 8.4), ("HTML", 6.6), ("SCSS", 5.6),
         ("JavaScript", 4.3), ("CSS", 3.7), ("other", 0.9)]


def stack(t):
    cw, gap = 210, 24
    p = []
    for c, (label, items) in enumerate(STACK):
        x = c * (cw + gap)
        p.append(text(x, 16, label.upper(), t, 13, "muted", "m", ls=1.5))
        p.append(hline(x, x + cw, 30, t))
        for i, k in enumerate(items):
            y = 66 + i * 36
            p.append(icon(k, x, y - 16, 19, t["fg"]))
            p.append(text(x + 32, y, TITLES.get(k, ICONS[k]["title"]), t, 18, "fg", "s"))
    x = 3 * (cw + gap)
    lw = W - x
    p.append(text(x, 16, "LANGUAGES · 42 REPOS", t, 13, "muted", "m", ls=1.5))
    p.append(hline(x, W, 30, t))
    for i, (name, pct) in enumerate(LANGS):
        y = 58 + i * 26.5
        top = i == 0
        p.append(text(x, y, name, t, 14, "fg" if top else "muted", "m"))
        p.append(text(W, y, f"{pct:.1f}", t, 14, "fg" if top else "muted", "m", "end"))
        bw = (lw - 152) * pct / LANGS[0][1]
        p.append(hline(x + 100, x + 100 + max(bw, 1), y - 5, t, "signal" if top else "faint"))
    y = 66 + 6 * 36
    p.append(hline(0, W, y, t, "rule", "2 3"))
    p.append(text(0, y + 34, "ALSO", t, 13, "muted", "m", ls=1.5))
    p.append(text(64, y + 34, " · ".join(ALSO), t, 17, "fg", "s"))
    return svg(W, y + 64, "\n".join(p))


# ---------------------------------------------------------------- footer
def footer(t):
    p = [hline(0, W, 14, t),
         text(0, 46, "close the world, open the nExt", t, 14, "muted", "m", ls=1),
         text(W, 46, "EOF", t, 14, "signal", "m", "end", ls=1.5)]
    return svg(W, 58, "\n".join(p))


SECTIONS = [
    ("about", 1, "About", "whoami"),
    ("principles", 2, "How I think", "three things I won't trade"),
    ("work", 3, "Selected work", "pinned · 6 repositories"),
    ("stack", 4, "Stack", "what I build with"),
    ("education", 5, "Education", "unirio · 2023–2027"),
]


def main():
    for sub in ("projects", "contact", "sections"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    for mode, t in THEMES.items():
        files = {
            f"header-{mode}.svg": header(t),
            f"principles-{mode}.svg": principles(t),
            f"stack-{mode}.svg": stack(t),
            f"footer-{mode}.svg": footer(t),
        }
        for kind in SOCIAL:
            files[f"contact/{kind}-{mode}.svg"] = social(kind, t)
        for key, num, title, note in SECTIONS:
            files[f"sections/{key}-{mode}.svg"] = heading(num, title, note, t)
        for i, proj in enumerate(PROJECTS):
            files[f"projects/{proj[0]}-{mode}.svg"] = project(i, proj, t, i == len(PROJECTS) - 1)
        for path, content in files.items():
            with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
                f.write(content)
    print("assets written to", OUT)


if __name__ == "__main__":
    main()
