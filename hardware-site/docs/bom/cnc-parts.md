# CNC parts

{{ bom_count("cnc-parts.csv") }} machined part rows, {{ bom_subtotal("cnc-parts.csv") }}.
**Qty** and **Unit cost** are the team BOM's; **Team ref** is its line.
{{ bom_unpriced_count("cnc-parts.csv") }} rows have no team BOM line, so no price and no quantity, and read
**TODO**{ .dh-missing } rather than zero: {{ bom_unpriced("cnc-parts.csv") }}.

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/part-index.md#mass-properties).

## Leg

{{ bom_count("cnc-parts.csv", subassembly="leg") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "leg" %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ (("not in the team BOM; " if "Not in the team BOM" in r.notes else "") ~ ("open question; " if "UNVERIFIED" in r.notes else "") ~ ("no price; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Leg subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}** | | | |

## Arm

{{ bom_count("cnc-parts.csv", subassembly="arm") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "arm" %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ (("not in the team BOM; " if "Not in the team BOM" in r.notes else "") ~ ("open question; " if "UNVERIFIED" in r.notes else "") ~ ("no price; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Arm subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}** | | | |

## Body

{{ bom_count("cnc-parts.csv", subassembly="body") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "body" %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ (("not in the team BOM; " if "Not in the team BOM" in r.notes else "") ~ ("open question; " if "UNVERIFIED" in r.notes else "") ~ ("no price; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Body subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}** | | | |

## Summary

**Machined total: {{ bom_subtotal("cnc-parts.csv") }}.** Raw data, every column:
[cnc-parts.csv](../data/cnc-parts.csv). Make them with the
[CNC guide](../fabrication/cnc-guide.md); check them with
[Incoming inspection](../fabrication/incoming-inspection.md).

The part IDs are the Fusion component names without their `_x<qty>` token, so every row with a
download link is checked against the CAD. Fusion occurrence counts per robot: `leg02` 7, `leg03` 5,
`leg09` 2, `leg10` 2, `leg11` 2, `leg12` 4, `arm04` 4, `arm10` 4, `body04` 4, all other linked rows 2 (body plates 1).
Rows with no download link and no mass / size are not in the Fusion model. `CNC_arm13_RS05_shaft_coupler` sits in
the gripper assembly (`dovetail_umi_gripper`) in Fusion: it is the gripper's mounting flange, the code repo's
`cnc_flange` (Aluminum 6061, 22.05 g in `parallel_gripper_fusion_info.py`; 22.1 g here).

!!! unverified "UNVERIFIED — whether the five rows with no team BOM line are machined parts at all: the team's booklet draws `CNC_arm05`, `CNC_arm06` and `CNC_arm11` as the printed lines `P4`, `P5` and `P6` on p.9, and Fusion has them as SLS nylon, so all three are listed again under Printed parts; `CNC_arm12_wrist_pitch` is absent from the team BOM, the booklet and the Fusion model alike; `CNC_arm13_RS05_shaft_coupler` is the gripper's machined flange inside `dovetail_umi_gripper` and the booklet's gripper page does not label it"
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

!!! unverified "UNVERIFIED — the unit price of `C25` *Shoulder/Elbow Support* ×4: the team BOM's 57.56 is exactly twice the earlier machining quote's 28.78 for the same part, and the team BOM's is the price shown above"
    The part itself is settled: booklet p.9 labels the same bracket at the shoulder and at
    the elbow of each arm, which is the Fusion component
    `CNC_arm04_x4_shoulder_elbow_support_shaft` and this line's count of 4.
    *Owner: BOM owner.*
