# Fasteners and hardware

No fastener schedule exists yet: `fasteners.csv` holds one placeholder row, so
this category reads {{ bom_subtotal("fasteners.csv") }}.

| Item | Specification |
| --- | --- |
| Screws | Torx button-head M4x12 (McMaster-Carr 90991A123) and M3x12 (90991A115) |
| Exception | M5 on the Motor04 shaft and the knee, where the CAD has M4 **UNVERIFIED**{ .dh-unverified }; see [CNC guide](../fabrication/cnc-guide.md#known-cad-errors) |
| Thread engagement | At least 4 mm of usable thread, 6 mm preferred |
| Main bearing | 50 × 65 × 7 mm (CAD model: McMaster-Carr 6656K229) |
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

!!! missing "MISSING — retaining compound and grease type per bearing and sliding surface"
    *Owner: hardware lead.*
