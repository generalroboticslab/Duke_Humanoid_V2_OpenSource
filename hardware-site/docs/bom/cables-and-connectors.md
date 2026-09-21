# Cables and connectors

Harness material: {{ bom_subtotal("cables-connectors.csv") }} across
{{ bom_count("cables-connectors.csv") }} lines — the team BOM carries one cable
line and no connector, sleeving or bulk-wire line, although the actuator and
harness tables below call out XT30 and GH1.25 connectors by part number. Build it with
[Harness fabrication](../electrical/index.md#harness-fabrication); route it with
[Routing](../electrical/index.md#routing).

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/cables-connectors.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | **Total** | **{{ bom_subtotal("cables-connectors.csv") }}** | |

**Team ref** is the team BOM line.

No connectors and no bulk wire here; see [Not in this list](#cables-not-in-this-list).

!!! note "Read off the model — cut length and route per run"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: electrical lead.*

## Actuator-side connectors

| Model (units) | Power | Controller Area Network (CAN) |
| --- | --- | --- |
| RS02 (6) | Amass XT30(2+2): board XT30PB(2+2)-M.G.B, cable XT30(2+2)-F.G.B. Pin 1 +, 2 −, 3 CAN_L, 4 CAN_H | Same shell |
| RS03 (11), RS04 (2) | Amass XT30: board XT30APW-M, cable XT30UW-F | GH1.25 2-pin: board GH1.25-2PWT, cable GH1.25-T |
| RS00, RS05, RS06 | **UNVERIFIED**{ .dh-unverified } | **UNVERIFIED**{ .dh-unverified } |

*Source: RobStride 02/03/04 manuals.*

- Each driver has in and out connectors for daisy-chaining.
- XT30(2+2)-F.G.B rating: 15 A with 18 AWG (American wire gauge) wire, 30 A for one minute below 80 °C. **Never mate or unmate it under power.**
- Solder the XT30 cups (iron at about 480 °C); do not crimp them.

**Wire to the team harness, not to the manuals.** The harness is what the
reference robot was built with, and it differs from the vendor documents in two
places:

| | Team harness (build to this) | RobStride manual |
| --- | --- | --- |
| Trunk connector | XT30(2+2) on every actuator | XT30 + GH1.25 on RS03/RS04 |
| CAN_H | Yellow | Blue |
| CAN_L | Blue | Brown |

Blue means CAN_H in the manual and CAN_L in the harness. Label both ends of
every CAN pair before you crimp, and ring them out before you power anything.

## Wire gauge

| Run | Gauge |
| --- | --- |
| Pack to lower-body distribution | 12 AWG |
| 12 V buck converter to computer | 16 AWG |
| 48 V riser to upper body, ground returns, motor branches, CAN | **TODO**{ .dh-missing } |

*Source: power wiring diagram.*

!!! note "Read off the model — run lengths; gauge follows from the current in the power diagram"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: electrical lead.*

## Not in this list { #cables-not-in-this-list }

| Item | Use | Status |
| --- | --- | --- |
| EC5 connectors | Battery leads and the series link (design log; example Amazon B073ZG47H3) | That the diagram's connectors are EC5 **UNVERIFIED**{ .dh-unverified } |
| Ethernet cable | CAN leads: its twisted pairs become CAN_H and CAN_L | Which runs **UNVERIFIED**{ .dh-unverified } |
| Heat-shrink, 3/32 in and 1/4 in | Connector wires; cable jacket | No quantity |
| XT30, XT30(2+2) and GH1.25 connectors | Every actuator branch ([Actuator-side connectors](#actuator-side-connectors)) | Not in the team BOM **TODO**{ .dh-missing } |
| Wire loom / sleeving | Limb runs ([Routing](../electrical/index.md#routing)) | Not in the team BOM **TODO**{ .dh-missing } |
| Bulk wire, CAN termination resistors, GH1.25 cable contacts | Harness | **TODO**{ .dh-missing } |

!!! note "Yours to source — connector housings and contacts, loom and sleeve, to suit your build"
    The team BOM's only cable line is the USB-A to USB-C pack, so ordering the harness from
    this site is not yet possible.
    *Owner: electrical lead.*

!!! note "Not used — two design-log parts with no role in the build"
    *Owner: electrical lead.*
