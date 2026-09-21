# Gripper

Build one rack-and-pinion parallel gripper (one serial-bus servo drives both jaws 1:1 on mirrored slides); build two.

!!! abstract "At a glance"
    - **You will:** configure the servos, build, then set the jaw positions.
    - **Parts:** per gripper, one servo and driver board ([Electronics](../bom/index.md#electronics)); `base` (servo, slides, two tag-holder plates, USB-C protector); `left_rack` and `right_rack` (the jaws); `cnc_flange` (machined disc, the wrist interface).
    - **Before this:** [Head and camera gimbal](#head-and-camera-gimbal).

!!! note "Read off the model — gripper parts list, fasteners and fits"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    - Material, process and cost of `base`, both racks and `cnc_flange`.
    - Pinion, slide parts, fasteners.
    - Per step: screws, torque, Loctite 222 use, order.
    - Servo retention, pinion mounting, backlash, rack timing, slide preload and
      lubrication.

    *Owner: hardware lead + BOM owner.*

{{ step(1, "Configure and label the two servos") }}

Set each servo ID on its board, one at a time. Mark ID and hand on the servo;
record each board's USB serial against its hand.

| | Left | Right |
| --- | --- | --- |
| Servo | Feetech HL-3915-C001, 12 V | same |
| Servo ID | 5 | 19 |
| Driver | Waveshare ST/SC board on USB hub 3, found by its CH340 serial | same |

*Source: `deploy/control/move_grip.py` line 42 (`GRIPPER_ID = 19  # 19 is the RIGHT gripper`).*

✅ **Check:** Each servo answers at its ID; hands and board serials recorded.

<figure markdown>
  ![One gripper exploded, parts labelled with team BOM ids](../assets/exploded/team/13-gripper.webp){ loading=lazy }
  <figcaption>Steps 2–5, one of two identical grippers: housing P10, racks P11, pinion P12, fingers P13, AprilTag holders P14, tags P15, servo E15, driver board E10, converter E12. Labels are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

{{ step(2, "Build the gripper base") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| `base` | 1 |
| Servo, ID set | 1 |

</div>

✅ **Check:** The servo is fixed and turns the pinion with no lost motion.

{{ step(3, "Fit both racks") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| `left_rack`, `right_rack` | 1 each |
| Slide or rail parts | **TODO**{ .dh-missing } |

</div>

Engage both racks on the pinion from opposite sides, jaws symmetric about the
centreline.

✅ **Check:** The jaws move together, parallel and symmetric, without binding.

{{ step(4, "Fit the jaw pads") }}

!!! note "Read off the model — whether jaw pads are fitted, and how"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: hardware lead.*

✅ **Check:** The pads meet flat when the jaws close.

{{ step(5, "Apply the AprilTags") }}

<div class="parts-needed" markdown>

| | |
| --- | --- |
| AprilTag tag36h11: 4 on the jaw plates, 4 on the base pads | 8 |

</div>

Seat each tag square in its pocket, with the ID that
`simulation/asset/duke_v2/parallel_gripper/tag_layout.py` assigns to that slot
and hand. A wrong tag is an invisible pose error.

Print each tag at the size the detector expects. Deploy perception configures a
16 mm black square (`tag_size` 0.016) inside a 2 mm white border, filling the
20 × 20 mm plate or pad (`deploy/perception/tagged_bodies/parallel_gripper/__init__.py`);
the simulation decals (`make_tags.py`) stretch the 8 × 8 black pattern to the
full 20 mm and do not set the print size.
`deploy/perception/asset/tag_creation/print_apriltags.py` takes the
black-to-black size as `--size-mm`.

!!! note "Yours to determine — AprilTag substrate, adhesive and replacement"
    *Owner: perception + hardware lead.*

✅ **Check:** All eight tags sit square, carry the right IDs, and detect at working distance.

{{ step(6, "Fit the mounting flange") }}

**Clock the jaws to open front-to-back at encoder zero.** Deploy asserts it on
every model rebuild (`deploy/control/rebuild_deploy_model.py`, lines 58 and 352);
a left-right build fails that check.

!!! note "Read off the model — flange bolt circle, pilot and keying"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    Document with the arm side ([Arm](#arm), step 8). *Owner: hardware lead.*

✅ **Check:** The flange is square to the body and matches the wrist bolt ring.

{{ step(7, "Set the open and closed positions") }}

!!! danger "Crush hazard"
    Keep fingers out of the jaws while powered. Set a torque limit before the
    first close.

Find each hand's closed position with the gripper service's zero routine
(`deploy/control/humanoid_end_effector_service.py`):

1. Empty both grippers; the routine records whatever it pinches as closed.
2. From `control/`, start the service with its test page:
   `python humanoid_end_effector_service.py --gui` (web page on port 8080).
3. Under one hand, press **Zero Gripper**. The service closes the jaws at
   reduced torque and speed until the servo stalls, backs off and pinches
   again (a third time if the two disagree), and keeps the deepest stall as
   that hand's closed position.
4. Note that the service sets the open position to closed − 6000 counts; it
   does not find the open end stop.
5. Repeat for the other hand. Each hand is calibrated on its own.

| Setting in the service | Deploy configures (raw servo value) |
| --- | --- |
| Default move torque (`TORQUE`) | 500 |
| Zeroing torque / speed (`ZERO_TORQUE`, `ZERO_SPEED`) | 150 / 300 |
| Grasp approach / squeeze torque | 300 / 350 |
| Static hold torque ceiling (`HOLD_TORQUE_DEFAULT`) | 200 |
| Open / closed position before zeroing (`HAND_POS_OPEN`, `HAND_POS_CLOSE`) | −3000 / 3200 |
| Open offset from zeroed closed (`OPEN_OFFSET_FROM_CLOSE`) | 6000 counts |

Record:

- servo position, fully open and fully closed;
- closing torque limit;
- measured finger gap (mm), open and at fingers-touch.

Each rack travels −50 mm to +34.7 mm in the URDF, so the two jaws separate by
about **169 mm** end to end — near the model docs' 184 mm, not the service
map's 90 mm. *Source: `humanoid_v21_full.urdf` (`L_left_rack_y` / `L_right_rack_y`).*

!!! unverified "UNVERIFIED — the uncalibrated service map reports 90 mm; measure the real gap in step 7"
    *Owner: hardware lead + controls.*

| Model value | |
| --- | --- |
| Mass with flange | ≈ 346 g (324 + 22 g) **UNVERIFIED**{ .dh-unverified } |
| Fingertip reach from mount face | ≈ 120 mm **UNVERIFIED**{ .dh-unverified } |
| Jaw coordinate | −0.05 m (open) to +0.0347 m; fingers touch near +0.018 m **UNVERIFIED**{ .dh-unverified } |

!!! note "Yours to determine — commissioning limits, matched across both hands"
    The zero routine finds only the closed stall, and the torques above are
    configured values, not a tested limit. *Owner: controls + hardware lead.*

✅ **Check:** Both jaws cycle under the servo without binding; values above recorded.
