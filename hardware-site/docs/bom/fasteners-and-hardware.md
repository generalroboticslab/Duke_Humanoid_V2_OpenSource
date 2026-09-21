# Fasteners and hardware

The team BOM lists {{ bom_count("fasteners.csv") }} hardware lines — six bearing sizes (Amazon) and three Torx button-head screw sizes (McMaster-Carr) — totalling {{ bom_subtotal("fasteners.csv") }}.

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/fasteners.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ "[" ~ r.vendor ~ "](" ~ r.vendor_url ~ ")" if r.vendor else "**TODO**{ .dh-missing }" }} |
{% endfor %}

**Team ref** is the team BOM line. Screw lines are counted as bought from McMaster-Carr (packs), not as pieces on the robot. Nuts, washers, dowel pins, retaining rings, shims and threadlocker are not in the team BOM.

| Item | Specification |
| --- | --- |
| Screws | Torx button-head. Team BOM: M3x10, M4x8, M4x10. Team design log: M4x12 (McMaster-Carr 90991A123) and M3x12 (90991A115) **UNVERIFIED**{ .dh-unverified } |
| Exception | M5 on the Motor04 shaft and the knee. The published CAD has M4 clearance there; enlarge to Ø5.3 mm at the machinist — see [CNC guide](../fabrication/index.md#known-cad-errors) |
| Thread engagement | At least 4 mm of usable thread, 6 mm preferred |
| Main bearing | 50 × 65 × 7 mm, 2 off (team BOM line `H1`; the Fusion model has two `bearing_50x65x7_6810_6.1kN_52g`). No part number in the team BOM **TODO**{ .dh-missing }; the team design log models McMaster-Carr 6656K229 |
| Ankle thrust bearing | Not specified **UNVERIFIED**{ .dh-unverified } |
| Threadlocker | Loctite 222 (removable) |

*Source: team design log, "Hardware Choice" and CNC checklist.*

!!! note "Read off the model — every screw, bearing and fit per location"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
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

!!! note "Build to the model — it places 26 of the 35 × 44 × 5 mm bearing, the team sheet buys 18"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    The other four bearing lines agree with the Fusion model, where each bearing is a
    `bearing_<size>` subassembly of two halves: `H0` 13, `H1` 2, `H3` 4, `H4` 2. No bearing
    line carries a part number or link.
    *Owner: hardware lead.*

!!! note "Yours to choose — bearing retaining compound and grease; the site specifies Loctite 222 for threads"
    *Owner: hardware lead.*
