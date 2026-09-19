# CNC parts

{{ bom_count("cnc-parts.csv") }} machined part rows, {{ bom_subtotal("cnc-parts.csv") }};
**Qty** is the lot each price was quoted for, not a count checked against CAD
**UNVERIFIED**{ .dh-unverified }.

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/part-index.md#mass-properties).

## Leg

{{ bom_count("cnc-parts.csv", subassembly="leg") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}.

| Part ID | Description | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "leg" %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }}{{ " **UNVERIFIED**{ .dh-unverified }" if ("QUANTITY CONFLICT" in r.notes or "DEDUPED" in r.notes) else "" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ money(r.total_cost_usd|float) }} | {{ (("qty conflict; " if "QUANTITY CONFLICT" in r.notes else "") ~ ("not in team list; " if ("Legacy numbering" in r.notes or "B-series" in r.notes) else "") ~ ("no unit cost; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Leg subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}** | | | |

## Arm

{{ bom_count("cnc-parts.csv", subassembly="arm") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}.

| Part ID | Description | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "arm" %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }}{{ " **UNVERIFIED**{ .dh-unverified }" if ("QUANTITY CONFLICT" in r.notes or "DEDUPED" in r.notes) else "" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ money(r.total_cost_usd|float) }} | {{ (("qty conflict; " if "QUANTITY CONFLICT" in r.notes else "") ~ ("not in team list; " if ("Legacy numbering" in r.notes or "B-series" in r.notes) else "") ~ ("no unit cost; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Arm subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}** | | | |

## Body

{{ bom_count("cnc-parts.csv", subassembly="body") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}.

| Part ID | Description | Qty | Unit cost | Line total | Flags | Mass / size | Files |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "body" %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }}{{ " **UNVERIFIED**{ .dh-unverified }" if ("QUANTITY CONFLICT" in r.notes or "DEDUPED" in r.notes) else "" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ money(r.total_cost_usd|float) }} | {{ (("qty conflict; " if "QUANTITY CONFLICT" in r.notes else "") ~ ("not in team list; " if ("Legacy numbering" in r.notes or "B-series" in r.notes) else "") ~ ("no unit cost; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Body subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}** | | | |

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

!!! unverified "UNVERIFIED — `CNC_arm12_wrist_pitch` is in the machining quote but not in the Fusion model; `CNC_arm06_RS02_shaft_coupler` is in Fusion only as the printed `3DP_arm06` (see Printed parts); `CNC_leg18_foot_plate` is in Fusion as a subassembly with the sole as a child component, so its CAD mass is not the plate's own; `CNC_arm05` and `CNC_arm11` are quoted as machined but are SLS nylon in Fusion (see Printed parts)"
    *Owner: hardware lead.*

**Flags:**

- *qty conflict*: the source part name gives a different count.
- *not in team list*: absent from the team's 32-part CNC list; may duplicate a current part.
- *no unit cost*: the lot price does not divide evenly.

!!! unverified "UNVERIFIED — the team's 32-part CNC list names `arm05`–`arm10` shifted by one ID from the Fusion names used here; the *not in team list* rows (`01_…`–`22_…`, `B1`–`B5`) are in neither the team list nor the Fusion model and are probably an older numbering of the same parts"
    *Owner: hardware lead.*
