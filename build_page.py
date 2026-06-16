#!/usr/bin/env python3
"""Generate the HCFS license template and the GitHub Pages site.

Reads the filled-in LICENSE (the licensor's own instance) and produces:
  - HCFS-1.0.txt : a generic, fill-in-the-blanks template (placeholders)
  - index.html   : the styled web page (adoption guide + the template text)

The full license body is read from LICENSE at runtime and transformed by
string substitution; it is never hand-edited here. Regenerate after editing
LICENSE or header.txt so everything stays in sync:

    python build_page.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")

CANONICAL_URL = "https://jsh562.github.io/HCFS/"
SPDX_ID = "LicenseRef-HCFS-1.0"
RAW_LATEST = "https://raw.githubusercontent.com/jsh562/HCFS/main/HCFS-1.0.txt"
RAW_PINNED = "https://raw.githubusercontent.com/jsh562/HCFS/v1.0/HCFS-1.0.txt"

# --- 1. Build the generic template by replacing instance-specific fields -----
# Order matters: longer / more specific phrases first so they win.
SUBS = [
    ("San Diego County, California, USA", "[COUNTY], [STATE], [COUNTRY]"),
    ("San Diego County, California", "[COUNTY], [STATE]"),
    ("California law", "[STATE] law"),
    ("San Diego Jurisdiction:", "Governing Law and Venue:"),
    ("San Diego County", "[COUNTY]"),
    ("James Han at jsh562@gmail.com", "[LICENSOR NAME] at [CONTACT EMAIL]"),
    ("Licensor: James Han", "Licensor: [LICENSOR NAME]"),
    ("Contributor: James Han", "Contributor: [LICENSOR NAME]"),
    ("Contributor: $name", "Contributor: [LICENSOR NAME]"),
    ("Source Code: https://github.com/jsh562/flutter_ecg_monitor", "Source Code: [SOURCE CODE URL]"),
    ("Source Code: $address", "Source Code: [SOURCE CODE URL]"),
]
template_body = license_text
for old, new in SUBS:
    template_body = template_body.replace(old, new)
template_body = template_body.rstrip() + "\n"

NOTICE = f"""\
===========================================================================
HAN CONDITIONAL FAIR SOURCE 1.0 (HCFS) -- LICENSE TEMPLATE
===========================================================================

Canonical home : {CANONICAL_URL}
Identifier     : HCFS 1.0  (SPDX expression: {SPDX_ID})

HOW TO USE THIS TEMPLATE
Replace every bracketed field below with your own information, then save the
result in your project as a file named LICENSE:

  [LICENSOR NAME]   - the person or entity granting the license
  [CONTACT EMAIL]   - where licensees reach you for commercial terms
  [SOURCE CODE URL] - the public location of your source code
  [COUNTY]          - county for governing law and venue
  [STATE]           - governing-law state or province
  [COUNTRY]         - governing-law country

COPYING THIS LICENSE
You may copy and distribute verbatim copies of this license document and use
it as the license for your own software. You may fill in the bracketed fields
above with your own information. You may not otherwise modify the wording. The
names "Han Conditional Fair Source" and "HCFS" refer only to the unmodified
text of this document.

===========================================================================

"""

(ROOT / "HCFS-1.0.txt").write_text(NOTICE + template_body, encoding="utf-8")

# --- 2. Build index.html from the template body -----------------------------
banner = re.compile(r"^={5,}\r?\n(SECTION ([A-D]):[^\n]*)\r?\n={5,}\r?$", re.M)
matches = list(banner.finditer(template_body))
if len(matches) != 4:
    raise SystemExit(f"Expected 4 SECTION banners, found {len(matches)}")

ANCHOR = {"A": "commercial", "B": "prosperity", "C": "parity", "D": "agpl"}
LABEL = {
    "A": "A &middot; Commercial License",
    "B": "B &middot; Prosperity Public License 3.0.0",
    "C": "C &middot; Parity License 7.0.0",
    "D": "D &middot; GNU Affero GPL v3.0",
}

framework_text = template_body[: matches[0].start()].rstrip()
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
toc = [
    '<li><a href="#adopt">How to adopt HCFS</a></li>',
    '<li><a href="#framework">HCFS Framework Terms (§1–§7)</a></li>',
]
for i, m in enumerate(matches):
    letter = m.group(2)
    start = m.start()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(template_body)
    block = html.escape(template_body[start:end].rstrip())
    cls = "doc mono" if letter == "D" else "doc"
    parts.append(f'<section id="{ANCHOR[letter]}"><pre class="{cls}">{block}</pre></section>')
    toc.append(f'<li><a href="#{ANCHOR[letter]}">{LABEL[letter]}</a></li>')

header_snippet = html.escape((ROOT / "header.txt").read_text(encoding="utf-8").rstrip())

ADOPT = f"""<section id="adopt" class="adopt">
<h2>Adopt this license</h2>
<p>HCFS is a reusable source-available license. To license your own project under it:</p>
<ol>
<li>Copy the <a href="./HCFS-1.0.txt">HCFS&nbsp;1.0 template</a> into a file named <code>LICENSE</code> at the root of your project.</li>
<li>Replace the bracketed fields &mdash; <code>[LICENSOR NAME]</code>, <code>[CONTACT EMAIL]</code>, <code>[SOURCE CODE URL]</code>, <code>[COUNTY]</code>, <code>[STATE]</code>, <code>[COUNTRY]</code> &mdash; with your own details. Do not change any other wording.</li>
<li>Add this header to the top of every source file:
<pre class="snippet">{header_snippet}</pre></li>
<li>Declare it in your package metadata &mdash; e.g. npm <code>"license": "SEE LICENSE IN LICENSE"</code>, or the SPDX expression <code>{SPDX_ID}</code>.</li>
</ol>
<p class="ids"><strong>Name:</strong> Han Conditional Fair Source 1.0 &nbsp;&middot;&nbsp; <strong>Short:</strong> HCFS 1.0 &nbsp;&middot;&nbsp; <strong>SPDX:</strong> <code>{SPDX_ID}</code></p>
<p class="ids"><strong>Reference URLs</strong><br>
Human-readable: <a href="{CANONICAL_URL}">{CANONICAL_URL}</a><br>
Raw template (latest): <code>{RAW_LATEST}</code><br>
Raw template (pinned): <code>{RAW_PINNED}</code></p>
<p class="note">Copying terms: you may use this license and fill in the bracketed fields, but not otherwise alter the wording. &ldquo;HCFS&rdquo; refers only to the unmodified text. The text below is the template &mdash; the bracketed fields show what you replace.</p>
</section>"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Han Conditional Fair Source 1.0 (HCFS) &mdash; reusable source-available license</title>
<meta name="description" content="HCFS is a reusable source-available software license. Copy the template, fill in your fields, and reference it as LicenseRef-HCFS-1.0.">
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
code{background:var(--pre);border:1px solid var(--border);border-radius:4px;padding:.05rem .35rem;font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.adopt{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem 1.4rem;margin:1.6rem 0}
.adopt h2{margin-top:0;font-size:1.25rem}
.adopt ol{padding-left:1.2rem}
.adopt li{margin:.5rem 0}
.adopt .ids{font-size:.92rem;margin:.6rem 0}
pre.snippet{background:var(--pre);border:1px solid var(--border);border-radius:8px;padding:.8rem 1rem;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word;font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;margin:.6rem 0}
pre.doc{white-space:pre-wrap;word-wrap:break-word;overflow-wrap:anywhere;font:inherit;margin:1.4rem 0;padding:0}
pre.doc.mono{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--pre);border:1px solid var(--border);border-radius:8px;padding:1rem;overflow-x:auto}
.note{background:var(--card);border-left:3px solid var(--accent);padding:.7rem 1rem;border-radius:4px;font-size:.9rem;color:var(--muted);margin:1.2rem 0}
footer.site{margin-top:2.6rem;padding-top:1.4rem;border-top:1px solid var(--border);color:var(--muted);font-size:.9rem}
</style>
</head>
<body>
<div class="wrap">
<header class="site">
<h1>Han Conditional Fair Source 1.0 (HCFS)</h1>
<p class="sub">A reusable source-available software license.</p>
<p class="sub">Created by James Han &middot; Identifier: HCFS 1.0 (__SPDX__)</p>
</header>

<nav class="toc">
<h2>Contents</h2>
<ol>
__TOC__
</ol>
</nav>

__ADOPT__

__BODY__

<footer class="site">
<p>HCFS was created by James Han. This page shows the reusable template; see <a href="./HCFS-1.0.txt">HCFS-1.0.txt</a> for the raw template and <a href="./LICENSE">LICENSE</a> for the author's own filled-in instance.</p>
</footer>
</div>
</body>
</html>
"""

out = (
    TEMPLATE.replace("__SPDX__", SPDX_ID)
    .replace("__TOC__", "\n".join(toc))
    .replace("__ADOPT__", ADOPT)
    .replace("__BODY__", "\n".join(parts))
)
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"Wrote HCFS-1.0.txt and index.html ({len(out)} bytes, {len(matches)} sections)")
