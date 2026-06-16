# Han Conditional Fair Source 1.0 (HCFS)

A reusable **source-available** software license by James Han. It lets you offer
your software free for non-commercial use and a 30-day commercial trial, while
reserving paid commercial rights — falling back to strong copyleft (Parity /
AGPL) for unauthorized commercial use.

- **📄 Read it:** https://jsh562.github.io/HCFS/
- **Identifier:** `HCFS 1.0` &nbsp;·&nbsp; SPDX expression: `LicenseRef-HCFS-1.0`

> ⚠️ HCFS is a **custom, source-available** license — not an OSI-approved open
> source license. GitHub and SPDX tooling won't auto-detect it, and adopters
> should review it (ideally with counsel) before use.

## Use HCFS for your own project

1. Copy [`HCFS-1.0.txt`](HCFS-1.0.txt) into a file named `LICENSE` at your repo root.
2. Replace the bracketed fields with your own details — and change nothing else:
   - `[LICENSOR NAME]` — you (the person/entity granting the license)
   - `[CONTACT EMAIL]` — where licensees reach you for commercial terms
   - `[SOURCE CODE URL]` — public location of your source
   - `[COUNTY]`, `[STATE]`, `[COUNTRY]` — governing law and venue
3. Add the header from [`header.txt`](header.txt) to the top of every source file
   (HCFS §1.6 requires per-file notices).
4. Declare it in your package metadata:
   - npm: `"license": "SEE LICENSE IN LICENSE"`
   - SPDX expression / SBOMs: `LicenseRef-HCFS-1.0`
   - One-line reference: `Licensed under HCFS 1.0 — https://jsh562.github.io/HCFS/`

## Reference URLs

| Purpose | URL |
|---|---|
| Human-readable page | https://jsh562.github.io/HCFS/ |
| Raw template (latest) | https://raw.githubusercontent.com/jsh562/HCFS/main/HCFS-1.0.txt |
| Raw template (pinned to v1.0) | https://raw.githubusercontent.com/jsh562/HCFS/v1.0/HCFS-1.0.txt |

Pin to the `v1.0` URL when you need a reference that never changes.

## Copying the license text

You may copy the HCFS document verbatim and use it as your project's license,
filling in the bracketed fields. You may **not** otherwise alter the wording.
The names "Han Conditional Fair Source" and "HCFS" refer only to the unmodified
text of this document.

## What's in this repo

| File | Purpose |
|---|---|
| [`HCFS-1.0.txt`](HCFS-1.0.txt) | **Canonical generic template** — the thing adopters copy. |
| [`header.txt`](header.txt) | Per-file header snippet for adopters. |
| [`LICENSE`](LICENSE) | The author's own filled-in instance (a worked example). |
| [`index.html`](index.html) | The styled web page (served via GitHub Pages). |
| [`build_page.py`](build_page.py) | Generates `HCFS-1.0.txt` and `index.html` from `LICENSE`. |

## Maintaining

`HCFS-1.0.txt` and `index.html` are **generated** from `LICENSE`. After editing
`LICENSE` (or `header.txt`), regenerate and commit everything:

```sh
python build_page.py
```
