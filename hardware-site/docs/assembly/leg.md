# Leg

Build one leg, hip to foot plate; build two.

!!! abstract "At a glance"
    - **You will:** set six IDs, then build from hip to foot.
    - **Parts:** RobStride 03 ×4, 04 ×1, 06 ×1 ([Actuators](../bom/index.md#actuators)); `CNC_leg01`–`CNC_leg18` ([machined parts](../bom/index.md#cnc-parts)).
    - **Before this:** [Tools](#tools).

RobStride 03 mounting interface (*manual, §1.1*); keep every screw within these depths:

- **Housing:** 8 × M4, 8 mm deep, on Ø98 mm.
- **Output:** 6 × M4, 6 mm deep; 3 × Ø4 mm pin holes, 7 mm deep; Ø70 mm pilot, 2.5 mm proud.

!!! note "Read off the model — leg parts list, fasteners and fits"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    - No printed-part, bearing, spacer or fastener list.
    - Per step: screws, torque, Loctite 222 use, bearings, press fits, order.
    - Retainer alignment and preload (steps 3, 8).
    - Whether the knee back cover is structural.
    - Whether ankle cabling must pass through the shank before it closes.

    *Owner: hardware lead, from the computer-aided design (CAD) and a photographed build.*

{{ step(1, "Configure and label the six actuators") }}

The six joints share one Controller Area Network (CAN) bus: `can24` left, `can23` right.
New units share a default ID: set each on the bench alone ([Motor ID and config](../bringup/index.md#motor-id-and-config)).

| Joint | Model axis | Actuator | ID L / R | Model limit L | Model limit R |
| --- | --- | --- | --- | --- | --- |
| `hip_1` | pitch | RobStride 03 | 31 / 41 | ±105° | ±105° |
| `hip_2` | roll | RobStride 03 | 32 / 42 | −105° to +30° | −30° to +105° |
| `hip_3` | yaw | RobStride 03 | 33 / 43 | ±90° | ±90° |
| `knee` | — | RobStride 04 | 34 / 44 | ±130° | ±130° |
| `ankle_1` | pitch | RobStride 03 | 35 / 45 | ±50° | ±50° |
| `ankle_2` | roll | RobStride 06 | 36 / 46 | ±60° | ±60° |

*Source: [`humanoid_config.py`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/humanoid_config.py); axes (at zero pose) and limits from `humanoid_v21.xml`.*

The model tilts the `hip_1` axis 15° from horizontal; `hip_3` is vertical.

!!! note "Not measured on the reference robot — hard-stop angles, where a leg joint has one"
    The travel each joint is commanded to is published in
    [Motor ID and configuration](../bringup/index.md#motor-id-and-config).
    *Owner: hardware lead.*

✅ **Check:** Each answers alone at its ID and is labelled.

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="1280" height="720"
    poster="../../assets/exploded/hip-assembly-poster.webp" aria-label="Exploded view of the pelvis block with the waist and four hip actuators"><source src="../../assets/exploded/hip-assembly.mp4" type="video/mp4"><a href="../../assets/exploded/hip-assembly.mp4">MP4</a></video>
  <figcaption>Pelvis: waist actuator with flange, ring and coupler; two hip actuators per side.</figcaption>
</figure>

<figure markdown>
  ![Hip pitch and roll exploded, parts labelled with team BOM ids](../assets/exploded/team/04-leg-upper.webp){ loading=lazy }
  <figcaption>Steps 2–3, body outward: brackets, retainers and shafts C4–C8, actuators E3, bearings H0. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

{{ step(2, "Build the hip-pitch joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 03 — `hip_1` | 1 |
| `CNC_leg01_x2_hip_center_back` | **TODO**{ .dh-missing } |
| `CNC_leg02_x7_RS03_shaft_coupler` | **TODO**{ .dh-missing } |
| `CNC_leg03_x5_RS03_shaft_bearing_retainer` | **TODO**{ .dh-missing } |

</div>

**UNVERIFIED**{ .dh-unverified }: the CAD puts `hip_1` and `hip_2` in the
pelvis ([Assembly](index.md)).

!!! note "Build to the model — `leg02` and `leg12` counts differ between the two lists"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    *Owner: hardware lead.*

✅ **Check:** Turns freely, even drag, no axial play.

{{ step(3, "Build the hip-roll joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 03 — `hip_2` | 1 |
| `CNC_leg06_x2_hip_roll_output_shaft` | **TODO**{ .dh-missing } |
| `CNC_leg07_x2_hip_roll_support_shaft` | **TODO**{ .dh-missing } |
| `CNC_leg04_x2_hip_roll_front_bearing_retainer` | **TODO**{ .dh-missing } |
| `CNC_leg05_x2_hip_roll_back_bearing_retainer` | **TODO**{ .dh-missing } |
| `CNC_leg02_x7_RS03_shaft_coupler` | **TODO**{ .dh-missing } |

</div>

Make both bearing retainers concentric before tightening.

✅ **Check:** Turns end to end without binding, equal drag both ways, no axial play.

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="1280" height="720"
    poster="../../assets/exploded/leg-poster.webp" aria-label="Exploded view of one leg hanging from the pelvis block"><source src="../../assets/exploded/leg.mp4" type="video/mp4"><a href="../../assets/exploded/leg.mp4">MP4</a></video>
  <figcaption>Leg below the pelvis: hip yaw, knee, two shank links, ankle pitch, ankle roll, foot plate.</figcaption>
</figure>

<figure markdown>
  ![Hip yaw to foot plate exploded, parts labelled with team BOM ids](../assets/exploded/team/05-leg-lower.webp){ loading=lazy }
  <figcaption>Steps 4–9, hip yaw down to the foot plate: machined parts C4, C5 and C9–C21, actuators E3, E4 and E6, bearings H0–H3. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

{{ step(4, "Build the hip-yaw joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 03 — `hip_3` | 1 |
| `CNC_leg02_x7_RS03_shaft_coupler` | **TODO**{ .dh-missing } |
| `CNC_leg03_x5_RS03_shaft_bearing_retainer` | **TODO**{ .dh-missing } |

</div>

!!! note "Build to the model — no machined part is named for hip yaw; the CAD shows the waist flange, ring and coupler"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    *Owner: hardware lead.*

✅ **Check:** The three hip joints move independently with no interference or taut cable.

{{ step(5, "Build the knee joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 04 — `knee` | 1 |
| `CNC_leg08_x2_knee_front_bearing_retainer` | **TODO**{ .dh-missing } |
| `CNC_leg09_x2_knee_motor_back_cover` | **TODO**{ .dh-missing } |

</div>

!!! note "The M5/M4 CAD error is tracked on [CNC guide](../fabrication/index.md#cnc-guide)"
    Found at the first-article fit check; whether the released CAD is fixed is
    unknown. Check your parts before choosing screws. *Owner: hardware lead.*

✅ **Check:** Turns freely, no axial play; back cover sits without a gap.

{{ step(6, "Join the shank to the knee") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| `CNC_leg10_x2_knee_output_shank` | **TODO**{ .dh-missing } |
| `CNC_leg11_x2_knee_support_shank` | **TODO**{ .dh-missing } |
| `CNC_leg12_x4_lower_leg_bearing` | **TODO**{ .dh-missing } |

</div>

Two links, knee to ankle: a flat plate and a pocketed truss. Which
is `leg10` is **UNVERIFIED**{ .dh-unverified }.

✅ **Check:** The knee still turns freely; ankle cabling moves freely in the shank.

{{ step(7, "Build the ankle-pitch joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 03 — `ankle_1` | 1 |
| `CNC_leg13_x2_ankle_pitch_front` | **TODO**{ .dh-missing } |
| `CNC_leg14_x2_ankle_pitch_back` | **TODO**{ .dh-missing } |
| `CNC_leg02_x7_RS03_shaft_coupler` | **TODO**{ .dh-missing } |
| `CNC_leg03_x5_RS03_shaft_bearing_retainer` | **TODO**{ .dh-missing } |

</div>

✅ **Check:** No axial play; clears the shank at both ends.

{{ step(8, "Build the ankle-roll joint") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 06 — `ankle_2` | 1 |
| `CNC_leg16_x2_ankle_roll_output_shaft` | **TODO**{ .dh-missing } |
| `CNC_leg17_x2_ankle_roll_support_shaft` | **TODO**{ .dh-missing } |
| `CNC_leg15_x2_RS06_shaft_bearing_retainer` | **TODO**{ .dh-missing } |

</div>

Make both shaft ends concentric before tightening.

✅ **Check:** No axial play; pitch and roll never collide.

{{ step(9, "Fit the foot plate") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| `CNC_leg18_x2_foot_plate` | **TODO**{ .dh-missing } |

</div>

!!! note "Read off the model — whether a foot sole or pad is fitted"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: hardware lead.*

✅ **Check:** At ankle zero the foot sits flat.

<figure markdown>
  ![Printed leg covers exploded, parts labelled with team BOM ids](../assets/exploded/team/06-leg-covers.webp){ loading=lazy }
  <figcaption>Printed leg covers P20–P32, hip to sole. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

{{ step(10, "Route the harness and close the leg") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| Leg harness branch: one CAN daisy chain plus power | 1 |
| Cable ties and anchors | As needed |

</div>

It leaves at the hip; join it in [Final integration](#final-integration).

!!! note "Read off the model — leg harness lengths, routes and service loops"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: hardware lead + electrical.*

✅ **Check:** All six joints move through their travel with no cable stretched or pinched. Nothing rattles.

## Build the second leg

Repeat steps 2–10, swapping each A cover with its B cover (P20/P21, P22/P23,
P24/P25, P26/P27): the other leg takes the same printed parts in the mirrored
positions.
*Source: team exploded-view booklet, page 8.*

**The legs are mirrored, not identical.** `hip_2` travel runs −105°…+30° on
the left and −30°…+105° on the right; every other leg joint takes the same
symmetric range on both sides. Which machined parts that makes handed is
readable off the model.
*Source: `humanoid_v21_full.urdf`.*
