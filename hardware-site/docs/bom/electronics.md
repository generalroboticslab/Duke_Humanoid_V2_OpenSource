# Electronics

Computer, battery, power conversion, Controller Area Network (CAN) and sensing:
{{ bom_subtotal("electronics.csv") }} across {{ bom_count("electronics.csv") }}
lines (MPN: manufacturer part number). Every line is priced in the team BOM.

| Team ref | Part ID | Description | MPN | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/electronics.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.mpn or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | | **Total** | **{{ bom_subtotal("electronics.csv") }}** | |

**Team ref** is the team BOM line every quantity and price on this page comes from.

What the deploy stack configures or assumes for the computer and the IMU:

| Item | Deploy configures or assumes | Source (deploy repo) |
| --- | --- | --- |
| Compute split | Every process runs on the robot computer (no CUDA needed) except the cuRobo plan/MPC server, which runs on a GPU machine with CUDA; the runbook allows the roles to share one box or not | `control/docs/OPERATIONS.md`, section 0 |
| CPU cores | The runbook's `taskset` core lists are written for 24 logical CPUs; re-derive them on any other machine | `control/docs/OPERATIONS.md`, section 0 |
| Python | 3.12 required | `control/docs/SETUP.md`, section 1 |
| Operator console | Any laptop with ssh and a browser | `control/docs/OPERATIONS.md`, section 0 |
| IMU frame | Deploy applies no mounting rotation: `humanoid_base.py` builds `IMU()` without a `rotation_offset` and writes its quaternion straight into the base orientation; the model's `imu_site` sits at the `base_link` origin, unrotated | `control/humanoid_base.py`; deploy `robot.xml` (`humanoid_site.MJCF_MODEL_PATH`) |

!!! note "Yours to specify — computer RAM, storage and OS release; camera firmware version"
    *Owner: electrical lead.*

**The IMU's own flange takes M2.** The vendor drawing gives Ø2.10 mm holes on
30 × 31 mm centres, which is an M2 clearance hole; the M3 in the team design log
is the screw that holds the bracket to the machined plate, not the screw that
holds the IMU to the bracket.

## Power path

Packs → surge protector → 48 V bus → lower-body distribution-block pair (legs,
waist) and upper-body pair (arms, both shoulder_1, gimbals, computer branch).
*Source: power wiring diagram.* Full drawing: [Power system](../electrical/index.md#power-system).

The ten TVS diodes (M1.5KE62CA) sit across the two distribution-block pairs.

## Not in this list { #electronics-not-in-this-list }

| Item | Evidence | Status |
| --- | --- | --- |
| 10 A fuse and holder | Power diagram, computer branch only | Part not identified **TODO**{ .dh-missing } |
| Battery charger | Design log | [iSDT K4 Smart Dual Charger (AC400W / DC600W ×2)](https://www.getfpv.com/isdt-k4-smart-dual-charger-ac400w-dc600w-x2.html), reference only — not in the team BOM |
| EC5 battery connectors | [Cables and connectors](#consumables-not-itemised) | — |

!!! missing "MISSING — a parts-list row (MPN, qty, link) for the 10 A fuse and its holder"
    *Owner: electrical lead.*
