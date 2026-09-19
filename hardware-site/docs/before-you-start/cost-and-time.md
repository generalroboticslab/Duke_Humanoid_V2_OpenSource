# Cost and time

## Cost

| Category | Subtotal |
| --- | --- |
| Actuators: {{ bom_qty("actuators.csv") }} units, {{ bom_count("actuators.csv") }} models | {{ bom_subtotal("actuators.csv") }} |
| Electronics | {{ bom_subtotal("electronics.csv") }} |
| Machined parts: {{ bom_count("cnc-parts.csv") }} rows, test fixture excluded | {{ bom_subtotal("cnc-parts.csv") }} |
| Cables and connectors | {{ bom_subtotal("cables-connectors.csv") }} |
| Fasteners and bearings | {{ bom_subtotal("fasteners.csv") }} |
| Printed parts | {{ bom_subtotal("printed-parts.csv") }} |
| **Parts, as far as priced** | **{{ bom_total() }}** |

Actuators are the largest block. Plan above the total: it excludes
{{ bom_unpriced("fasteners.csv") }} in fasteners,
{{ bom_unpriced("printed-parts.csv") }} in printed parts, tools, shipping, duty
and machining setup fees.

!!! missing "MISSING — A real price: priced fasteners and bearings, printed-part cost, tools tier (with gantry), options tier, shipping/duty/setup allowance, a priced_as_of date per row"
    *Owner: hardware lead. Blocks any public cost claim.*

## Time

!!! missing "MISSING — Build time: elapsed time and person-hours per stage (procurement, fabrication, assembly, wiring, bring-up)"
    *Owner: whoever performs the first complete build with a stopwatch.*

Order long-lead items first. The Intel RealSense D436 and the 31 RobStride
actuators (six models) are single-source.

!!! missing "MISSING — Quoted lead times (cameras, each actuator model, machining), tested alternates for both single-source items, ordering sequence"
    *Owner: hardware lead. See [Sourcing](../bom/sourcing.md).*
