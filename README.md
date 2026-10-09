# Utkarsh Tyagi · Research profile

A lightweight, responsive research website with three pages: Intro, Publications, and CV.
The site is served directly by GitHub Pages from the root of `gh-pages`. `.nojekyll`
keeps the generated HTML independent of the previous Jekyll template.

## Update news or publications

1. Edit `content/profile.json`. Put news in reverse chronological order using `YYYY-MM` dates.
2. Add publication records with their title, paper URL, venue, and year. Keep submissions explicitly marked.
3. For featured papers, add a local figure under `assets/research/`, descriptive alt text,
   and the original figure URL for provenance. Cards link to the corresponding paper.
4. Run `python3 scripts/build_profile.py` to regenerate the pages.
5. Preview with `python3 -m http.server 8765`, then visit `http://localhost:8765/`.

All monthly updates appear in a keyboard-accessible scrollable panel on the Intro page,
including announcements preserved from the original website. The selected publication list
is organized by year, without modality sections.

## Visitor analytics

The site uses [Umami](https://umami.is/), which can track page views,
anonymous visitors, approximate location, referrers, device/browser information, and
CV/paper/Scholar clicks. It does not reveal people's names, email addresses, or employers.
The author's Umami Cloud website ID is configured; collection begins when these pages
are published to the production domain.

1. In an Umami Cloud account, add `utkarsh4430.github.io` as a website.
2. Copy its public website ID from the tracking code (not an account password or API key).
3. Set `analytics.website_id` in `content/profile.json` and regenerate the pages.
4. Publish the site, visit it, and verify the live dashboard receives visits and click events.

With no ID set, no tracking script is generated and no analytics requests are made.
The integration limits collection to the production hostname, excludes local previews,
respects Do Not Track, and omits URL query strings and fragments. Identifying visitors or
recording their screens is not enabled. A direct PDF visit bypasses the website tracker;
`cv_download` counts clicks on the site's download button, not confirmed completed downloads.
Tracking starts after activation and cannot reconstruct historical visits. Ad blockers
and browser settings can prevent some visits from being counted.

Setup reference: [collect data](https://docs.umami.is/docs/collect-data),
[tracker configuration](https://docs.umami.is/docs/tracker-configuration), and
[event tracking](https://docs.umami.is/docs/track-events).

## Update the CV

Replace `assets/Utkarsh_resume.pdf` with the approved PDF and update `updated` in
`content/profile.json`, then regenerate. The original PDF URL remains valid for existing links.
`assets/Utkarsh_resume.tex` is the corresponding source; generate the PDF in Overleaf or
the document editor before replacing it. Refresh `assets/cv-page-1.webp` and
`assets/cv-page-2.webp` from that same PDF for the on-page preview (1600 pixels wide).

## Files and compatibility

- `assets/profile.css`: shared design and responsive layouts.
- `assets/updates.js`: shows scroll fades and an “Older updates” control; the full timeline still works without JavaScript.
- `index.html`, `publications/index.html`, `cv/index.html`: generated pages; no JavaScript required.
- `/about/`, `/research/`, `/open_source/`, `/others/`: redirects for earlier navigation links.
- `visual/`: existing separate application, preserved.
- Old Jekyll templates and styles remain in the repository but are not used by the new pages.

Recent acceptance announcements use the month of the decision notification; older announcements
retain the months from the original website. Submission statuses reflect the author's confirmation.
No email contents or private account information are stored in the website content.
