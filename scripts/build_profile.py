#!/usr/bin/env python3
"""Generate the three GitHub Pages profile pages using only Python's standard library."""
from datetime import datetime
from html import escape
from hashlib import sha256
import json
from pathlib import Path
import re
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/profile.json").read_text())
PAPERS = {p["id"]: p for p in DATA["publications"]}
SCHOLAR = "https://scholar.google.com/citations?user=RLjKaTwAAAAJ&hl=en"
CV = "/assets/Utkarsh_resume.pdf"
UPDATED_MONTH = datetime.strptime(DATA["updated"], "%B %d, %Y").strftime("%B %Y")
CSS_VERSION = sha256((ROOT / "assets/profile.css").read_bytes()).hexdigest()[:10]
UPDATES_VERSION = sha256((ROOT / "assets/updates.js").read_bytes()).hexdigest()[:10]


def analytics_tag():
    """Enable the public Umami tracker only once a real website ID is configured."""
    analytics = DATA.get("analytics", {})
    website_id = analytics.get("website_id")
    if not website_id:
        return ""
    # Umami website IDs are public UUIDs, never account passwords or API tokens.
    UUID(website_id)
    return (f'<script defer src="https://cloud.umami.is/script.js" '
            f'data-website-id="{escape(website_id, quote=True)}" '
            'data-domains="utkarsh4430.github.io" data-do-not-track="true" '
            'data-exclude-search="true" data-exclude-hash="true"></script>')


def event(name, **properties):
    attrs = f' data-umami-event="{escape(name, quote=True)}"'
    for key, value in properties.items():
        attrs += f' data-umami-event-{key}="{escape(value, quote=True)}"'
    return attrs


def link(url, label, attrs=""):
    return f'<a href="{escape(url, quote=True)}"{attrs}>{escape(label)}</a>'


def page(title, active, description, body, route):
    updates_script = f'<script defer src="/assets/updates.js?v={UPDATES_VERSION}"></script>' if active == 'intro' else ''
    nav = "".join(link(path, label, ' aria-current="page"' if key == active else "")
                  for key, label, path in [("intro", "Intro", "/"),
                                           ("publications", "Publications", "/publications/"),
                                           ("cv", "CV", "/cv/")])
    canonical = f"https://utkarsh4430.github.io{route}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} — Utkarsh Tyagi</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#fbfaf8">
  <meta property="og:title" content="{escape(title, quote=True)} — Utkarsh Tyagi">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://utkarsh4430.github.io/assets/IMG_4207.jpeg">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/profile.css?v={CSS_VERSION}">
{updates_script}{analytics_tag()}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="shell">
    <header class="site-header">
      <a class="brand" href="/">Utkarsh Tyagi</a>
      <nav class="site-nav" aria-label="Main navigation">{nav}</nav>
    </header>
    <main id="main">{body}</main>
    <footer class="site-footer">
      <span>Utkarsh Tyagi · San Francisco</span>
      <span>Updated {UPDATED_MONTH} · {link("mailto:utkarsht@umd.edu", "Get in touch")}</span>
    </footer>
  </div>
</body>
</html>
'''


def news_text(text):
    result = escape(text)
    for ref in re.findall(r"\{([^}]+)\}", text):
        if ref == "patent":
            anchor = link("https://patents.google.com/patent/US12505292B2/en", "U.S. Patent 12,505,292")
        else:
            paper = PAPERS[ref]
            label = paper.get("name", paper["title"].split(":")[0])
            # The accepted VDGD title has no short prefix.
            if ref == "vdgd":
                label = "VDGD"
            anchor = link(paper["url"], label, event("paper_click", paper=ref))
        result = result.replace("{" + ref + "}", anchor)
    return result


def news_rows(items):
    rows = []
    for item in items:
        month = datetime.strptime(item["month"], "%Y-%m").strftime("%b %Y")
        rows.append(f'<li class="news-item"><time datetime="{item["month"]}">{month}</time>'
                    f'<p>{news_text(item["text"])}</p></li>')
    return '<ul class="news-list">' + "\n".join(rows) + "</ul>"


intro = f'''
      <section class="hero" aria-labelledby="intro-title">
        <div class="bio">
          <p class="eyebrow">Audio &amp; multimodal AI · RL &amp; post-training</p>
          <h1 id="intro-title">Utkarsh Tyagi</h1>
          <p>I’m a <strong>Machine Learning Research Engineer at Scale AI</strong> in San Francisco.
            My research focuses on audio and multimodal AI, with an emphasis on post-training,
            reinforcement learning, and speech-to-speech models.</p>
          <p>I work on steerable speech dialogue, rubric-based learning, and evaluations of
            how models reason across audio, images, and video.</p>
          <p>I’m particularly interested in designing better learning signals and building models
            that remain reliable across natural, multi-turn interactions.</p>
          <p>Previously, I completed my M.S. in Computer Science at the University of Maryland,
            where I worked with {link("https://gamma.umd.edu/", "GAMMA Lab")},
            Prof. Dinesh Manocha, and Prof. Ramani Duraiswami.
            I’ve also worked at Atlassian and Samsung.</p>
          <div class="contact-links" aria-label="Contact and profiles">
            {link("mailto:utkarsht@umd.edu", "Email")}
            {link(SCHOLAR, "Google Scholar", event("scholar_click"))}
            {link("https://www.linkedin.com/in/utkarsh4430/", "LinkedIn")}
            {link("https://github.com/Utkarsh4430", "GitHub")}
          </div>
          <ul class="interests" aria-label="Research interests">
            <li>Speech &amp; audio</li><li>Multimodal reasoning</li><li>RL &amp; post-training</li>
          </ul>
        </div>
        <div class="hero-photo">
          <img class="portrait" src="/assets/IMG_4207.jpeg" alt="Utkarsh Tyagi" width="212" height="258">
          <p class="portrait-caption">San Francisco, California</p>
        </div>
      </section>
      <section class="news-section" aria-labelledby="news-title">
        <div class="section-heading"><h2 id="news-title">Updates</h2><span class="quiet">{DATA["news"][-1]["month"][:4]}–{DATA["news"][0]["month"][:4]}</span></div>
        <div class="news-window">
          <div class="news-scroll" id="updates-timeline" tabindex="0" role="region" aria-label="All updates, newest first. Scroll for earlier updates.">
            {news_rows(DATA["news"])}
          </div>
          <div class="news-controls">
            <button class="news-more" type="button" aria-controls="updates-timeline" hidden>
              <span class="news-more-label">Explore earlier updates</span>
              <svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="m5 8 5 5 5-5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>
      </section>
'''


def venue(p):
    result = escape(p["venue"])
    if p.get("recognition"):
        result += ' · <span class="recognition">' + escape(p["recognition"]) + "</span>"
    return result


cards = []
for p in DATA["publications"]:
    if not p.get("featured"):
        continue
    img = f'/assets/research/{p["image"]}'
    # Short card titles remain easy to scan; the full title is in the list below.
    subtitle = p["title"].split(": ", 1)[1] if ": " in p["title"] else p["title"]
    if p["id"] == "pow3r":
        subtitle = p["title"]
    cards.append(f'''
        <article class="paper-card" aria-labelledby="card-{p["id"]}">
          <a class="paper-figure" href="{img}" aria-label="View {escape(p["name"], quote=True)} figure at full size">
            <img src="{img}" alt="{escape(p["alt"], quote=True)}" width="440" height="210" loading="lazy">
          </a>
          <div class="paper-body">
            <p class="eyebrow">{escape(p["topic"])}</p>
            <h3 id="card-{p["id"]}">{link(p["url"], p["name"], event("paper_click", paper=p["id"]))}</h3>
            <p class="paper-subtitle">{escape(subtitle)}</p>
            <p class="venue">{venue(p)}</p>
            <p class="description">{escape(p["description"])}</p>
            <div class="paper-actions">{link(p["url"], "Read paper ↗", event("paper_click", paper=p["id"]))}</div>
          </div>
        </article>''')

lists = []
for year in sorted({p["year"] for p in DATA["publications"]}, reverse=True):
    entries = "\n".join(f'<li>{link(p["url"], p["title"], event("paper_click", paper=p["id"]))}<span class="venue">{venue(p)}</span></li>'
                        for p in DATA["publications"] if p["year"] == year)
    lists.append(f'<h3 class="publication-year">{year}</h3><ul class="publication-list">{entries}</ul>')

publications = f'''
      <div class="page-intro">
        <p class="eyebrow">Research</p><h1>Publications</h1>
        <p>Recent work on speech dialogue, multimodal reasoning, and learning from rubric feedback.</p>
      </div>
      <section aria-labelledby="featured-title">
        <div class="section-heading"><h2 id="featured-title">Featured work</h2><span class="quiet">Figures from the papers</span></div>
        <div class="featured-grid">{"".join(cards)}</div>
      </section>
      <section class="selected-section" aria-labelledby="selected-title">
        <h2 id="selected-title">Selected publications</h2>
        <p>Conference papers and recent preprints. Submission statuses are indicated below.</p>
        {"".join(lists)}
        <p class="scholar-link">{link(SCHOLAR, "Full publication list on Google Scholar ↗", event("scholar_click"))}</p>
      </section>
'''

cv = f'''
      <div class="page-intro">
        <p class="eyebrow">Experience &amp; background</p><h1>Curriculum vitae</h1>
        <p>My research, publications, experience, technical skills, and professional service.</p>
        <div class="cv-actions">
          {link(CV, "Download CV ↓", ' class="button primary" download="Utkarsh_Tyagi_CV.pdf"' + event("cv_download"))}
          {link(CV, "Open PDF ↗", ' class="button" target="_blank" rel="noopener"' + event("cv_open"))}
        </div>
        <p class="cv-meta">Updated {escape(DATA["updated"])} · PDF · 2 pages</p>
      </div>
      <figure class="cv-preview" aria-label="Preview of the current two-page CV">
        <div class="cv-page"><a href="{CV}" aria-label="Open the full CV PDF"{event("cv_open")}>
          <img src="/assets/cv-page-1.webp" width="1600" height="2071" alt="CV page 1: current research at Scale AI and selected publications.">
        </a></div>
        <div class="cv-page"><a href="{CV}" aria-label="Open the full CV PDF"{event("cv_open")}>
          <img src="/assets/cv-page-2.webp" width="1600" height="2071" alt="CV page 2: additional experience, education, technical skills, awards, service, and patents." loading="lazy">
        </a></div>
        <figcaption>For selectable text and publication links, {link(CV, "open the PDF", event("cv_open"))}.</figcaption>
      </figure>
'''

for path, title, active, description, body, route in [
    ("index.html", "Audio & Multimodal AI Research", "intro", "Utkarsh Tyagi, Machine Learning Research Engineer at Scale AI. Audio and multimodal AI, speech dialogue, reinforcement learning, and post-training.", intro, "/"),
    ("publications/index.html", "Publications", "publications", "Selected research by Utkarsh Tyagi, including SteerDuplex, POW3R, Humanity’s Sixth Sense, Rubric Dropout, and Audio MultiChallenge.", publications, "/publications/"),
    ("cv/index.html", "CV", "cv", "Utkarsh Tyagi’s current CV: research, publications, professional experience, skills, and service.", cv, "/cv/")
]:
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page(title, active, description, body, route))

# Preserve previously published navigation URLs.
for old, new in {"about": "/", "research": "/publications/", "open_source": "/publications/", "others": "/"}.items():
    dest = ROOT / old / "index.html"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0;url={new}"><link rel="canonical" href="https://utkarsh4430.github.io{new}">
<title>Utkarsh Tyagi</title></head><body><p>This page has moved. {link(new, "Continue to the updated site")}</p></body></html>
''')
print("Built Intro, Publications, CV, and four redirects.")
