# Acceptance tests

Run A0 to A11 in order; each adds energy.

!!! abstract "At a glance"
    - **On a failure:** fix the cause, then re-run that test and every later one.
    - **Before this:** [Camera calibration](camera-calibration.md). Keep the robot hung, legs straight, until A11.

## Run offline tests

Run before hardware work and after software changes. Expected: import errors
before the C++ build; skips without cuRobo or the model.

```bash
cd <deploy-repo>/control && python -m unittest discover -s tests
```

## A0. Check physical conformance

Unpowered. *Source: [project README](https://github.com/generalroboticslab/duke_humanoid_v2).*

| Quantity | Published | Tolerance |
| --- | --- | --- |
| Total mass | 36 kg | **TODO**{ .dh-missing } |
| Height | 1.2 m | **TODO**{ .dh-missing } |
| Arm reach | 0.46 m | **TODO**{ .dh-missing } |
| Leg length | 0.39 m | **TODO**{ .dh-missing } |
| Gripper mass, each | 350 g | **TODO**{ .dh-missing } |
| Degrees of freedom | 31 | Exact |
| Actuators RS00 / RS02 / RS03 / RS04 / RS05 / RS06 | 2 / 6 / 11 / 2 / 6 / 4 | Exact |

!!! missing "MISSING — A0 tolerances; mass breakdown by subassembly; source of the model's 967 g cable mass"
    *Owner: hardware lead.*

## A1. Prove bus integrity

1. Bring up the CAN (Controller Area Network) buses:

    ```bash
    python humanoid_setup_can.py
    ```

2. Read the motors:

    ```bash
    python humanoid_motor_temps.py
    ```

| Pass | Abort |
| --- | --- |
| Every check of [First power-on](first-power-on.md) steps 3 and 5, from a cold power-up, three times in a row | Any ERROR-WARNING, error frame or fewer than 31 answers |

## A2. Measure CAN latency

```bash
python humanoid_profile_motor_latency.py  # 1 % torque, no position command
```

| Check | Pass |
| --- | --- |
| Per-bus average and 99th-percentile latency | **TODO**{ .dh-missing } |
| Spread across one bus | **TODO**{ .dh-missing } |
| Headroom against the 200 Hz (5 ms) loop | **TODO**{ .dh-missing } |

!!! missing "MISSING — A2 reference latency per bus and the harness-fault threshold"
    *Owner: controls lead.*

## A3. Wiggle the harness

1. Motors unpowered, start the watch:

    ```bash
    python humanoid_wiggle_watch.py
    ```

2. Wiggle every connector, clamp and limb entry while stirring the limb
   ([Routing](../electrical/routing.md#verifying-a-routing-job)).

| Pass | Abort |
| --- | --- |
| **Zero** dropout alarms, both sides | One alarm: fix, re-run A1–A3 |

## A4. Test per-joint motion

```bash
python humanoid_test_motor.py  # 5 % torque, 0.1 rad sine, arm joints
```

| Check | Pass |
| --- | --- |
| Commanded joints | All move ([joint set](motor-id-and-config.md#step-3) **UNVERIFIED**{ .dh-unverified }) |
| Other joints | Still |
| Direction | Per the convention **TODO**{ .dh-missing } |
| Tracking error, current | **TODO**{ .dh-missing } |
| Noise | No grinding, knocking or binding |

!!! missing "MISSING — A4 motion test for legs, waist, gimbals; reference tracking and current; range-of-motion sweep"
    *Owner: controls lead.*

## A5. Check zero and model fidelity

1. Ramp to zero:

    ```bash
    python humanoid_config.py --zero  # 10 % torque
    ```

2. Check gravity torque:

    ```bash
    python humanoid_mass_check.py
    ```

| Check | Pass |
| --- | --- |
| Zero pose reached | Matches the [zero pose](joint-zeroing.md#set-zeros) **TODO**{ .dh-missing } |
| Residual, `shoulder_2`, `shoulder_3`, `elbow`, `wrist_1` | **TODO**{ .dh-missing } |
| Residual pattern | Not growing from wrist to shoulder |

!!! missing "MISSING — A5 acceptable gravity-torque residual per joint"
    *Owner: controls lead.*

## A6. Check perception

Procedure: [Camera calibration](camera-calibration.md).

| Check | Pass |
| --- | --- |
| Port mapping | Survives power cycle and replug |
| USB link | Both `5000M` in `lsusb -t` |
| Depth | Across 0.1–3.0 m |
| Gimbal zeros | Look direction matches the robot |
| Hand-eye solve | `VALID`, within the residual table, YAML loaded |
| Gimbal tracking | **TODO**{ .dh-missing } |

!!! missing "MISSING — A6 gimbal tracking test with error and lag figures"
    *Owner: perception lead.*

## A7. Test grippers

Per torque level, high to low: squeeze, settle, hold, then tug for 8 s as a
carry would.

1. Left:

    ```bash
    python humanoid_grip_slip_test.py --side left
    ```

2. Right:

    ```bash
    python humanoid_grip_slip_test.py --side right
    ```

| Check | Pass |
| --- | --- |
| Open and close | Full travel, both |
| Lowest zero-slip level | Recorded per side |
| Carry and park torque | About 1.5× that level |
| Symmetry, cycle endurance | **TODO**{ .dh-missing } |

!!! missing "MISSING — A7 reference no-slip levels, test object, asymmetry limit, endurance test"
    *Owner: controls lead.*

## A8. Hold whole-body posture

1. Scripted poses:

    ```bash
    python humanoid_static_stand.py  # 30 % torque, arm poses over zeroed legs
    ```

2. Real stack:

    ```bash
    # still hung
    python -u humanoid_real_env.py --task <deploy-task> \
      --torque-limit 0.8 --enable-motor true --no-use-ik --grav-comp --ee-service \
      --arm-sender-ip 127.0.0.1 --high-level-controller-ip 127.0.0.1 2>&1 | tee /tmp/realenv.log
    ```

| Check | Pass |
| --- | --- |
| Scripted poses | Reached smoothly, no binding |
| **Two minutes under the policy, watched** | **No `WATCHDOG` banner** |
| Tilt gate | No `TORSO-TILT` refusal, start or 5 s watch |
| Motor temperature, standing current | **TODO**{ .dh-missing } |

RobStride defaults: fault 80 °C, warning 75 °C (stored × 10). Do not change
torque limit, protection temperature or over-temperature time. On a tilt
refusal, straighten the hang; never widen the envelope.

!!! missing "MISSING — A8 reference motor temperatures and standing current, with fail values"
    *Owner: controls lead.*

## A9. Test arm transit

```bash
python humanoid_stage_walk_test.py  # front, side, rear, side, front at 0.025 rad/s
```

Biggest hop about 89 s, out-and-back about 4.5 min **UNVERIFIED**{ .dh-unverified }.

| Check | Pass |
| --- | --- |
| Out-and-back | Completes, each arm |
| Contact | None with torso, other arm or itself |
| Ctrl+C | Arm crawls back to the power-on pose |
| Margins | Audit gives ≥ 40° to joint limits, ≥ 49.9 mm clearance; confirm on your build |

!!! missing "MISSING — A9 launch conditions: prerequisites, arm selection, torque and motor group"
    *Owner: controls lead.*

## A10. Reach and grasp

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="800" height="450" poster="../../assets/images/two_target_handoff_left_right-poster.webp" aria-label="The reference robot grasping one target from a bench while a person holds the second">
    <source src="../../assets/images/two_target_handoff_left_right.mp4" type="video/mp4">
    <a href="../../assets/images/two_target_handoff_left_right.mp4">A10 video</a>
  </video>
  <figcaption>A10 passing on the reference robot.</figcaption>
</figure>

1. Place objects rotated about 45° (two tag faces visible), front-left at
   **|y| ≥ 0.15 m**, **z ≥ 0.09 m**, radius about **0.45–0.55 m**.
2. Follow
   [`OPERATIONS.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/OPERATIONS.md)
   section 2, ladder T0–T6, exactly.

| Stage | Pass |
| --- | --- |
| T0 CAN | All six ERROR-ACTIVE |
| T1 Cameras | Both streams; port order matches serials |
| T2 Grippers | `Connected left/right hand` |
| T3 `real_env` | Two minutes, no watchdog |
| T4 Monitor | `[detection] publishing detected targets` |
| T5 Plan probe | **Three PASS lines** |
| T6 Dry run | Gates pass before `--execute` |
| T6 Execute | Success rate **TODO**{ .dh-missing } |

A `[verdict]` banner names each abort:

- executor or follow → wiring, torque;
- envelope or no-progress → tags, placement;
- clearance-standoff → object too near the torso.

!!! missing "MISSING — A10 reference grasp success rate over N attempts"
    *Owner: controls lead.*

## A11. Walk

!!! danger "First run on the floor"
    Hoist attached and slack, path clear, e-stop (emergency stop) held. Confirm the safety layers,
    in order, before the first command.

```bash
python humanoid_nav_step_test.py  # one measured velocity step; not a gamepad
```

| Check | Pass |
| --- | --- |
| Step | Robot walks, hoist slack, path clear |
| Coast after zero command | **TODO**{ .dh-missing } |
| Post-stop yaw rate | Recorded against 0.10 rad/s |
| Safety layers, before the run | Ctrl+C zeroes; process death zeroes after 1.0 s; gamepad seizes control; e-stop **TODO**{ .dh-missing } |

!!! missing "MISSING — SAFETY — A11 coast distance and pass threshold; the coast constant was never measured"
    *Owner: controls lead.*

!!! unverified "UNVERIFIED — A11 stillness threshold 0.10 rad/s is untested"
    *Owner: controls lead.*

✅ **Check:** every test passes against the published reference values.
