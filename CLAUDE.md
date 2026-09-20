# Duke Humanoid V2 — open-source hardware release (working rules)

This folder prepares the **hardware** open-source release of Duke Humanoid V2
(General Robotics Lab, Duke). The code is already public at
github.com/generalroboticslab/duke_humanoid_v2. V1/V2 are **our own** robots,
not reference material.

## How to talk to the user
- **Reply in 简体中文, always** — including short status replies. Technical
  terms, paths, commands and product names stay in English.
- The user is often waiting; give honest time estimates and check background
  work by looking at real signals (file mtimes, build output), not assumptions.

## Site rules (`hardware-site/`, MkDocs Material)
- **100 % English** on the site. Zero Chinese characters anywhere under `docs/`.
- **One job:** let a stranger build an identical robot — buy, make, assemble,
  wire, bring up, verify, safety, specs. No dev diary, dates, options
  considered-and-dropped, selection process, comparisons with other projects,
  or meta-commentary. Design rationale belongs in the paper, not the site.
- **Clear and scannable:** imperative headings, numbered steps (one action
  each), tables, figures above the steps they explain, `✅ **Check:**` lines,
  an `!!! abstract "At a glance"` box on build pages, no paragraph over ~3
  sentences, no stacked boxes.
- **Never invent a hardware fact.** Every number traces to the code repo
  (`reference/duke-humanoid-v2/repo`, not in git — reclone if needed), the BOM
  CSVs, the team wiring diagrams (`hardware/`), or the team's Fusion 360 model.
  If unknown → a gap, not a guess.
- **Every gap is RED and BOLD**, one line, with an owner:
  `!!! missing "MISSING — …"` / `!!! unverified "UNVERIFIED — …"` (+ `*Owner: role.*`),
  inline `**TODO**{ .dh-missing }` / `**UNVERIFIED**{ .dh-unverified }`.
  `MISSING — SAFETY — …` = blocks release. Styles in `docs/stylesheets/extra.css`.
- As-built only in build pages. Conflicts between sources: state both values, mark UNVERIFIED.
- Generated files — never hand-edit: `docs/reference/todo.md` (punch list),
  `docs/assets/MANIFEST.md` (images needed), `docs/data/cad-files.csv`,
  `docs/files/SHA256SUMS.txt`. Regenerate with the scripts in `tools/`.
- `mkdocs build --strict` must pass with zero warnings before you stop.

## Build / preview
```
cd hardware-site
python -m venv .venv                     # Windows: py -m venv .venv
.venv/bin/pip install -r requirements.txt    # Windows: .venv\Scripts\pip …
.venv/bin/mkdocs serve -a 127.0.0.1:8321     # Windows: .venv\Scripts\mkdocs …
# open http://localhost:8321/duke_humanoid_v2/   (the /duke_humanoid_v2/ prefix is intentional)
```
Regenerate after edits: `python tools/gen_punchlist.py`, `tools/gen_image_manifest.py`,
`tools/gen_cad_manifest.py` (indexes `docs/files/` and enforces GitHub size limits).

## Layout
- `hardware-site/` — the site. `docs/files/{step,print,drawings,plates,assembly}/` receive CAD
  exports; download links appear automatically once files are named `<part_id>_rev<NN>.<ext>`.
- `hardware/` — team power and data wiring diagrams (source of truth for electrical pages).
- `reference/bom/` — the team's BOM spreadsheets the `docs/data/*.csv` are generated from.
- `reference/team/` — the team's exploded-view booklet (`duke_humanoid_v2_hardware.pdf`); its pages are the
  site's assembly figures, rendered to `hardware-site/docs/assets/exploded/team/`.
- `_archive/hardware-site-docs-before-slim/` — the verbose pre-slim site, for recovering facts.
- `V2_RELEASE_PLAYBOOK.md`, `CAD_RELEASE_COMPARISON.md` — analyses (Chinese), for the team.
- `HANDOFF.md` — current status and next steps. Read it first.
