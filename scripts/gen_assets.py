#!/usr/bin/env python3
"""
Generates every SVG used by the profile README, in a dark and a light variant.

Run:  python3 scripts/gen_assets.py     # writes to ./assets

Direction: a technical datasheet. Transparent backgrounds, 1px rules, mono
labels, one signal color used sparingly. The header figure is a WaveDrom-style
timing diagram of the race the profile talks about: two requests, one item
left, a row lock in between.

Constraints:
  - An SVG served through <img> cannot load webfonts: system font stacks only.
  - GitHub strips <script> but keeps <style>; motion is CSS inside the file and
    stops under prefers-reduced-motion.
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
    "dark": dict(fg="#e6e6e3", muted="#8b9098", faint="#5b616b", rule="#30363d", signal="#ff6a3d"),
    "light": dict(fg="#16181d", muted="#5f6670", faint="#9aa1ab", rule="#d0d7de", signal="#d9480f"),
}

STYLE = """<style>
  .s { font-family: %s; }
  .m { font-family: %s; }
  .scan { animation: scan 11s linear infinite; }
  @keyframes scan { from { transform: translateX(0); } to { transform: translateX(840px); } }
  @media (prefers-reduced-motion: reduce) { .scan { animation: none; opacity: 0; } }
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


def svg(w, h, body, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'fill="none">\n{STYLE}\n<defs>{extra_defs}</defs>\n{body}\n</svg>\n'
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


# ---------------------------------------------------------------- header
U, X0 = 70, 120  # one time slot in px, x of t0


def tx(slot):
    return X0 + slot * U


def bus(a, b, yc, label, t, hatch=False, color="fg"):
    """A WaveDrom bus segment between slots a and b."""
    x1, x2, h, s = tx(a), tx(b), 10, 5
    pts = f"{x1},{yc} {x1 + s},{yc - h} {x2 - s},{yc - h} {x2},{yc} {x2 - s},{yc + h} {x1 + s},{yc + h}"
    fill = 'fill="url(#hatch)"' if hatch else 'fill="none"'
    out = f'<polygon points="{pts}" {fill} stroke="{t[color] if color != "fg" else t["faint"]}" stroke-width="1"/>'
    if label:
        out += text((x1 + x2) / 2, yc + 4, label, t, 11, color if color != "fg" else "fg", "m", "middle")
    return out


def idle(a, b, yc, t):
    return hline(tx(a), tx(b), yc, t, "faint", "2 3")


def header(t):
    h = 452
    lanes = {"T1": 268, "T2": 308, "row lock": 348, "stock": 388}
    p = []
    # meta row
    p.append(text(0, 16, "PF-01 · PROFILE · REV. 2026.10", t, 11, "muted", "m", ls=1.5))
    p.append(text(W, 16, "RIO DE JANEIRO  22.9068°S  43.1729°W", t, 11, "muted", "m", "end", ls=1.5))
    p.append(hline(0, W, 30, t))
    # identity
    p.append(text(-3, 108, "Pablo Farina", t, 62, "fg", "s", weight=600, ls=-2.5))
    p.append(text(0, 146, "Backend engineer.", t, 17, "fg", "s", weight=500))
    p.append(text(0, 172, "Concurrency, architecture and coding-agent verification.", t, 17, "muted", "s"))
    # spec block with leaders
    spec = [
        ("role", "backend engineer"),
        ("at", "bagaggio · dev intern"),
        ("school", "unirio · information systems"),
        ("shipped", "200+ stores · 10+ projects"),
        ("commits", "605 in 12 mo · 21 repos"),
    ]
    sx = 640
    for i, (k, v) in enumerate(spec):
        y = 70 + i * 24
        p.append(text(sx, y, k, t, 12, "muted", "m"))
        kw, vw = len(k) * 7.25, len(v) * 7.25
        p.append(hline(sx + kw + 8, W - vw - 8, y - 3, t, "faint", "1 3"))
        p.append(text(W, y, v, t, 12, "fg", "m", "end"))
    p.append(hline(0, W, 206, t))
    # figure
    p.append(text(0, 230, "FIG. 1", t, 11, "signal", "m", ls=1.5))
    p.append(text(56, 230, "two requests, one item left", t, 11, "muted", "m", ls=.5))
    p.append(text(W, 230, "postgres · read committed", t, 11, "muted", "m", "end", ls=.5))
    # clock ticks
    for i in range(13):
        x = tx(i)
        p.append(f'<line x1="{x}" y1="244" x2="{x}" y2="{252 if i % 2 == 0 else 249}" stroke="{t["faint"]}"/>')
        p.append(vline(x, 256, 404, t, "rule").replace('stroke-width="1"', 'stroke-width="1" stroke-dasharray="1 5"'))
        if i % 2 == 0 and i < 12:
            p.append(text(x + 3, 252, f"t{i}", t, 9, "faint", "m"))
    for name, y in lanes.items():
        p.append(text(X0 - 20, y + 4, name, t, 12, "muted", "m", "end"))
    # T1
    y = lanes["T1"]
    p += [bus(0, 1, y, "BEGIN", t), bus(1, 4, y, "SELECT … FOR UPDATE", t),
          bus(4, 6, y, "UPDATE qty = 0", t), bus(6, 7, y, "COMMIT", t), idle(7, 12, y, t)]
    # T2
    y = lanes["T2"]
    p += [idle(0, 1, y, t), bus(1, 2, y, "BEGIN", t), bus(2, 7, y, "", t, hatch=True),
          text((tx(2) + tx(7)) / 2, y + 4, "UPDATE … blocked on row lock", t, 11, "muted", "m", "middle"),
          bus(7, 9, y, "0 rows → sold out", t, color="signal"), bus(9, 10, y, "END", t), idle(10, 12, y, t)]
    # lock signal
    y = lanes["row lock"]
    lo, hi = y + 9, y - 9
    p.append(
        f'<polyline points="{tx(0)},{lo} {tx(1)},{lo} {tx(1) + 4},{hi} {tx(7)},{hi} {tx(7) + 4},{lo} {tx(12)},{lo}" '
        f'stroke="{t["signal"]}" stroke-width="1.5" fill="none"/>'
    )
    p.append(text(tx(1) + 10, hi - 5, "held by T1", t, 10, "signal", "m"))
    # stock
    y = lanes["stock"]
    p += [bus(0, 7, y, "1", t), bus(7, 12, y, "0", t)]
    # playhead
    p.append(
        f'<g class="scan"><line x1="{X0}" y1="240" x2="{X0}" y2="404" stroke="{t["signal"]}" '
        f'stroke-width="1" opacity=".7"/><path d="M{X0 - 4} 240h8l-4 6z" fill="{t["signal"]}"/></g>'
    )
    p.append(hline(0, W, 420, t))
    p.append(text(0, 440, "T2 waits for T1's commit, then its guarded UPDATE matches 0 rows. No oversell, "
                          "no retry loop.", t, 11, "muted", "m"))
    hatch = (f'<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" '
             f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{t["rule"]}" '
             f'stroke-width="2"/></pattern>')
    return svg(W, h, "\n".join(p), hatch)


# ---------------------------------------------------------------- section heading
def heading(num, title, note, t):
    h = 44
    p = [text(0, 26, f"§{num:02d}", t, 12, "signal", "m", ls=1),
         text(44, 27, title, t, 19, "fg", "s", weight=600, ls=-.3),
         text(W, 26, note, t, 11, "muted", "m", "end", ls=.5),
         hline(0, W, 40, t)]
    return svg(W, h, "\n".join(p))


# ---------------------------------------------------------------- contact link
def link(label, t):
    w, h = int(len(label) * 7.8) + 18, 24
    p = [text(0, 16, label, t, 13, "fg", "m"),
         text(w, 16, "↗", t, 13, "signal", "m", "end")]
    return svg(w, h, "\n".join(p))


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
     ['await bus.publish("order.created", e)', "# who listens is not my problem"]),
    ("Verification",
     "Agents write code faster than I can review it, and better prompts don't fix that. "
     "That's why I started JevGuard.",
     ["verdict = gate(diff, rules)", "# PASS | WARN | FAIL, decided locally"]),
]


def principles(t):
    cw, gap = 310, 35
    texts = [wrap(d, 40) for _, d, _ in PRINCIPLES]
    body_h = max(len(x) for x in texts) * 21
    code_y = 76 + body_h + 8
    h = code_y + 3 * 19 + 10
    p = []
    for i, ((title, _, code), lines) in enumerate(zip(PRINCIPLES, texts)):
        x = i * (cw + gap)
        if i:
            p.append(vline(x - gap / 2, 4, h - 4, t))
        p.append(text(x, 18, f"{i + 1:02d}", t, 11, "signal", "m", ls=1))
        p.append(text(x, 46, title, t, 17, "fg", "s", weight=600))
        for j, l in enumerate(lines):
            p.append(text(x, 76 + j * 21, l, t, 14, "muted", "s"))
        p.append(hline(x, x + cw, code_y - 16, t, "rule", "2 3"))
        for j, c in enumerate(code):
            color = "faint" if c.lstrip().startswith(("#", "--")) else "fg"
            p.append(f'<text class="m" x="{x}" y="{code_y + 6 + j * 19}" font-size="12" fill="{t[color]}" '
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
    lines = wrap(desc, 64)
    h = max(92, 34 + len(lines) * 20)
    p = [hline(0, W, .5, t)]
    p.append(text(0, 32, f"{i + 1:02d}", t, 11, "signal", "m", ls=1))
    p.append(text(40, 34, name, t, 19, "fg", "s", weight=600, ls=-.3))
    p.append(text(40, 56, f"pablozr/{name} <tspan fill=\"{t['signal']}\">↗</tspan>", t, 11, "faint", "m", raw=True))
    for j, l in enumerate(lines):
        p.append(text(330, 32 + j * 20, l, t, 14, "muted", "s"))
    p.append(text(W, 32, lang, t, 12, "fg", "m", "end"))
    for j, tag in enumerate(tags.split(" · ")):
        p.append(text(W, 52 + j * 17, tag, t, 11, "faint", "m", "end"))
    h = max(h, 52 + len(tags.split(" · ")) * 17 + 8)
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
ALSO = "REST APIs · ERP integration · WebRTC · SSO · Server Actions · Phaser · unit tests with Bun"
LANGS = [("TypeScript", 49.8), ("Python", 20.7), ("Java", 8.4), ("HTML", 6.6), ("SCSS", 5.6),
         ("JavaScript", 4.3), ("CSS", 3.7), ("other", 0.9)]


def stack(t):
    cw = 230
    p = []
    for c, (label, items) in enumerate(STACK):
        x = c * (cw + 20)
        p.append(text(x, 14, label.upper(), t, 11, "muted", "m", ls=1.5))
        p.append(hline(x, x + cw, 26, t))
        for i, k in enumerate(items):
            y = 54 + i * 30
            p.append(icon(k, x, y - 13, 15, t["fg"]))
            p.append(text(x + 26, y, TITLES.get(k, ICONS[k]["title"]), t, 14, "fg", "s"))
    # languages column
    x = 3 * (cw + 20)
    lw = W - x
    p.append(text(x, 14, "LANGUAGES · 42 REPOS", t, 11, "muted", "m", ls=1.5))
    p.append(hline(x, W, 26, t))
    for i, (name, pct) in enumerate(LANGS):
        y = 50 + i * 22
        p.append(text(x, y, name, t, 12, "fg" if i == 0 else "muted", "m"))
        p.append(text(W, y, f"{pct:.1f}", t, 12, "fg" if i == 0 else "muted", "m", "end"))
        bw = (lw - 130) * pct / LANGS[0][1]
        p.append(hline(x + 92, x + 92 + max(bw, 1), y - 4, t, "signal" if i == 0 else "faint"))
    y = 54 + 6 * 30 + 8
    p.append(hline(0, W, y, t, "rule", "2 3"))
    p.append(text(0, y + 26, "ALSO", t, 11, "muted", "m", ls=1.5))
    p.append(text(60, y + 26, ALSO, t, 13, "fg", "s"))
    return svg(W, y + 36, "\n".join(p))


# ---------------------------------------------------------------- footer
def footer(t):
    p = [hline(0, W, 12, t),
         text(0, 40, "close the world, open the nExt", t, 12, "muted", "m", ls=1),
         text(W, 40, "EOF", t, 12, "signal", "m", "end", ls=1.5)]
    return svg(W, 52, "\n".join(p))


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
            f"contact/linkedin-{mode}.svg": link("linkedin", t),
            f"contact/email-{mode}.svg": link("pablo.farina28@outlook.com", t),
            f"contact/github-{mode}.svg": link("github", t),
        }
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
