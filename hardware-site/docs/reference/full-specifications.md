# Full specifications

Headline figures: [home page](../index.md#specifications).

## Actuators

| Model | Joints (per side unless noted) | Qty | Peak torque (N·m) | Kt (N·m/A~rms~) |
| --- | --- | ---: | ---: | ---: |
| RS00 | wrist_2 | 2 | 14 | 1.48 |
| RS02 | shoulder_3, elbow, wrist_1 | 6 | 17 | 1.22 |
| RS03 | waist (1), hip_1–3, ankle_1, shoulder_1 | 11 | 60 | 2.36 |
| RS04 | knee | 2 | 120 | 2.10 |
| RS05 | wrist_3; camera yaw and pitch (4) | 6 | 5.5 | 0.94 |
| RS06 | ankle_2, shoulder_2 | 4 | 36 | 1.1 |
| **Total** | | **{{ bom_qty("actuators.csv") }}** | | |

*Source: `deploy/control/humanoid_config.py`, `py_motor.py`.* CAN (Controller Area
Network) IDs and buses: [CAN bus](../electrical/can-bus.md).

Deploy writes each motor's torque limit as its peak torque above × a ratio: 0.1 by
default (`humanoid_real_env.py --torque_limit`), stepped by 0.1 within 0.1–0.8 with
gamepad X/B. `humanoid_set_current_limit.py` writes current limits of the per-type
default × `--scale` (default 0.6), capped at 40 A.

| Model | Current default (A) | Written at × 0.6 (A) |
| --- | ---: | ---: |
| RS00 | 16 | 9.6 |
| RS02 | 23 | 13.8 |
| RS03 | 43 | 25.8 |
| RS04 | 60 | 36.0 |
| RS05 | 11 | 6.6 |
| RS06 | 57 | 34.2 |

*Source: `py_motor.py` `MAX_TORQUE`, `MOTOR_CURRENT_LIMIT_DEFAULTS`.*

RS02/03/04 manuals:

- Rated 48 VDC, range 24–60 VDC (RS00/05/06 **UNVERIFIED**{ .dh-unverified })
- Operating −20 to 50 °C, storage −30 to 70 °C, 5–85 % RH non-condensing
- Over-temperature warning 75 °C, fault 80 °C

## Joint limits

Limits in the published model (`humanoid_v21.xml`, `head_cam/`), not measured
mechanical stops.

| Joint | Limit | Joint | Limit |
| --- | --- | --- | --- |
| waist | ±90° | shoulder_1 | ±180° |
| hip_1 | ±105° | shoulder_2 | L −180° to +30°, R −30° to +180° |
| hip_2 | L −105° to +30°, R −30° to +105° | shoulder_3 | ±180° |
| hip_3 | ±90° | elbow | ±125° |
| knee | ±130° | wrist_1 | ±180° |
| ankle_1 | ±50° | wrist_2 | ±92° |
| ankle_2 | ±60° | wrist_3 | ±90° |
| camera yaw | ±270° (training choice) | camera pitch | ±90° |

## Electronics, power, structure

| | |
| --- | --- |
| Computer | MINISFORUM X1-470 mini PC |
| IMU | SYD Dynamics TransducerM TM171, 9-axis AHRS, 40 × 34 × 12.6 mm, USB-C |
| Cameras | 2 × Intel RealSense D436 |
| CAN | 6 × CANable PRO V2.0, 1 Mbit/s, `can9` and `can21`–`can25` |
| Grippers | 2 × Feetech HL-3915-C001 (12 V) on 2 × Waveshare ST/SC bus servo adapters |
| Battery | 2 × Zeee 6S 10000 mAh LiPo in series: 44.4 V nominal, 50.4 V full |
| Fuse | 10 A, computer branch only |
| Control | 50 Hz policy, 200 Hz motor loop; cuRobo planner on a separate CUDA machine |
| Structure | Machined aluminium, 6061 or 7075 **UNVERIFIED**{ .dh-unverified } (repo comments say 6061) |
| Hardware | Torx button-head M4×12 and M3×12; main bearing 50 × 65 × 7 mm; Loctite 222. Motor04 shaft and knee need M5 where the CAD has M4 **UNVERIFIED**{ .dh-unverified } |
| Model mass | 34.5 kg in `humanoid_v21.xml`: `base_link` 9.30, waist 2.32, each leg 7.45, each arm 3.99 (with the 0.17 kg end-effector attachment); per-link CoM and inertia in its `<inertial>` entries. Head camera module 1.158 kg (`head_cam/cam_fusion_info.py`); gripper with flange ≈ 346 g (`parallel_gripper/README.md`) |
| Model foot contact | Six parallel capsules per foot, radius 7 mm, 221 mm segment, axes 11.6 mm apart across 58 mm (`humanoid_v21.xml`, `foot_*_collision0`–`5`) |
| Commanded velocity | Full stick ±1.0 m/s forward and lateral, ±0.7 rad/s yaw, the trained command range (`humanoid_real_env.py` `VEL_SCALE_*`); `gamepad.py` publisher caps x 0.3 m/s, y 0.25 m/s, yaw 0.2 rad/s |
| Gaze slew | Reference capped at 1.5 rad/s (`humanoid_auto_operator.py` `GAZE_SLEW_RATE`); failsafe return to zero at 0.75 rad/s (`humanoid_real_env.py`) |

!!! missing "MISSING — Unspecified: mechanical stops, as-built mass breakdown, measured CoM and inertia, physical foot geometry, current draw and runtime, payload, measured walking speed, measured gimbal range and slew rate, IP rating, robot temperature range, noise"
    *Owner: hardware lead + controls lead.*
