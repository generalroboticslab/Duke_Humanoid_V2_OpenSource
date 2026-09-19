# tools/

Everything in `docs/data/` and two of the pages in `docs/` are **derived**, not
written. This directory holds the derivations, so that the published data can be
reproduced from its source and the published lists cannot drift away from the
pages they describe.

Run them from the site root with the site's virtualenv:

```console
$ python tools/gen_sheet1.py        # bought parts  -> docs/data/*.csv
$ python tools/gen_cnc.py           # machined parts -> cnc-parts.csv, test-fixtures.csv
$ python tools/gen_recon.py         # the audit table -> bom-reconciliation.csv
$ python tools/gen_punchlist.py     # TODO blocks    -> docs/reference/todo.md
$ python tools/gen_image_manifest.py# figure gaps    -> docs/assets/MANIFEST.md
```

| Script | Reads | Writes |
| --- | --- | --- |
| `gen_sheet1.py` | `duke-humanoid-v2_BOM_sheet1_main.csv` | `actuators.csv`, `electronics.csv`, `cables-connectors.csv`, `fasteners.csv`, `printed-parts.csv` |
| `gen_cnc.py` | `duke-humanoid-v2_BOM_sheet2_cnc-parts.csv` | `cnc-parts.csv`, `test-fixtures.csv` |
| `gen_recon.py` | nothing — the audit figures are constants with their provenance | `bom-reconciliation.csv` |
| `audit_sheet2.py` | the machined sheet | nothing; prints the arithmetic check |
| `gen_punchlist.py` | every `!!! missing` and `!!! unverified` block in `docs/` | `docs/reference/todo.md` |
| `gen_image_manifest.py` | figure placeholders in `docs/`, plus `part_id` columns | `docs/assets/MANIFEST.md` |
| `gen_printed.py` | the newest `cad/*/tree.csv` (after `gen_sheet1.py`) | `printed-parts.csv`: one row per printed Fusion component, plus the three material rows |
| `stage_cad_export.py` | a `cad/<export>/` folder from `fusion_export` | copies STEP/STL/overall drawing into `docs/files/` as `<part_id>_rev01.<ext>`; zips a whole-robot STEP over 95 MB; skips the `.f3z` (release asset) |
| `fusion_export/` | the open Fusion 360 design (run it *inside* Fusion: Utilities > Add-Ins > Scripts) | `tree.csv` (every component: qty, material, mass, size), whole-robot STEP + `.f3z`, one STEP and STL per leaf part, into a dated folder you choose. Rename to `<part_id>_rev01.<ext>`, copy into `docs/files/`, then run `gen_cad_manifest.py` |
| `gen_cad_manifest.py` | files under `docs/files/` | `docs/data/cad-files.csv`, `docs/files/SHA256SUMS.txt`; fails on files over GitHub's limits |

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

## After running any of them

```console
$ python -m mkdocs build --strict
```

The build must exit 0 with no `WARNING` line. The one expected `INFO` is that
`data/README.md` and `assets/MANIFEST.md` are outside the nav, which they are on
purpose.
