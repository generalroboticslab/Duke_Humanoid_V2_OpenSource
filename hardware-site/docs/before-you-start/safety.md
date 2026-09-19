# Safety

Read before ordering parts and again before first power-on. This is not a risk
assessment: do one with your environmental health and safety (EHS) office and
close every red box with them first.

## Rules

1. **Prepare the space.** Clear floor away from walkways; no flammables near the
   charging station; barriers or floor marking keep people out of the envelope
   while powered.

2. **Suspend the robot for every early test.** Keep it on the gantry, **legs
   straight**, until the acceptance tests pass. Bent legs tilt the torso and
   corrupt the perception geometry.

    !!! missing "MISSING — SAFETY — Lifting specification: gantry rating over 36 kg, lifting points, slings, clearance zone; the gantry is in no parts list"
        *Owner: hardware lead.*

3. **Keep out of the envelope.** Nobody and nothing enters the range of motion
   while powered. Power off before approaching, with a second person guarding
   the switch.

    !!! missing "MISSING — SAFETY — Bystander distances: suspended, standing, walking (including fall radius)"
        *Owner: hardware lead + local EHS office.*

4. **Wear personal protective equipment (PPE).** Safety glasses whenever
   powered; no loose sleeves, lanyards or untied hair near a powered robot.

    !!! missing "MISSING — SAFETY — Rest of the PPE list: safety shoes, and whether gloves are required or forbidden"
        *Owner: hardware lead + local EHS office.*

5. **Have an emergency stop (e-stop)** within reach of a person outside the
   envelope. Pressing it is often right, but the robot falls: it never makes
   approaching safe.

    !!! missing "MISSING — SAFETY — E-stop: none in the bill of materials or power diagram, yet the run scripts assume one; mounting, what it cuts, remote or dead-man switch, restart checks"
        Scripts: `humanoid_nav_step_test.py`, `humanoid_joint_monkey_hw.py`.
        *Owner: electrical lead. Blocks [First power-on](../bringup/first-power-on.md).*

6. **Follow the power sequence.** After power-on, start the software in the
   order of deploy's runbook (`deploy/control/docs/OPERATIONS.md`, section 2)
   and pass each check before the next step:

    1. Run `python humanoid_setup_can.py`. All six CAN buses (can9, can21 to
       can25) must report ERROR-ACTIVE. A bus stuck in ERROR-WARNING means
       power-cycle again; if it recurs, inspect the harness.
    2. Start the camera server. If a camera drops to USB2 after a power
       cycle, replug it or move ports until `lsusb -t` shows 5000M.
    3. Start the gripper service and wait for both `Connected left/right hand`.
    4. Start `humanoid_real_env.py` and let it run for two minutes, watching
       for `██ WATCHDOG ██`, before anything else.

    !!! missing "MISSING — SAFETY — Physical power-on and power-off order (computer, USB-CAN adapters, motor bus, camera gimbals), with a check at each step, and the software shutdown order before power-off"
        *Owner: electrical lead. Blocks [Pre-power checks](../electrical/pre-power-checks.md).*

7. **Isolate before touching.** Disconnect the packs and move them away before
   any work; lock-out/tag-out on a shared robot.

    !!! missing "MISSING — SAFETY — Isolation and lock-out/tag-out procedure, including how to confirm the converters have discharged"
        *Owner: electrical lead.*

8. **Two people** for every lift and gantry transfer. During
   powered tests the second person's only job is the e-stop.

    !!! missing "MISSING — SAFETY — Which steps need a second person and which need a hoist"
        *Owner: hardware lead.*

9. **Log incidents.** Record near-misses; revise these rules.

    !!! missing "MISSING — SAFETY — Numbered mechanical and electrical incident register, like deploy's control-stack register"
        *Owner: hardware lead, continuously.*

## Hazards

### Power loss means collapse

Every joint is quasi-direct-drive, with no self-locking gearbox. Removing
power, including an e-stop, drops the 36 kg body and whatever the arms hold.

!!! missing "MISSING — SAFETY — Collapse behaviour and standoff distance on power loss; safe pose before planned power-down"
    *Owner: hardware lead, from a drop test with the robot suspended. Blocks [First power-on](../bringup/first-power-on.md).*

### Lithium-polymer (LiPo) packs

Two Zeee 6S 10000 mAh LiPo packs in series feed the 48V bus through a surge
protector: 44.4 V nominal, 50.4 V full, about 222 Wh per pack (computed).
*Source: team power wiring diagram (V2).*

<figure markdown>
  ![Team power wiring diagram (V2)](../assets/wiring/power-supply-v2.webp){ loading=lazy }
  <figcaption>Series packs, surge protector, 48V bus to upper- and lower-body distribution blocks, TVS diodes, 10 A fuse and 48V-to-12V buck to the computer.</figcaption>
</figure>

- RobStride 02/03/04: rated 48 VDC, range 24–60 VDC. RS00/05/06 range
  **UNVERIFIED**{ .dh-unverified }.
- The only fuse is 10 A, on the computer branch. No pack fuse, e-stop, main
  disconnect, pre-charge or pack monitoring is drawn.
- Power runs on XT30 connectors. A dropped tool shorts them.
- A pack burns if over-discharged, over-charged, punctured, crushed or shorted.
  Never charge unattended. An office extinguisher will not put it out.

!!! missing "MISSING — SAFETY — Battery procedure: charger and charge rate, voltage floor, storage, fire response, disposal, pack-path protection"
    The team linked an "ISDT ... DC600Wx2" charger; the model is **UNVERIFIED**{ .dh-unverified }.
    *Owner: hardware lead with the local EHS office. Blocks [Power system](../electrical/power-system.md).*

### Crush

With no clutch, a limb closes on a hand with full commanded torque.

- RobStride manuals: motor over-temperature warning 75 °C, fault 80 °C; driver
  board rated to 80 °C.
- Do not change the torque limit, protection temperature or over-temperature time.
- Mechanical end stops on any joint: **UNVERIFIED**{ .dh-unverified }.

Deploy sets each RobStride joint's run-time torque limit (drive parameter
0x700B) to a per-motor-type ceiling times one global ratio. These are software
settings, not measured joint torques.

| Deploy motor type | Ceiling (Nm) | Joints |
| --- | --- | --- |
| R04 | 120 | Left and right knee |
| R03 | 60 | Waist; hip 1, 2, 3; ankle 1; shoulder 1 |
| R06 | 36 | Ankle 2; shoulder 2 |
| R02 | 17 | Shoulder 3; elbow; wrist 1 |
| R00 | 14 | Wrist 2 |
| R05 | 5.5 | Wrist 3; the four camera gimbal motors |

*Source: `deploy/control/hardware_bindings/motor/py_motor.py` (`MAX_TORQUE`,
`set_max_torque_ratio`); joint-to-type map in `deploy/control/humanoid_config.py`.*

- The motor controller starts at a ratio of 0.05; `humanoid_real_env.py`
  defaults to 0.1, and the runbook's T3 command passes `--torque-limit 0.8`
  (96 Nm at the knee, computed).
- The torque-up and torque-down commands step the ratio by 0.1 between 0.1 and
  0.8. The camera gimbals follow the same ratio as the body.

!!! missing "MISSING — SAFETY — Pinch-point diagram (knee, elbow, hip-roll/thigh, waist, gripper jaws, camera gimbals)"
    *Owner: hardware lead for the geometry.*

### Falls

A biped can fall on its own: 36 kg at floor level, possibly on a foot.

!!! missing "MISSING — SAFETY — Conditions for letting the robot stand free"
    *Owner: hardware lead + controls lead. See [Acceptance tests](../bringup/acceptance-tests.md).*

## Inspect and log before each session

| Check | Why |
| --- | --- |
| Fasteners: hips, shoulders, gantry attachment | Vibration loosens them |
| Mechanical limits and hard stops | Impacts deform them |
| Noise or catching in a joint | Damaged bearing, bent frame or trapped cable |
| Cables and connectors at joints | Bending breaks conductors; a chafed bus wire near a pack is a fire |
| Packs: swelling, dents, connectors, cell balance | Retire a puffed pack |
| Gantry, slings, lifting points | Shock-loaded gear is no longer rated |

!!! missing "MISSING — SAFETY — Inspection intervals, pass/fail criteria and owners for the table above"
    *Owner: hardware lead.*
