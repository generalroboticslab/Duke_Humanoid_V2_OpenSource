# Cables and connectors

The team BOM has one cable line. Connectors, wire, sleeving, heat-shrink and termination resistors are lab consumables: listed below without prices. Build the harness with [Harness fabrication](../electrical/index.md#harness-fabrication); route it with [Routing](../electrical/index.md#routing).

| Team ref | Part ID | Description | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/cables-connectors.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | **Total** | **{{ bom_subtotal("cables-connectors.csv") }}** | |

**Team ref** is the team BOM line.

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

## Consumables (not itemised)

Standard lab stock; buy to suit your build.

| Item | Use |
| --- | --- |
| Amass XT30 and XT30(2+2) connectors, male and female | Power branches; every actuator trunk ([Actuator-side connectors](#actuator-side-connectors)) |
| GH1.25 2-pin housings and cable contacts | CAN on RS03 / RS04 |
| EC5 connectors | Battery leads and the series link |
| Silicone wire, 12 / 16 / 18 AWG | Pack trunk, computer branch, motor branches ([Wire gauge](#wire-gauge)) |
| Ethernet cable | CAN leads: a twisted pair becomes CAN_H / CAN_L |
| Wire loom / sleeving, 1/4 in and 3/8 in | Limb runs ([Routing](../electrical/index.md#routing)) |
| Heat-shrink, 3/32 in and 1/4 in | Connector wires; cable jackets |
| 120 Ω CAN termination resistors | Both ends of each bus |
| 10 A fuse and inline fuse holder | Computer branch, after the 48 V→12 V buck converter ([Power system](../electrical/index.md#power-system)) |
