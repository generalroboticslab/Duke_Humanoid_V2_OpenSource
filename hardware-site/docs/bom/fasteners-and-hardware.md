# Fasteners and hardware

The team BOM lists {{ bom_count("fasteners.csv") }} hardware lines, six bearing
sizes and three screw sizes, and prices none of them, so every cost cell reads
**TODO**{ .dh-missing } and this category reads
{{ bom_subtotal("fasteners.csv") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/fasteners.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ "[" ~ r.vendor ~ "](" ~ r.vendor_url ~ ")" if r.vendor else "**TODO**{ .dh-missing }" }} |
{% endfor %}

**Team ref** is the team BOM line. No line there
carries a price, a vendor or a link, and the three screw lines carry no
quantity either, so those cells read TODO rather than zero. Nuts, washers,
dowel pins, retaining rings, shims and threadlocker are not in the team BOM at
all.

| Item | Specification |
| --- | --- |
| Screws | Torx button-head. Team BOM: M3x10, M4x8, M4x10. Team design log: M4x12 (McMaster-Carr 90991A123) and M3x12 (90991A115) **UNVERIFIED**{ .dh-unverified } |
| Exception | M5 on the Motor04 shaft and the knee, where the CAD has M4 **UNVERIFIED**{ .dh-unverified }; see [CNC guide](../fabrication/cnc-guide.md#known-cad-errors) |
| Thread engagement | At least 4 mm of usable thread, 6 mm preferred |
| Main bearing | 50 × 65 × 7 mm, 2 off (team BOM line `H1`; the Fusion model has two `bearing_50x65x7_6810_6.1kN_52g`). No part number in the team BOM **TODO**{ .dh-missing }; the team design log models McMaster-Carr 6656K229 |
| Ankle thrust bearing | Not specified **UNVERIFIED**{ .dh-unverified } |
| Threadlocker | Loctite 222 (removable) |

*Source: team design log, "Hardware Choice" and CNC checklist.*

!!! missing "MISSING — SAFETY — fastener schedule from CAD: every screw (thread, length, head, drive, qty), bearings and fits per location, dowel pins, retaining rings, shims, threadlocker locations, torque per size and joint, purchase links"
    *Owner: hardware lead, from the CAD. Blocks every page under [Assembly](../assembly/index.md).*

## Screwing into an actuator

RS03 mounting interface (RobStride 03 manual §1.1):

| Face | Features |
| --- | --- |
| Housing | 8 × M4, 8 mm deep, equally spaced on Ø98 ±0.2 mm |
| Output | 6 × M4 blind, 6 mm deep, and 3 × Ø4 (+0.1/0) blind, 7 mm deep, on Ø30.36 ±0.2 mm |
| Pilot | Ø70 (0/−0.1), 2.5 mm proud of the housing |

Never drive a screw deeper than the actuator's thread depth (RS02/03/04
manuals). Check every screw that goes into an actuator.

!!! unverified "UNVERIFIED — the 35 × 44 × 5 mm bearing count: team BOM line `H2` buys 18, the Fusion model places 26 `bearing_35x44x5_6707_1.6kN_15g` (at least one of them inside the RobStride 06 actuator model, so not every occurrence need be a bought part); and the 10 × 15 × 4 mm bearing (`H5`, 2 off) has no component named for it in Fusion"
    The other four bearing lines agree with the Fusion model, where each bearing is a
    `bearing_<size>` subassembly of two halves: `H0` 13, `H1` 2, `H3` 4, `H4` 2. No bearing
    line carries a part number or link.
    *Owner: hardware lead.*

!!! missing "MISSING — retaining compound and grease type per bearing and sliding surface"
    *Owner: hardware lead.*
