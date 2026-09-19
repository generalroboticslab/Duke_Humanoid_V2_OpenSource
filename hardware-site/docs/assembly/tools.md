# Tools

Gather these before the first assembly step.

!!! abstract "At a glance"
    - **You will:** count every fastener into a divided tray by size; a leftover means a missed step.
    - **Before this:** [Incoming inspection](../fabrication/incoming-inspection.md).

Tools subtotal: {{ bom_subtotal("tools.csv") }} — `tools.csv` is not written
yet **TODO**{ .dh-missing }.

!!! unverified "UNVERIFIED — tool list derived from the parts list, not checked against a build"
    *Owner: hardware lead, from the first documented build.*

## Required

| Tool | Use | Specification |
| --- | --- | --- |
| Torx drivers | Torx button-head M4x12 and M3x12 screws | Sizes **TODO**{ .dh-missing } |
| Torque driver | Every torqued screw | Range **TODO**{ .dh-missing } |
| Soldering iron and solder | XT30 solder cups; heat-set inserts in printed parts | About 480 °C for XT30 cups |
| Heat gun, heat-shrink | Over soldered joints | Sized over XT30 joints |
| Wire strippers, flush cutters | Harness | Gauges per [Harness fabrication](../electrical/harness-fabrication.md) |
| Crimp tool | Signal connectors | **TODO**{ .dh-missing } |
| Multimeter | Continuity, polarity, voltage | Any |
| Hoist or gantry, sling | Lifting the robot; hanging it legs straight | Rated well above 36 kg |
| Limb stand or jig | Holding a limb | **TODO**{ .dh-missing } |
| Lithium-polymer (LiPo) balance charger | Two 6S 10000 mAh packs | 6S, balance leads to match |
| Fire-rated LiPo bag | Charging and storing packs | Fits one pack |
| Linux computer | Setting IDs on the bench | See [Software](../software.md) |
| USB to Controller Area Network adapter, servo board | Bench ID setting | The robot's own units |

## Consumables

| Item | Specification |
| --- | --- |
| Threadlocker | Loctite 222 (removable). Never a stronger grade |
| Cable ties and anchors | **TODO**{ .dh-missing } |
| Masking tape, marker | Label every actuator before it goes into a limb |
| Isopropyl alcohol, wipes | Clean cutting fluid off machined parts |
| Cut-resistant gloves | Freshly machined aluminium |

**Optional:** soft-face mallet (never on actuators, bearings or cameras),
powered screwdriver (finish with the torque driver), third-hand clamp, bench
power supply, thermal camera, 0.01 mm digital calipers.

!!! missing "MISSING — tools that cannot be specified yet: bearing press and arbors, driver sizes, torque range, crimp dies, retaining-ring pliers, zeroing fixtures"
    *Owner: hardware lead.*
