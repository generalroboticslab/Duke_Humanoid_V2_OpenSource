# CAD downloads

Download the manufacturing files. Each part's files are also linked from its row in the parts lists.

!!! abstract "At a glance"
    - **You will:** download the files for the parts you are making, and check them.
    - **Parts lists:** [CNC parts](../bom/cnc-parts.md) · [Printed parts](../bom/printed-parts.md).
    - **Before this:** [Bill of materials](../bom/index.md).

## Files

{% if cad_count() %}
Files are named `<part_id>_rev<NN>`, matching the parts lists. Left and right parts are separate files.

### Parts (STEP)

For machining, or to edit or re-mesh a part.

{{ cad_table("step") }}

### Printable meshes (3MF / STL)

Open in your slicer. Units are millimetres.

{{ cad_table("print") }}

### Drawings (PDF)

Send with the STEP to the machine shop.

{{ cad_table("drawings") }}

### Ready-to-print plates

Slicer projects with orientation, supports and settings already set.

{{ cad_table("plates") }}

### Whole robot

Assembly STEP, and the Fusion 360 archive (`.f3z`) for editing.

{{ cad_table("assembly") }}

Checksums for every file: [SHA256SUMS.txt](../files/SHA256SUMS.txt){ download="" }.
{% else %}
!!! missing "MISSING — SAFETY — no manufacturing CAD published: per-part STEP, printable 3MF/STL, PDF drawings, whole-robot STEP and Fusion 360 archive"
    *Owner: hardware lead.*
{% endif %}

All STEP files are AP214 (`AUTOMOTIVE_DESIGN`), written by Fusion 360 build 2705.1.15 from the
`humanoid_2.1_latest` design. The whole-robot STEP is zipped because it is over GitHub's file-size limit.

The native Fusion 360 archive is too large for this repository and is published as a release asset:

| File | Size | SHA-256 |
| --- | ---: | --- |
| [humanoid_2.1_latest.f3z](https://github.com/rivery927/Duke_Humanoid_V2_OpenSource/releases/download/cad-v2.1-rc1/humanoid_2.1_latest.f3z) (101 linked designs included, release `cad-v2.1-rc1`) | 319 MB | `f440621df68f0775f521c87d02f8a644ae0a65f64ef76b385fdd2bc22a04d420` |

Known CAD errors are listed in the [CNC guide](cnc-guide.md#known-cad-errors). No hardware or
documentation licence is declared yet ([Citation and licence](../reference/citation-and-license.md)).

## Not manufacturing files

The code repository also holds simulation meshes (`simulation/asset/duke_v2/`) and camera-calibration
fixtures (`deploy/perception/asset/*.step`). Meshes carry no tolerance, thread, finish or material:
**never send them to a shop**. `cartesian_hand_v3/` is not on this robot.

## Check a download

1. Hash the file:

    ```bash
    shasum -a 256 <file>
    ```

2. Compare the result with that file's line in `SHA256SUMS.txt`. If it differs, download the file again.

3. Write the `_revNN` of every file you use into your build log.

✅ **Check:** every file matches its checksum before anything goes to a shop.
