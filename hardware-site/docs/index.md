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

<figure markdown>
  ![The robot with both camera columns and both grippers lifted off](assets/exploded/team/15-whole-robot.webp){ loading=lazy }
  <figcaption markdown="span">
    What you build: torso, two legs, two arms, two camera columns, two
    grippers. Exploded views of each are on the
    [Assembly](assembly/index.md) pages.
  </figcaption>
</figure>

## Build path

!!! danger "Before step 1: read Safety"
    36 kg, no self-locking joints: removing power — pulling the pack disconnect
    included — drops the robot and whatever it holds. Two 6S lithium-polymer packs
    in series reach 50.4 V. Read [Safety](fabrication/index.md#safety) before
    ordering parts and before first power-on.

<div class="grid cards" markdown>

-   :material-cart: **1 · Buy** — what to buy and have made. [Bill of materials →](bom/index.md)
-   :material-hammer-screwdriver: **2 · Make** — CAD, machining, printing, inspection. [Fabrication →](fabrication/index.md)
-   :material-wrench: **3 · Assemble** — subassembly by subassembly. [Assembly →](assembly/index.md)
-   :material-flash: **4 · Wire** — power, harnesses, six CAN (Controller Area Network) buses. [Electrical →](electrical/index.md)
-   :material-power: **5 · Bring up** — motor IDs, zeroing, calibration. [Bring-up →](bringup/index.md)
-   :material-check-decagram: **6 · Verify** — before leaving the gantry. [Acceptance tests →](bringup/index.md#acceptance-tests)

</div>

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
| Also needed | A CUDA machine for the planner; a gantry rated 50 kg or more, 1.4 m or more of clear height |
| People | At least two |

*Source: project README (first seven rows).* See also
[Full specifications](reference/index.md#full-specifications).

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
    [camera gimbal](assembly/index.md#head-and-camera-gimbal) is why this robot exists.
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
