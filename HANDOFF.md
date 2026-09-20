# Handoff — Duke Humanoid V2 hardware release site

Last worked on: 2026-09-19 (Windows). Continue from this repo. Read `CLAUDE.md` for the working rules.

## Status

| Item | State |
|---|---|
| Site (`hardware-site/`, MkDocs Material) | 50 pages, English, `mkdocs build --strict` exits 0 with zero `WARNING` |
| Punch list (`docs/reference/todo.md`, generated) | **184 open items across 42 pages, 56 block release** — every gap is a red MISSING/UNVERIFIED box |
| Images still needed (`docs/assets/MANIFEST.md`, generated) | **83** (the generator's split: 2 placed, 26 named, 55 per-part). The whole-robot exploded view is no longer among them: the booklet's page 15 fills it on the home page and on `assembly/index.md` |
| Team exploded-view booklet | `reference/team/duke_humanoid_v2_hardware.pdf` (Eric Lu, 2026-09-19, 15 pages). Its pages are rendered to `docs/assets/exploded/team/NN-<name>.webp` (2400 × 1350) and **published as the site's assembly figures** (`docs/assembly/*.md`; page 15, the whole robot, opens the home page and `assembly/index.md`). The PDF itself is staged as `docs/files/drawings/duke_humanoid_v2_exploded_views_rev01.pdf` (untracked until committed) and indexed in `cad-files.csv`. Pages 08 and 12 read "switch A ↔ B": on the other leg / arm the covers labelled A and B swap sides (confirmed by the user) |
| Exploded-view animations | 9 web MP4s in `docs/assets/exploded/`, embedded on the assembly pages |
| Wiring diagrams | `hardware/*.jpg` → `docs/assets/wiring/`, on the electrical pages |
| CAD downloads (`docs/files/`) | **329 files, 706 MB** (672.9 MiB as `gen_cad_manifest.py` prints it): 1 whole-robot STEP (zip, 34 MB), 80 module STEPs (481 MB), 76 part STEPs (77 MB), 45 printed-part STLs (51 MB), 125 vendor files (55 MB) — all from the canonical export — and 2 PDFs under `drawings/` (overall dimensions 2.6 MB, the exploded-view booklet 6.2 MB). Numbers from `docs/data/cad-files.csv`, which matches the folder file for file (generator re-run, no diff). `.f3z` (319 MB) is the release asset `cad-v2.1-rc1`: the 14:23 export's archive (sha256 `f440621d…`, the hash on the CAD downloads page). No per-part drawings exist |
| Canonical CAD export | `cad/humanoid_2.1_latest_2026-09-19_1607/` — **complete**. The 16:46 `fusion_export` run's output was merged into this folder (its `export.log` still names `…_1646/`, which no longer exists). It holds `tree.csv` (629 components with Fusion mass, COM, inertia, appearance colour and a unique `file_name`), `assembly/` (whole-robot STEP 194 MB and the script's archive export, a 1.2 MB `humanoid_2.1_latest.f3z.f3d` — the 319 MB `.f3z` exists only in `…_1423/assembly/`), `step/` (410), `print/` (408), `modules/` (128 + `modules.csv`), `joints.csv` (1205 joints; `export_joints.log` says "from 630 components", the file's `component` column holds 62 distinct names), `transforms.csv` (2088 occurrences), and the logs `export.log`, `export_modules.log`, `export_joints.log`, `export_missing.log`, `export_cameras.log` |
| BOM source | **The team's spreadsheet `reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx` (2026-09-19, WIP) is the parts list** — the team's sheet wins over every other source. `tools/gen_bom.py` writes all six parts CSVs and `team-map.csv` from it, maps each line to the CAD part IDs the viewer and `docs/files/` key on, and records the sheet line in a `team_ref` column shown first on every BOM table. Rows the sheet does not price carry a **blank** cost and render a red TODO, never `$0.00`. The two-sheet CSV source and `gen_sheet1.py` / `gen_cnc.py` / `gen_recon.py` / `audit_sheet2.py` / `bom-reconciliation.csv` / `test-fixtures.csv` are superseded and deleted |
| Parts data (generated, `docs/data/`) | `cnc-parts.csv` 35, `printed-parts.csv` 48, `electronics.csv` 14, `actuators.csv` 6, `fasteners.csv` 9, `cables-connectors.csv` 1; `part-properties.csv` 76 (volume filled on 71), `joints.csv` 1205, `modules.csv` 128, `vendor-parts.csv` 287, `cad-files.csv` 329; `team-map.csv` 100 (from `gen_bom.py`: one row per team BOM line with the booklet page that labels it, the CAD count and a `status`: 77 settled, 23 open) |
| 3D viewer (`docs/assets/viewer/`) | `robot.glb` (2.3 MB, Draco), `parts.json`, `downloads.json`, `vendor-map.json`. Fusion appearance colours (own parts black-grey, purchased parts in their Fusion colours), joint axes, preview and download per part, hide/show the selection (Fusion-style eye) and an x-ray ghost where it is occluded |
| Local preview | `http://localhost:8321/Duke_Humanoid_V2_OpenSource/` — the `/Duke_Humanoid_V2_OpenSource/` prefix is intentional (`site_url`) |

## CAD export pipeline — three download levels

Principle (the user's): everything visible in the Fusion model is downloadable at three levels — **whole
robot** (`assembly/`), **module** (`modules/`: every sub-assembly down to two levels below the root, vendor
assemblies included) and **part** (`step/` + `print/`: every component with bodies, vendor parts included).
`hardware-site/tools/README.md` documents every script.

Folders under `cad/` (`.gitignore` ignores `cad/*/assembly/`, `step/`, `print/`, `modules/`, `viewer/` and
`cad/_scratch/`; tracked are `tree.csv`, `joints.csv`, `transforms.csv`, `modules.csv`, the logs and
`…_1423/drawings/`):

- `humanoid_2.1_latest_2026-09-19_1423/` — OLD. Complete (317 STEP/STL) but the export wrote one file per
  component *name*, so same-named components overwrote each other. Has `viewer/` (`context.stl`,
  `occurrences.csv`, `parts/`) and a `transforms.csv` in the old naming. Nothing on the site comes from it.
- `humanoid_2.1_latest_2026-09-19_1607/` — **canonical**. All site data and every staged file come from here.
- `_scratch/` — Draco / decimation experiments for the viewer (`reencode_glb.py`: DracoPy q14 level 10 takes
  the 15 MB GLB to 1.6 MB; `decim_compare.py`: pymeshlab quadric collapse is ~10× more accurate than
  fast_simplification at equal face count).

Fusion scripts that exist now (`hardware-site/tools/fusion_export*/`, run inside Fusion, all into one dated
folder): `fusion_export` (tree, whole robot, per-part STEP + STL), `fusion_export_modules` (module STEPs +
`joints.csv` + `transforms.csv`), `fusion_export_joints` (joints and transforms only, 30 s),
`fusion_export_missing` (re-export the STLs that failed on Windows' 260-character path limit),
`fusion_export_cameras` (RealSense components as whole-occurrence STLs, mesh bodies included),
`fusion_export_viewer` (optional) and `fusion_export_transforms` (superseded by the first two, kept for the
14:23 export). Run order and outputs: `hardware-site/tools/README.md`.

Site-side, in order: `gen_bom.py` → `gen_printed.py` → `gen_part_properties.py <export>` → `gen_modules.py <export>`
→ `gen_vendor_map.py <export>` → `stage_cad_export.py <export> --apply` → `gen_cad_manifest.py` →
`build_viewer.py` → `gen_punchlist.py` → `gen_image_manifest.py` → `mkdocs build --strict`.

### Findings from `tree.csv` (2026-09-19)

- **Fusion's `getXYZMomentsOfInertia()` is about the component-frame origin, not the centre of mass**, with
  tensor-form products (`ixy` = −∫xy dm). Verified numerically against trimesh on four parts' STLs (e.g.
  `CNC_arm13`: Fusion Ixx 381 692 = STL about origin 382 472, not the 3 223 about the COM).
  `fusion_export.py`'s docstring and the `tree.csv` column comment say "about the COM" — wrong, not fixed.
  `gen_part_properties.py` shifts to the COM (parallel-axis) and keeps the raw values in `*_origin` columns.
  Because `tree.csv` rounds mass to 0.1 g, the shift is uncertain by ±0.05 g × |COM|²; the row notes state the
  bound and the page has an UNVERIFIED box. Fix: have `fusion_export.py` write `mass_g` to 0.001 g (or take the
  tensor about the COM inside Fusion) and re-run `gen_part_properties.py`.
- The left and right arm designs, and the two leg designs, are separate linked designs, so most parts are 2–3
  Fusion components (`name`, `name~2`, `name_1`, `name (1)`); `gen_printed.py` sums their quantities and
  `gen_part_properties.py` compares the copies (`CNC_leg12` copies differ in the sign of the COM z; the
  `3DP_arm06` copies differ in COM by ~2 mm). The bounding box and COM of a component that carries children
  follow the pose of those children.
- Printed parts listed: 45 from the Fusion tree, incl. the end-effector attachment
  `v15_right_end_effector_attachment` (SLS nylon, both wrists), ankle covers `Component46`/`47`
  (`ANKLE_1_PROTECTION`), shoulder-yaw cover C, the gripper's `base`, `custom_umi_gripper v6` (finger), `rail`,
  `apriltag_holder`, `Component9` (pinion), `apriltag` (tile), and the camera-column `gimbal_mount`,
  `gimbal_neck`, `gimbal_arm`, `Component92`. Materials `rail` / `Base` / `Neck` / `Arm` are custom Fusion names
  → material and process blank + UNVERIFIED box. `3DP_body05` is `PLA (for Bambu H2D)` → PLA, FDM.
- The gripper's `cnc_flange` of the code repo **is** `CNC_arm13_RS05_shaft_coupler` (Aluminum 6061, 22.05 g
  there, 22.1 g here; the code repo's Ixx about the COM, 5647.755, is the tree's Izz 5647.8 — the disc axis is
  x in the code repo's frame and z in Fusion's). The gripper rack `double_helix_rack_30teeth_6mm v2` has **no
  geometry** (its only child `Component115` is empty) → MISSING box on Printed parts.
- Not listed, noted on Printed parts: `Hub` (Bambu PAHT-CF, inside `Vention USB Hub`), `ankle_top_cover`
  (Steel, right leg only), the gripper root's own body. Torso spine, battery holders, IMU bracket and computer
  T-brackets are not in the Fusion tree at all.
- **The Fusion model carries no joint limits**: of the 1205 joints in `joints.csv` (1162 rigid, 37 revolute,
  4 slider, 2 planar) exactly one has a limit value. Limits must come from the team or from the MJCF.
- Model masses (CAD) on Full specifications: 35.27 kg total (lower body 17.51, torso 7.85, arms 4.61/4.60,
  grippers 0.35 each); 33.4 kg without grippers and camera columns vs 34.5 kg in the MJCF → UNVERIFIED.

### Next steps, in order

1. Commit the two untracked generated outputs: the staged booklet PDF
   `docs/files/drawings/duke_humanoid_v2_exploded_views_rev01.pdf` (already listed in `cad-files.csv` and
   `SHA256SUMS.txt`) and `docs/data/team-map.csv`.
2. Close the shank-cover MISSING box on Printed parts (`3DP_legP09` / `3DP_legP10`): the canonical export has
   unique file names, so re-check whether the staged files are still byte-identical to `3DP_armP05` / `06`.
3. Answer the open mapping questions in the UNVERIFIED boxes on `docs/bom/cnc-parts.md` and
   `docs/bom/printed-parts.md` (see *What the team must supply*).
4. Re-run `gen_punchlist.py` and `gen_image_manifest.py` after every page change, then
   `mkdocs build --strict`.
5. `stage_cad_export.py` stages site parts, modules and vendor parts; watch the GitHub limits
   (95 MB/file, 900 MB total, both as `gen_cad_manifest.py` measures them in MiB — the staged tree is at 672.9 MiB
   (706 MB), the largest file 70.1 MiB (73.5 MB); `stage_cad_export.py` has its own 700 MB budget for `docs/files/`).

## What the team must supply (blocking)

1. **Licence** — hardware and docs licence is undecided; a red box on the site.
2. **E-stop / main disconnect** — none in the power diagram, but the run scripts assume one. `MISSING — SAFETY`.
3. **Joint limits** — the Fusion model has none (see above). Needed for the joint table and the specs page.
4. **Open BOM questions** (each is a red box on the page named):
   - `RS06` count: the team BOM lists 2, the robot has four RS06 joints (`docs/bom/actuators.md`).
   - **Fastener schedule**: every screw (thread, length, head, drive, qty), fits, dowel pins, retaining rings,
     shims, threadlocker locations and torques. `MISSING — SAFETY` on `docs/bom/fasteners-and-hardware.md`.
   - **Bearings**: `H2` (35 × 44 × 5 mm) — the team BOM buys 18, Fusion places 26; `H5` (10 × 15 × 4 mm, 2 off)
     has no component named for it in Fusion.
   - **AprilTag count**: team BOM line `P15` buys 12 tiles, Fusion places 16 (eight per gripper) — 12 or 16?
     (`docs/bom/printed-parts.md`).
   - **Torso plates** `3DP_body06`–`09`: PLA in the team BOM vs `ABS Plastic 60%infill` in Fusion.
   - **Cables and connectors**: the team BOM has no lines for XT30 / XT30(2+2) / GH1.25 / EC5, loom, Ethernet,
     heat-shrink, bulk wire or CAN termination resistors; wire gauges are `MISSING — SAFETY`.
   - Machined parts with no team BOM line: `CNC_arm05`, `CNC_arm06`, `CNC_arm11` (SLS nylon in Fusion),
     `CNC_arm12_wrist_pitch` (in neither the BOM nor the model), `CNC_arm13_RS05_shaft_coupler`.
   - Electronics: fuse and holder, battery charger, surge protector MPN, distribution terminals; 1 vs 3
     48 V→12 V converters; battery retention.
5. **CAD, remaining**: no per-part drawings — `docs/files/drawings/` holds only the overall-dimensions drawing
   (`humanoid_2.1_latest_overall_rev01.pdf`) and the exploded-view booklet — so machined parts are ordered from STEP. Slicer plates (3MF) →
   `docs/files/plates/` if the team has them; the `.f3z` must be re-released on the public repo. Whether the
   recorded CAD errors are fixed in this export is still unknown: Motor04 shaft and knee need M5 holes (CAD had
   M4); design error on the RS03 shaft bearing retainer above the knee.
6. **Hardware revision id**: Fusion says `2.1`, MJCF is `humanoid_v21` → fill the revision box with v2.1.

## Repo layout

- `hardware-site/` — site. `tools/` regenerates everything derived (see `tools/README.md`).
- `hardware/` — team power & data wiring diagrams (source of truth for the electrical pages).
- `reference/bom/` — the team's BOM spreadsheet (the parts list).
- `reference/team/` — the team's exploded-view booklet `duke_humanoid_v2_hardware.pdf` (the assembly figures).
- `reference/_meta/cad-trees/` — evidence for `CAD_RELEASE_COMPARISON.md`.
- The rest of `reference/` (mirrors of Asimov/OpenArm/ToddlerBot/Berkeley, clones of our repos, papers; 4.4 GB)
  is **not in git**. Reclone `github.com/generalroboticslab/duke_humanoid_v2` (with submodules) into
  `reference/duke-humanoid-v2/repo/` if a page needs re-verifying against code (the gripper facts above come
  from `simulation/asset/duke_v2/parallel_gripper/`).
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
generator in `tools/` writes LF and POSIX paths on both systems (before 2026-09-19 `gen_punchlist.py`
and `gen_image_manifest.py` produced wrong counts on Windows because they compared backslash paths).
Set `PYTHONIOENCODING=utf-8` when a generator prints `×` or `·` to a cp1252 console.

## Publishing — NOT YET

The site is **not public** and must stay that way until the team decides (licence first). Collaborators
need only **write** access to edit and push; every push to `main` runs the strict build in Actions.

Deployment is gated: `.github/workflows/docs.yml` uploads and deploys Pages only when the repository
variable `DEPLOY_PAGES` equals `true` (Settings → Secrets and variables → Actions → Variables). It is unset.
Repository Settings → Pages → Source should be **None** until then. When the team decides to publish:
set `DEPLOY_PAGES=true`, set Pages Source to **GitHub Actions**, push. `site_url` is
`https://rivery927.github.io/Duke_Humanoid_V2_OpenSource/`. Note: a Pages site built from a private
repository is public — everything under `docs/files/` (674 MB of CAD) becomes downloadable by anyone.
