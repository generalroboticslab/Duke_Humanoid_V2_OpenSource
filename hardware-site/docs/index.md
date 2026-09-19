# Duke Humanoid V2 — Hardware

<figure markdown>
  ![Duke Humanoid V2 in simulation and on hardware](assets/images/teaser.webp)
  <figcaption>
    Duke Humanoid V2: 31 degrees of freedom (DoF), 36&nbsp;kg, 1.2&nbsp;m, two
    independently aimed RGB-D camera modules.
  </figcaption>
</figure>

How to build an identical Duke Humanoid V2. The code is open; see
[Software](software.md).

## Build path

!!! danger "Before step 1: read Safety"
    36 kg, no self-locking joints: removing power, including an emergency stop
    (e-stop), drops the robot and whatever it holds. Two 6S lithium-polymer packs
    in series reach 50.4 V. Read [Safety](before-you-start/safety.md) before
    ordering parts and before first power-on.

<div class="grid cards" markdown>

-   :material-cart: **1 · Buy** — what to buy and have made. [Bill of materials →](bom/index.md)
-   :material-hammer-screwdriver: **2 · Make** — CAD, machining, printing, inspection. [Fabrication →](fabrication/index.md)
-   :material-wrench: **3 · Assemble** — subassembly by subassembly. [Assembly →](assembly/index.md)
-   :material-flash: **4 · Wire** — power, harnesses, six CAN (Controller Area Network) buses. [Electrical →](electrical/index.md)
-   :material-power: **5 · Bring up** — motor IDs, zeroing, calibration. [Bring-up →](bringup/index.md)
-   :material-check-decagram: **6 · Verify** — before leaving the gantry. [Acceptance tests →](bringup/acceptance-tests.md)

</div>

Red bold **MISSING**{ .dh-missing } and **UNVERIFIED**{ .dh-unverified } marks
are open gaps, listed on [Open items](reference/todo.md).

!!! missing "Not yet: a second robot cannot be built"
    | Blocker | Tracked on |
    | --- | --- |
    | No robot CAD published | [CAD downloads](fabrication/cad-downloads.md) |
    | No fastener schedule | [Fasteners](bom/fasteners-and-hardware.md) |
    | No torque values (threadlocker: Loctite 222) | [Assembly](assembly/index.md) |
    | No hardware or documentation licence | [Citation and licence](reference/citation-and-license.md) |
    | No human-safety procedure | [Safety](before-you-start/safety.md) |
    | No e-stop, pack fuse or main disconnect | [Power system](electrical/power-system.md) |
    | No hardware/software contract | [Software](software.md) |

## Specifications

| | |
| --- | --- |
| DoF | 31: 27-DoF body (waist ×1, legs 2×6, arms 2×7) + two 2-DoF camera gimbals, +1 per gripper |
| Mass / height | 36 kg / 1.2 m |
| Arm reach / leg length | 0.46 m / 0.39 m |
| Cameras | 2 × Intel RealSense D436, 90°×65° RGB field of view, 0.1–3.0 m, each on its own yaw-pitch gimbal |
| End effectors | parallel grippers, 350 g each, one mimic-coupled jaw slide |
| Actuation | quasi-direct-drive throughout |
| Control | 50 Hz learned whole-body policy onboard, 200 Hz CAN motor loop |
| Parts cost | {{ bom_total() }}, a floor: fasteners, printed parts, tools, shipping and setup fees unpriced |
| Build time | **TODO**{ .dh-missing } not measured |
| Also needed | A CUDA machine for the planner; a gantry rated well over 36 kg |
| People | At least two |

*Source: project README (first seven rows).* See also
[Full specifications](reference/full-specifications.md).

<figure markdown>
  ![Duke Humanoid V2 hardware overview with joints numbered](assets/images/hardware.webp){ loading=lazy }
  <figcaption>
    Orange: actuated joints. (1&ndash;7) shoulder pitch/roll/yaw, elbow, wrist
    roll/pitch/yaw; (8) waist; (9&ndash;14) hip pitch/roll/yaw, knee, ankle
    pitch/roll; (15&ndash;16) camera yaw/pitch. Green: (I) camera, (II) gripper,
    (III) onboard computer. Dimensions in mm.
  </figcaption>
</figure>

## The camera modules

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="800" height="450" poster="assets/images/hardware_tracking-poster.webp" aria-label="Each camera module tracking its own target">
    <source src="assets/images/hardware_tracking.mp4" type="video/mp4">
    <a href="assets/images/hardware_tracking.mp4">Each camera module tracking its own target</a>
  </video>
  <figcaption markdown="span">
    Each module tracks its own target. The
    [camera gimbal](assembly/head-and-camera-gimbal.md) is why this robot exists.
  </figcaption>
</figure>

<figure markdown>
  <video class="dh-clip" autoplay loop muted playsinline preload="metadata" width="800" height="400" poster="assets/images/vrw_fixed_vs_actuated-poster.webp" aria-label="Visible-reachable workspace, fixed versus actuated cameras">
    <source src="assets/images/vrw_fixed_vs_actuated.mp4" type="video/mp4">
    <a href="assets/images/vrw_fixed_vs_actuated.mp4">Visible-reachable workspace, fixed versus actuated cameras</a>
  </video>
  <figcaption>
    Volume the robot can see and reach at once, fixed head versus actuated
    modules. Without gimbals it is a different robot.
  </figcaption>
</figure>
