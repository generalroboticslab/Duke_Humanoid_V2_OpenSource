# Printing guide

Print PLA and TPU by fused deposition (FDM) and nylon powder by laser
sintering (SLS).

!!! abstract "At a glance"
    - **You will:** print a test part, then the set.
    - **Parts:** [Printed parts](../bom/printed-parts.md).
    - **Files:** a 3MF per part in the Files column of [Printed parts](../bom/printed-parts.md), all on [CAD downloads](cad-downloads.md).
    - **Before this:** [CNC guide](cnc-guide.md).

## Print profiles

{% if data_file_exists("print_profiles.csv") %}
{{ read_csv('data/print_profiles.csv') }}
{% else %}
!!! note "Yours to determine — print profile per part: layer height, walls, infill, orientation"
    *Owner: hardware lead, from the printer the reference build used.*
{% endif %}

!!! note "Yours to determine — material settings for your printer and filament"
    *Owner: hardware lead.*

## Which process each part takes

The `Process` and `Material` columns on
[Printed parts](../bom/printed-parts.md) carry the assignment for every part:
**40 parts are FDM** (PLA and TPU) and **seven are SLS** in nylon 12.

The seven SLS parts are the drivetrain parts — every one of them transmits
actuator torque or carries a bearing:

| Part | Qty |
| --- | ---: |
| `3DP_arm05_RS02_shaft_bearing_retainer` | 4 |
| `3DP_arm06_RS02_shaft_coupler` | 2 |
| `3DP_arm11_wrist_roll` | 2 |
| `3DP_arm14_wrist_block` | 2 |
| `3DP_arm15_end_effector_attachment` | 2 |
| `3DP_grip05_pinion` | 2 |

Print these in SLS nylon. The remaining parts are covers, mounts and TPU pads,
and FDM is what the reference robot used for all of them.

!!! note "Not tested on the reference robot — an FDM substitute for any of the seven SLS parts"
    They were printed SLS and never tried in FDM, so no substitute material or
    wall schedule is published. *Owner: hardware lead.*

## Print the parts

1. Print one small fit-critical part: one that mates with a machined part or
   takes a heat-set insert.
2. Print the full set.

✅ **Check:** the test part matches the drawing before step 2.

## Post-process

<figure markdown>
  ![Soldering iron setting a heat-set insert in a printed battery holder](../assets/photos/body-heat-set-inserts.webp){ loading=lazy width="400" }
  <figcaption>Heat-set inserts melted into a printed battery holder with a soldering iron.</figcaption>
</figure>

!!! note "Yours to determine — post-processing: support removal, reaming, heat-set insert fitting"
    *Owner: hardware lead.*

Next: [Incoming inspection](incoming-inspection.md#check-printed-parts).
