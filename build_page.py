#!/usr/bin/env python3
"""Generate index.html from the LICENSE file.

The full license text is read from LICENSE at runtime and wrapped in a
styled, self-contained HTML page (table of contents + anchor links per
section). Regenerate this after editing LICENSE so the page stays in sync:

    python build_page.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")

# Match each bundled-section banner:  =====\nSECTION X: ...\n=====
banner = re.compile(r"^={5,}\r?\n(SECTION ([A-D]):[^\n]*)\r?\n={5,}\r?$", re.M)
matches = list(banner.finditer(license_text))
if len(matches) != 4:
    raise SystemExit(f"Expected 4 SECTION banners in LICENSE, found {len(matches)}")

ANCHOR = {"A": "commercial", "B": "prosperity", "C": "parity", "D": "agpl"}
LABEL = {
    "A": "A &middot; Commercial License",
    "B": "B &middot; Prosperity Public License 3.0.0",
    "C": "C &middot; Parity License 7.0.0",
    "D": "D &middot; GNU Affero GPL v3.0",
}

# Everything before the first banner is the HCFS framework (sections 1-7).
framework_text = license_text[: matches[0].start()].rstrip()
fw = html.escape(framework_text)

# Turn the plain-text in-body nav ("Commercial ~ Line 249", ...) into anchors.
nav_links = {
    "Commercial ~ Line 249": '<a href="#commercial">Commercial License &darr;</a>',
    "PROSPERITY 3.0.0 ~ Line 257": '<a href="#prosperity">Prosperity 3.0.0 &darr;</a>',
    "PARITY 7.0.0 ~ Line 321": '<a href="#parity">Parity 7.0.0 &darr;</a>',
    "AGPL-3.0 ~ Line 388": '<a href="#agpl">AGPL-3.0 &darr;</a>',
}
for raw, link in nav_links.items():
    fw = fw.replace(html.escape(raw), link)

parts = [f'<section id="framework"><pre class="doc">{fw}</pre></section>']
toc = ['<li><a href="#framework">HCFS Framework Terms (§1–§7)</a></li>']

for i, m in enumerate(matches):
    letter = m.group(2)
    start = m.start()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(license_text)
    block = html.escape(license_text[start:end].rstrip())
    cls = "doc mono" if letter == "D" else "doc"
    parts.append(f'<section id="{ANCHOR[letter]}"><pre class="{cls}">{block}</pre></section>')
    toc.append(f'<li><a href="#{ANCHOR[letter]}">{LABEL[letter]}</a></li>')

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Han Conditional Fair Source v1.0 (HCFS) &mdash; License</title>
<meta name="description" content="The Han Conditional Fair Source v1.0 (HCFS) software license by James Han.">
<style>
:root{--bg:#fff;--fg:#1a1a1a;--muted:#566;--accent:#0b5fff;--border:#e3e3e6;--card:#f6f7f9;--pre:#f7f8fa}
@media (prefers-color-scheme:dark){:root{--bg:#15171a;--fg:#e7e7e7;--muted:#9aa0a6;--accent:#7aa2ff;--border:#2a2d31;--card:#1c1f23;--pre:#101215}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:2.2rem 1.2rem 5rem}
header.site{border-bottom:1px solid var(--border);padding-bottom:1.4rem}
h1{font-size:1.6rem;line-height:1.25;margin:0 0 .4rem}
.sub{color:var(--muted);font-size:.95rem;margin:.12rem 0}
nav.toc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin:1.6rem 0}
nav.toc h2{font-size:.75rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:0 0 .6rem}
nav.toc ol{margin:0;padding-left:1.2rem}
nav.toc li{margin:.28rem 0}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
section{scroll-margin-top:1rem}
pre.doc{white-space:pre-wrap;word-wrap:break-word;overflow-wrap:anywhere;font:inherit;margin:1.4rem 0;padding:0}
pre.doc.mono{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--pre);border:1px solid var(--border);border-radius:8px;padding:1rem;overflow-x:auto}
.note{background:var(--card);border-left:3px solid var(--accent);padding:.7rem 1rem;border-radius:4px;font-size:.9rem;color:var(--muted);margin:1.2rem 0}
footer.site{margin-top:2.6rem;padding-top:1.4rem;border-top:1px solid var(--border);color:var(--muted);font-size:.9rem}
</style>
</head>
<body>
<div class="wrap">
<header class="site">
<h1>Han Conditional Fair Source v1.0 (HCFS)</h1>
<p class="sub">Licensor: James Han</p>
<p class="sub">Jurisdiction: San Diego County, California, USA</p>
</header>

<nav class="toc">
<h2>Contents</h2>
<ol>
__TOC__
</ol>
</nav>

<p class="note">This page reproduces the license for convenient reading. The canonical, binding text is the <a href="./LICENSE">LICENSE</a> file in this repository.</p>

__BODY__

<footer class="site">
<p>For commercial licensing, contact James Han at jsh562@gmail.com.</p>
<p>Canonical text: <a href="./LICENSE">LICENSE</a></p>
</footer>
</div>
</body>
</html>
"""

out = TEMPLATE.replace("__TOC__", "\n".join(toc)).replace("__BODY__", "\n".join(parts))
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"Wrote {ROOT / 'index.html'} ({len(out)} bytes, {len(matches)} sections)")
