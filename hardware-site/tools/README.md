# tools/

Everything in `docs/data/`, the files under `docs/files/` and `docs/assets/viewer/`, and two of the pages in
`docs/` are **derived**, not written. This directory holds the derivations, so that the published data can be
reproduced from its source and the published lists cannot drift away from the pages they describe.

Run them from the site root with the site's virtualenv:

```console
$ python tools/gen_sheet1.py        # bought parts  -> docs/data/*.csv
$ python tools/gen_cnc.py           # machined parts -> cnc-parts.csv, test-fixtures.csv
$ python tools/gen_printed.py       # printed parts  -> printed-parts.csv (from the newest cad/*/tree.csv)
$ python tools/gen_part_properties.py ../cad/<export>   # mass properties -> part-properties.csv, joints -> joints.csv
$ python tools/gen_recon.py         # the audit table -> bom-reconciliation.csv
$ python tools/gen_punchlist.py     # TODO blocks    -> docs/reference/todo.md
$ python tools/gen_image_manifest.py# figure gaps    -> docs/assets/MANIFEST.md
```

| Script | Reads | Writes |
| --- | --- | --- |
| `gen_sheet1.py` | `duke-humanoid-v2_BOM_sheet1_main.csv` | `actuators.csv`, `electronics.csv`, `cables-connectors.csv`, `fasteners.csv`, `printed-parts.csv` (the three `MAT_*` rows) |
| `gen_cnc.py` | `duke-humanoid-v2_BOM_sheet2_cnc-parts.csv` | `cnc-parts.csv`, `test-fixtures.csv` |
| `gen_recon.py` | nothing — the audit figures are constants with their provenance | `bom-reconciliation.csv` |
| `audit_sheet2.py` | the machined sheet | nothing; prints the arithmetic check |
| `gen_punchlist.py` | every `!!! missing` and `!!! unverified` block in `docs/` | `docs/reference/todo.md` |
| `gen_image_manifest.py` | figure placeholders in `docs/`, plus `part_id` columns | `docs/assets/MANIFEST.md` |
| `gen_printed.py` | the newest `cad/*/tree.csv` (after `gen_sheet1.py`) | `printed-parts.csv`: one row per printed component of our design in `PRINTED` (torso plates, wrist parts, covers, gripper parts, camera-column parts, end-effector attachment), quantities summed over the left/right Fusion copies, material and process from the Fusion material name only, plus the three material rows |
| `gen_part_properties.py` | `cad/<export>/tree.csv` (+ `print/*.stl` for volume, `joints.csv` from `fusion_export_modules`) | `part-properties.csv`: Fusion mass, bounding box, centre of mass and inertia per site part (inertia about the centre of mass, shifted from Fusion's origin-referenced tensor, and the raw `*_origin` values); `joints.csv`: every joint with limits in degrees |
| `stage_cad_export.py` | a `cad/<export>/` folder from `fusion_export` | copies STEP/STL/overall drawing into `docs/files/` as `<part_id>_rev<NN>.<ext>`; zips a whole-robot STEP over 95 MB; skips the `.f3z` (release asset) |
| `gen_cad_manifest.py` | files under `docs/files/` | `docs/data/cad-files.csv`, `docs/files/SHA256SUMS.txt`; fails on files over GitHub's limits |
| `build_viewer.py` | `cad/<export>/print/*.stl` placed with `transforms.csv`, or a `fusion_export_viewer` folder | `docs/assets/viewer/robot.glb`, `parts.json` for the part viewer on the CAD downloads page |

## Fusion 360 scripts (run inside Fusion: Utilities > Add-Ins > Scripts and Add-Ins)

With `humanoid_2.1_latest` open, in this order, all into one dated folder `cad/humanoid_2.1_latest_<stamp>/`:

| Script | Writes | Notes |
| --- | --- | --- |
| `fusion_export/` | `tree.csv` (every component: `fusion_name`, `file_name`, kind, qty, bodies, children, material, mass, bounding box, linked / out-of-date, path, `color_rgb` and appearance name, centre of mass, moments and products of inertia); `assembly/<design>.step` and `.f3z`; `step/<file_name>.step` and `print/<file_name>.stl` for **every** component with bodies, vendor parts included; `joints.csv` (root only, empty: the joints live in the linked designs); `export.log` when done | `file_name` is unique per component: a second component with the same name is `name~2`. Mass to 0.1 g. **The inertia columns are about the component-frame origin, not the centre of mass** (verified against the STLs); `gen_part_properties.py` shifts them. |
| `fusion_export_modules/` | `modules/<file_name>.step` (one STEP per sub-assembly down to two levels below the root: lower body, torso, arms, gripper; legs, camera columns, wrists, hip / knee / shoulder / elbow modules, electronics tray, and the vendor assemblies at those levels); `modules.csv`; `joints.csv` (every joint of every component: type, the two occurrences, origin and axis **in that component's frame**, limits and value in rad or cm, suppressed flag); `transforms.csv` (every occurrence with bodies: path, name, the `file_name` of `tree.csv`, visible, 4×4 transform to the root in cm, row-major); `export_modules.log` | Pick the same dated folder. Overwrites the root-only `joints.csv`. |
| `fusion_export_transforms/` | `transforms.csv` (old naming) and bodies-only STL/STEP of the `CNC_`/`3DP_` components that carry children | Superseded by `fusion_export` + `fusion_export_modules`; kept for the 14:23 export. |
| `fusion_export_viewer/` | `viewer/context.stl` (whole robot, world coordinates, low resolution), `viewer/parts/NNNN.stl` per occurrence of a releasable part, `occurrences.csv` | Optional: `build_viewer.py` can place `print/*.stl` with `transforms.csv` instead. |

## Three download levels

Everything visible in the Fusion model is downloadable at three levels, all from the dated export folder:

1. **Whole robot** — `assembly/<design>.step` (+ `.f3z` as a release asset), staged into `docs/files/assembly/`.
2. **Module** — `modules/<file_name>.step`, one per sub-assembly (see `modules.csv` for name, path, depth, mass).
3. **Part** — `step/<file_name>.step` and `print/<file_name>.stl` per component with bodies, machined, printed
   and vendor parts alike; `stage_cad_export.py` stages the ones with a site part ID into `docs/files/step/` and
   `docs/files/print/` under that ID.

## Where the BOM source lives

The two spreadsheets the BOM is derived from are **not** in this repository.
The generators look for them in `../reference/bom/` next to the site, and
`BOM_SOURCE_DIR` overrides that:

```console
$ BOM_SOURCE_DIR=/path/to/sheets python tools/gen_cnc.py
```

Every transformation these scripts perform is also written out in prose in the
"Cleanups applied" table on `docs/bom/index.md`, so nothing is lost to a reader
who never runs them. They exist so that a re-sourced price is a one-line edit to
a spreadsheet and a re-run, rather than an afternoon of hand-editing CSVs.

## Rules these scripts enforce

`gen_punchlist.py` **fails** if any TODO block has no `*Owner:*` line. That is
deliberate: an unowned TODO is a wish rather than a work item, and this site's
whole claim is that its holes are tracked.

`gen_cnc.py` and `gen_sheet1.py` never invent a figure. Where the source
arithmetic does not divide exactly, the derived unit cost is left blank rather
than rounded into something a reader's recomputation would contradict.

`gen_printed.py` and `gen_part_properties.py` never guess a material or a
value: a custom Fusion material name gives a blank cell and a note, a component
that carries child components gets no own mass, and an inertia the export's
0.1 g mass rounding cannot support is left blank with the bound in `notes`.

## Generated files — never hand-edit

`docs/data/*.csv` (all of them, including `part-properties.csv`, `joints.csv`, `cad-files.csv`),
`docs/reference/todo.md`, `docs/assets/MANIFEST.md`, `docs/files/SHA256SUMS.txt`, `docs/assets/viewer/*`.
Change the source (spreadsheet, Fusion model, page text) and re-run the generator.

## After running any of them

```console
$ python -m mkdocs build --strict
```

The build must exit 0 with no `WARNING` line. The one expected `INFO` is that
`data/README.md` and `assets/MANIFEST.md` are outside the nav, which they are on
purpose.
