# Safety

## Hazards

| | |
| --- | --- |
| **Power loss = collapse** | Every joint is quasi-direct-drive with no self-locking gearbox. Cutting power — pulling the pack disconnect included — drops the 36 kg body and whatever the arms hold. |
| **48 V LiPo** | Two Zeee 6S 10000 mAh packs in series: 44.4 V nominal, 50.4 V full. The only fuse is 10 A on the computer branch. Power runs on XT30 connectors; a dropped tool shorts them. A damaged pack burns, and an office extinguisher will not put it out. |
| **Crush** | No clutch: a limb closes on a hand with the full commanded torque, up to 96 Nm at the knee at the runbook's default ratio 0.8 (ceilings per motor: [Actuators](../bom/index.md#actuators)). |
| **Falls** | A biped falls on its own: 36 kg at floor level. |

*Source: team power wiring diagram; `deploy/control/py_motor.py`; RobStride manuals.*

## Rules

1. **Suspend the robot** on a gantry (≥ 50 kg, ≥ 1.4 m clear height under the beam; the reference build used a [Unitree G1 gantry](https://stemfinity.com/products/unitree-gantry)), **legs straight**, until the acceptance tests pass. Lift by the body top plate.
2. **Keep out of the envelope** while powered. Power off before approaching, with a second person at the switch.
3. **Safety glasses**; no loose sleeves, lanyards or untied hair near a powered robot.
4. **Know the stop.** Halting the operator process, losing the network or terminating `humanoid_real_env.py` stops the motors (silence failsafe: nav 1 s, arm 0.5 s, gaze 2 s); a joint whose feedback freezes latches into a damped hold. Every stop drops the robot — plan the lift, not the stance.
5. **Never cut power with a hold active.** On Ctrl+C the arms keep their last target: empty the grippers, wait for the holds to release, then exit.
6. **Isolate before touching.** Disconnect the packs and move them away. Never charge unattended.
7. **Two people** for every lift; during powered tests the second person only watches the stop.

Software start-up order and its checks: [Bring-up](../bringup/index.md).
