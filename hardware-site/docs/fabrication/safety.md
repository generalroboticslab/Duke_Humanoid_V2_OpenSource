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
   corrupt the perception geometry. Any gantry rated **50 kg or more** with
   **1.4 m or more of clear height** under the beam suits a 36 kg, 1256 mm
   robot; the reference build used a
   [Unitree G1 gantry](https://stemfinity.com/products/unitree-gantry).

    !!! note "Yours to determine — sling route and lifting points on the robot; clearance zone under the gantry"
        The gantry itself is specified above; where to attach to the robot and how
        much floor to keep clear are your build's call.
        *Owner: hardware lead.*

3. **Keep out of the envelope.** Nobody and nothing enters the range of motion
   while powered. Power off before approaching, with a second person guarding
   the switch.
4. **Wear personal protective equipment (PPE).** Safety glasses whenever
   powered; no loose sleeves, lanyards or untied hair near a powered robot.

5. **Have a way to stop.** Three independent layers:

    1. **Software e-stop** — the deployed mission loop always publishes, and
       every silence triggers a fail-closed response from the robot:

       | Stream | Timeout (no packet = action) | Action |
       | --- | ---: | --- |
       | nav (base) | 1 s | robot stops the base |
       | arm | 0.5 s | robot ramps both arms to the default pose |
       | gaze (cameras) | 2 s | robot parks both gimbals |

       Halting the operator process, losing the network, or terminating
       `humanoid_real_env.py` *is* the e-stop: nothing else reaches the motors.
       *Source: `deploy/control/humanoid_real_env.py`, lines 355–360;
       `deploy/control/docs/auto_operator_safety_contract.md` SAFE-SHUTDOWN-001
       and the silence-failsafe constants `nav 1 s / arm 0.5 s / gaze 2 s`.*

    2. **CAN watchdog** — a joint whose feedback freezes for
       `_WATCHDOG_STALE_TICKS` latches the arm into a damped hold
       (position pinned, integrator cleared, feed-forward zeroed) until
       restart. Guarded by `--arm-watchdog` (default on). *Source:
       `deploy/control/humanoid_real_env.py`, lines 355–365.*

    3. **Physical disconnect** — the runbook assumes one, with the same
       effect as a watchdog latch: every motor releases the bus and the robot
       drops. Plan the lift, not the stance.

    Pressing any layer is often right, but the robot falls: removing power
    on this quasi-direct-drive rig drops the 36 kg body and anything the
    arms hold.

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

    Shut the software down in the reverse order, and **never cut power with a
    hold active**: on Ctrl+C the arms hold their last target — there is no
    robot-side retract — so clear anything in the grippers, wait for the holds
    to release, and only then exit. The mission loop publishes
    `nav_cmd [0, 0, 0]` on the way out. *Source:
    `deploy/control/docs/auto_operator_safety_contract.md`, SAFE-SHUTDOWN-001
    and the shutdown-protocol notes.*

    !!! note "Yours to determine — physical power-on and power-off order: computer, USB-CAN adapters, motor bus, camera gimbals, with a check at each step"
        The software ladder above is published; the order the hardware itself is
        switched is your build's call.
        *Owner: electrical lead.*

7. **Isolate before touching.** Disconnect the packs and move them away before
   any work.
8. **Two people** for every lift and gantry transfer. During
   powered tests the second person's only job is the stop layers below.
9. **Log incidents.** Record near-misses; revise these rules.

## Hazards

### Power loss means collapse

Every joint is quasi-direct-drive, with no self-locking gearbox. Removing
power — pulling the pack disconnect included — drops the 36 kg body and
whatever the arms hold.

### Lithium-polymer (LiPo) packs

Two Zeee 6S 10000 mAh LiPo packs in series feed the 48V bus through a surge
protector: 44.4 V nominal, 50.4 V full, about 222 Wh per pack (computed).
*Source: team power wiring diagram (V2).*

<figure markdown>
  ![Team power wiring diagram (V2)](../assets/wiring/power-supply-v2.webp){ loading=lazy }
  <figcaption>Series packs, surge protector, 48V bus to upper- and lower-body distribution blocks, TVS diodes, 10 A fuse and 48V-to-12V buck to the computer.</figcaption>
</figure>

- RobStride 00/02/03/04/05/06: rated 48 VDC, range 24–60 VDC.
- The only fuse is 10 A, on the computer branch. No pack fuse or pack monitoring is drawn.
- Power runs on XT30 connectors. A dropped tool shorts them.
- A pack burns if over-discharged, over-charged, punctured, crushed or shorted.
  Never charge unattended. An office extinguisher will not put it out.

### Crush

With no clutch, a limb closes on a hand with full commanded torque.

- RobStride manuals: motor over-temperature warning 75 °C, fault 80 °C; driver
  board rated to 80 °C.
- Do not change the torque limit, protection temperature or over-temperature time.

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

### Falls

A biped can fall on its own: 36 kg at floor level, possibly on a foot.

## Inspect and log before each session

| Check | Why |
| --- | --- |
| Fasteners: hips, shoulders, gantry attachment | Vibration loosens them |
| Mechanical limits and hard stops | Impacts deform them |
| Noise or catching in a joint | Damaged bearing, bent frame or trapped cable |
| Cables and connectors at joints | Bending breaks conductors; a chafed bus wire near a pack is a fire |
| Packs: swelling, dents, connectors, cell balance | Retire a puffed pack |
| Gantry, slings, lifting points | Shock-loaded gear is no longer rated |
