# Cost and time

## Cost

| Category | Subtotal |
| --- | --- |
| Actuators: {{ bom_qty("actuators.csv") }} units, {{ bom_count("actuators.csv") }} models | {{ bom_subtotal("actuators.csv") }} |
| Electronics | {{ bom_subtotal("electronics.csv") }} |
| Machined parts: {{ bom_count("cnc-parts.csv") }} rows | {{ bom_subtotal("cnc-parts.csv") }} |
| Cables and connectors | {{ bom_subtotal("cables-connectors.csv") }} |
| Fasteners and bearings | {{ bom_subtotal("fasteners.csv") }} |
| Printed parts | {{ bom_subtotal("printed-parts.csv") }} |
| **Parts, as far as priced** | **{{ bom_total() }}** |

Every figure is the team's own bill of materials, totalled from the [parts lists](../bom/index.md).
Those lists hold
{{ bom_row_count() }} rows, and {{ bom_unpriced_count() }} of them have no
usable price (the team BOM prices them at zero, leaves them blank or has no
line for them); those rows read **TODO**{ .dh-missing } on their pages and are
in no figure above.

Actuators are the largest block. Plan well above the total: it excludes
{{ bom_unpriced_count("fasteners.csv") }} of
{{ bom_row_count("fasteners.csv") }} fastener and bearing lines,
{{ bom_unpriced_count("printed-parts.csv") }} of
{{ bom_row_count("printed-parts.csv") }} printed-part rows, and tools, shipping,
duty and machining setup fees.

!!! note "Not recorded — a priced total: the BOM carries unit prices where the team recorded them"
    *Owner: hardware lead. Blocks any public cost claim.*

## Time

!!! note "Not measured on the reference robot — build time: elapsed time and person-hours per stage"
    *Owner: whoever performs the first complete build with a stopwatch.*

Order long-lead items first. The Intel RealSense D436 and the
{{ bom_qty("actuators.csv") }} RobStride actuators
({{ bom_count("actuators.csv") }} models) are single-source.

!!! note "Yours to determine — quoted lead times (cameras, each actuator model, machining), tested alternates for both single-source items, ordering sequence"
    *Owner: hardware lead. See [Sourcing](../bom/index.md#sourcing).*
