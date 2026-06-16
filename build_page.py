#!/usr/bin/env python3
"""Generate the HCFS license template and the GitHub Pages site.

Reads the filled-in LICENSE (the licensor's own instance) and produces:
  - HCFS-1.0.txt : a generic, fill-in-the-blanks template (placeholders)
  - index.html   : the styled web page with an in-browser license generator,
                   adoption helpers, FAQ, and the full template text.

The full license body is read from LICENSE at runtime and transformed by
string substitution; it is never hand-edited here. Regenerate after editing
LICENSE or header.txt so everything stays in sync:

    python build_page.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
header_raw = (ROOT / "header.txt").read_text(encoding="utf-8")

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
result in your project as a file named LICENSE. The generator at the canonical
home above can do this for you:

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

# --- 2. Parse the template body into the framework + bundled sections --------
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
    '<li><a href="#adopt">Adopt HCFS (generator)</a></li>',
    '<li><a href="#faq">FAQ</a></li>',
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

header_snippet = html.escape(header_raw.rstrip())
badge_md = (
    "[![License: HCFS 1.0]"
    "(https://img.shields.io/badge/license-HCFS%201.0-blue)]"
    f"({CANONICAL_URL})"
)

# --- 3. Adoption section: generator form + helpers --------------------------
ADOPT = f"""<section id="adopt" class="adopt">
<h2>Adopt this license</h2>
<p>HCFS is a reusable source-available license. Fill in the fields below and copy or
download a ready-to-use <code>LICENSE</code> for your project. Everything runs in your
browser &mdash; nothing is uploaded.</p>

<form id="gen-form" class="gen" autocomplete="on">
<div class="grid">
<label>Licensor name <small>(full legal / entity name)</small><input id="g-name" placeholder="Acme, Inc."></label>
<label>Contact email<input id="g-email" type="email" placeholder="legal@acme.com"></label>
<label>Source-code URL<input id="g-url" type="url" placeholder="https://github.com/acme/widget"></label>
<label>County<input id="g-county" placeholder="Santa Clara County"></label>
<label>State / Province<input id="g-state" placeholder="California"></label>
<label>Country<input id="g-country" placeholder="USA"></label>
<label>Copyright year<input id="g-year" inputmode="numeric" placeholder="2026"></label>
</div>
</form>

<div class="out-head"><strong>Your LICENSE</strong>
<span class="btns"><button type="button" id="copy-license">Copy</button><button type="button" id="dl-license">Download</button></span></div>
<pre id="out-license" class="snippet gen-out"></pre>

<div class="out-head"><strong>Per-file header</strong> <small>(replace the description line per file)</small>
<span class="btns"><button type="button" id="copy-header">Copy</button><button type="button" id="dl-header">Download</button></span></div>
<pre id="out-header" class="snippet"></pre>

<p class="note">The generator only fills the bracketed fields &mdash; it never changes the license wording.
This is not legal advice; HCFS is a real contract (fees, liquidated damages, telemetry consent, immunity
waivers), so consider a one-time review with counsel before relying on it. For a company, enter your exact
registered entity name.</p>

<details class="manual"><summary>Prefer to do it by hand?</summary>
<ol>
<li>Copy the <a href="./HCFS-1.0.txt">HCFS&nbsp;1.0 template</a> into a file named <code>LICENSE</code> at your repo root.</li>
<li>Replace the bracketed fields (<code>[LICENSOR NAME]</code>, <code>[CONTACT EMAIL]</code>, <code>[SOURCE CODE URL]</code>, <code>[COUNTY]</code>, <code>[STATE]</code>, <code>[COUNTRY]</code>) and change nothing else.</li>
<li>Add this header to the top of every source file:
<pre class="snippet">{header_snippet}</pre></li>
</ol>
</details>

<h3>Add a badge</h3>
<p>Show the license in your README:</p>
<pre id="badge-md" class="snippet">{html.escape(badge_md)}</pre>
<p><button type="button" data-copy="badge-md">Copy badge</button> &nbsp; Renders as: <img alt="License: HCFS 1.0" src="https://img.shields.io/badge/license-HCFS%201.0-blue"></p>

<h3>Declare it in package metadata</h3>
<p>npm <code>package.json</code></p>
<pre id="pkg-npm" class="snippet">"license": "SEE LICENSE IN LICENSE"</pre>
<p><button type="button" data-copy="pkg-npm">Copy</button></p>
<p>Python <code>pyproject.toml</code> (PEP 639)</p>
<pre id="pkg-py" class="snippet">license = "{SPDX_ID}"</pre>
<p><button type="button" data-copy="pkg-py">Copy</button></p>
<p>Rust <code>Cargo.toml</code></p>
<pre id="pkg-rs" class="snippet">license-file = "LICENSE"</pre>
<p><button type="button" data-copy="pkg-rs">Copy</button></p>

<h3>Use this repo as a template</h3>
<p>Repo owner: in GitHub <strong>Settings &rarr; General</strong>, tick <strong>Template repository</strong>.
Then anyone can click <strong>&ldquo;Use this template&rdquo;</strong> to start a project pre-wired with HCFS.</p>

<p class="ids"><strong>Name:</strong> Han Conditional Fair Source 1.0 &nbsp;&middot;&nbsp; <strong>Short:</strong> HCFS 1.0 &nbsp;&middot;&nbsp; <strong>SPDX:</strong> <code>{SPDX_ID}</code></p>
<p class="ids"><strong>Reference URLs</strong><br>
Human-readable: <a href="{CANONICAL_URL}">{CANONICAL_URL}</a><br>
Raw template (latest): <code>{RAW_LATEST}</code><br>
Raw template (pinned): <code>{RAW_PINNED}</code></p>
</section>"""

FAQ = f"""<section id="faq">
<h2>FAQ</h2>
<details><summary>Is HCFS open source?</summary><p>No. It is <em>source-available</em>: the code is public and free for non-commercial use, but it is not an OSI-approved open-source license and it reserves commercial rights.</p></details>
<details><summary>Can people use it commercially?</summary><p>Yes &mdash; there is a one-time 30-day commercial trial. After that, commercial use requires a paid agreement; otherwise it falls back to the Parity license, which requires publishing your full source.</p></details>
<details><summary>What happens after the 30-day trial?</summary><p>You either sign a paid commercial agreement, or your only remaining right is under Parity 7.0.0 (strong copyleft). Unpaid commercial use past day 30 also accrues fees.</p></details>
<details><summary>Can I modify the licensed software?</summary><p>Yes, subject to your user category (non-commercial under AGPL/Prosperity, or under the relevant commercial terms). You must keep the notices and per-file headers.</p></details>
<details><summary>How do I reference HCFS?</summary><p>Name: &ldquo;HCFS 1.0&rdquo;. SPDX: <code>{SPDX_ID}</code>. Link: <a href="{CANONICAL_URL}">{CANONICAL_URL}</a>.</p></details>
</section>"""

# --- 4. Client-side script (plain string; __TPL__/__HDR__ injected) ---------
SCRIPT = """<script>
(function(){
"use strict";
var TPL=__TPL__;
var HDR=__HDR__;
var FIELDS={"[LICENSOR NAME]":"g-name","[CONTACT EMAIL]":"g-email","[SOURCE CODE URL]":"g-url","[COUNTY]":"g-county","[STATE]":"g-state","[COUNTRY]":"g-country"};
function val(id){var el=document.getElementById(id);return el?el.value.trim():"";}
function fillLicense(){var out=TPL;for(var ph in FIELDS){var v=val(FIELDS[ph])||ph;out=out.split(ph).join(v);}return out;}
function fillHeader(){var name=val("g-name")||"[LICENSOR NAME]";var year=val("g-year")||"[YEAR]";return HDR.split("[LICENSOR NAME]").join(name).split("[YEAR]").join(year);}
function update(){var a=document.getElementById("out-license");if(a)a.textContent=fillLicense();var b=document.getElementById("out-header");if(b)b.textContent=fillHeader();}
function download(name,text){var blob=new Blob([text],{type:"text/plain"});var u=URL.createObjectURL(blob);var a=document.createElement("a");a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);}
function flash(btn){if(!btn)return;var t=btn.textContent;btn.textContent="Copied!";setTimeout(function(){btn.textContent=t;},1200);}
function fallback(text,btn){var ta=document.createElement("textarea");ta.value=text;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();try{document.execCommand("copy");flash(btn);}catch(e){}ta.remove();}
function copy(text,btn){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(function(){flash(btn);},function(){fallback(text,btn);});}else{fallback(text,btn);}}
document.addEventListener("DOMContentLoaded",function(){
var y=document.getElementById("g-year");if(y&&!y.value)y.value=String(new Date().getFullYear());
var inputs=document.querySelectorAll("#gen-form input");for(var i=0;i<inputs.length;i++)inputs[i].addEventListener("input",update);
function on(id,fn){var el=document.getElementById(id);if(el)el.addEventListener("click",fn);}
on("copy-license",function(e){copy(fillLicense(),e.currentTarget);});
on("dl-license",function(){download("LICENSE",fillLicense());});
on("copy-header",function(e){copy(fillHeader(),e.currentTarget);});
on("dl-header",function(){download("HCFS-header.txt",fillHeader());});
var cbs=document.querySelectorAll("[data-copy]");for(var j=0;j<cbs.length;j++){cbs[j].addEventListener("click",function(e){var el=document.getElementById(e.currentTarget.getAttribute("data-copy"));if(el)copy(el.textContent,e.currentTarget);});}
update();
});
})();
</script>"""
SCRIPT = SCRIPT.replace("__TPL__", json.dumps(template_body).replace("</", "<\\/"))
SCRIPT = SCRIPT.replace("__HDR__", json.dumps(header_raw).replace("</", "<\\/"))

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Han Conditional Fair Source 1.0 (HCFS) &mdash; reusable source-available license</title>
<meta name="description" content="HCFS is a reusable source-available software license. Fill in the generator, copy your LICENSE, and reference it as LicenseRef-HCFS-1.0.">
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
.adopt h3{font-size:1rem;margin:1.4rem 0 .3rem}
.adopt .ids{font-size:.92rem;margin:.6rem 0}
.gen .grid{display:grid;grid-template-columns:1fr 1fr;gap:.7rem 1rem;margin:.4rem 0 1rem}
.gen label{display:flex;flex-direction:column;gap:.25rem;font-size:.85rem;color:var(--muted)}
.gen label small{font-weight:400}
.gen input{font:14px/1.4 inherit;padding:.45rem .55rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--fg)}
@media (max-width:560px){.gen .grid{grid-template-columns:1fr}}
.out-head{display:flex;align-items:center;justify-content:space-between;gap:.5rem;flex-wrap:wrap;margin:.9rem 0 .3rem}
.btns{display:flex;gap:.4rem}
button{font:13px/1 inherit;padding:.42rem .7rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--accent);cursor:pointer}
button:hover{background:var(--pre)}
details summary{cursor:pointer}
pre.snippet{background:var(--pre);border:1px solid var(--border);border-radius:8px;padding:.8rem 1rem;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word;font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;margin:.6rem 0}
pre.gen-out{max-height:340px;overflow:auto}
pre.doc{white-space:pre-wrap;word-wrap:break-word;overflow-wrap:anywhere;font:inherit;margin:1.4rem 0;padding:0}
pre.doc.mono{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--pre);border:1px solid var(--border);border-radius:8px;padding:1rem;overflow-x:auto}
.note{background:var(--card);border-left:3px solid var(--accent);padding:.7rem 1rem;border-radius:4px;font-size:.9rem;color:var(--muted);margin:1.2rem 0}
#faq details{border:1px solid var(--border);border-radius:8px;padding:.5rem .85rem;margin:.5rem 0;background:var(--card)}
#faq summary{font-weight:600}
#faq details p{margin:.55rem 0 .2rem}
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

__FAQ__

__BODY__

<footer class="site">
<p>HCFS was created by James Han. This page shows the reusable template; see <a href="./HCFS-1.0.txt">HCFS-1.0.txt</a> for the raw template and <a href="./LICENSE">LICENSE</a> for the author's own filled-in instance.</p>
</footer>
</div>
__SCRIPT__
</body>
</html>
"""

out = (
    TEMPLATE.replace("__SPDX__", SPDX_ID)
    .replace("__TOC__", "\n".join(toc))
    .replace("__ADOPT__", ADOPT)
    .replace("__FAQ__", FAQ)
    .replace("__BODY__", "\n".join(parts))
    .replace("__SCRIPT__", SCRIPT)
)
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"Wrote HCFS-1.0.txt and index.html ({len(out)} bytes, {len(matches)} sections)")
