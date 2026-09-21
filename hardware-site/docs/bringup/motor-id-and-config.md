# Motor ID and config

Give each actuator its CAN (Controller Area Network) ID and configuration before
any joint is commanded.

!!! abstract "At a glance"
    - **Tools:** RobStride software ([robstride.com/download](https://www.robstride.com/download), "Lingzu v0.0.4") and USB-CAN module (CH340, AT mode), not the robot's `gs_usb` adapters **UNVERIFIED**{ .dh-unverified }.
    - **Before this:** [First power-on](first-power-on.md). Robot hung, legs straight, e-stop (emergency stop) held, `humanoid_real_env.py` stopped.

| Property | Set by | Verified by |
| --- | --- | --- |
| CAN ID and bus | Vendor tool | `humanoid_motor_temps.py` against the [actuator map](../electrical/can-bus.md#the-actuator-map) |
| Actuator model | Assembly | Actuator map |
| Firmware version | Vendor tool | **TODO**{ .dh-missing } |
| Current limit | `humanoid_set_current_limit.py` | Self-check after a power cycle |
| Torque limit | Runtime flag | Self-check |
| Zero, `−π..+π` flag | [`humanoid_set_zero.py`](joint-zeroing.md) | Model comparison |
| Direction | Actuator orientation at assembly | Smoke test, [Positive direction](#positive-direction) |

## Set an ID

RS03 and RS04 ship at CAN ID **127** (other models
**UNVERIFIED**{ .dh-unverified }). Address actuators before you install them.

1. Open the RobStride software.
2. Device module → **modify motor CAN ID**; parameter table editable in standby
   only.
3. If an ID can only be set with the motor alone on the bus
   (**UNVERIFIED**{ .dh-unverified }), set all 31 one at a time on the bench.
4. Write ID and joint on each actuator.

!!! unverified "UNVERIFIED — whether an ID can only be set with the motor alone on the bus, and what firmware baseline the team ran"
    The procedure above is the vendor tool's. *Owner: controls lead.*

## Set current limits

1. Go to `control/`:

    ```bash
    cd <deploy-repo>/control
    ```

2. Run and type `yes`:

    ```bash
    python humanoid_set_current_limit.py  # default scale 0.6
    ```

    Or:

    ```bash
    python humanoid_set_current_limit.py --scale 0.5
    ```

It writes `min(default × scale, 40 A)` per motor and **saves to the drives**.
Values: [Power system](../electrical/power-system.md#configured-current-limits).
Register `0x7018` range: RS02 0–23 A, RS03 0–43 A, RS04 0–90 A (RobStride manuals).

!!! note "The `0x7018` range is tracked on [Actuators](../bom/actuators.md)"
    *Owner: controls lead.*

## Set runtime torque limits

```bash
python humanoid_real_env.py --task <task> --torque-limit 0.8 --enable-motor true ...
```

- `--torque-limit`: global ratio. Standing `0.8`, joint-monkey `0.5`, smoke test
  `0.05`. The gimbals can be capped lower.
- `--enable-motor`: `true`, `false`, `leg`, `arm`, `camera`, `arm_camera`. Power
  only the group under test.

## Verify the configuration

{{ step(1, "Run the self-check") }}

```bash
python humanoid_config.py  # type, bus voltage, position, limits per motor; nothing moves
```

{{ step(2, "Power-cycle and re-read") }}

1. Power-cycle and bring the buses up.
2. Run the self-check again. Every value must match.

{{ step(3, "Smoke-test at 5 % torque") }}

!!! danger "First powered motion"
    Everyone clear, e-stop in hand. Watch for a wrong joint moving, a joint
    moving backwards, a joint not moving, and noise. A reversed joint passes
    every other check.

```bash
python humanoid_test_motor.py  # 0.1 rad sine at 300 Hz on indices 13-30; no flags
```

The script enables all 31 motors (kp 10, kd 5) and drives `motor_setup`
indices 13–30: the 14 arm joints (13–26) and the 4 camera-gimbal joints
(27–30). The waist and legs (0–12) are enabled with a zero position
reference. *Source: `deploy/control/humanoid_test_motor.py` lines 30–48;
`humanoid_config.py` lines 27–61; `hardware_bindings/motor/py_motor.py`
line 304.*

✅ **Check:** every actuator answers at its ID and bus, reads back unchanged
after a power cycle, and the smoke test moves the expected joints the expected
way, quietly.

## Confirm directions

The deployed model sets the joint ranges below, in `motor_setup` order. Deploy
reads them as its joint limits and clamps IK and gaze targets to them. They are
software limits, not measured mechanical stops.

| Index | Joint | Model min (rad) | Model max (rad) |
| --- | --- | --- | --- |
| 0 | `waist` | -1.5708 | 1.5708 |
| 1 | `left_hip_1` | -1.8326 | 1.8326 |
| 2 | `left_hip_2` | -1.8326 | 0.523599 |
| 3 | `left_hip_3` | -1.5708 | 1.5708 |
| 4 | `left_knee` | -2.26893 | 2.26893 |
| 5 | `left_ankle_1` | -0.872665 | 0.872665 |
| 6 | `left_ankle_2` | -1.0472 | 1.0472 |
| 7 | `right_hip_1` | -1.8326 | 1.8326 |
| 8 | `right_hip_2` | -0.523599 | 1.8326 |
| 9 | `right_hip_3` | -1.5708 | 1.5708 |
| 10 | `right_knee` | -2.26893 | 2.26893 |
| 11 | `right_ankle_1` | -0.872665 | 0.872665 |
| 12 | `right_ankle_2` | -1.0472 | 1.0472 |
| 13 | `left_shoulder_1` | -3.14159 | 3.14159 |
| 14 | `left_shoulder_2` | -3.14159 | 0.523599 |
| 15 | `left_shoulder_3` | -3.14159 | 3.14159 |
| 16 | `left_elbow` | -2.18166 | 2.18166 |
| 17 | `left_wrist_1` | -3.14159 | 3.14159 |
| 18 | `left_wrist_2` | -1.6057 | 1.6057 |
| 19 | `left_wrist_3` | -1.5708 | 1.5708 |
| 20 | `right_shoulder_1` | -3.14159 | 3.14159 |
| 21 | `right_shoulder_2` | -0.523599 | 3.14159 |
| 22 | `right_shoulder_3` | -3.14159 | 3.14159 |
| 23 | `right_elbow` | -2.18166 | 2.18166 |
| 24 | `right_wrist_1` | -3.14159 | 3.14159 |
| 25 | `right_wrist_2` | -1.6057 | 1.6057 |
| 26 | `right_wrist_3` | -1.5708 | 1.5708 |
| 27 | `cam_yaw_left` | -4.7124 | 4.7124 |
| 28 | `cam_pitch_left` | -1.5708 | 1.5708 |
| 29 | `cam_yaw_right` | -4.7124 | 4.7124 |
| 30 | `cam_pitch_right` | -1.5708 | 1.5708 |

*Source: `deploy/control/legged_env_bundle/mj_envs/deploy/runs/HumanoidRmaVelEstArmFlashSacv159bMixedArmsCam/robot.xml`
lines 156–449 (the default `MJCF_MODEL_PATH`, `humanoid_site.py` lines 159–171);
`humanoid_base.py` line 51; `humanoid_real_env.py` lines 1105, 1718.*

## Positive direction

**Every joint's positive rotation axis points from the motor's output shaft
towards the back of the motor.** Fit the actuator the way the model orients it
and the sign follows; no per-joint sign table is needed. Apply the right-hand
rule about that axis.

The deployed MuJoCo model is the reference for what the robot actually does:
`deploy/control/legged_env_bundle/mj_envs/deploy/runs/HumanoidRmaVelEstArmFlashSacv159bMixedArmsCam/robot.xml`.
Where the simulation model mirrors a mesh and flips an axis sign for the same
joint, that is a modelling convention, not a difference in the hardware.

!!! note "Not measured on the reference robot — hard-stop angles, where a joint has one"
    The table gives the travel the models command, not a measured mechanical
    limit. *Owner: hardware lead.*
