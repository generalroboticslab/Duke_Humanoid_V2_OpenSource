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
| Direction | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |

## Set an ID

RS03 and RS04 ship at CAN ID **127** (other models
**UNVERIFIED**{ .dh-unverified }). Address actuators before you install them.

1. Open the RobStride software.
2. Device module → **modify motor CAN ID**; parameter table editable in standby
   only.
3. If an ID can only be set with the motor alone on the bus
   (**UNVERIFIED**{ .dh-unverified }), set all 31 one at a time on the bench.
4. Write ID and joint on each actuator.

!!! missing "MISSING — Motor ID-setting steps and interface, bus-isolation rule, firmware baseline, label scheme"
    *Owner: controls lead + hardware lead. Blocks [Assembly](../assembly/index.md).*

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

!!! unverified "UNVERIFIED — 0x7018 range for RS00, RS05, RS06: check the datasheets first"
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
python humanoid_test_motor.py  # 0.1 rad sine at 300 Hz on the arm joints; no flags
```

✅ **Check:** every actuator answers at its ID and bus, reads back unchanged
after a power cycle, and the smoke test moves the expected joints the expected
way, quietly.

!!! unverified "UNVERIFIED — Smoke-test joints: index 13 onward may include the 4 gimbal joints"
    *Owner: controls lead.*

## Confirm directions

!!! missing "MISSING — SAFETY — Positive direction and travel limits of all 31 joints: table, figure, per-joint check"
    *Owner: controls lead. Blocks [Acceptance tests](acceptance-tests.md).*
