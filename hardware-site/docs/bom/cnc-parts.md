# CNC parts

{{ bom_count("cnc-parts.csv") }} machined part rows, {{ bom_subtotal("cnc-parts.csv") }}.
**Qty** and **Unit cost** are the team BOM's; **Team ref** is its line.


## Leg

{{ bom_count("cnc-parts.csv", subassembly="leg") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Files |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "leg" %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Leg subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}** | |

## Arm

{{ bom_count("cnc-parts.csv", subassembly="arm") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Files |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "arm" %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Arm subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}** | |

## Body

{{ bom_count("cnc-parts.csv", subassembly="body") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Files |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "body" %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Body subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}** | |

## Summary

**Machined total: {{ bom_subtotal("cnc-parts.csv") }}.** Raw data, every column:
[cnc-parts.csv](../data/cnc-parts.csv). Make them with the
[CNC guide](../fabrication/index.md#cnc-guide); check them with
[Incoming inspection](../fabrication/index.md#incoming-inspection).

The part IDs are the Fusion component names without their `_x<qty>` token, so every row with a
download link is checked against the CAD. Fusion occurrence counts per robot: `leg02` 7, `leg03` 5,
`leg09` 2, `leg10` 2, `leg11` 2, `leg12` 4, `arm04` 4, `arm10` 4, `body04` 4, all other linked rows 2 (body plates 1).

!!! note "Build to the model — five rows have no team BOM line"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    `CNC_leg18_foot_plate` is a separate doubt: Fusion holds it as a subassembly with
    the sole as a child component, so its CAD mass is not the plate's own.
    *Owner: hardware lead.*

**Flags:**

- *not in the team BOM*: the team BOM has no line for this part, so it has no price and no quantity.
- *open question*: the row's `notes` carry a question the sources do not settle — its count, its price, or whether the part exists.
- *no price*: no unit cost in the team BOM.

The team BOM names its machined lines by function (`Hip 1 Motor Bracket`, `Foot`), not by part ID. Every
row above is paired with its line by the team's exploded-view booklet, which labels each assembly with the
spreadsheet's own ids, plus the line's quantity and price; `C27` *Shoulder/Elbow Coupler* is the round dished
cover drawn once in the shoulder and once in the elbow joint stack (booklet p.9, two per arm), which the CAD
calls a back cover — one part under two names.

`C4` *Robstride 03 Bearing Retainer* ×5 and `C5` *Robstride 03 Output Shaft* ×7 are the ring and the square
coupler on the output of the waist actuator (p.4, the unlabelled actuator marked *Body*), of hip 1 and hip 3
on each leg, and (`C5` only) of the shoulder-1 actuator on each arm: five and seven positions, the sheet's
counts. One question the booklet cannot answer:

!!! note "Build to the model — `C25` unit price looks doubled in the team sheet"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    The part itself is settled: booklet p.9 labels the same bracket at the shoulder and at
    the elbow of each arm, which is the Fusion component
    `CNC_arm04_x4_shoulder_elbow_support_shaft` and this line's count of 4.
    *Owner: BOM owner.*
