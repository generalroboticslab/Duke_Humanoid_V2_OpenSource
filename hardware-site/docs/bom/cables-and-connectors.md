# Cables and connectors

Harness material: {{ bom_subtotal("cables-connectors.csv") }} across
{{ bom_count("cables-connectors.csv") }} lines — the team BOM carries one cable
line and no connector, sleeving or bulk-wire line, although the actuator and
harness tables below call out XT30 and GH1.25 connectors by part number. Build it with
[Harness fabrication](../electrical/harness-fabrication.md); route it with
[Routing](../electrical/routing.md).

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/cables-connectors.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | **Total** | **{{ bom_subtotal("cables-connectors.csv") }}** | |

**Team ref** is the line in the team BOM spreadsheet
(`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`, 2026-09-19).

No connectors and no bulk wire here; see [Not in this list](#not-in-this-list).

!!! missing "MISSING — pinout of every custom cable, cut length per run, strain relief and service loops at moving joints"
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

!!! unverified "UNVERIFIED — trunk connector (harness pages: XT30(2+2) on every actuator; manuals: XT30 + GH1.25 on RS03/RS04) and CAN wire colours (RS04 manual: blue = CAN_H, brown = CAN_L; team harness, blue/yellow: yellow = CAN_H, blue = CAN_L)"
    *Owner: electrical lead.*

## Wire gauge

| Run | Gauge |
| --- | --- |
| Pack to lower-body distribution | 12 AWG |
| 12 V buck converter to computer | 16 AWG |
| 48 V riser to upper body, ground returns, motor branches, CAN | **TODO**{ .dh-missing } |

*Source: power wiring diagram.*

!!! missing "MISSING — SAFETY — wire gauge of the 48 V riser, the ground returns, the motor branches and the CAN wire"
    *Owner: electrical lead.*

## Not in this list

| Item | Use | Status |
| --- | --- | --- |
| EC5 connectors | Battery leads and the series link (design log; example Amazon B073ZG47H3) | That the diagram's connectors are EC5 **UNVERIFIED**{ .dh-unverified } |
| Ethernet cable | CAN leads: its twisted pairs become CAN_H and CAN_L | Which runs **UNVERIFIED**{ .dh-unverified } |
| Heat-shrink, 3/32 in and 1/4 in | Connector wires; cable jacket | No quantity |
| XT30, XT30(2+2) and GH1.25 connectors | Every actuator branch ([Actuator-side connectors](#actuator-side-connectors)) | Not in the team BOM **TODO**{ .dh-missing } |
| Wire loom / sleeving | Limb runs ([Routing](../electrical/routing.md)) | Not in the team BOM **TODO**{ .dh-missing } |
| Bulk wire, CAN termination resistors, GH1.25 cable contacts | Harness | **TODO**{ .dh-missing } |

!!! missing "MISSING — parts-list rows for every connector the harness uses (XT30, XT30(2+2), GH1.25 housings and contacts, EC5), for wire loom or sleeving, Ethernet cable, heat-shrink, bulk wire (gauge, rating, colour, length) and CAN termination resistors"
    The team BOM's only cable line is the USB-A to USB-C pack, so ordering the harness from
    this site is not yet possible.
    *Owner: electrical lead.*

!!! unverified "UNVERIFIED — two design-log parts with no role: Amazon B0774VBJ3J and connector-housing kit B0BHZTQ1WV"
    *Owner: electrical lead.*
