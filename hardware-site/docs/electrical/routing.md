# Routing

Route every limb cable, then verify.

!!! abstract "At a glance"
    - **You will:** work in step with [Assembly](../assembly/index.md).

## Route each cable

1. Size each service loop for full travel, not one pose: every limb cable
   crosses several rotating joints.
    - **Wrists:** `humanoid_joint_monkey_hw.py` limits sweep and speed against
      cable wrap and the wrist encoders' ±π wrap, assuming the reference routing.
2. Each D436 USB-C cable crosses two gimbal axes and must hold USB 3: use the
   40 Gbit/s extension and right-angle cable ([Cables and connectors](../bom/cables-and-connectors.md)).

!!! missing "MISSING — Routing record for leg, arm, waist, torso, gimbal, gripper: photo, bend radius, service loop and the pose it is sized at, clamp points, pinch clearance"
    *Owner: electrical lead, from a photographed build.*

✅ **Check:** `lsusb -t` shows `5000M`; if not, replug or change port.

## Verify the routing

Robot suspended, motors unpowered.
{ #verifying-a-routing-job }

1. Drive each joint slowly to both extremes by hand, watching the cable: none
   taut, pinched, rubbing or over-bent. Do it before closing the limb.
2. Start `real_env` in the safe bench profile. Deploy leaves the arm motors
   disabled but still polled on CAN; only the camera gimbal motors are enabled,
   capped at 1% of max motor torque.

    ```bash
    cd <deploy-repo>/control
    python humanoid_real_env.py --task HumanoidRmaVelEstArmFlashSacv2GridGaitInitStartNearZeroTurnInPlaceBankFlatDecoupledCosine \
        --torque_limit 0.01 --enable-motor camera
    ```

3. Run the wiggle test while squeezing and flexing every connector, clamp and
   limb entry. Keep two other joints on that limb moving, or it false-alarms.

    ```bash
    cd <deploy-repo>/control
    python humanoid_wiggle_watch.py              # right arm (default)
    python humanoid_wiggle_watch.py --arm left   # left arm
    ```

    It watches one arm per run on the port 9870 telemetry stream. It alarms
    when a joint's position, velocity and effort stay bit-identical for five
    rows (about 100 ms) mid-motion.

!!! unverified "UNVERIFIED — Supplies that must be on for the wiggle test: which rails feed CAN polling while the arm motors stay disabled"
    *Owner: controls lead + electrical lead.*

✅ **Check:** every joint driven to both extremes by hand leaves every cable free,
and a full wiggle test raises no dropout alarm.

## Check for trapped cables

!!! missing "MISSING — Trapped-cable check after final integration: where to look, without disassembly"
    *Owner: electrical lead + assembly lead.*
