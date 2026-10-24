#!/usr/bin/env python3
"""Builds the Danu Water website.

Edit the content in _src/content/*.json (or the page text below), then run:
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
    # Add the company LinkedIn page URL here to show "Follow us on LinkedIn" links.
    "linkedin": "",
}

STATUS = {
    "pilot": ("Industrial pilot", "Running, or about to run, on a real industrial site."),
    "feasibility": ("Feasibility", "Modelling and design work on real water data."),
    "exploring": ("Exploring", "Early conversations with partners about need and fit."),
}

e = lambda s: html.escape(str(s), quote=True)
industries = json.loads((CONTENT / "industries.json").read_text())
news = sorted(json.loads((CONTENT / "news.json").read_text()), key=lambda n: n["date"], reverse=True)

# ---------------------------------------------------------------- layout

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C11 10 7 15 7 20a9 9 0 0 0 18 0c0-5-4-10-9-17Z" '
        'fill="#36bdb3"/><path d="M11 21c1.5 2.6 4 3.6 6.5 3.2" fill="none" stroke="#0a1d30" stroke-width="2" stroke-linecap="round"/></svg>')

NAV = [("/industries/", "Industries", "industries"), ("/technology/", "Technology", "technology"),
       ("/impact/", "Understand your impact", "impact"), ("/news/", "News & insights", "news"),
       ("/contact/", "Contact", "contact")]


def page(path, title, desc, body, active=""):
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    ind = "".join(f'<li><a href="/industries/{i["slug"]}/">{e(i["name"])}</a></li>' for i in industries)
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
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
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
        <p style="margin-top:.8rem;max-width:22rem">Adaptive electromembrane separation for industrial wastewater reuse.</p>
      </div>
      <div><h2>Industries</h2><ul>{ind}</ul></div>
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


def status(key):
    return f'<span class="status {key}">{STATUS[key][0]}</span>'


def cta_band(heading="Have a water problem we should look at?",
             text="Tell us about your site and your water. We are looking for industrial partners for pilots and first commercial systems."):
    return f"""<section class="band dark cta"><div class="wrap">
<h2>{heading}</h2><p class="lede">{text}</p>
<div class="actions"><a class="btn" href="/contact/">Talk to us</a><a class="btn ghost" href="{SITE["newsletter"]}">Get the newsletter</a></div>
</div></section>"""

# ---------------------------------------------------------------- flow diagrams


def wrap_label(text, width=17):
    return textwrap.wrap(text, width) or [""]


def text_lines(x, cy, text, width=17, cls=""):
    lines = wrap_label(text, width)
    lh = 17
    y0 = cy - (len(lines) - 1) * lh / 2 + 5
    spans = "".join(f'<tspan x="{x}" y="{y0 + i * lh:.0f}">{e(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text text-anchor="middle"{cls}>{spans}</text>'


def box(x, y, w, h, label, kind, width=17):
    r = 10 if kind == "fl-danu" else 6
    return (f'<g class="{kind}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
            f'{text_lines(x + w / 2, y + h / 2, label, width)}</g>')


DEFS = ('<defs><marker id="a{id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>')


def flow_h(spec, uid):
    nodes = list(spec["steps"])
    nodes.insert(spec["danu"], "Danu Water")
    d = spec["danu"]
    ret = spec.get("ret")
    w, h, gap, pad = 150, 62, 46, 14
    top = 78
    extra = 0 if ret is not None or d < len(nodes) - 1 else 1
    n = len(nodes) + extra
    W = pad * 2 + n * w + (n - 1) * gap
    H = top + h + 54 + 50 + pad
    x = lambda i: pad + i * (w + gap)
    m = f'marker-end="url(#a{uid})"'
    parts = [DEFS.replace("{id}", uid)]
    for i, label in enumerate(nodes):
        parts.append(box(x(i), top, w, h, label, "fl-danu" if i == d else "fl-step"))
        if i:
            cls = "fl-line"
            parts.append(f'<path class="{cls}" d="M{x(i) - gap + 2} {top + h / 2}H{x(i) - 3}" {m}/>')
    if ret is not None:
        r = ret if ret < d else ret + 1
        x1, x2 = x(d) + w / 2, x(r) + w / 2
        parts.append(f'<path class="fl-clean" d="M{x1} {top - 2}V32H{x2}V{top - 4}" {m}/>')
        parts.append(f'<text class="fl-label clean" x="{(x1 + x2) / 2}" y="24" text-anchor="middle">{e(spec["clean"])}</text>')
    else:
        xe = x(len(nodes))
        parts.append(f'<path class="fl-clean" d="M{x(d) + w + 2} {top + h / 2}H{xe - 3}" {m}/>')
        parts.append(f'<g class="fl-out" style="--o:1"><rect x="{xe}" y="{top}" width="{w}" height="{h}" rx="6" style="stroke:var(--teal);stroke-dasharray:none;stroke-width:2"/>'
                     f'{text_lines(xe + w / 2, top + h / 2, spec["clean"], 17)}</g>')
    sx = x(d) + w / 2
    parts.append(f'<path class="fl-brine" d="M{sx} {top + h + 2}V{top + h + 50}" {m}/>')
    parts.append(f'<g class="fl-out"><rect x="{x(d) - 10}" y="{top + h + 54}" width="{w + 20}" height="44" rx="6"/>'
                 f'{text_lines(sx, top + h + 76, spec["side"], 22)}</g>')
    return f'<svg class="h" viewBox="0 0 {W} {H}" style="max-width:{W}px" role="img" aria-label="{e(alt(spec, nodes))}">{"".join(parts)}</svg>'


def flow_v(spec, uid):
    nodes = list(spec["steps"])
    nodes.insert(spec["danu"], "Danu Water")
    d = spec["danu"]
    ret = spec.get("ret")
    w, h, gap = 200, 54, 34
    left, top = 44, 10
    if ret is None and d == len(nodes) - 1:
        nodes_draw = nodes + [None]
    else:
        nodes_draw = nodes
    y = lambda i: top + i * (h + gap)
    m = f'marker-end="url(#v{uid})"'
    parts = [DEFS.replace("{id}", "v" + uid).replace('id="av', 'id="v')]
    for i, label in enumerate(nodes_draw):
        if label is None:
            parts.append(f'<g class="fl-out"><rect x="{left}" y="{y(i)}" width="{w}" height="{h}" rx="6" style="stroke:var(--teal);stroke-dasharray:none;stroke-width:2"/>'
                         f'{text_lines(left + w / 2, y(i) + h / 2, spec["clean"], 24)}</g>')
            parts.append(f'<path class="fl-clean" d="M{left + w / 2} {y(i) - gap + 2}V{y(i) - 3}" {m}/>')
            continue
        parts.append(box(left, y(i), w, h, label, "fl-danu" if i == d else "fl-step", 24))
        if i:
            parts.append(f'<path class="fl-line" d="M{left + w / 2} {y(i) - gap + 2}V{y(i) - 3}" {m}/>')
    if ret is not None:
        r = ret if ret < d else ret + 1
        rx = left + w + 34
        parts.append(f'<path class="fl-clean" d="M{left + w + 2} {y(d) + h / 2}H{rx}V{y(r) + h / 2}H{left + w + 4}" {m}/>')
        cy = (y(d) + y(r)) / 2 + h / 2
        parts.append(f'<text class="fl-label clean" transform="translate({rx + 16} {cy}) rotate(90)" text-anchor="middle">{e(spec["clean"])}</text>')
    bottom = y(len(nodes_draw)) + 6
    parts.append(f'<path class="fl-brine" d="M{left - 2} {y(d) + h / 2}H16V{bottom + 22}H{left - 4}" {m}/>')
    parts.append(f'<g class="fl-out"><rect x="{left}" y="{bottom}" width="{w}" height="44" rx="6"/>'
                 f'{text_lines(left + w / 2, bottom + 22, spec["side"], 26)}</g>')
    H = bottom + 54
    W = left + w + 64
    return f'<svg class="v" viewBox="0 0 {W} {H}" role="img" aria-label="{e(alt(spec, nodes))}">{"".join(parts)}</svg>'


def alt(spec, nodes):
    s = "Process flow: " + ", then ".join(nodes) + ". "
    if spec.get("ret") is not None:
        s += f"Danu Water sends {spec['clean'].lower()} to {spec['steps'][spec['ret']]}. "
    else:
        s += f"Danu Water produces {spec['clean'].lower()}. "
    return s + f"A side stream carries {spec['side'].lower()}."


def flow(spec, uid, caption=True):
    cap = f'<figcaption>{e(spec["caption"])}</figcaption>' if caption and spec.get("caption") else ""
    return f'<figure class="flow">{flow_h(spec, uid)}{flow_v(spec, uid)}{cap}</figure>'

# ---------------------------------------------------------------- pages


def news_meta(n):
    upcoming = n["date"] > TODAY
    tags = "".join(f'<span class="tag{" linkedin" if t == "linkedin" else ""}">{TAGNAMES.get(t, t.title())}</span>' for t in n["tags"][:1])
    if upcoming:
        tags = '<span class="tag">Coming up</span>' + tags
    return tags


TAGNAMES = {"news": "News", "event": "Event", "insight": "Insight", "linkedin": "LinkedIn", "pilot": "Pilot", "funding": "Funding"}


def news_href(n):
    if n.get("link"):
        return n["link"]
    return f'/news/{n["slug"]}/' if n.get("body") else None


def home():
    hero_spec = {"steps": ["Fresh water", "Your process", "Wastewater"], "danu": 3, "ret": 1,
                 "clean": "Clean water back to your process", "side": "Concentrated salts, for recovery"}
    latest = [n for n in news if news_href(n)][:3]
    cards = "".join(f'<li><time datetime="{n["date"]}">{e(n["when"])}</time><h3><a href="{news_href(n)}">{e(n["title"])}</a></h3><p>{e(n["summary"])}</p></li>' for n in latest)
    rows = "".join(f'''<li><a class="row" href="/industries/{i["slug"]}/"><h3>{e(i["name"])}</h3><p>{e(i["summary"])}</p>
<div class="offers">{"".join(status(o["status"]) for o in sorted(i["offerings"], key=lambda o: list(STATUS).index(o["status"]))[:1])}<span class="muted sans" style="font-size:.9rem">{len(i["offerings"])} offerings</span></div></a></li>''' for i in industries)
    body = f"""
<section class="hero"><div class="wrap">
  <h1>Industrial wastewater, back in use</h1>
  <p class="lede">Danu Water removes dissolved salts from industrial wastewater so it can go back into the process. Our adaptive electromembrane separation system shifts in real time to handle the variability of industrial water. It is now running at industrial pilot scale.</p>
  <div class="actions"><a class="btn" href="/industries/">See what it does for your industry</a><a class="btn ghost" href="/technology/">How it works</a></div>
  <div class="hero-flow">{flow(hero_spec, "hero", caption=False)}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="head-row"><h2>Where we are</h2><a href="/news/">All news</a></div>
  <ol class="timeline">
    <li class="done"><time datetime="2024-10">October 2024</time><h3>Company founded</h3><p>Kyra Sedransk Campbell and Jack Ledingham start Danu Water.</p></li>
    <li class="done"><time datetime="2026-03">March 2026</time><h3>Pre-seed backed by SFC Capital</h3><p>Funding the build of our industrial pilot units.</p></li>
    <li class="done"><time datetime="2026-10">October 2026</time><h3>Pilot running at WEPA Bridgend</h3><p>Industrial-scale unit treating real paper mill water in Wales.</p></li>
    <li><time datetime="2026-11">November 2026</time><h3>Pilot at Essity Valls</h3><p>Seven weeks on two streams at Essity's site in Catalonia.</p></li>
    <li><span class="when">Next</span><h3>First commercial systems</h3><p>Turning pilot results into orders.</p></li>
  </ol>
</div></section>

<section class="band mist"><div class="wrap">
  <div class="head-row"><div><h2>Industries</h2><p class="muted measure" style="margin:0">Each industry has its own water problem. These sheets show where Danu Water fits and how far each offering has got.</p></div><a href="/industries/">All industries</a></div>
  <ul class="industry-list">{rows}</ul>
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
    page("/", None, "Danu Water removes dissolved salts from industrial wastewater so it can be reused, using adaptive electromembrane separation. Now at industrial pilot scale.", body)


def industries_index():
    rows = ""
    for i in industries:
        offers = "".join(f'<li style="list-style:none;display:flex;gap:.75rem;flex-wrap:wrap;align-items:baseline"><a href="/industries/{i["slug"]}/#{o["id"]}" class="sans" style="font-weight:600">{e(o["name"])}</a>{status(o["status"])}</li>' for o in i["offerings"])
        rows += f'''<li style="padding:1.75rem 0;display:grid;grid-template-columns:minmax(12rem,1fr) 2fr;gap:1.5rem" class="ind-row">
<div><h3 style="margin:0 0 .4rem;font-size:1.4rem"><a href="/industries/{i["slug"]}/" style="color:inherit">{e(i["name"])}</a></h3><p class="muted" style="margin:0">{e(i["summary"])}</p></div>
<ul style="margin:0;padding:0;display:grid;gap:.6rem">{offers}<li style="list-style:none"><a href="/industries/{i["slug"]}/">Read the {e(i["name"].lower())} sheet</a></li></ul></li>'''
    legend = "".join(f'<div>{status(k)}<p>{v[1]}</p></div>' for k, v in STATUS.items())
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Industries</h1>
  <p class="lede">The same core technology solves different problems in different industries. Each information sheet sets out the water challenge, where Danu Water fits in the process, and how far each offering has got.</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="legend">{legend}</div>
  <ul class="industry-list" style="border-top:0">{rows}</ul>
  <style>@media (max-width:760px){{.ind-row{{grid-template-columns:1fr!important}}}}</style>
  <h2 style="margin-top:3.5rem;font-size:1.4rem">Also exploring</h2>
  <p class="muted measure">Conversations are under way in other sectors where salt is the barrier to reuse. If yours is one of them, we would like to hear from you.</p>
  <ul class="also"><li>Textiles and dyeing</li><li>Commercial laundries</li><li>Steel</li><li>Electronics</li><li>Chemicals</li><li>Food and drink</li><li>High-salinity desalination</li></ul>
</div></section>
{cta_band("Don't see your industry?", "If dissolved salts stop you reusing water, the technology probably applies. Tell us about your stream.")}
"""
    page("/industries/", "Industries", "Information sheets on how Danu Water helps paper and pulp, mining, distilling, and municipal and utility water users reuse water.", body, "industries")


def industry_sheet(i):
    pains = "".join(f"<li><strong>{e(a)}</strong><br>{e(b)}</li>" for a, b in i["pains"])
    facts = "".join(f"<li>{e(f)}</li>" for f in i["facts"])
    jump = "".join(f'<li><a href="#{o["id"]}">{e(o["name"])}</a></li>' for o in i["offerings"])
    offers = ""
    for o in i["offerings"]:
        ben = "".join(f"<li>{e(b)}</li>" for b in o["benefits"])
        fl = flow(o["flow"], o["id"]) if o.get("flow") else ""
        offers += f"""<article class="offer" id="{o["id"]}">
  <div class="offer-head"><h3>{e(o["name"])}</h3>{status(o["status"])}</div>
  <p class="measure" style="font-size:1.1rem">{e(o["what"])}</p>
  <div class="offer-cols">
    <div><h4>What it changes</h4><ul>{ben}</ul></div>
    <div><h4>Best suited to</h4><p>{e(o["fit"])}</p></div>
    <div><h4>Where it stands</h4><p>{e(o["status_note"])}</p></div>
  </div>
  {fl}
</article>"""
    others = "".join(f'<li><a href="/industries/{x["slug"]}/">{e(x["name"])}</a></li>' for x in industries if x is not i)
    n = len(i["offerings"])
    body = f"""
<section class="page-head"><div class="wrap">
  <p class="crumbs"><a href="/industries/">Industries</a></p>
  <h1>{e(i["title"])}</h1>
  <p class="lede">{e(i["lede"])}</p>
  <ul class="jump" aria-label="Offerings on this page">{jump}</ul>
</div></section>
<section class="band"><div class="wrap sheet-grid">
  <div>
    <h2>The challenge</h2>
    <p class="measure">{e(i["problem_intro"])}</p>
    <ul class="pain measure">{pains}</ul>
  </div>
  <aside class="facts"><h2>Progress so far</h2><ul>{facts}</ul></aside>
</div></section>
<section class="band mist"><div class="wrap">
  <h2>{"What we offer" if n > 1 else "What we offer"}</h2>
  <p class="muted measure" style="margin-bottom:2.5rem">{n} offering{"s" if n != 1 else ""} for {e(i["name"].lower())}. Each status shows how far it has got.</p>
  {offers}
</div></section>
<section class="band"><div class="wrap">
  <h2 style="font-size:1.3rem">Other industries</h2>
  <ul class="also">{others}</ul>
</div></section>
{cta_band(f"Talk to us about your {i['name'].lower().replace(' & ', ' and ')} site", "Share what you know about your water, even roughly, and we will tell you honestly whether and where Danu Water fits.")}
"""
    page(f"/industries/{i['slug']}/", i["title"], i["summary"], body, "industries")


def technology():
    spec = {"steps": ["Incoming water"], "danu": 1, "ret": None, "clean": "Low-salt water for reuse",
            "side": "Concentrated salts", "caption": "Every Danu Water system splits one stream into two: water clean enough to reuse, and a small concentrate."}
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>Adaptive electromembrane separation</h1>
  <p class="lede">A dynamic system that shifts in real time to handle the variability of industrial water.</p>
</div></section>
<section class="band"><div class="wrap split">
  <div class="measure">
    <h2>How it works</h2>
    <p>Most of what stops wastewater being reused is dissolved salt: sodium, chloride, calcium, sulphate and more. It cannot be filtered out, because it is dissolved.</p>
    <p>Our system uses an electric field to pull those charged ions out of the water and through selective membranes. One stream comes out with the salts removed. The other carries them away in concentrated form.</p>
    <p>The water itself never has to be pushed through a membrane at high pressure, which is why the approach copes with water that would quickly foul reverse osmosis.</p>
  </div>
  <div>{flow(spec, "tech")}</div>
</div></section>
<section class="band mist"><div class="wrap split">
  <div class="measure">
    <h2>Why adaptive matters</h2>
    <p>Industrial water changes by the hour: with production rates, products, raw materials, temperature and season. A system tuned for one condition is either over-designed or failing for much of the time.</p>
    <p>Ours monitors the incoming water and adjusts how it operates as conditions change. That keeps the output on target and the energy use down, without an operator chasing it.</p>
    <p>Our industrial pilots test this directly, running the same streams at fixed and at dynamic setpoints.</p>
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
    <div><h3>Jack Ledingham</h3><p class="role">Co-founder and CTO</p><p>Leads the technical build, from system design to running our industrial pilots on site.</p></div>
  </div>
  <p class="muted" style="margin-top:2rem">Backed by SFC Capital.</p>
</div></section>
{cta_band()}
"""
    page("/technology/", "Technology", "How Danu Water's adaptive electromembrane separation removes dissolved salts from industrial wastewater, adjusting in real time to changing water.", body, "technology")


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
    <p>That is the water Danu Water works on. When industrial sites can clean and reuse their own wastewater, the hidden water in everyday things goes down.</p>
    <p><a href="/industries/">See how we help industry</a></p>
  </div>
  <div class="measure">
    <h2>Where these came from</h2>
    <p>We built these explorers for our booth at TechCrunch Disrupt 2026 in San Francisco, where visitors guessed the water footprint of objects on our table. Each page shows its numbers, assumptions and sources.</p>
    <p><a href="/news/techcrunch-disrupt-2026/">Read about TechCrunch Disrupt</a></p>
  </div>
</div></section>
{cta_band("Want to cut the water behind what you make?", "If you run an industrial site, we can help you reuse your wastewater.")}
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
        items += f'''<li class="news-item" data-tags="{" ".join(n["tags"])}">
<div class="meta"><time datetime="{n["date"]}">{e(n["when"])}</time>{news_meta(n)}</div>
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
  <p class="lede">We are working with industrial partners on pilots and first commercial systems, and we are always glad to hear about a difficult water stream.</p>
</div></section>
<section class="band"><div class="wrap split">
  <div class="measure">
    <h2>Email</h2>
    <p><a class="sans" style="font-size:1.3rem;font-weight:700" href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
    <p>It helps to tell us your industry, roughly how much water you use or discharge, and what stops you reusing it today. A water analysis, if you have one, is even better.</p>
  </div>
  <div class="measure">
    <h2>Stay in touch</h2>
    <p>Our newsletter covers pilot results, new applications and events, a few times a year.</p>
    <p><a class="btn" href="{SITE["newsletter"]}">Sign up for the newsletter</a></p>
  </div>
</div></section>
"""
    page("/contact/", "Contact", "Contact Danu Water about industrial wastewater reuse, pilots and partnerships.", body, "contact")


if __name__ == "__main__":
    (ROOT / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M16 3C11 10 7 15 7 20a9 9 0 0 0 18 0c0-5-4-10-9-17Z" fill="#1f9e96"/></svg>')
    home(); industries_index()
    for i in industries:
        industry_sheet(i)
    technology(); impact(); news_index(); contact()
