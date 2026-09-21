# Actuators

Every joint is a RobStride quasi-direct-drive actuator:
{{ bom_qty("actuators.csv") }} units, {{ bom_count("actuators.csv") }} models,
{{ bom_subtotal("actuators.csv") }}.

| Team ref | Model | Part ID | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/actuators.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | {{ r.mpn }} | `{{ r.part_id }}` | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | **Total** | | **{{ bom_qty("actuators.csv") }}** | | **{{ bom_subtotal("actuators.csv") }}** | |

**Team ref** is the line in the team BOM spreadsheet
(`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`, 2026-09-19), which is where
every quantity and price on this page comes from.
No model has a published alternate ([Sourcing](sourcing.md#supply-risk-parts)).
Check each on arrival: [Incoming inspection](../fabrication/incoming-inspection.md#check-actuators).

## Which model goes in which joint

| Model | Qty | Joints (both sides unless noted) |
| --- | ---: | --- |
| RS00 | 2 | wrist_2 |
| RS02 | 6 | shoulder_3, elbow, wrist_1 |
| RS03 | 11 | waist (1), hip_1, hip_2, hip_3, ankle_1, shoulder_1 |
| RS04 | 2 | knee |
| RS05 | 6 | wrist_3; cam_yaw and cam_pitch on both camera gimbals |
| RS06 | 4 | ankle_2, shoulder_2 |

*Source: `deploy/control/humanoid_config.py`.* Controller Area Network (CAN) IDs
and buses: [CAN bus](../electrical/can-bus.md). Connectors:
[Cables and connectors](cables-and-connectors.md#actuator-side-connectors).

The team BOM also lists 6 RS05 (`Duke_Humanoid_V2_BOM_WIP.xlsx`, line `E5`).
The CAD-derived head-camera note names RS05 as the yaw and pitch motors
(`simulation/asset/duke_v2/head_cam/PositionDeter/RELATIVE_POSITION_top_plate__head_cameras.md`),
and the Cartesian-hand model's base group includes `CNC_arm13_x2_RS05_shaft_coupler`
(`simulation/asset/duke_v2/cartesian_hand_v3/source/groups.json`).

!!! note "Not checked on the reference robot — RS05 on `wrist_3` and the four camera joints"
    *Owner: hardware lead + controls lead.*

**Order four RS06, not two.** The robot has four RS06 joints — `ankle_2` and
`shoulder_2` on both sides — and the team BOM line `E6` buys two. Deploy's
joint-to-type map and the team's own booklet both show four. *Source:
`deploy/control/humanoid_config.py`; the team booklet, p.5 and p.9.*

## Motor data

| Model | Rated torque (N·m) | Max torque (N·m) | Torque constant (N·m/Arms) | `0x7018` current-limit range (A) |
| --- | ---: | ---: | ---: | --- |
| RS00 | 5 | 14 | 1.48 | **UNVERIFIED**{ .dh-unverified } |
| RS02 | 6 | 17 | 1.22 | 0–23 |
| RS03 | 20 | 60 | 2.36 | 0–43 |
| RS04 | 40 | 120 | 2.1 | 0–90 |
| RS05 | 1.6 | 5.5 | 0.94 | **UNVERIFIED**{ .dh-unverified } |
| RS06 | 11 | 36 | 1.1 | **UNVERIFIED**{ .dh-unverified } |

*Source: team motor spec; RobStride 02/03/04 manuals.*

- Max torque and torque constant equal `MAX_TORQUE` and `MOTOR_TORQUE_CONSTANTS` in `py_motor.py`; the control code clamps to max torque.
- RS02, RS03, RS04 (manuals): 48 VDC rated, 24–60 VDC operating; CAN at 1 Mbps; 14-bit single-turn absolute encoder; reduction 7.75:1 (RS02) and 9:1 (RS03, RS04).
- Current-limit defaults, resistance and back-EMF: [Power system](../electrical/power-system.md).
- Deploy sets the `0x700B` torque limit of every motor to one ratio of its max torque. The ratio comes from `--torque-limit` (default 0.1; the `OPERATIONS.md` robot launch uses 0.8), and the operator steps it by 0.1 between 0.1 and 0.8. The four camera motors follow the same ratio (`deploy/control/humanoid_real_env.py`: `torque_limit`, `[TORQUE_UP]`/`[TORQUE_DOWN]`, `_apply_group_torque_limits`).

!!! missing "MISSING — RS00, RS05, RS06 manual data (voltage range, reduction, encoder, `0x7018` range); firmware version and per-joint limits as run on the reference robot"
    *Owner: hardware lead + controls lead.*
