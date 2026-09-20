# CNC parts

{{ bom_count("cnc-parts.csv") }} machined part rows, {{ bom_subtotal("cnc-parts.csv") }}.
**Qty** and **Unit cost** are the team BOM's. **Team ref** is the line they come
from in the team BOM spreadsheet (`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`,
2026-09-19); the row's `notes` in [cnc-parts.csv](../data/cnc-parts.csv) quote
that line in full. {{ bom_unpriced_count("cnc-parts.csv") }} rows have no team
BOM line and so no price and no quantity, and read
**TODO**{ .dh-missing } rather than zero: {{ bom_unpriced("cnc-parts.csv") }}.

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/part-index.md#mass-properties).

## Leg

{{ bom_count("cnc-parts.csv", subassembly="leg") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}.

| Part ID | Description | Team ref | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "leg" %}| `{{ r.part_id }}` | {{ r.description }} | {{ team_ref_cell(r) }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ (("not in the team BOM; " if "Not in the team BOM" in r.notes else "") ~ ("match unverified; " if "UNVERIFIED" in r.notes else "") ~ ("no price; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Leg subtotal** | | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}** | | | |

## Arm

{{ bom_count("cnc-parts.csv", subassembly="arm") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}.

| Part ID | Description | Team ref | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "arm" %}| `{{ r.part_id }}` | {{ r.description }} | {{ team_ref_cell(r) }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ (("not in the team BOM; " if "Not in the team BOM" in r.notes else "") ~ ("match unverified; " if "UNVERIFIED" in r.notes else "") ~ ("no price; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Arm subtotal** | | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}** | | | |

## Body

{{ bom_count("cnc-parts.csv", subassembly="body") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}.

| Part ID | Description | Team ref | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "body" %}| `{{ r.part_id }}` | {{ r.description }} | {{ team_ref_cell(r) }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ (("not in the team BOM; " if "Not in the team BOM" in r.notes else "") ~ ("match unverified; " if "UNVERIFIED" in r.notes else "") ~ ("no price; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Body subtotal** | | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}** | | | |

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

!!! unverified "UNVERIFIED — whether the five rows with no team BOM line are machined parts at all: `CNC_arm05`, `CNC_arm06` and `CNC_arm11` are SLS nylon in Fusion and are listed again under Printed parts, `CNC_arm12_wrist_pitch` is in neither the team BOM nor the Fusion model, and `CNC_arm13_RS05_shaft_coupler` is the gripper's machined flange inside `dovetail_umi_gripper`"
    `CNC_leg18_foot_plate` is a separate doubt: Fusion holds it as a subassembly with
    the sole as a child component, so its CAD mass is not the plate's own.
    *Owner: hardware lead.*

**Flags:**

- *not in the team BOM*: the team BOM has no line for this part, so it has no price and no quantity.
- *match unverified*: the team BOM line and this part ID agree on price and count but not on the name.
- *no price*: no unit cost in the team BOM.

!!! unverified "UNVERIFIED — the team BOM names its machined lines by function (`Hip 1 Motor Bracket`, `Foot`), not by part ID, so every row above is paired with its line by name, quantity and price together, and two pairings are not confirmed by all three"
    - `C25` *Shoulder/Elbow Support* ×4 → `CNC_arm04_shoulder_roll_support_shaft`, whose
      Fusion component is `CNC_arm04_x4_shoulder_elbow_support_shaft`: the count matches and
      the names are the same words, but the team BOM's unit price is exactly twice the
      earlier machining quote's for this part; the team BOM's price is the one shown.
    - `C27` *Shoulder/Elbow Coupler* ×4 → `CNC_arm10_r03_back_cover`: price and count match
      the earlier machining quote exactly, but the team calls it a coupler and the CAD a back
      cover. One part under two names, or two parts?
    *Owner: hardware lead.*
