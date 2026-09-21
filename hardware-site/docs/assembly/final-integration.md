# Final integration

Join the subassemblies into one robot, **battery disconnected throughout**.

!!! abstract "At a glance"
    - **You will:** mount, wire, inspect, weigh and hang the robot.
    - **Parts:** two legs and two arms, each past its final check; torso complete; two camera columns bench-tested; two grippers with open and closed positions recorded.
    - **Before this:** [Gripper](#gripper); every actuator labelled with joint, ID and bus; camera and gripper-board serials recorded against their sides.

{{ step(1, "Support the torso") }}

!!! danger "Two people or a hoist from here on"
    The robot is 36 kg and 1.2 m tall, and less stable with each limb. Read
    [Safety](../before-you-start/index.md#safety).

Support it level, waist free, hips and shoulders reachable.

!!! note "Lifting points and sling route are tracked on [Safety](../before-you-start/index.md#rules)"
    - None defined; needed before the first lift.
    - Sling attachment.
    - What holds the torso (upright or lying down) while limbs go on.
    - How the robot hangs with its legs straight: a bent-leg hang tilts the
      torso and corrupts the camera geometry.

    *Owner: hardware lead + Safety sign-off.*

✅ **Check:** The torso cannot fall or rotate when a limb is offered up.

{{ step(2, "Attach the first leg") }}

Bolt the leg to the pelvis, supporting its weight. Joint location
**UNVERIFIED**{ .dh-unverified } ([Assembly](index.md)).

!!! note "Read off the model — hip, shoulder and wrist interfaces: screws and locating features"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: hardware lead.*

✅ **Check:** All six joints still move; the harness branch reaches the torso, unconnected.

{{ step(3, "Attach the second leg") }}

Check the side: the legs differ by bus and IDs.

✅ **Check:** Both legs move freely; a dimension measured on both sides matches.

{{ step(4, "Attach both arms") }}

Bolt each arm to its `shoulder_1` output through the square adapter.

✅ **Check:** Each arm moves through its travel without touching the torso or a leg.

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="1154" height="650"
    poster="../../assets/exploded/camera-mount-poster.webp" aria-label="Whole robot with camera columns and grippers lifting off"><source src="../../assets/exploded/camera-mount.mp4" type="video/mp4"><a href="../../assets/exploded/camera-mount.mp4">MP4</a></video>
  <figcaption>Camera columns lift off the top plate; grippers come off the wrists (steps 5 and 6).</figcaption>
</figure>

{{ step(5, "Install the camera columns") }}

Follow [Head and camera gimbal](#head-and-camera-gimbal), step 9.

✅ **Check:** Yaw axes 130.00 mm apart; no column touches an arm in any pose.

{{ step(6, "Install the grippers") }}

Bolt each gripper flange to its `wrist_3` output. Run the servo cable up the arm
to its driver board.

✅ **Check:** Both grippers work; their tags are visible to the cameras in some arm pose.

{{ step(7, "Join the harnesses") }}

Join one branch at a time against the bus table: six buses, two gripper
links, two camera cables, power.

| Bus | Carries |
| --- | --- |
| `can22` | Waist (ID 1), both `shoulder_1` (10, 20) |
| `can9` / `can21` | Left / right arm, IDs 11–16 / 21–26 |
| `can24` / `can23` | Left / right leg, IDs 31–36 / 41–46 |
| `can25` | Camera gimbals, IDs 5–8 |

!!! note "Read off the model — torso harness lengths, routes and service loops"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    See [Harness fabrication](../electrical/index.md#harness-fabrication).
    *Owner: electrical lead.*

✅ **Check:** Every branch is labelled; waist, hips and shoulders move with nothing pulled or pinched.

{{ step(8, "Inspect the whole robot") }}

- every fastener present, none left in the kitting tray;
- every joint moves by hand, alone and in close combinations;
- no cable stretched, pinched or kinked in any pose;
- nothing rattles;
- lenses clean;
- packs disconnected.

!!! note "Yours to determine — signed inspection checklist keyed to the fastener schedule"
    *Owner: hardware lead.*

✅ **Check:** Every item above is confirmed.

{{ step(9, "Weigh and hang the robot") }}

Weigh it: far from 36 kg means a part was missed, doubled or substituted. Hang
it with the **legs straight**.

!!! note "Not measured on the reference robot — as-built mass by subassembly"
    *Owner: whoever performs the first documented build.*

✅ **Check:** It hangs level, legs straight, mass recorded.

Next: [Electrical](../electrical/index.md),
[Pre-power checks](../electrical/index.md#pre-power-checks), then
[Bring-up](../bringup/index.md).
