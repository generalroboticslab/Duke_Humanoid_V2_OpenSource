# Handoff — Duke Humanoid V2 hardware release site

Last worked on: 2026-09-19 (Windows). Continue from this repo. Read `CLAUDE.md` for the working rules.

## Status

| Item | State |
|---|---|
| Site (`hardware-site/`, MkDocs Material) | 50 pages, English, `mkdocs build --strict` clean |
| Punch list (`docs/reference/todo.md`, generated) | **184 open items, 56 block release** — every gap is a red MISSING/UNVERIFIED box |
| Images still needed (`docs/assets/MANIFEST.md`, generated) | 89, incl. the whole-robot exploded view (`assets/images/exploded-overview.png`, not yet made) |
| Exploded-view animations | 9 web MP4s in `docs/assets/exploded/`, embedded on the assembly pages |
| Wiring diagrams | `hardware/*.jpg` → `docs/assets/wiring/`, on the electrical pages |
| CAD downloads (`docs/files/`) | 86 files live (120 MB) **from the 14:23 export**: 32 CNC STEP, 27 printed parts (STEP + STL), whole-robot STEP (zip), overall-dimensions PDF; `.f3z` (319 MB) as release asset `cad-v2.1-rc1`. Must be re-staged from the 16:46 export (unique file names, 45 printed parts now). No per-part drawings exist |
| Authoritative CAD export | `cad/humanoid_2.1_latest_2026-09-19_1646/` — `fusion_export` re-run started 16:46 (the 16:07 run never wrote `assembly/`, `step/` or `print/`): `tree.csv` complete (629 components with Fusion mass, centre of mass, inertia, appearance colour, unique `file_name`; same values as the 16:07 tree except the pose-dependent bounding boxes of 16 subassemblies and 2 mixed components), whole-robot STEP + `.f3z` written 16:51, `step/` + `print/` being written at 16:55, no `export.log` yet. `<1607>/modules/` holds the 128 module STEPs + `modules.csv` from a 16:42 run of `fusion_export_modules`, but that run wrote no `joints.csv` / `transforms.csv` (its log has no `wrote joints.csv` line, so Fusion ran a copy of the script from before those writers were added): re-run it on `<1646>/` |
| BOM source | **The team's BOM spreadsheet `reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx` (2026-09-19, WIP) is the parts list** ("以团队的为准"). `tools/gen_bom.py` writes all six parts CSVs from it (114 rows, $12,345.9485 = the sheet's own SUM cell), maps each line to the CAD part IDs the viewer and `docs/files/` key on, and records the sheet line in a `team_ref` column shown on every BOM table. 53 rows have no usable cost (the sheet's 30 zero-priced printed lines and 9 blank hardware lines, plus 13 rows the sheet has no line for): they carry a **blank** cost in the CSV and render a red TODO, never `$0.00`. The two-sheet CSV source and `gen_sheet1.py` / `gen_cnc.py` / `gen_recon.py` / `audit_sheet2.py` / `bom-reconciliation.csv` / `test-fixtures.csv` are superseded and deleted |
| Parts data (generated) | `docs/data/printed-parts.csv` 49 rows: 45 printed parts from the Fusion tree, `P39` (a team BOM line with no CAD match yet) and 3 material rows; `docs/data/part-properties.csv` 76 rows from the 16:46 tree (Fusion mass / COM / inertia; volumes fill in as `print/*.stl` appear — re-run after `export.log`); `docs/data/joints.csv` not written yet (needs the modules export with the joints writer) |
| Local preview | `http://localhost:8321/duke_humanoid_v2/` — the `/duke_humanoid_v2/` prefix is intentional (`site_url`) |

## CAD export pipeline — three download levels

Principle (the user's): everything visible in the Fusion model is downloadable at three levels — **whole
robot** (`assembly/`), **module** (`modules/`: every sub-assembly down to two levels below the root, vendor
assemblies included) and **part** (`step/` + `print/`: every component with bodies, vendor parts included).
The 3D viewer shows the Fusion appearance colours (`color_rgb` in `tree.csv`); hover and selection are the
only colour changes. `hardware-site/tools/README.md` documents every script.

Folders under `cad/` (`.gitignore` ignores `cad/*/assembly/`, `step/` and `print/` only — `modules/`,
`viewer/`, `modules.csv` and `transforms.csv` are not ignored yet):

- `humanoid_2.1_latest_2026-09-19_1423/` — OLD, complete (317 STEP/STL, whole-robot STEP and `.f3z`) but the
  export wrote one file per component *name*, so same-named components overwrote each other. Has `viewer/`
  (`context.stl`, `occurrences.csv`, `parts/`) and `transforms.csv` in the old naming. The files in
  `docs/files/` come from here.
- `humanoid_2.1_latest_2026-09-19_1607/` — `tree.csv` + the module export (`modules/` 128 STEPs, `modules.csv`,
  `export_modules.log`; no `joints.csv` with a `component` column, no `transforms.csv`); its `fusion_export` run
  produced no STEP/STL.
- `humanoid_2.1_latest_2026-09-19_1646/` — **authoritative**. `fusion_export` re-run in progress (see the status
  table). Site data is generated from its `tree.csv`.
- `_scratch/` — Draco / decimation experiments for the viewer (`reencode_glb.py`: DracoPy q14 level 10 takes
  the 15 MB GLB to 1.6 MB; `decim_compare.py`: pymeshlab quadric collapse is ~10× more accurate than
  fast_simplification at equal face count).

Fusion scripts (`hardware-site/tools/fusion_export*/`, run inside Fusion, in this order, same dated folder):

1. `fusion_export` → `tree.csv`, `assembly/<design>.step` + `.f3z`, `step/<file_name>.step` and
   `print/<file_name>.stl` for every component with bodies, a root-only (empty) `joints.csv`, `export.log`
   when done. `file_name` is unique per component (`name`, `name~2`, …) and recorded in `tree.csv`.
2. `fusion_export_modules` → `modules/<file_name>.step`, `modules.csv`, `joints.csv` (per component, with a
   `component` column; origin and axis in that component's frame; limits in rad/cm), `transforms.csv` (with
   the `file_name` of `tree.csv`), `export_modules.log`.
3. `fusion_export_transforms` (superseded by 1 + 2) and `fusion_export_viewer` (optional: `build_viewer.py`
   can place `print/*.stl` with `transforms.csv` instead).

Site-side, in order: `gen_printed.py` → `gen_part_properties.py <export>` → `stage_cad_export.py <export> --apply`
→ `gen_cad_manifest.py` → `build_viewer.py` → `gen_punchlist.py` → `mkdocs build --strict`.

### Findings from the 16:07 / 16:46 `tree.csv` (2026-09-19; identical mass, COM and inertia values)

- **Fusion's `getXYZMomentsOfInertia()` is about the component-frame origin, not the centre of mass**, with
  tensor-form products (`ixy` = −∫xy dm). Verified numerically against trimesh on four parts' STLs from the
  14:23 export (e.g. `CNC_arm13`: Fusion Ixx 381 692 = STL about origin 382 472, not the 3 223 about the COM).
  `fusion_export.py`'s docstring and the `tree.csv` column comment say "about the COM" — wrong, not fixed
  (not this lane). `gen_part_properties.py` shifts to the COM (parallel-axis) and keeps the raw values in
  `*_origin` columns. Because `tree.csv` rounds mass to 0.1 g, the shift is uncertain by ±0.05 g × |COM|²;
  the row notes state the bound and the page has an UNVERIFIED box. Fix: have `fusion_export.py` write
  `mass_g` to 0.001 g (or take the tensor about the COM inside Fusion) and re-run `gen_part_properties.py`.
- The left and right arm designs, and the two leg designs, are separate linked designs, so most parts are 2–3
  Fusion components (`name`, `name~2`, `name_1`, `name (1)`); `gen_printed.py` sums their quantities and
  `gen_part_properties.py` compares the copies (`CNC_leg12` copies differ in the sign of the COM z; the
  `3DP_arm06` copies differ in COM by ~2 mm). The bounding box and COM of a component that carries children
  follow the pose of those children: the 16:07 tree gave `3DP_arm06~2` a 40 × 385 × 166.6 mm box, the 16:46
  tree 40 × 55 × 71.2 mm like the left copy — not a stray body.
- Newly listed printed parts (45 rows; the last commit had 27): the end-effector attachment `v15_right_end_effector_attachment`
  (SLS nylon, both wrists), ankle covers `Component46`/`47` (`ANKLE_1_PROTECTION`), shoulder-yaw cover C (the
  `shoulder_yaw_protection` group's own body), the gripper's `base`, `custom_umi_gripper v6` (finger), `rail`,
  `apriltag_holder`, `Component9` (pinion), `apriltag` (tile), and the camera-column `gimbal_mount`,
  `gimbal_neck`, `gimbal_arm`, `Component92`. Materials `rail`/`Base`/`Neck`/`Arm` are custom names →
  material/process blank + UNVERIFIED box. `3DP_body05` is `PLA (for Bambu H2D)` → PLA, FDM.
- The gripper's `cnc_flange` of the code repo **is** `CNC_arm13_RS05_shaft_coupler` (Aluminum 6061, 22.05 g
  there, 22.1 g here; the code repo's Ixx about the COM, 5647.755, is the tree's Izz 5647.8 — the disc axis is
  x in the code repo's frame and z in Fusion's, and the COM lies on that axis so the origin shift leaves it). The gripper rack `double_helix_rack_30teeth_6mm v2` has **no
  geometry** (its only child `Component115` is empty) → MISSING box on Printed parts.
- Not listed, noted on Printed parts: `Hub` (Bambu PAHT-CF material, inside `Vention USB Hub`),
  `ankle_top_cover` (Steel, right leg only), the gripper root's own body. Torso spine, battery holders, IMU
  bracket, computer T-brackets are not in the Fusion tree at all.
- Model masses (CAD) on Full specifications: 35.27 kg total (lower body 17.51, torso 7.85, arms 4.61/4.60,
  grippers 0.35 each); 33.4 kg without grippers and camera columns vs 34.5 kg in the MJCF → UNVERIFIED.

### Next steps, in order

1. Wait for `export.log` in `<1646>/` (whole-robot STEP and `.f3z` are done; ~410 STEP + STL follow).
2. Run `fusion_export_modules` in Fusion on `<1646>/` (the current script writes `joints.csv` and
   `transforms.csv` before the module STEPs; check the log for `wrote joints.csv`).
3. `python tools/gen_part_properties.py ../cad/humanoid_2.1_latest_2026-09-19_1646` → volumes fill in and
   `docs/data/joints.csv` appears (the Joints table on `reference/part-index.md` renders and its MISSING box
   leaves the punch list); then `python tools/gen_punchlist.py`.
4. `python tools/stage_cad_export.py ../cad/humanoid_2.1_latest_2026-09-19_1646 --apply` →
   `python tools/gen_cad_manifest.py` (closes the shank-cover box on Printed parts; ~18 more STEP+STL; watch
   the 95 MB / 900 MB limits). `stage_cad_export.py` stages site parts only — module STEPs and vendor parts
   need a staging rule and a page section (viewer/downloads lane).
5. `build_viewer.py` from `<1646>/print/` + `transforms.csv` with the appearance colours and Draco.

## What the team must supply (blocking)

1. **CAD, remaining** (`humanoid_2.1_latest`, project humanoid/humanoid_v2/v2.1): only an overall-dimensions
   drawing exists (staged as `humanoid_2.1_latest_overall_rev01.pdf`); there are no per-part drawings, so
   machined parts are ordered from STEP. Slicer plates (3MF) → `docs/files/plates/` if the team has them; the
   `.f3z` must be re-released on the public repo.
   - Naming: Fusion names are `CNC_<sub><NN>_x<qty>_<desc>` and match the site IDs (`ALIASES` in
     `stage_cad_export.py`). Resolved from geometry: `leg09`–`leg12` and `leg03` duplicates are the same parts
     under two names; `arm09` = `elbow_roll_output_shaft`. Still open (red boxes): `CNC_arm06`, `CNC_leg18`,
     `CNC_arm12` are quoted but not in Fusion; `arm05`/`arm11` are quoted as CNC but are SLS nylon in Fusion;
     the `*_protection` covers have no filament grade; the gripper and camera-column parts have custom
     material names (`rail`, `Base`, `Neck`, `Arm`).
   - Whether the recorded CAD errors are fixed in this export is still unknown: Motor04 shaft and knee need
     M5 holes (CAD had M4); design error on the RS03 shaft bearing retainer above the knee.
2. **Whole-robot exploded view** (image or animation) — the 9 animations are per subassembly only.
3. **Decisions** (each is a red box on the site): hardware + docs licence; e-stop / main disconnect (none in the
   power diagram; run scripts assume one); fuse, surge protector, distribution blocks missing from the BOM;
   1 vs 3 × 48V→12V converters; fastener schedule and torques; battery retention. (Fusion says all CNC parts
   are Aluminum 6061, so 6061 vs 7075 is settled unless the shop used something else.)
4. **Hardware revision id**: Fusion says `2.1`, MJCF is `humanoid_v21` → fill the revision box with v2.1.

## Repo layout

- `hardware-site/` — site. `tools/` regenerates everything derived (see `tools/README.md`): BOM generators
  (`gen_bom.py`, reads `reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`), `gen_printed.py`,
  `gen_part_properties.py`, `stage_cad_export.py`, `gen_cad_manifest.py` (also enforces GitHub limits: 95
  MB/file, 900 MB total), `build_viewer.py`, `gen_punchlist.py`, `gen_image_manifest.py`, and the four Fusion
  scripts.
- `hardware/` — team power & data wiring diagrams (source of truth).
- `reference/bom/` — team BOM spreadsheets; `reference/_meta/cad-trees/` — evidence for `CAD_RELEASE_COMPARISON.md`.
  The rest of `reference/` (mirrors of Asimov/OpenArm/ToddlerBot/Berkeley, clones of our repos, papers; 4.4 GB)
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

## Publishing (later)

The 319 MB `.f3z` is a release asset (`cad-v2.1-rc1`) on this private repo; the link on the CAD downloads page
only works for collaborators until the release is re-created on the public repo.

`.github/workflows/docs.yml` builds with `--strict` and deploys GitHub Pages from `main`. `site_url` is still
`https://generalroboticslab.github.io/duke_humanoid_v2/` — change it (and the Pages source) when the final
home of the site is decided. This private repo cannot serve Pages on a free plan; publish from the public one.
