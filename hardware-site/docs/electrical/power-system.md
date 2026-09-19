# Power system

Wire the 48 V and 12 V rails.

!!! abstract "At a glance"
    - **You will:** join the packs in series, then feed every block.
    - **Parts:** [Electronics](../bom/electronics.md) BOM (bill of materials), plus team-log parts below.

<figure markdown>
  ![Power wiring diagram, Duke Humanoid V2](../assets/wiring/power-supply-v2.webp){ loading=lazy }
</figure>

[Full-size diagram](../assets/wiring/power-supply-v2.png)

## Wire the 48 V bus

1. Join two Zeee 6S 10000 mAh LiPo packs **in series**: 44.4 V nominal, 50.4 V
   full (computed); bus labelled 48V. Not parallel (22.2 V): RobStride
   RS02/RS03/RS04 drives are rated 48 VDC, range 24–60 VDC.

    !!! missing "MISSING — SAFETY — Series-link connector part number, wire gauge and length"
        *Owner: hardware lead.*

    !!! missing "MISSING — SAFETY — Pack retention in the torso rear bay and lead protection at its exit; balance-lead protection, pack monitoring and shutdown voltage; charger model, charge rate, balance-charging procedure and charging location"
        *Owner: hardware lead (retention) + electrical lead + safety officer.*

2. Run free pack + → surge protector → bus; free pack − → ground distribution
   blocks.
3. Feed lower-body blocks: both legs, waist (13 actuators); pack-to-block run
   **12 AWG**.
4. Feed upper-body blocks: both arms, both `shoulder_1`, four gaze motors (18
   actuators).
5. Fit TVS (transient-voltage suppression) diodes, Microchip M1.5KE62CA (53 V
   stand-off, 85 V clamp), across power and ground at each block pair.

    !!! unverified "UNVERIFIED — TVS diodes fitted at each location (BOM: 10)"
        *Owner: electrical lead.*

No other gauge is labelled; no e-stop (emergency stop) or pack monitor is drawn.
*Source: power wiring diagram.*

Team log (not in the BOM):

- Distribution blocks: double-row 8-hole copper terminal bars (AliExpress
  3256806176225478; 114 mm mount centres, 126 mm overall; M5 × 8 and M8 × 1 screws).
- Pack connectors EC5; charger Amazon B09WKN863V ("ISDT ... DC600Wx2").

!!! unverified "UNVERIFIED — Surge protector, 4 distribution blocks, 10 A fuse, EC5 connectors, charger: diagram or team log only, not the BOM; no confirmed part numbers"
    *Owner: BOM owner + electrical lead.*

✅ **Check:** the series link passes C3 ([Pre-power checks](pre-power-checks.md)).

## Feed the 12 V rail

Run upper-body power block → 10 A fuse → 48V-to-12V buck → MINISFORUM X1-470;
12 V run **16 AWG**. The computer has no power unless the upper-body block
is energised. The two gripper servos are the other 12 V loads (supply not
drawn).

!!! unverified "UNVERIFIED — 12 V conversion: power diagram draws one 48V-to-12V buck (computer only); BOM lists three (2 × 48 V→12 V, 1 × 20–60 V→12 V)"
    *Owner: electrical lead.*

!!! missing "MISSING — Gripper-servo 12 V supply (source, fuse, wiring), USB hub power and power budget"
    *Owner: electrical lead.*

## Protection, disconnect and e-stop

!!! missing "MISSING — SAFETY — No e-stop, main disconnect or pre-charge in the power diagram or BOM, though `humanoid_nav_step_test.py` and `humanoid_joint_monkey_hw.py` require a physical e-stop; part, location and what it cuts unspecified"
    *Owner: electrical lead + safety officer. Blocks pre-power checks and first power-on.*

!!! missing "MISSING — SAFETY — Pack-path fuse (none drawn); surge protector part number and rating"
    *Owner: electrical lead + safety officer.*

## Configured current limits

??? info "Full actuator electrical data"
    | Model | Qty | Max torque (N·m) | Default current limit (A) | Written at scale 0.6 (A) | K<sub>t</sub> (N·m/A<sub>rms</sub>) | R (Ω ±10 %) | K<sub>e</sub> (V<sub>rms</sub>/(rad/s)) |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | RS00 | 2 | 14 | 16.0 | 9.6 | 1.48 | 1.5 | 0.91 |
    | RS02 | 6 | 17.0 | 23.0 | 13.8 | 1.22 | 0.55 | 0.92 |
    | RS03 | 11 | 60.0 | 43.0 | 25.8 | 2.36 | 0.39 | 0.16 |
    | RS04 | 2 | 120.0 | 60.0 | 36.0 | 2.10 | 0.16 | 0.16 |
    | RS05 | 6 | 5.5 | 11.0 | 6.6 | 0.94 | 2.72 | 0.071 |
    | RS06 | 4 | 36 | 57.0 | 34.2 | 1.1 | 0.23 | 0.073 |

    *Source: `control/hardware_bindings/motor/py_motor.py`.*

`control/humanoid_set_current_limit.py` writes `min(default × scale, 40 A)` to
every motor (default scale 0.6). Per-motor phase limits: never sum them to size
wire or fuses.

!!! unverified "UNVERIFIED — RS00, RS05, RS06 voltage range and constants not checked against a manual; back-EMF basis (rotor or output speed) unknown for all models; scale the reference robot ran (script default 0.6, script comment `04 --> scale=0.55`)"
    *Owner: controls lead + hardware lead.*

!!! missing "MISSING — SAFETY — Measured bus current (quiescent, standing, walking) and peak inrush at pack connection"
    *Owner: electrical lead + controls lead.*

✅ **Check:** before any pack is connected: packs in series, bus voltage measured,
fitted converters rated for it, every MISSING — SAFETY item here closed.
