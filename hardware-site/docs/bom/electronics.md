# Electronics

Computer, battery, power conversion, Controller Area Network (CAN) and sensing:
{{ bom_subtotal("electronics.csv") }} across {{ bom_count("electronics.csv") }}
lines (MPN: manufacturer part number). Every line is priced in the team BOM.

| Team ref | Part ID | Description | MPN | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/electronics.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.mpn or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | | **Total** | **{{ bom_subtotal("electronics.csv") }}** | |

**Team ref** is the line in the team BOM spreadsheet
(`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`, 2026-09-19), which is where
every quantity and price on this page comes from.

## Where each part goes

| Part ID | Use |
| --- | --- |
| `EL_COMPUTE_MINIPC` | Onboard computer, fed from the upper-body distribution block via a 10 A fuse and a `EL_BUCK_60V_12V` (60 V→12 V) buck converter |
| `EL_BATTERY_6S` | 2-pack = both packs, in series (one pack's + to the other's −): 44.4 V nominal, 50.4 V full |
| `EL_CAN_ADAPTER` | One per CAN bus, 1 Mbit/s: can9 left arm, can21 right arm, can22 waist and both shoulder_1, can23 right leg, can24 left leg, can25 camera gimbals |
| `EL_CAM_D436` | One per camera gimbal. Needs librealsense 2.58.1 or later ([Camera calibration](../bringup/index.md#camera-calibration)) |
| `EL_IMU_TM171` | Body inertial measurement unit (IMU), 40 × 34 × 12.6 mm, read over USB. Configuration: [Software](../software.md) |
| `EL_SERVO_FEETECH`, `EL_SERVO_DRIVER` | One servo per gripper, each on its own Waveshare driver board ([Gripper](../assembly/index.md#gripper)) |
| `EL_TVS_DIODE` | Transient-voltage-suppression (TVS) diode across power and ground at each distribution-block pair |
| `EL_BUCK_60V_12V`, `EL_BUCK_12V_ENC` | 60 V→12 V conversion (E12) and 20–60 V→12 V encased (E11); conflict under [Power path](#power-path) |
| `EL_SURGE_PROTECTOR` | Pack lead, before the 48 V bus. T Tocas E9 150 A circuit breaker with manual reset, 12–48 VDC ([B01F76VJ3I](https://www.amazon.com/dp/B01F76VJ3I/)) |
| `EL_DIST_BLOCK` | The four copper grounding bars, 6×8-7 holes; the two power + ground pairs on the power diagram |
| `EL_USB_HUB` | 3 off. Which devices hang off which hub is **UNVERIFIED**{ .dh-unverified } |
| `EL_VOLTAGE_CHECKER` | Pack voltage check, 1–8S. Two off; mounting location on the robot is **TODO**{ .dh-missing } |

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

!!! unverified "UNVERIFIED — 60 V→12 V conversion (power diagram: one buck converter, computer only, no 5 V rail; this list: three); TVS diode (M1.5KE62CA, from the DigiKey link) and how many of the ten sit at each distribution-block pair"
    *Owner: electrical lead.*

## Not in this list { #electronics-not-in-this-list }

| Item | Evidence | Status |
| --- | --- | --- |
| 10 A fuse and holder | Power diagram, computer branch only | Part not identified **TODO**{ .dh-missing } |
| Battery charger | Design log | [iSDT K4 Smart Dual Charger (AC400W / DC600W ×2)](https://www.getfpv.com/isdt-k4-smart-dual-charger-ac400w-dc600w-x2.html), reference only — not in the team BOM |
| EC5 battery connectors | [Cables and connectors](#cables-not-in-this-list) | — |

!!! missing "MISSING — a parts-list row (MPN, qty, link) for the 10 A fuse and holder, and a manufacturer part number for the surge protector, the four distribution terminals, the USB hubs and the voltage checker, which the team BOM identifies by a vendor link alone"
    *Owner: electrical lead.*
