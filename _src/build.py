#!/usr/bin/env python3
"""Builds the Danu Water website.

Edit the content in _src/content/ (sectors.json, news.json), then run:
    python3 _src/build.py
and commit the generated HTML. Folders starting with "_" are not published by GitHub Pages.
The impact explorers (/cups/, /power-bank/, /giveaways/) are hand-written pages and are not touched.
"""
import datetime, html, json, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "_src" / "content"
TODAY = datetime.date.today().isoformat()

SITE = {
    "email": "hello@danuwater.com",
    "newsletter": "/newsletter/",
    # Add the company LinkedIn page URL here to show LinkedIn links.
    "linkedin": "",
}

e = lambda s: html.escape(str(s), quote=True)
sectors = json.loads((CONTENT / "sectors.json").read_text())
news = sorted(json.loads((CONTENT / "news.json").read_text()), key=lambda n: n["date"], reverse=True)

# Every product or application, keyed by id, with the sector whose pages it lives under.
ITEMS = {}
for s in sectors:
    for it in s["items"]:
        if "ref" not in it:
            ITEMS[it["id"]] = dict(it, sector=s)


def item_url(pid):
    it = ITEMS[pid]
    return f"/sectors/{it['sector']['slug']}/{pid}/"


def resolve(it):
    if "ref" in it:
        return ITEMS[it["ref"].split("/")[1]]
    return ITEMS[it["id"]]

# ---------------------------------------------------------------- layout

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C11 10 7 15 7 20a9 9 0 0 0 18 0c0-5-4-10-9-17Z" '
        'fill="#7CC4BC"/><path d="M11 21c1.5 2.6 4 3.6 6.5 3.2" fill="none" stroke="#0D2B2E" stroke-width="2" stroke-linecap="round"/></svg>')

NAV = [("/sectors/", "Sectors", "sectors"), ("/technology/", "Technology", "technology"),
       ("/impact/", "Understand your impact", "impact"), ("/news/", "News & insights", "news"),
       ("/contact/", "Contact", "contact")]


def page(path, title, desc, body, active=""):
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    sec = "".join(f'<li><a href="/sectors/{s["slug"]}/">{e(s["name"])}</a></li>' for s in sectors)
    li = f'<li><a href="{SITE["linkedin"]}">LinkedIn</a></li>' if SITE["linkedin"] else ""
    full_title = "Danu Water" if title is None else f"{title} | Danu Water"
    doc = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="/">{LOGO}Danu Water</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="/">{LOGO}Danu Water</a>
        <p style="margin-top:.8rem;max-width:22rem">Adaptive electromembrane separation for industrial water reuse.</p>
      </div>
      <div><h2>Sectors</h2><ul class="two">{sec}</ul></div>
      <div><h2>Company</h2><ul><li><a href="/technology/">Technology</a></li><li><a href="/technology/#team">Team</a></li><li><a href="/news/">News &amp; insights</a></li><li><a href="/impact/">Understand your impact</a></li></ul></div>
      <div><h2>Get in touch</h2><ul><li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li><li><a href="{SITE["newsletter"]}">Newsletter</a></li>{li}</ul></div>
    </div>
    <p class="fine">&copy; {datetime.date.today().year} Danu Water Ltd.</p>
  </div>
</footer>
<script src="/assets/site.js"></script>
</body>
</html>
"""
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    print("wrote", out.relative_to(ROOT))


def cta_band(heading="Have a water problem we should look at?",
             text="Tell us about your site and your water, and we will tell you honestly where Danu Water fits."):
    return f"""<section class="band dark cta"><div class="wrap">
<h2>{heading}</h2><p class="lede">{text}</p>
<div class="actions"><a class="btn" href="/contact/">Talk to us</a><a class="btn ghost" href="{SITE["newsletter"]}">Get the newsletter</a></div>
</div></section>"""

# ---------------------------------------------------------------- flow diagrams
# Matches the layout of the product sheets: a main process line, with Danu Water
# products inline, as kidneys on a step, as return loops, or as optional add-ons.

W, H, GAP, PAD = 158, 58, 58, 16


def lines(x, cy, title, sub, width=19, fill_cls=""):
    t = textwrap.wrap(title, width) or [""]
    s = textwrap.wrap(sub, width + 4) if sub else []
    rows = [(l, "t") for l in t] + [(l, "s") for l in s]
    lh = 16
    y0 = cy - (len(rows) - 1) * lh / 2 + 5
    spans = "".join(f'<tspan x="{x}" y="{y0 + i * lh:.0f}" class="{c}">{e(l)}</tspan>' for i, (l, c) in enumerate(rows))
    return f'<text text-anchor="middle"{fill_cls}>{spans}</text>'


def node_svg(x, y, n, link=True, current=None):
    pid = n.get("product")
    if pid:
        it = ITEMS.get(pid)
        name = (it.get("short") or it["name"]) if it else pid
        opt = it.get("optional") if it else False
        cls = "dn-opt" if opt else "dn-prod"
        g = f'<g class="{cls}"><rect x="{x}" y="{y}" width="{W}" height="{H}" rx="8"/>{lines(x + W / 2, y + H / 2, name, n.get("sub", ""))}</g>'
        if link and it and pid != current and not pid.startswith("_"):
            g = f'<a href="{item_url(pid)}">{g}</a>'
        return g
    return f'<g class="dn-step"><rect x="{x}" y="{y}" width="{W}" height="{H}" rx="8"/>{lines(x + W / 2, y + H / 2, n["label"], n.get("sub", ""))}</g>'


def diagram(spec, uid, current=None):
    main = spec["main"]
    att = spec.get("attach", [])
    idx = {n["id"]: i for i, n in enumerate(main)}
    top_k = any(a["type"] == "kidney" and a.get("side") == "top" for a in att)
    below = [a for a in att if a["type"] in ("loop", "addon") or (a["type"] == "kidney" and a.get("side") == "bottom")]
    extra_right = any(a["type"] == "loop" and idx[a["from_after"]] == len(main) - 1 for a in att)
    row = PAD + (H + 70 if top_k else 0)
    depth = 0
    for a in below:
        d = H + 70
        if a["type"] == "addon" and a.get("then"):
            d += H + 46
        depth = max(depth, d)
    n = len(main)
    width = PAD * 2 + n * W + (n - 1) * GAP + (110 if extra_right else 0)
    height = row + H + depth + PAD
    x = lambda i: PAD + i * (W + GAP)
    m = f'marker-end="url(#m{uid})"'
    p = [f'<defs><marker id="m{uid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>']
    mid = row + H / 2
    for i in range(1, n):
        p.append(f'<path class="dl" d="M{x(i) - GAP + 2} {mid}H{x(i) - 4}" {m}/>')
    for a in att:
        t = a["type"]
        pn = {"product": a["product"], "sub": a.get("sub", "")}
        if t == "kidney":
            i = idx[a["at"]]
            bx = x(i)
            x1, x2 = bx + W * 0.36, bx + W * 0.64
            if a.get("side") == "top":
                by = row - 70 - H
                p.append(node_svg(bx, by, pn, current=current))
                p.append(f'<path class="dp" d="M{x1} {row - 2}V{by + H + 4}" {m}/><path class="dp" d="M{x2} {by + H + 2}V{row - 4}" {m}/>')
                ly = row - 32
            else:
                by = row + H + 70
                p.append(node_svg(bx, by, pn, current=current))
                p.append(f'<path class="dp" d="M{x1} {row + H + 2}V{by - 4}" {m}/><path class="dp" d="M{x2} {by - 2}V{row + H + 4}" {m}/>')
                ly = row + H + 40
            p.append(f'<text class="dlab" x="{x1 - 8}" y="{ly}" text-anchor="end">draw-off</text><text class="dlab" x="{x2 + 8}" y="{ly}">return</text>')
        elif t == "loop":
            a_i, b_i = idx[a["from_after"]], idx[a["to_before"]]
            sx = x(a_i) + W + (GAP / 2 if a_i < n - 1 else 26)
            ex = x(b_i) - GAP / 2
            by = row + H + 70
            bx = (sx + ex) / 2 - W / 2
            byc = by + H / 2
            p.append(node_svg(bx, by, pn, current=current))
            p.append(f'<path class="dp" d="M{sx} {mid}V{byc}H{bx + W + 4}" {m}/>')
            p.append(f'<path class="dp" d="M{bx - 2} {byc}H{ex}V{mid + 4}" {m}/>')
            if a_i == n - 1:
                p.append(f'<path class="dl" d="M{x(a_i) + W + 2} {mid}H{sx}"/>')
            labs = a.get("labels", ["", ""])
            p.append(f'<text class="dlab" x="{sx + 8}" y="{(mid + byc) / 2 + 12}">{e(labs[0])}</text>')
            p.append(f'<text class="dlab" x="{ex - 8}" y="{(mid + byc) / 2 + 12}" text-anchor="end">{e(labs[1])}</text>')
        elif t == "addon":
            i = idx[a["at"]]
            bx, by = x(i), row + H + 70
            p.append(f'<path class="dp dash" d="M{bx + W / 2} {row + H + 2}V{by - 4}" {m}/>')
            p.append(node_svg(bx, by, pn, current=current))
            if a.get("then"):
                ty = by + H + 46
                p.append(f'<path class="dl" d="M{bx + W / 2} {by + H + 2}V{ty - 4}" {m}/>')
                p.append(node_svg(bx, ty, {"label": a["then"]}))
    for i, nd in enumerate(main):
        p.append(node_svg(x(i), row, nd, current=current))
    label = "Process diagram: " + ", then ".join(
        (ITEMS[nd["product"]]["name"] if nd.get("product") in ITEMS else nd.get("label", "")) for nd in main)
    for a in att:
        nm = ITEMS[a["product"]]["name"] if a["product"] in ITEMS else a["product"]
        if a["type"] == "kidney":
            where = "as a kidney on " + next(nd.get("label", "") for nd in main if nd["id"] == a["at"])
        elif a["type"] == "loop":
            where = "returning water to the process"
        else:
            where = "as an optional add-on"
        label += f". {nm} {where}"
    minw = int(width * 0.85)
    return (f'<div class="diagram-scroll"><svg class="diagram" viewBox="0 0 {width:.0f} {height:.0f}" '
            f'style="max-width:{width:.0f}px;min-width:{minw}px" role="img" aria-label="{e(label)}">{"".join(p)}</svg></div>')


def legend(spec, extra=None):
    has_opt = any((a["type"] == "addon") for a in spec.get("attach", []))
    bits = ['<span class="lg"><i class="sw prod"></i>Danu Water product</span>']
    if has_opt:
        bits.append('<span class="lg"><i class="sw dash"></i>Optional or site-specific connection</span>')
    if extra:
        bits = [f'<span class="lg"><i class="sw line"></i>{e(extra)}</span>']
    return f'<p class="legend">{"".join(bits)}</p>'


def illustration(key, which):
    f = CONTENT / "illustrations" / f"{key}-{which}.svg"
    return f.read_text() if f.exists() else ""

# ---------------------------------------------------------------- pages


TAGNAMES = {"news": "News", "event": "Event", "insight": "Insight", "linkedin": "LinkedIn", "pilot": "Pilot", "funding": "Funding"}


def news_href(n):
    if n.get("link"):
        return n["link"]
    return f'/news/{n["slug"]}/' if n.get("body") else None


PILOT_VIDEO = "assets/pilot-copper-sulphate.mp4"


def pilot_video():
    """Shown on the homepage once the video file is in /assets/."""
    if not (ROOT / PILOT_VIDEO).exists():
        return ""
    poster = PILOT_VIDEO.replace(".mp4", ".jpg")
    pa = f' poster="/{poster}"' if (ROOT / poster).exists() else ""
    return f"""<div class="pilot-video">
    <video src="/{PILOT_VIDEO}"{pa} muted loop playsinline autoplay controls preload="metadata" aria-label="Danu Water pilot unit removing copper sulphate from water"></video>
    <div><h3>See it working</h3><p>Our pilot unit removing copper sulphate from water.</p><p><a href="/technology/">How it works</a></p></div>
  </div>"""


def sector_tiles():
    return "".join(f'<li><a href="/sectors/{s["slug"]}/"><h3>{e(s["name"])}</h3><p>{e(s["card"])}</p></a></li>' for s in sectors)


def home():
    hero = {"main": [{"id": "in", "label": "Water in"}, {"id": "proc", "label": "Your process"},
                     {"id": "ww", "label": "Wastewater"}, {"id": "out", "label": "Discharge", "sub": "Much less"}],
            "attach": [{"type": "loop", "product": "_danu", "sub": "Salts out, water back", "from_after": "ww", "to_before": "proc", "labels": ["wastewater", "reuse water"]}]}
    latest = [n for n in news if news_href(n)][:3]
    cards = "".join(f'<li><time datetime="{n["date"]}">{e(n["when"])}</time><h3><a href="{news_href(n)}">{e(n["title"])}</a></h3><p>{e(n["summary"])}</p></li>' for n in latest)
    body = f"""
<section class="hero"><div class="wrap">
  <h1>Industrial water, back in use</h1>
  <p class="lede">Danu Water removes the salts, hardness and metals that stop water being reused. Our adaptive electromembrane separation shifts in real time to handle the variability of industrial water, from a laundrette to a mine site.</p>
  <div class="actions"><a class="btn" href="/sectors/">Find your sector</a><a class="btn ghost" href="/technology/">How it works</a></div>
  <div class="hero-flow">{diagram(hero, "hero")}</div>
</div></section>

<section class="band"><div class="wrap">
  <h2>Find your sector</h2>
  <p class="muted measure">Each sector has its own water problems. Choose yours to see what Danu Water can do and where it fits in your process.</p>
  <ul class="tiles">{sector_tiles()}</ul>
</div></section>

<section class="band mist"><div class="wrap">
  <div class="head-row"><h2>Where we are</h2><a href="/news/">All news</a></div>
  <ol class="timeline">
    <li class="done"><time datetime="2024-10">October 2024</time><h3>Company founded</h3><p>Kyra Sedransk Campbell and Jack Ledingham start Danu Water.</p></li>
    <li class="done"><time datetime="2026-03">March 2026</time><h3>Pre-seed backed by SFC Capital</h3><p>Funding the build of our industrial pilot units.</p></li>
    <li class="done"><time datetime="2026-10">October 2026</time><h3>Pilot running at WEPA Bridgend</h3><p>Industrial-scale unit treating real paper mill water in Wales.</p></li>
    <li class="done"><time datetime="2026-10">October 2026</time><h3>Startup Battlefield 200</h3><p>Selected for TechCrunch Disrupt in San Francisco.</p></li>
    <li><span class="when">Next</span><h3>First commercial systems</h3><p>Turning pilot results into orders.</p></li>
  </ol>
  {pilot_video()}
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <h2>Why it is different</h2>
    <p>Industrial water is never the same two days running. Most treatment is designed for a fixed condition and struggles when the water changes. Our system measures what is coming in and adjusts how it runs, continuously.</p>
    <p>That makes reuse dependable enough to build a process around, and affordable enough that there is no green premium to argue about.</p>
    <p><a href="/technology/">How adaptive electromembrane separation works</a></p>
  </div>
  <ul class="proof">
    <li><strong>95%+ water recovery</strong><span>from industrial wastewater streams</span></li>
    <li><strong>70–80% less energy</strong><span>than zero liquid discharge technologies</span></li>
    <li><strong>Continuous and onsite</strong><span>a plug-and-play system, with no tankering or offsite treatment</span></li>
    <li><strong>Salts as a resource</strong><span>a small concentrate stream that can be recovered, not a large dilute waste</span></li>
  </ul>
</div></section>

<section class="band mist"><div class="wrap split">
  <div>
    <h2>Understand your impact</h2>
    <p>How much water does it take to make a reusable coffee cup? A power bank? A bag of conference giveaways? Try guessing, then see the answer and how we worked it out.</p>
    <p><a class="btn" href="/impact/">Test your guesses</a></p>
  </div>
  <div>
    <h2>Latest</h2>
    <ul class="news-cards" style="grid-template-columns:1fr">{cards}</ul>
  </div>
</div></section>
{cta_band()}
"""
    page("/", None, "Danu Water removes the salts, hardness and metals that stop industrial water being reused, using adaptive electromembrane separation.", body)


def sectors_index():
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Sectors</h1>
  <p class="lede">One adaptive platform, applied wherever salts, hardness or metals stop water being reused. Choose your sector to see what we can do and where it fits in your process.</p>
</div></section>
<section class="band"><div class="wrap">
  <ul class="tiles">{sector_tiles()}</ul>
</div></section>
{cta_band("Don't see your sector?", "If dissolved salts, hardness or metals stop you reusing water, the technology probably applies. Tell us about your stream.")}
"""
    page("/sectors/", "Sectors", "How Danu Water helps paper, textiles, tanneries, laundries, steel, mining, distilling, utilities, groundwater users and desalination plants reuse water.", body, "sectors")


def product_card(it, sector):
    fam = (it.get("family") or "Application").replace(" family", "").replace("loops", "loop")
    cls = ' class="opt"' if it.get("optional") else ""
    return (f'<li{cls}><a href="{item_url(it["id"])}"><p class="fam">{e(fam)}</p><h3>{e(it["name"])}</h3>'
            f'<p>{e(it["card"])}</p><span class="go">View {"listing" if it.get("family") else "details"}</span></a></li>')


def sector_page(s):
    items = [resolve(it) for it in s["items"]]
    branded = any(it.get("family") for it in items)
    cards = "".join(product_card(it, s) for it in items)
    others = "".join(f'<li><a href="/sectors/{x["slug"]}/">{e(x["name"])}</a></li>' for x in sectors if x is not s)
    body = f"""
<section class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/sectors/">Sectors</a> / {e(s["name"])}</p>
  <h1>{e(s["title"])}</h1>
  <p class="lede">{e(s["lede"])}</p>
</div></section>
<section class="band"><div class="wrap">
  <h2 class="small-head">Where {"each product sits" if branded else "Danu Water fits"}</h2>
  <figure class="diagram-card">{diagram(s["flow"], s["slug"])}{legend(s["flow"])}<p class="scroll-hint">Scroll sideways to see the whole process.</p></figure>
  <div class="jobs-note">
    <h3>These are jobs, not a fixed line-up</h3>
    <p>The {"products" if branded else "applications"} illustrate the jobs that are often needed in a {e(s["place"])}. In practice, we design around each site's own combination of problems. Where and how much water we take, and where we return it, is up to you. Often a single unit can do several jobs, or a pair are designed to work together.</p>
  </div>
  <ul class="products">{cards}</ul>
</div></section>
<section class="band mist"><div class="wrap">
  <h2 class="small-head">Other sectors</h2>
  <ul class="also">{others}</ul>
</div></section>
{cta_band(f"Talk to us about your {s['name'].lower().replace(' & ', ' and ')} site", "Share what you know about your water, even roughly, and we will tell you where Danu Water fits.")}
"""
    page(f"/sectors/{s['slug']}/", s["name"], s["card"], body, "sectors")


def item_page(it):
    s = it["sector"]
    fam = it.get("family") or s["name"]
    ben = "".join(f"<li>{e(b)}</li>" for b in it["benefits"])
    illus = ""
    if it.get("illus"):
        il = it["illus"]
        illus = f"""<div class="illus">
  <figure>{illustration(il["key"], "without")}<figcaption><strong class="bad">{e(il.get("without_label", "Without"))}</strong>{e(il["without"])}</figcaption></figure>
  <figure>{illustration(il["key"], "with")}<figcaption><strong class="good">With {e(it["name"])}</strong>{e(il["with"])}</figcaption></figure>
</div>"""
    addon = ""
    if it.get("addon") and it["addon"] in ITEMS:
        a = ITEMS[it["addon"]]
        addon = f'<div class="addon"><p class="fam">Add-on</p><h3><a href="{item_url(a["id"])}">{e(a["name"])}</a></h3><p>{e(a["application"])}</p></div>'
    side = illus or addon
    if illus and addon:
        side = illus + addon
    grid = ""
    if it.get("grid"):
        g = it["grid"]
        cells = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in g["items"])
        grid = f'<section class="band" style="padding-top:0"><div class="wrap"><h2 class="small-head">{e(g["title"])}</h2><ul class="cells">{cells}</ul></div></section>'
    used = [x for x in [resolve(i) for i in s["items"]] if x["id"] != it["id"]]
    more = "".join(product_card(x, s) for x in used)
    more_block = f'<h2 class="small-head" style="margin-top:3rem">More for {e(s["name"].lower())}</h2><ul class="products">{more}</ul>' if more else ""
    body = f"""
<section class="page-head light"><div class="wrap">
  <p class="crumbs"><a href="/sectors/">Sectors</a> / <a href="/sectors/{s["slug"]}/">{e(s["name"])}</a></p>
  <p class="fam">{e(fam)}</p>
  <h1>{e(it["name"])}</h1>
  <p class="tagline">{e(it["tagline"])}</p>
</div></section>
<section class="band" style="padding-top:2.5rem"><div class="wrap listing">
  <div>
    <h2 class="small-head">The problem</h2><p>{e(it["problem"])}</p>
    <h2 class="small-head">Benefits</h2><ul class="ticks">{ben}</ul>
    <h2 class="small-head">Application</h2><p>{e(it["application"])}</p>
  </div>
  <aside>{side}</aside>
</div></section>
{grid}
<section class="band mist"><div class="wrap">
  <h2 class="small-head">Where it sits in the {e(s["place"])}</h2>
  <figure class="diagram-card">{diagram(it["flow"], it["id"], current=it["id"])}{legend(it["flow"], it["flow"].get("legend"))}<p class="scroll-hint">Scroll sideways to see the whole process.</p></figure>
  <p class="footnote">Shown as a standalone job for clarity. Where and how much water is taken and returned is designed around each site, and one unit may do several jobs. Powered by Danu Water's adaptive electromembrane separation.</p>
  {more_block}
</div></section>
{cta_band(f"Could {e(it['name'])} work on your site?", "Tell us about your water and we will design around your process.")}
"""
    page(item_url(it["id"]), f'{it["name"]} | {s["name"]}', it["card"], body, "sectors")


def technology():
    spec = {"main": [{"id": "in", "label": "Incoming water", "sub": "Variable quality"},
                     {"id": "d", "product": "_danu", "sub": "Adaptive separation"},
                     {"id": "out", "label": "Water for reuse", "sub": "Salts removed"}],
            "attach": [{"type": "addon", "product": "_conc", "sub": "Concentrated salts", "at": "d"}]}
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Adaptive electromembrane separation</h1>
  <p class="lede">A dynamic system that shifts in real time to handle the variability of industrial water.</p>
</div></section>
<section class="band"><div class="wrap split">
  <div class="measure">
    <h2>How it works</h2>
    <p>Most of what stops water being reused is dissolved: salts such as sodium, chloride and sulphate, hardness from calcium and magnesium, and metals. None of it can be filtered out.</p>
    <p>Our system uses an electric field to pull those charged ions out of the water and through selective membranes. One stream comes out with them removed. The other carries them away in concentrated form.</p>
    <p>The water itself never has to be pushed through a membrane at high pressure, which is why the approach copes with water that would quickly foul reverse osmosis.</p>
  </div>
  <figure class="diagram-card">{diagram(spec, "tech")}<figcaption class="footnote" style="margin-top:.75rem">Every system splits one stream into two: water clean enough to reuse, and a small concentrate.</figcaption></figure>
</div></section>
<section class="band mist"><div class="wrap split">
  <div class="measure">
    <h2>Why adaptive matters</h2>
    <p>Industrial water changes by the hour: with production rates, products, raw materials, temperature and season. A system tuned for one condition is either over-designed or failing for much of the time.</p>
    <p>Ours monitors the incoming water and adjusts how it operates as conditions change. That keeps the output on target and the energy use down, and lets us treat only to the level each use needs.</p>
    <p>Our industrial pilot puts this to the test on real, changing mill water.</p>
  </div>
  <ul class="proof">
    <li><strong>95%+ water recovery</strong><span>from industrial wastewater streams</span></li>
    <li><strong>70–80% less energy</strong><span>than zero liquid discharge technologies</span></li>
    <li><strong>Plug-and-play</strong><span>continuous onsite operation, with minimal disruption to install</span></li>
    <li><strong>Built for messy water</strong><span>solids, scaling and variability that defeat other approaches</span></li>
  </ul>
</div></section>
<section class="band"><div class="wrap measure">
  <h2>No green premium</h2>
  <p>Industrial wastewater treatment has long been seen as technically intractable, expensive, or both. Danu Water is designed to pay for itself, through lower freshwater and discharge costs, less downtime from scaling and corrosion, and in some cases valuable products recovered from the concentrate. When the business case stands on its own, sustainability follows.</p>
</div></section>
<section class="band mist" id="team"><div class="wrap">
  <h2>Team</h2>
  <div class="people" style="margin-top:1.5rem">
    <div><h3>Kyra Sedransk Campbell</h3><p class="role">Co-founder and CEO</p><p>Formerly Professor of Chemical Engineering and a Royal Society Research Fellow. Kyra leads the business, commercial strategy and partnerships.</p></div>
    <div><h3>Jack Ledingham</h3><p class="role">Co-founder and CTO</p><p>Leads the technical build, from system design to running our industrial pilot on site.</p></div>
  </div>
  <p class="muted" style="margin-top:2rem">Backed by SFC Capital.</p>
</div></section>
{cta_band()}
"""
    page("/technology/", "Technology", "How Danu Water's adaptive electromembrane separation removes dissolved salts, hardness and metals from water, adjusting in real time.", body, "technology")


def impact():
    items = [
        ("/cups/", "Reusable coffee cups", "How much water does it take to make a reusable coffee cup?", "And how many coffees until it beats paper cups, once you count the washing up?"),
        ("/power-bank/", "Power banks", "How much water does it take to make a power bank?", "Why cheap ones can cost the planet more than you think."),
        ("/giveaways/", "Conference giveaways", "Which of these giveaways took the most water to make?", "The hidden water in a bag of freebies."),
    ]
    drop = '<svg class="drop" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C11 10 7 15 7 20a9 9 0 0 0 18 0c0-5-4-10-9-17Z" fill="var(--teal)"/></svg>'
    cards = "".join(f'<li><a href="{h}">{drop}<p class="q">{e(q)}</p><h3>{e(t)}</h3><p class="muted" style="margin:0">{e(s)}</p><span class="go">Make your guess</span></a></li>' for h, t, q, s in items)
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Understand your impact</h1>
  <p class="lede">Almost everything you own took water to make, usually far more than you would guess. Pick an object, make a guess, then see the answer and how we worked it out.</p>
</div></section>
<section class="band"><div class="wrap">
  <ul class="explorers">{cards}</ul>
</div></section>
<section class="band mist"><div class="wrap split">
  <div class="measure">
    <h2>Why a water company cares</h2>
    <p>Most of the water in these objects was used in factories: making paper and card, glass, plastics, metals and electronics. Much of it was used once and discharged.</p>
    <p>That is the water Danu Water works on. When industrial sites can clean and reuse their own water, the hidden water in everyday things goes down.</p>
    <p><a href="/sectors/">See how we help industry</a></p>
  </div>
  <div class="measure">
    <h2>Where these came from</h2>
    <p>We built these explorers for our booth at TechCrunch Disrupt 2026 in San Francisco, where visitors guessed the water footprint of objects on our table. Each page shows its numbers, assumptions and sources.</p>
    <p><a href="/news/techcrunch-disrupt-2026/">Read about TechCrunch Disrupt</a></p>
  </div>
</div></section>
{cta_band("Want to cut the water behind what you make?", "If you run an industrial site, we can help you reuse your water.")}
"""
    page("/impact/", "Understand your impact", "Guess how much water it takes to make everyday objects, then see the answer and how it was worked out.", body, "impact")


def news_index():
    used = []
    for n in news:
        for t in n["tags"]:
            if t not in used:
                used.append(t)
    order = [t for t in ["news", "pilot", "event", "funding", "insight", "linkedin"] if t in used]
    btns = '<button data-filter="all" aria-pressed="true">All</button>' + "".join(f'<button data-filter="{t}" aria-pressed="false">{TAGNAMES[t]}</button>' for t in order)
    items = ""
    for n in news:
        href = news_href(n)
        title = f'<a href="{href}">{e(n["title"])}</a>' if href else e(n["title"])
        more = ""
        if n.get("link"):
            more = f'<a class="more" href="{n["link"]}">{"Read on LinkedIn" if "linkedin" in n["tags"] else "Read more"}</a>'
        elif href:
            more = f'<a class="more" href="{href}">Read more</a>'
        tag = n["tags"][0]
        items += f'''<li class="news-item" data-tags="{" ".join(n["tags"])}">
<div class="meta"><time datetime="{n["date"]}">{e(n["when"])}</time><span class="tag{" linkedin" if tag == "linkedin" else ""}">{TAGNAMES.get(tag, tag.title())}</span></div>
<div><h3>{title}</h3><p>{e(n["summary"])}</p>{more}</div></li>'''
    follow = f'<p class="muted">More updates on <a href="{SITE["linkedin"]}">our LinkedIn page</a>.</p>' if SITE["linkedin"] else ""
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>News &amp; insights</h1>
  <p class="lede">Pilots, events and milestones, along with our thinking on industrial water. Selected LinkedIn posts appear here too.</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter by type">{btns}</div>
  <ul class="news-list">{items}</ul>
  <div style="margin-top:2rem">{follow}<p><a href="{SITE["newsletter"]}">Get the Danu Water newsletter</a></p></div>
</div></section>
"""
    page("/news/", "News & insights", "News, pilots, events and insights from Danu Water.", body, "news")
    for n in news:
        if not n.get("body") or n.get("link"):
            continue
        paras = "".join(f"<p>{e(p)}</p>" for p in n["body"])
        cta = f'<p><a class="btn" href="{n["cta"][1]}">{e(n["cta"][0])}</a></p>' if n.get("cta") else ""
        b = f"""
<section class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/news/">News &amp; insights</a></p>
  <h1>{e(n["title"])}</h1>
  <p class="lede"><time datetime="{n["date"]}">{e(n["when"])}</time></p>
</div></section>
<section class="band"><div class="wrap"><div class="article">{paras}{cta}<p style="margin-top:2.5rem"><a href="/news/">All news</a></p></div></div></section>
{cta_band()}
"""
        page(f"/news/{n['slug']}/", n["title"], n["summary"], b, "news")


def contact():
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Talk to us</h1>
  <p class="lede">We work with industrial partners on pilots and commercial systems, and we are always glad to hear about a difficult water stream.</p>
</div></section>
<section class="band"><div class="wrap split">
  <div class="measure">
    <h2>Email</h2>
    <p><a class="big-link" href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
    <p>It helps to tell us your sector, roughly how much water you use or discharge, and what stops you reusing it today. A water analysis, if you have one, is even better.</p>
  </div>
  <div class="measure">
    <h2>Stay in touch</h2>
    <p>Our newsletter covers new applications, results and events, a few times a year.</p>
    <p><a class="btn" href="{SITE["newsletter"]}">Sign up for the newsletter</a></p>
  </div>
</div></section>
"""
    page("/contact/", "Contact", "Contact Danu Water about industrial water reuse, pilots and partnerships.", body, "contact")


if __name__ == "__main__":
    # Generic nodes used in the hero and technology diagrams
    ITEMS["_danu"] = {"id": "_danu", "name": "Danu Water", "sector": sectors[0]}
    ITEMS["_conc"] = {"id": "_conc", "name": "Concentrate", "optional": True, "sector": sectors[0]}
    (ROOT / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M16 3C11 10 7 15 7 20a9 9 0 0 0 18 0c0-5-4-10-9-17Z" fill="#0B6E69"/></svg>')
    home(); sectors_index()
    for s in sectors:
        sector_page(s)
        for it in s["items"]:
            if "ref" not in it:
                item_page(ITEMS[it["id"]])
    technology(); impact(); news_index(); contact()
