# Cost { #cost-and-time }

| Category | Subtotal |
| --- | --- |
| Actuators: {{ bom_qty("actuators.csv") }} units, {{ bom_count("actuators.csv") }} models | {{ bom_subtotal("actuators.csv") }} |
| Electronics | {{ bom_subtotal("electronics.csv") }} |
| Machined parts: {{ bom_count("cnc-parts.csv") }} rows | {{ bom_subtotal("cnc-parts.csv") }} |
| Cables and connectors | {{ bom_subtotal("cables-connectors.csv") }} |
| Fasteners and bearings | {{ bom_subtotal("fasteners.csv") }} |
| Printed parts (filament and powder) | {{ bom_subtotal("printed-parts.csv") }} |
| **Parts, as far as priced** | **{{ bom_total() }}** |

Bearings, screws and five machined parts are not priced yet **TODO**{ .dh-missing }. Tools, shipping, duty and machining setup are not included. Order the single-source items first: the two RealSense D436 and the {{ bom_qty("actuators.csv") }} RobStride actuators.
