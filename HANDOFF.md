# Handoff — Duke Humanoid V2 hardware release site

Last worked on: 2026-09-19 (Windows). Continue from this repo. Read `CLAUDE.md` for the working rules.

## Status

| Item | State |
|---|---|
| Site (`hardware-site/`, MkDocs Material) | 50 pages, ~22,500 words, English, `mkdocs build --strict` clean |
| Punch list (`docs/reference/todo.md`, generated) | **171 open items, 52 block release** — every gap is a red MISSING/UNVERIFIED box |
| Images still needed (`docs/assets/MANIFEST.md`, generated) | 112, incl. the whole-robot exploded view (`assets/images/exploded-overview.png`, not yet made) |
| Exploded-view animations | 9 web MP4s in `docs/assets/exploded/`, embedded on the assembly pages |
| Wiring diagrams | `hardware/*.jpg` → `docs/assets/wiring/`, on the electrical pages |
| CAD downloads | 86 files live (120 MB): 32 CNC STEP, 27 printed parts (STEP + STL, incl. covers from the `*_protection` materials), whole-robot STEP (zip), overall-dimensions PDF; `.f3z` (319 MB) as release asset `cad-v2.1-rc1`. No per-part drawings exist. Raw export + `tree.csv` in `cad/humanoid_2.1_latest_2026-09-19_1423/` |
| Local preview | `http://localhost:8321/duke_humanoid_v2/` — the `/duke_humanoid_v2/` prefix is intentional (`site_url`) |

## What the team must supply (blocking)

1. **CAD, remaining** (`humanoid_2.1_latest`, project humanoid/humanoid_v2/v2.1; done 2026-09-19: linked
   components updated, STEP/STL/f3z exported with `tools/fusion_export/`, staged with `tools/stage_cad_export.py`):
   - PDF drawings from `humanoid_2.1_latest_Drawing` → `docs/files/drawings/<part_id>_rev01.pdf`;
   - slicer plates (3MF) → `docs/files/plates/`; the `.f3z` must be re-released on the public repo.
   - Naming: Fusion names are `CNC_<sub><NN>_x<qty>_<desc>` and match the site IDs (see `ALIASES` in
     `stage_cad_export.py`). Team must settle: `CNC_arm06`, `CNC_arm09`, `CNC_leg18` are in the quote sheet but
     not in Fusion (arm09 is `elbow_roll_output_shaft` there); `CNC_arm12_wrist_pitch` is in neither; `CNC_leg09`,
     `leg10`, `leg11` each have two differently named components; `leg03` is x4 in one place and x5 in another.
     `arm05` and `arm11` are SLS nylon (`3DP_`), not CNC. The team's `01_m03_shaft` list is not used in Fusion.
   - Whether the recorded CAD errors are fixed in this export is still unknown: Motor04 shaft and knee need
     M5 holes (CAD had M4); design error on the RS03 shaft bearing retainer above the knee.
2. **Whole-robot exploded view** (image or animation) — the 9 animations are per subassembly only.
3. **Decisions** (each is a red box on the site): hardware + docs licence; e-stop / main disconnect (none in the
   power diagram; run scripts assume one); fuse, surge protector, distribution blocks missing from the BOM;
   1 vs 3 × 48V→12V converters; fastener schedule and torques; battery retention. (Fusion says all CNC parts
   are Aluminum 6061, so 6061 vs 7075 is settled unless the shop used something else.)
4. **Hardware revision id**: Fusion says `2.1`, MJCF is `humanoid_v21` → fill the revision box with v2.1.

## Repo layout

- `hardware-site/` — site. `tools/` regenerates: `gen_punchlist.py`, `gen_image_manifest.py`,
  `gen_cad_manifest.py` (also enforces GitHub limits: 95 MB/file, 900 MB total), BOM generators
  (`gen_sheet1.py`, `gen_cnc.py`, `gen_recon.py`, read `reference/bom/`).
- `hardware/` — team power & data wiring diagrams (source of truth).
- `reference/bom/` — team BOM spreadsheets; `reference/_meta/cad-trees/` — evidence for `CAD_RELEASE_COMPARISON.md`.
  The rest of `reference/` (mirrors of Asimov/OpenArm/ToddlerBot/Berkeley, clones of our repos, papers; 4.4 GB)
  is **not in git**. Reclone `github.com/generalroboticslab/duke_humanoid_v2` (with submodules) into
  `reference/duke-humanoid-v2/repo/` if a page needs re-verifying against code.
- Not in git either: the Notion design-log export (1.7 GB; vendor PDFs — do not redistribute) and the AVI
  originals of the exploded views (web versions are in the site).
- `_archive/hardware-site-docs-before-slim/` — the 96k-word pre-slim site, to recover a fact if needed.
- `V2_RELEASE_PLAYBOOK.md`, `CAD_RELEASE_COMPARISON.md` — Chinese analyses for the team.

## Windows notes

```
cd hardware-site
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\mkdocs serve -a 127.0.0.1:8321
```
`.claude/launch.json` has two entries: `hardware-site` (Windows, `.venv/Scripts/python.exe`) and
`hardware-site-macos` (`.venv/bin/python`). Line endings are forced to LF by `.gitattributes`, and every
generator in `tools/` now writes LF and POSIX paths on both systems (before 2026-09-19 `gen_punchlist.py`
and `gen_image_manifest.py` produced wrong counts on Windows because they compared backslash paths).

## Publishing (later)

The 319 MB `.f3z` is a release asset (`cad-v2.1-rc1`) on this private repo; the link on the CAD downloads page
only works for collaborators until the release is re-created on the public repo.

`.github/workflows/docs.yml` builds with `--strict` and deploys GitHub Pages from `main`. `site_url` is still
`https://generalroboticslab.github.io/duke_humanoid_v2/` — change it (and the Pages source) when the final
home of the site is decided. This private repo cannot serve Pages on a free plan; publish from the public one.
