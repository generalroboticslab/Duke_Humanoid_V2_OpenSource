# Bill of materials

Everything in one robot, computed from the CSVs below; *not yet published* means no data exists yet.

The parts lists come from one file: the team's BOM spreadsheet
`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx` (2026-09-19, work in progress),
which is the list the reference robot was bought and built from. `tools/gen_bom.py`
writes the six CSVs from it: it keeps the sheet's own item text, quantity and
price, maps each line to the part ID the CAD export and the 3D viewer use, and
records the sheet line each row came from in a `team_ref` column
(`E3`, `C21`, `P20`, `H1`), which every table below shows.
[team-map.csv](../data/team-map.csv) is the same mapping the other way round:
one row per team BOM line, the CAD part it is, the team and CAD quantities, and
the page of the team's exploded-view booklet that settles it.

| Tier | Category | Covers | Subtotal |
| --- | --- | --- | --- |
| **Robot** | [Actuators](actuators.md) | {{ bom_qty("actuators.csv") }} RobStride units, {{ bom_count("actuators.csv") }} models | {{ bom_subtotal("actuators.csv") }} |
| | [Electronics](electronics.md) | Computer, battery, power conversion, Controller Area Network (CAN) adapters, inertial measurement unit (IMU), cameras | {{ bom_subtotal("electronics.csv") }} |
| | [CNC parts](cnc-parts.md) | {{ bom_count("cnc-parts.csv") }} machined part rows, {{ bom_unpriced_count("cnc-parts.csv") }} of them with no team BOM line and no price **TODO**{ .dh-missing } | {{ bom_subtotal("cnc-parts.csv") }} |
| | [Cables and connectors](cables-and-connectors.md) | Harness material: the team BOM has one cable line and no connector, sleeving or bulk-wire line **TODO**{ .dh-missing } | {{ bom_subtotal("cables-connectors.csv") }} |
| | [Fasteners and hardware](fasteners-and-hardware.md) | {{ bom_count("fasteners.csv") }} bearing and screw lines, none priced; no fastener schedule yet **TODO**{ .dh-missing } | {{ bom_subtotal("fasteners.csv") }} |
| | [Printed parts](printed-parts.md) | {{ bom_count("printed-parts.csv") }} rows of fused-deposition (FDM) and laser-sintered (SLS) prints; the team BOM prices the nylon and torso parts only **TODO**{ .dh-missing } | {{ bom_subtotal("printed-parts.csv") }} |
| | **Robot subtotal (a floor, not a price)** | | **{{ bom_total() }}** |
| **Tools** | Listed with specifications on [Tools](../assembly/tools.md); not priced, because what you already own decides the cost | | — |
| **Optional** | A third camera module, spares and upgrades; quote them from the same vendors as the parts they duplicate | | — |

- {{ bom_unpriced_count() }} of the {{ bom_row_count() }} rows carry no usable unit cost: the team BOM prices the line at `0`, leaves it blank, or has no line for the part. They read **TODO**{ .dh-missing } wherever a price would go, never `$0.00`, and no subtotal above includes them.
- The robot subtotal therefore excludes every bearing and screw, most printed parts, bulk wire, tools, shipping, duty and labour ([Cost and time](../before-you-start/cost-and-time.md)).
- Prices are the team BOM's as of {{ bom_priced_as_of("actuators.csv") }}; order sequence, vendors and alternates: [Sourcing](sourcing.md).

!!! missing "MISSING — a unit price for every unpriced team BOM row: all nine bearing and screw lines, every printed part except the ten the sheet prices by weight, and the five machined parts the sheet has no line for"
    The sheet carries a `0` or an empty cell there, so every table on this site shows a red
    TODO in their place rather than a zero, and no robot cost on this site is a complete one.
    *Owner: BOM owner.*

!!! note "Yours to determine — allowance for tax, scrap and re-machining in the robot cost"
    *Owner: hardware lead.*

**Data files:**
[actuators.csv](../data/actuators.csv) ·
[electronics.csv](../data/electronics.csv) ·
[cnc-parts.csv](../data/cnc-parts.csv) ·
[cables-connectors.csv](../data/cables-connectors.csv) ·
[fasteners.csv](../data/fasteners.csv) ·
[printed-parts.csv](../data/printed-parts.csv) ·
[team-map.csv](../data/team-map.csv)
