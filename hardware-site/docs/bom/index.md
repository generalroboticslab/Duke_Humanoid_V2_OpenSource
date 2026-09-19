# Bill of materials

Everything in one robot, computed from the CSVs below; *not yet published* means no data exists yet.

| Tier | Category | Covers | Subtotal |
| --- | --- | --- | --- |
| **Robot** | [Actuators](actuators.md) | {{ bom_qty("actuators.csv") }} RobStride units, {{ bom_count("actuators.csv") }} models | {{ bom_subtotal("actuators.csv") }} |
| | [Electronics](electronics.md) | Computer, battery, power conversion, Controller Area Network (CAN) adapters, inertial measurement unit (IMU), cameras | {{ bom_subtotal("electronics.csv") }} |
| | [CNC parts](cnc-parts.md) | {{ bom_count("cnc-parts.csv") }} machined part rows; quoted lots, not CAD counts **UNVERIFIED**{ .dh-unverified } | {{ bom_subtotal("cnc-parts.csv") }} |
| | [Cables and connectors](cables-and-connectors.md) | Harness material | {{ bom_subtotal("cables-connectors.csv") }} |
| | [Fasteners and hardware](fasteners-and-hardware.md) | Fasteners, bearings, hardware standard; no schedule yet **TODO**{ .dh-missing } | {{ bom_subtotal("fasteners.csv") }} |
| | [Printed parts](printed-parts.md) | Fused-deposition (FDM) and laser-sintered (SLS) prints; no part list yet **TODO**{ .dh-missing } | {{ bom_subtotal("printed-parts.csv") }} |
| | **Robot subtotal (a floor, not a price)** | | **{{ bom_total() }}** |
| **Tools** | Tools a builder must own **TODO**{ .dh-missing } | | {{ bom_subtotal("tools.csv") }} |
| **Optional** | Third camera module (~$600 **UNVERIFIED**{ .dh-unverified }), spares, upgrades **TODO**{ .dh-missing } | | {{ bom_subtotal("optional.csv") }} |

- The robot subtotal excludes fasteners and bearings, printed parts, bulk wire, tools, shipping, duty and labour ([Cost and time](../before-you-start/cost-and-time.md)).
- No price is dated; order sequence, vendors and alternates: [Sourcing](sourcing.md).

!!! missing "MISSING — allowance for tax, scrap and re-machining in the robot cost"
    *Owner: hardware lead.*

**Data files:**
[actuators.csv](../data/actuators.csv) ·
[electronics.csv](../data/electronics.csv) ·
[cnc-parts.csv](../data/cnc-parts.csv) ·
[cables-connectors.csv](../data/cables-connectors.csv) ·
[fasteners.csv](../data/fasteners.csv) ·
[printed-parts.csv](../data/printed-parts.csv)
