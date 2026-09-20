# Image manifest

Every image this site needs and does not have, with the exact path it must be
saved to and one line on what it must show. **89 images are missing.**

This is the list to hand to whoever renders the exploded views. It is not a
wish list: each path below is already named on a page, so dropping a file at
that path is all that is needed — no page has to be rewritten to accept it.

!!! warning "Why no page shows a broken image"
    `mkdocs build --strict` fails on a link to an image that does not exist, so
    a placeholder cannot be a real `![](…)`. Pages mark a missing figure as a
    blockquote instead:

    ```markdown
    > **Figure** <span class="pending-figure">not produced yet</span> —
    > `assets/assembly/leg-step-02.png`: what the render must show.
    ```

    When the file lands, swap those three lines for the image and delete the
    row from this manifest. Both happen in the same commit or neither does.

## What to produce first

| Priority | What | Why it is first |
| --- | --- | --- |
| 1 | `assets/images/exploded-overview.png` | **The team already has this render.** One file, four pages: the home page, What you get, Bill of materials and Assembly all want the whole-robot exploded view, and it is the single image that makes the machine legible |
| 2 | The 5 subassembly exploded views (leg, arm, torso, head, gripper) | Each one makes its assembly page usable as a whole rather than step by step |
| 3 | The 0 step renders | Written steps without a figure are the site's largest readability gap |
| 4 | The 6 routing photographs | A routing decision does not survive being written down. These must be taken during a build, not reconstructed after one |
| 5 | Everything else | — |

## Format and size

| | |
| --- | --- |
| CAD renders, diagrams | `.png`, or `.svg` for anything with text in it. Long edge 1600 px, transparent or white background |
| Photographs | `.jpg`, long edge 2000 px, under 500 KB. The part in focus, the rest of the bench not |
| Wiring and pinout drawings | `.svg` — they will be read at 200% and they will be corrected |
| Anything animated | `.webp`. Keep it under 5 MB; the existing demo loops are the ceiling, not the target |

Filenames are lowercase with hyphens, except the per-part families below, whose
filenames must match a `part_id` character for character so the page can find
them without a lookup table.

## Missing — referenced by a page (8)

Each of these already has a placeholder blockquote on the page named.

| Path | Page | What it must show |
| --- | --- | --- |
| `assets/assembly/arm-exploded.png` | `assembly/arm.md` | The arm exploded, every part labelled |
| `assets/assembly/gripper-exploded.png` | `assembly/gripper.md` | One gripper exploded and labelled, slide direction and jaw travel drawn |
| `assets/assembly/head-axes-diagram.png` | `assembly/head-and-camera-gimbal.md` | Frame P with both yaw axes, the pitch axis and the optical centre, dimensioned |
| `assets/assembly/head-exploded.png` | `assembly/head-and-camera-gimbal.md` | One column exploded, labelled, axes drawn |
| `assets/assembly/leg-exploded.png` | `assembly/leg.md` | The leg exploded, every part labelled |
| `assets/assembly/subassembly-map.png` | `assembly/index.md` | The build order as a diagram |
| `assets/assembly/torso-exploded.png` | `assembly/torso-and-waist.md` | The torso exploded, every item labelled in its mounting position |
| `assets/images/exploded-overview.png` | `assembly/index.md` | The whole robot exploded into its subassemblies, each labelled with its page |

## Missing — named on a page but not yet placed (26)

These are named in a TODO block or an image manifest but have no placeholder
in the page body yet; add the placeholder in the commit that adds the file.

| Path | Page that will use it | What it must show |
| --- | --- | --- |
| `assets/images/camera-module.png` | `index.md, reference/faq.md` | One camera gimbal module alone, off the robot, dimensioned — so it can be judged as a component by someone who wants only the module. |
| `assets/images/safety-pinch-points.png` | `before-you-start/safety.md` | The robot with every pinch point marked on the real link geometry: between limb and torso, inside each joint, and the jaw closing line. |
| `assets/images/safety-lifting-points.png` | `before-you-start/safety.md, assembly/final-integration.md` | The sanctioned lifting points marked on the machine, with the sling route drawn, and the places that look like handles but are not. |
| `assets/images/safety-hanging-legs-straight.png` | `before-you-start/safety.md` | The robot correctly suspended with the legs hanging straight, next to the same robot hung wrong with the legs bent. Three bring-up sessions were lost to this exact mistake; the pair of images is the whole lesson. |
| `assets/images/safety-estop-location.png` | `before-you-start/safety.md, electrical/power-system.md` | Where the e-stop is mounted and how far an operator has to reach to hit it from outside the robot's envelope. Cannot be produced until an e-stop exists — see the punch list. |
| `assets/bom/fasteners/fastener-size-chart.png` | `bom/fasteners-and-hardware.md` | One-page visual size chart for every fastener in the build, printed 1:1 so a screw can be laid on the page and identified. Blocked on the fastener schedule existing at all. |
| `assets/electrical/system-wiring-diagram.svg` | `electrical/index.md` | Every load, rail, bus and connector on one sheet. The single most valuable missing artefact in the Electrical section. |
| `assets/electrical/power-tree.svg` | `electrical/power-system.md` | Packs, their series/parallel configuration, each converter, each rail and what it feeds, with the fusing and the disconnect drawn where they belong. |
| `assets/electrical/connector-xt30-2p2-pinout.svg` | `electrical/harness-fabrication.md` | XT30(2+2) pinout drawn from the mating face, with the orientation feature and the wire-colour convention. |
| `assets/electrical/connector-actuator-pinout.svg` | `electrical/harness-fabrication.md` | Actuator connector pinout from the mating face, both halves, with the mating part number. |
| `assets/electrical/connector-gripper-servo-pinout.svg` | `electrical/harness-fabrication.md` | Gripper servo connector pinout from the mating face, both halves. |
| `assets/electrical/routing-leg.jpg` | `electrical/routing.md, assembly/leg.md` | Photograph of the finished leg routing before the shank closes, every clamp point visible. Prose does not transfer a routing decision. |
| `assets/electrical/routing-arm.jpg` | `electrical/routing.md, assembly/arm.md` | Photograph of the finished arm routing, showing the service loop at the shoulder and at the wrist. |
| `assets/electrical/routing-waist.jpg` | `electrical/routing.md, assembly/torso-and-waist.md` | Photograph of the waist crossing, the one place a bus spans three subassemblies. |
| `assets/electrical/routing-torso.jpg` | `electrical/routing.md, assembly/torso-and-waist.md` | Photograph of the torso interior with the computer, converters, CAN adapters and packs installed and the harness dressed. |
| `assets/electrical/routing-camera-gimbal.jpg` | `electrical/routing.md, assembly/head-and-camera-gimbal.md` | Photograph of the camera cable through a gimbal column at both yaw extremes, showing the loop and every retention point. The cable across the yaw axis is the highest-risk routing on the robot. |
| `assets/electrical/routing-gripper.jpg` | `electrical/routing.md, assembly/gripper.md` | Photograph of the gripper servo cable and its strain relief at the wrist. |
| `assets/bringup/zero-pose-front.jpg` | `bringup/joint-zeroing.md` | The reference robot held in the zero pose, front view, with the mechanical feature that defines each joint's zero called out. |
| `assets/bringup/zero-pose-side.jpg` | `bringup/joint-zeroing.md` | The same zero pose from the side. Two views are the minimum: one view cannot show both pitch and roll zeros. |
| `assets/bringup/joint-direction-convention.svg` | `bringup/motor-id-and-config.md` | Every joint with its positive direction drawn as an arrow on the real geometry. A backwards joint passes every other check in the site. |
| `assets/bringup/tag-cube-wrist-mounting.jpg` | `bringup/camera-calibration.md` | The tag cube mounted on the wrist interface, with the tag family, tag size and orientation visible. Without this fixture the robot cannot be calibrated. |
| `assets/fabrication/cad-release-assets.png` | `fabrication/cad-downloads.md` | Screenshot of a tagged release page with the CAD archives attached, so a reader knows what a correct release looks like when they see one. |
| `assets/fabrication/machined-parts-laid-out.jpg` | `fabrication/incoming-inspection.md` | The full machined batch laid out and counted on arrival, grouped as the inspection procedure groups them. |
| `assets/fabrication/bearing-bore-measurement.jpg` | `fabrication/incoming-inspection.md` | A bearing bore being measured correctly, showing the instrument and where it sits on the part. |
| `assets/fabrication/printed-parts-orientation.png` | `fabrication/printing-guide.md` | Each structural printed part shown in its validated print orientation, with the load direction the layer lines must not align with drawn on it. |
| `assets/fabrication/heat-set-insert-seated.jpg` | `fabrication/printing-guide.md` | A heat-set insert correctly seated, next to one pressed in too far and one left proud. |

## Missing — per-part families (55)

One image per row of a BOM CSV. The filename **is** the `part_id`, so these
can be produced in a batch and dropped in without touching a page.

| Path pattern | Count | Page | What each must show |
| --- | ---: | --- | --- |
| `assets/bom/cnc/<part_id>.png` | 35 | `bom/cnc-parts.md` | One render per machined part, filename exactly the `part_id` in `cnc-parts.csv`. A machined part a builder cannot see is a part they will order wrong. |
| `assets/bom/electronics/<part_id>.jpg` | 14 | `bom/electronics.md` | One photograph per bought electronic part, filename exactly the `part_id` in `electronics.csv`, so a builder can confirm the thing in the box is the thing on the list. |
| `assets/bom/actuators/<part_id>.jpg` | 6 | `bom/actuators.md` | One photograph per Robstride model, filename exactly the `part_id` in `actuators.csv`. The models look alike and are not interchangeable. |

??? note "The 35 filenames for `assets/bom/cnc/<part_id>.png`"

    - `CNC_leg01_hip_center_back`
    - `CNC_leg02_RS03_shaft_coupler`
    - `CNC_leg03_RS03_shaft_bearing_retainer`
    - `CNC_leg04_hip_roll_front_bearing_retainer`
    - `CNC_leg05_hip_roll_back_bearing_retainer`
    - `CNC_leg06_hip_roll_output_shaft`
    - `CNC_leg07_hip_roll_support_shaft`
    - `CNC_leg08_knee_front_bearing_retainer`
    - `CNC_leg09_knee_motor_back_cover`
    - `CNC_leg10_knee_output_shank`
    - `CNC_leg11_knee_support_shank`
    - `CNC_leg12_lower_leg_bearing`
    - `CNC_leg13_ankle_pitch_front`
    - `CNC_leg14_ankle_pitch_back`
    - `CNC_leg15_RS06_shaft_bearing_retainer`
    - `CNC_leg16_ankle_roll_output_shaft`
    - `CNC_leg17_ankle_roll_support_shaft`
    - `CNC_leg18_foot_plate`
    - `CNC_arm01_shoulder_roll_front_bearing`
    - `CNC_arm02_shoulder_roll_back_bearing`
    - `CNC_arm03_shoulder_roll_output_shaft`
    - `CNC_arm04_shoulder_roll_support_shaft`
    - `CNC_arm05_RS02_shaft_bearing`
    - `CNC_arm06_RS02_shaft_coupler`
    - `CNC_arm07_elbow_front_bearing`
    - `CNC_arm08_elbow_back_bearing`
    - `CNC_arm09_elbow_output_shaft`
    - `CNC_arm10_r03_back_cover`
    - `CNC_arm11_wrist_roll`
    - `CNC_arm12_wrist_pitch`
    - `CNC_arm13_RS05_shaft_coupler`
    - `CNC_body01_bottom_plate`
    - `CNC_body02_side_plate`
    - `CNC_body03_top_plate`
    - `CNC_body04_front_plate`

??? note "The 14 filenames for `assets/bom/electronics/<part_id>.jpg`"

    - `EL_COMPUTE_MINIPC`
    - `EL_BATTERY_6S`
    - `EL_TVS_DIODE`
    - `EL_SERVO_DRIVER`
    - `EL_BUCK_12V_ENC`
    - `EL_BUCK_48V_12V`
    - `EL_CAN_ADAPTER`
    - `EL_CAM_D436`
    - `EL_SERVO_FEETECH`
    - `EL_USB_HUB`
    - `EL_IMU_TM171`
    - `EL_SURGE_PROTECTOR`
    - `EL_DIST_BLOCK`
    - `EL_VOLTAGE_CHECKER`

??? note "The 6 filenames for `assets/bom/actuators/<part_id>.jpg`"

    - `ACT_RS00`
    - `ACT_RS02`
    - `ACT_RS03`
    - `ACT_RS04`
    - `ACT_RS05`
    - `ACT_RS06`

## Already here (7)

Real photographs of the reference robot, copied from the project repository's
`media/` directory. They show a working machine; none of them is an assembly
figure, and none of them substitutes for a render.

| Path | Used on | What it shows |
| --- | --- | --- |
| `assets/images/teaser.webp` | `index.md` | The robot in simulation and on hardware, side by side. |
| `assets/images/hardware.webp` | `index.md` | Hardware overview with all joints numbered and the three modules labelled. |
| `assets/images/hardware_tracking.mp4` | `index.md` | The reference robot tracking two independently moving targets. |
| `assets/images/vrw_fixed_vs_actuated.mp4` | `index.md` | Visible-reachable workspace, fixed head versus actuated camera modules. |
| `assets/images/hardware_close_front_back.mp4` | `assembly/head-and-camera-gimbal.md` | The two finished camera modules aiming independently. |
| `assets/images/two_target_handoff_left_right.mp4` | `bringup/acceptance-tests.md` | What passing acceptance test A10 looks like. |
| `assets/images/workspace.webp` | `reference/faq.md` | Visible-reachable workspace across six humanoid platforms. |

## Counting

| | |
| --- | ---: |
| Referenced by a page, missing | 8 |
| Named on a page, not yet placed | 26 |
| Per-part families | 55 |
| **Missing, total** | **89** |
| Present | 7 |

## Regenerating this page

Derived from the placeholders on the pages and from the BOM CSVs, not
maintained by hand:

```console
$ python tools/gen_image_manifest.py
```

The per-part families come from `part_id` columns, so a new row in
`cnc-parts.csv` adds its render to this list automatically. Figures that are
named on a page but have no placeholder yet are the one hand-maintained part,
in the `EXTRA` table at the top of that script.

