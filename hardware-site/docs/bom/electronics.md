# Electronics

Computer, battery, power conversion, Controller Area Network (CAN) and sensing:
{{ bom_subtotal("electronics.csv") }} across {{ bom_count("electronics.csv") }}
lines (MPN: manufacturer part number).

| Part ID | Description | MPN | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/electronics.csv", dtype="str", keep_default_na=False).to_dict("records") %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.mpn or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot }} | {{ money(r.unit_cost_usd|float) }} | {{ money((r.unit_cost_usd|float) * (r.qty_per_robot|int)) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | **Total** | **{{ bom_subtotal("electronics.csv") }}** | |

## Where each part goes

| Part ID | Use |
| --- | --- |
| `EL_COMPUTE_MINIPC` | Onboard computer, fed from the upper-body distribution block via a 10 A fuse and a 48 V→12 V buck converter |
| `EL_BATTERY_6S` | 2-pack = both packs, in series (one pack's + to the other's −): 44.4 V nominal, 50.4 V full |
| `EL_CAN_ADAPTER` | One per CAN bus, 1 Mbit/s: can9 left arm, can21 right arm, can22 waist and both shoulder_1, can23 right leg, can24 left leg, can25 camera gimbals |
| `EL_CAM_D436` | One per camera gimbal. Needs librealsense 2.58.1 or later ([Camera calibration](../bringup/camera-calibration.md)) |
| `EL_IMU_TM171` | Body inertial measurement unit (IMU), 40 × 34 × 12.6 mm, read over USB. Configuration: [Software](../software.md) |
| `EL_SERVO_FEETECH`, `EL_SERVO_DRIVER` | One servo per gripper, each on its own Waveshare driver board ([Gripper](../assembly/gripper.md)) |
| `EL_TVS_DIODE` | Transient-voltage-suppression (TVS) diode across power and ground at each distribution-block pair |
| `EL_BUCK_48V_12V`, `EL_BUCK_12V_ENC` | 48 V→12 V conversion; conflict under [Power path](#power-path) |

!!! missing "MISSING — computer configuration (RAM, storage, OS, power input), camera firmware version, IMU orientation and frame, peripherals needed at bring-up"
    *Owner: electrical lead.*

!!! unverified "UNVERIFIED — IMU mounting screw: M3 (team log) vs Ø2.10 flange holes on 30 × 31 mm centres (vendor drawing)"
    *Owner: hardware lead.*

## Power path

Packs → surge protector → 48 V bus → lower-body distribution-block pair (legs,
waist) and upper-body pair (arms, both shoulder_1, gimbals, computer branch).
*Source: power wiring diagram.* Full drawing: [Power system](../electrical/power-system.md).

!!! unverified "UNVERIFIED — 48 V→12 V conversion (power diagram: one buck converter, computer only, no 5 V rail; this list: three); TVS diode (M1.5KE62CA, from the DigiKey link) and how many of the ten sit at each distribution-block pair"
    *Owner: electrical lead.*

## Not in this list

| Item | Evidence | Status |
| --- | --- | --- |
| Surge protector | Power diagram, pack lead before the 48 V bus | Part not identified **TODO**{ .dh-missing } |
| 10 A fuse and holder | Power diagram, computer branch only | Part not identified **TODO**{ .dh-missing } |
| Distribution blocks, 4 (two power + ground pairs) | Power diagram; design log links AliExpress 3256806176225478, "Double row 8" | Count and variant **UNVERIFIED**{ .dh-unverified } |
| Battery charger | Design log links Amazon B09WKN863V (listing says ISDT) | Model **UNVERIFIED**{ .dh-unverified } |
| EC5 battery connectors | [Cables and connectors](cables-and-connectors.md#not-in-this-list) | — |
| E-stop, main disconnect, pre-charge | Not drawn; the run scripts assume a physical e-stop | [Power system](../electrical/power-system.md) **TODO**{ .dh-missing } |

!!! missing "MISSING — parts-list rows (MPN, qty, link) for the surge protector, 10 A fuse and holder, the four power distribution terminal bars and the charger"
    *Owner: electrical lead.*
