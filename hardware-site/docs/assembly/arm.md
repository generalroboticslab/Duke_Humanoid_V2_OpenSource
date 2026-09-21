# Arm

Build one seven-joint arm (0.46 m reach); build two. Grippers go on in [Final integration](#final-integration).

!!! abstract "At a glance"
    - **You will:** set seven IDs, then build from shoulder to wrist.
    - **Parts:** RobStride 02 ×3; 00, 03, 05, 06 ×1 each ([Actuators](../bom/index.md#actuators)); `CNC_arm01`–`CNC_arm13` ([machined parts](../bom/index.md#cnc-parts)).
    - **Before this:** [Leg](#leg).

!!! note "Read off the model — arm parts list, fasteners and fits"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    - No bearing, spacer, printed-part or fastener list.
    - Per step: screws, torque, Loctite 222 use, bearings, press fits, order,
      alignment and preload (steps 3, 5).
    - Whether shoulder cabling must pass through a joint before it closes.

    *Owner: hardware lead, from the computer-aided design (CAD) and a photographed build.*

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="1280" height="720"
    poster="../../assets/exploded/arm-poster.webp" aria-label="Exploded view of one arm, shoulder-pitch actuator to wrist"><source src="../../assets/exploded/arm.mp4" type="video/mp4"><a href="../../assets/exploded/arm.mp4">MP4</a></video>
  <figcaption>Shoulder pitch to wrist. Shoulder roll and elbow each sit in a two-plate yoke, one bearing per plate.</figcaption>
</figure>

{{ step(1, "Configure and label the seven actuators") }}

Set each ID on the bench, one at a time. Label joint, ID **and bus**:
`shoulder_1` is on `can22`, not its arm's bus.

| Joint | Axis | Actuator | ID L / R | Bus L / R | Model limit |
| --- | --- | --- | --- | --- | --- |
| `shoulder_1` | pitch | RobStride 03 | 10 / 20 | `can22` / `can22` | ±180° |
| `shoulder_2` | roll | RobStride 06 | 11 / 21 | `can9` / `can21` | L −180° to +30°, R −30° to +180° |
| `shoulder_3` | yaw | RobStride 02 | 12 / 22 | `can9` / `can21` | ±180° |
| `elbow` | — | RobStride 02 | 13 / 23 | `can9` / `can21` | ±125° |
| `wrist_1` | roll | RobStride 02 | 14 / 24 | `can9` / `can21` | ±180° |
| `wrist_2` | pitch | RobStride 00 | 15 / 25 | `can9` / `can21` | ±92° |
| `wrist_3` | yaw | RobStride 05 | 16 / 26 | `can9` / `can21` | ±90° |

*Source: [`humanoid_config.py`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/humanoid_config.py); limits from `humanoid_v21.xml`; axes from the repo `README.md` (Hardware), which names joints 1–7 shoulder pitch/roll/yaw, elbow, wrist roll/pitch/yaw.*

!!! note "Not measured on the reference robot — hard stops, and how far the four ±180° joints really turn with cabling fitted"
    *Owner: hardware lead.*

✅ **Check:** Each answers alone at its ID and is labelled.

<figure markdown>
  ![Right arm exploded, parts labelled with team BOM ids](../assets/exploded/team/09-arm.webp){ loading=lazy }
  <figcaption>Steps 2–8, body outward to the wrist: machined parts C5 and C22–C29, printed parts P4–P8, actuators E1, E2, E5 and E6, bearings H2 and H4. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

{{ step(2, "Build the shoulder-pitch joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 03 — `shoulder_1` | 1 |
| `CNC_arm10_x4_r03_back_cover` | **TODO**{ .dh-missing } |

</div>

In the CAD the body sits in the torso side plate, output outward; the arm
starts with a square adapter on that output. Plate or arm first:
**UNVERIFIED**{ .dh-unverified } ([Assembly](index.md)).

!!! note "Build to the model — `arm05`–`arm10` IDs differ between the team list and this site"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    Steps below use site IDs; order by part name until settled. Team list:
    `arm05` RS02 back cover, `arm06` RS02 bearing retainer, `arm07` RS02
    coupler ×4, `arm08`/`arm09` elbow front/back retainer, `arm10` elbow output
    shaft ×2; no RS03 back cover, no `arm11`–`arm13`. *Owner: hardware lead.*

✅ **Check:** Turns freely, no axial play; back cover sits without a gap.

{{ step(3, "Build the shoulder-roll joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 06 — `shoulder_2` | 1 |
| `CNC_arm03_x2_shoulder_roll_output_shaft` | **TODO**{ .dh-missing } |
| `CNC_arm04_x4_shoulder_roll_support_shaft` | **TODO**{ .dh-missing } |
| `CNC_arm01_x2_shoulder_roll_front_bearing` | **TODO**{ .dh-missing } |
| `CNC_arm02_x2_shoulder_roll_back_bearing` | **TODO**{ .dh-missing } |

</div>

Make both bearing housings concentric before tightening.

✅ **Check:** Turns end to end, equal drag both ways, no axial play.

{{ step(4, "Build the shoulder-yaw joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 02 — `shoulder_3` | 1 |
| `CNC_arm05_x4_RS02_shaft_bearing` | **TODO**{ .dh-missing } |
| `CNC_arm06_x4_RS02_shaft_coupler` | **TODO**{ .dh-missing } |

</div>

✅ **Check:** The three shoulder joints move independently, nothing taut.

{{ step(5, "Build the elbow joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 02 — `elbow` | 1 |
| `CNC_arm09_x2_elbow_output_shaft` | **TODO**{ .dh-missing } |
| `CNC_arm07_x2_elbow_front_bearing` | **TODO**{ .dh-missing } |
| `CNC_arm08_x2_elbow_back_bearing` | **TODO**{ .dh-missing } |
| `CNC_arm05_x4_RS02_shaft_bearing` | **TODO**{ .dh-missing } |
| `CNC_arm06_x4_RS02_shaft_coupler` | **TODO**{ .dh-missing } |

</div>

✅ **Check:** No axial play; clears the upper arm at both ends.

{{ step(6, "Build the wrist-roll joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 02 — `wrist_1` | 1 |
| `CNC_arm11_x2_wrist_roll` | **TODO**{ .dh-missing } |
| `CNC_arm05_x4_RS02_shaft_bearing` | **TODO**{ .dh-missing } |
| `CNC_arm06_x4_RS02_shaft_coupler` | **TODO**{ .dh-missing } |

</div>

✅ **Check:** Turns freely, no axial play.

{{ step(7, "Build the wrist-pitch joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 00 — `wrist_2` | 1 |
| `CNC_arm12_x2_wrist_pitch` | **TODO**{ .dh-missing } |

</div>

Check the RobStride 00 screw sizes; they may differ.

✅ **Check:** No binding; clears the wrist-roll body at both ends.

{{ step(8, "Build the wrist-yaw joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 05 — `wrist_3` | 1 |
| `CNC_arm13_x2_RS05_shaft_coupler` | **TODO**{ .dh-missing } |

</div>

The `wrist_3` output carries the gripper's own flange.

!!! note "Read off the model — wrist-to-gripper interface: bolt circle, pilot, keying, cable pass-through"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: hardware lead.*

✅ **Check:** The three wrist axes move together without contact.

<figure markdown>
  ![Printed arm covers exploded, parts labelled with team BOM ids](../assets/exploded/team/10-arm-covers.webp){ loading=lazy }
  <figcaption>Printed arm covers P33–P39, shoulder to wrist. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

{{ step(9, "Route the harness and close the arm") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| Arm harness branch | 1 |
| Gripper servo cable, shoulder to wrist | 1 |
| Cable ties and anchors | As needed |

</div>

Three cable groups:

- `can22` to `shoulder_1`;
- `can9` or `can21` to the other six joints;
- the gripper servo cable, from its driver board in the torso.

!!! note "Read off the model — arm harness lengths, routes and service loops"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    See [Harness fabrication](../electrical/index.md#harness-fabrication).
    *Owner: hardware lead + electrical.*

✅ **Check:** All seven joints move through their travel with no cable stretched or pinched; measured travel recorded per joint.

## Build the second arm

<figure markdown>
  ![Left arm exploded with the left wrist housing labelled](../assets/exploded/team/11-torso-p9.webp){ loading=lazy }
  <figcaption>The second arm uses the same chain with the left wrist housing P9 in place of the right housing P7. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

Repeat steps 2–9, swapping each A cover with its B cover (P33/P34, P37/P38):
the other arm takes the same printed covers in the mirrored positions.
*Source: team exploded-view booklet, pages 11 and 12.*

**The arms are mirrored, not identical.** `shoulder_2` travel runs −180°…+30°
on the left and −30°…+180° on the right; every other arm joint takes the same
symmetric range on both sides. Which machined parts that makes handed is
readable off the model.
*Source: `humanoid_v21_full.urdf`.*
