# Fabrication

Turn the CAD into parts: order the machined parts, print the rest, check every part before assembly.

1. [CAD downloads](#cad-downloads) — one release tag; verify each SHA-256.
2. [CNC guide](#cnc-guide) — order the machined parts first; they take longest.
3. [Printing guide](#printing-guide) — print while the shop works.
4. [Incoming inspection](#incoming-inspection) — count, measure, record.

## What you need

| | |
| --- | --- |
| Machining | 3-axis CNC milling or a machine shop: {{ bom_count("cnc-parts.csv") }} parts in aluminium 6061 |
| Printing | An FDM printer for PLA and TPU; SLS nylon 12 from a print service for the drivetrain parts |
| Tools | Digital caliper (0.01 mm); soldering iron for XT30 cups and heat-set inserts; crimp tool for signal connectors |
| Space | Two people, a bench, a gantry rated 50 kg with 1.4 m clear height, a charging spot away from flammables |

{% include "fabrication/cost-and-time.md" %}

{% include "fabrication/cad-downloads.md" %}

{% include "fabrication/cnc-guide.md" %}

{% include "fabrication/printing-guide.md" %}

{% include "fabrication/incoming-inspection.md" %}
