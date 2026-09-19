# Head and camera gimbal

Build two identical camera columns, each a RealSense D436 on its own yaw–pitch gimbal.

!!! abstract "At a glance"
    - **You will:** build and bench-test each (the right is the left rotated 180°), then mount both.
    - **Parts:** RobStride 05 ×4 ([Actuators](../bom/actuators.md)); Intel RealSense D436 ×2 ([Electronics](../bom/electronics.md)); per column `gimbal_mount`, `gimbal_neck`, `gimbal_arm`, `U-joint_type_C_adapter`.
    - **Before this:** [Torso and waist](torso-and-waist.md).

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="800" height="800" poster="../../assets/images/hardware_close_front_back-poster.webp" aria-label="The two camera modules on the reference robot, each aiming at a different target">
    <source src="../../assets/images/hardware_close_front_back.mp4" type="video/mp4">
    <a href="../../assets/images/hardware_close_front_back.mp4">MP4</a>
  </video>
  <figcaption>The finished columns on the robot, aiming independently.</figcaption>
</figure>

!!! missing "MISSING — gimbal column procedure: fasteners, torques, locations, zeros"
    - Per step: screws, torque, Loctite 222 use, order.
    - Yaw actuator location and any yaw bearing; neck keying.
    - Yaw and pitch zeros; hard stops.
    - Camera screw torque and pose tolerance; mount location and plate flatness.

    *Owner: hardware lead.*

> **Figure** <span class="pending-figure">not produced yet</span> —
> `assets/assembly/head-exploded.png`: one column exploded, labelled, axes drawn.

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="1280" height="720"
    poster="../../assets/exploded/twincities-poster.webp" aria-label="Exploded view of one camera gimbal column"><source src="../../assets/exploded/twincities.mp4" type="video/mp4"><a href="../../assets/exploded/twincities.mp4">MP4</a></video>
  <figcaption>One column: pedestal, yaw actuator, neck, pitch actuator, two L-shaped arms (pitch output and idler bearing), camera.</figcaption>
</figure>

{{ step(1, "Configure the actuators and record the camera serials") }}

Set and label IDs 5–8 on the bench. Assign each camera serial to a side: the
software binds cameras by serial.

| Joint | Actuator | ID | Bus |
| --- | --- | --- | --- |
| `cam_yaw_right` | RobStride 05 | 5 | `can25` |
| `cam_pitch_right` | RobStride 05 | 6 | `can25` |
| `cam_yaw_left` | RobStride 05 | 7 | `can25` |
| `cam_pitch_left` | RobStride 05 | 8 | `can25` |

*Source: [`humanoid_config.py`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/humanoid_config.py).*

!!! missing "MISSING — which physical side carries `cam_yaw_left` (ID 7) and `cam_pitch_left` (ID 8)"
    Computer-aided design (CAD): left at y = −65 mm; MuJoCo model: y = +0.065 m.
    A swap fails silently. *Owner: hardware lead + controls.*

✅ **Check:** IDs 5 to 8 answer on can25; both serials assigned.

{{ step(2, "Install the yaw actuator in the mount") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| `gimbal_mount` — the base | 1 |
| RobStride 05 — yaw, ID 7 (left) / 5 (right) | 1 |

</div>

Centre the actuator on the yaw axis: tilt here is magnified at the camera.

!!! missing "MISSING — gimbal parts are in no bill of materials: material, process, tolerance, cost, bearing, fasteners"
    *Owner: hardware lead + BOM owner.*

✅ **Check:** Turns freely, no axial play; mount bottom face flat and clean.

{{ step(3, "Fit the neck to the yaw output") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| `gimbal_neck` — carries the pitch actuator | 1 |

</div>

✅ **Check:** The neck spins square to the yaw axis without wobble.

{{ step(4, "Install the pitch actuator and the arm") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| RobStride 05 — pitch, ID 8 (left) / 6 (right) | 1 |
| `gimbal_arm` — yoke carrying the camera | 1 **UNVERIFIED**{ .dh-unverified } |
| Flanged ball bearing, pitch idler, size **TODO**{ .dh-missing } | 1 |

</div>

Make the pitch axis perpendicular to, and intersecting, the yaw axis.

!!! unverified "UNVERIFIED — `gimbal_arm`: one part or two; `U-joint_type_C_adapter`: mechanical or a USB-C cable adapter"
    *Owner: hardware lead.*

✅ **Check:** No binding; the arm clears neck and mount.

{{ step(5, "Mount the camera") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| Intel RealSense D436 for this side | 1 |
| `U-joint_type_C_adapter` | 1 |

</div>

Hold the camera by its body; keep the lens film on until done. Factory
extrinsics differ per unit: read your own at
[Camera calibration](../bringup/camera-calibration.md).

!!! unverified "UNVERIFIED — the bracket CAD names a D435 body; confirm the D436 fits before machining"
    *Owner: hardware lead.*

✅ **Check:** The camera does not move under hand pressure.

{{ step(6, "Route the camera cable") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| USB-C cable, type and length **TODO**{ .dh-missing } | 1 |
| Cable retention **TODO**{ .dh-missing } | As needed |

</div>

Avoid tight bends: a flexed USB 3 cable can drop the camera to USB 2.

| Joint | Model limit | Note |
| --- | --- | --- |
| Yaw | ±270° | Training choice, not a mechanical limit |
| Pitch | ±90° **UNVERIFIED**{ .dh-unverified } | CAD fit: −89.71° to +87.91° |

!!! missing "MISSING — SAFETY — camera cable across the yaw and pitch axes"
    - Real yaw travel; how the USB-C cable crosses yaw (slip ring, helix or stop).
    - Cable type, length, bend radius, service loop, retention.
    - Until then, command yaw only within travel verified by hand with the
      cable fitted.

    *Owner: hardware lead + electrical.*

✅ **Check:** No cable tension through verified travel; USB 3 at every extreme.

{{ step(7, "Bench-test the column") }}

- both actuators move and report on `can25`;
- colour and depth stream;
- yaw moves the image sideways, pitch vertically;
- nothing heats or binds over a few hundred cycles of verified travel.

!!! missing "MISSING — single-column bench harness and written test procedure"
    *Owner: hardware lead + controls.*

✅ **Check:** All checks pass with no camera dropout.

{{ step(8, "Build the second column") }}

Repeat steps 2–7 with the other side's IDs and camera.

✅ **Check:** The second column passes the bench test.

> **Figure** <span class="pending-figure">not produced yet</span> —
> `assets/assembly/head-axes-diagram.png`: frame P with both yaw axes, the
> pitch axis and the optical centre, dimensioned.

{{ step(9, "Mount both columns on the top plate") }}

Mount bolt holes are concentric with plate holes: align each mount by its holes,
flush on the plate, the second column rotated 180°.

??? info "Full mounting geometry (from the CAD, not measured)"
    | Quantity | Value |
    | --- | --- |
    | Top plate `CNC_body03_x1_top_plate` | 130 × 180 × 8 mm, 31 holes |
    | Mount bottom face | Flush on the plate top face (z = 0) |
    | Yaw axes | Vertical, x = 0, y = ±65 mm |
    | Yaw-axis spacing | **130.00 mm** (±0.01 mm self-check) |
    | Pitch axis | Along Y, x ≈ 0, z = **+213.44 mm**; collinear for both columns |
    | Yaw reference to pitch axis | 105.44 mm |
    | Camera optical centre | z ≈ +250 mm **UNVERIFIED**{ .dh-unverified } |
    | Mount envelope | 80 × 66.3 × 84 mm |
    | Column mass (CAD) | 0.58 kg: base 0.246 kg, yaw link 0.233 kg, pitch link 0.100 kg **UNVERIFIED**{ .dh-unverified } |

Frame P: origin at the centre of the top plate's central hole, on its top face;
+Z up.

!!! unverified "UNVERIFIED — top plate central hole: round (CAD parse) or hexagonal (CAD animation)"
    *Owner: hardware lead.*

✅ **Check:** Yaw axes 130.00 mm apart, pitch axes collinear, no shims, columns never touch.

{{ step(10, "Record the as-built geometry") }}

Record, for [Camera calibration](../bringup/camera-calibration.md):

- camera serial per side;
- IDs per column;
- measured yaw-axis spacing;
- verified travel per joint.
