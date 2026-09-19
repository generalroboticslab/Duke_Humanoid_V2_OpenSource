# Joint zeroing

Record each joint's encoder reading at the model's zero pose.

!!! abstract "At a glance"
    - **Before this:** [Motor ID and config](motor-id-and-config.md). Robot hung, legs straight, emergency stop held, motors **not** enabled.

## Set zeros

The zero pose is the deploy model at all-zero joint angles: deploy assumes
encoder 0 equals model `qpos` 0. The model is `robot.xml` in the
`HumanoidRmaVelEstArmFlashSacv159bMixedArmsCam` run directory
(`humanoid_site.DEPLOY_MODEL_TASK`). Joint order and IDs:
[actuator map](../electrical/can-bus.md#the-actuator-map).

| Joint | Zero as the software defines it |
|---|---|
| `cam_yaw_*`, `cam_pitch_*` | Camera looks straight ahead (gimbal FK assumption) |
| `left_wrist_1`, `right_wrist_1` | The model sets `ref` −π/2 (left), +π/2 (right) to keep encoder 0 at `qpos` 0, 90° from the upstream model's wrist_1 zero ("working pose") |

!!! missing "MISSING — Zero pose: figure, physical per-joint description for legs, waist and arms, holding method or fixture"
    *Owner: hardware lead + controls lead.*

The wrist encoders wrap at ±π. Keep the wrists' zero well away from the wrap
**TODO**{ .dh-missing }.

!!! danger "It zeroes all 31 motors, every time"
    Re-zeroing to fix an arm also wipes the gimbal zeros. After any run, redo
    [Camera calibration](camera-calibration.md).

1. Go to `control/`:

    ```bash
    cd <deploy-repo>/control
    ```

2. Hold every joint at its mechanical zero by hand while it runs:

    ```bash
    python humanoid_set_zero.py
    ```

3. Type `yes`.

It writes each motor's current position as its zero, sets `zero_sta = 1`
(range `−π..+π`), and **saves both to the drives**. Do not use the vendor tool's
*set mechanical zero*: it is lost at power-off.

## Verify zeros

!!! danger "31 joints move at once"
    10 % of an RS04's torque still traps a finger. Stay clear.

1. Ramp to zero. Every joint must end at the zero pose.

    ```bash
    python humanoid_config.py --zero  # 10 % torque, 300 steps at 200 Hz
    ```

2. Check the gimbal zeros: compare the printed look direction with the cameras.
   A mismatch gives the offset.

    ```bash
    python humanoid_gimbal_zero_check.py  # needs humanoid_real_env.py publishing telemetry
    ```

3. Check gravity torque against the model. It scores `shoulder_2`, `shoulder_3`,
   `elbow`, `wrist_1`; a residual growing from wrist to shoulder locates the
   faulty link.

    ```bash
    python humanoid_mass_check.py
    ```

✅ **Check:** every joint matches the model at the zero pose, the gimbal check
agrees with the cameras, and the offsets are saved and backed up. Pass values:
[A5](acceptance-tests.md#a5-check-zero-and-model-fidelity).

## Back up zeros

!!! missing "MISSING — Reading out, backing up and restoring the 31 zero offsets; what to redo after a drive swap"
    *Owner: controls lead.*

## Check accuracy

!!! missing "MISSING — Zeroing accuracy target per joint"
    *Owner: controls lead + hardware lead.*
