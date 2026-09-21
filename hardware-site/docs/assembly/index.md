# Assembly

<figure markdown>
  ![The robot with both camera columns and both grippers lifted off](../assets/exploded/team/15-whole-robot.webp){ loading=lazy }
  <figcaption>The subassemblies below: torso, two legs and two arms assembled; the two camera columns and two grippers lifted off. Part labels on the pages that follow are the team BOM ids (Team ref column of the parts lists).</figcaption>
</figure>

Build the robot (31 RobStride-driven joints, Feetech bus servos in the grippers; 36 kg, 1.2 m) as these bench subassemblies, in this order:

1. [Tools](#tools), once.
2. [Leg](#leg) ×2: 6 RobStride each.
3. [Arm](#arm) ×2: 7 RobStride each.
4. [Torso and waist](#torso-and-waist) ×1: 1 RobStride.
5. [Head and camera gimbal](#head-and-camera-gimbal): two gimbal columns, 2 RobStride each.
6. [Gripper](#gripper) ×2: 1 Feetech servo each.
7. [Final integration](#final-integration): the whole robot.

Then [Electrical](../electrical/index.md) and [Bring-up](../bringup/index.md).

!!! note "Yours to determine — build order and subassembly boundaries"
    Open, pending a build:

    - whether harness branches go into a limb before it closes;
    - whether `hip_1` and `hip_2` belong to the leg or, as in the
      computer-aided design (CAD), to the pelvis with the waist;
    - whether `shoulder_1` is fitted in the torso side plate (as in the CAD) or
      on the arm.

    *Owner: hardware lead.*

## Follow these rules on every page

- Set each Controller Area Network (CAN) ID on the bench before the actuator
  goes into a housing; label joint, ID and bus. IDs and buses:
  [`humanoid_config.py`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/humanoid_config.py),
  six buses at 1 Mbit/s ([Motor ID and config](../bringup/index.md#motor-id-and-config)).
- Hardware standard: Torx button-head M4x12 (McMaster-Carr 90991A123) and
  M3x12 (90991A115) screws; 50 × 65 × 7 mm main bearing; Loctite 222.
- No screw may go deeper than the actuator's thread depth.
- Machined-part quantities read **TODO**{ .dh-missing }: the machined-parts
  sheet's `_xN` names disagree with its quantity column
  ([machined parts](../bom/index.md#cnc-parts)).

!!! note "Not measured on the reference robot — build time and crew size per subassembly"
    *Owner: whoever performs the first externally documented build.*

## Figures still needed

No step figure exists **TODO**{ .dh-missing }. Name them
`assets/assembly/<page>-step-NN.png`, showing only that step's parts.

> **Figure** <span class="pending-figure">not produced yet</span> —
> `assets/assembly/subassembly-map.png`: the build order as a diagram.

{{ step_ns("tools") }}
{% include "assembly/tools.md" %}

{{ step_ns("leg") }}
{% include "assembly/leg.md" %}

{{ step_ns("arm") }}
{% include "assembly/arm.md" %}

{{ step_ns("torso-and-waist") }}
{% include "assembly/torso-and-waist.md" %}

{{ step_ns("head-and-camera-gimbal") }}
{% include "assembly/head-and-camera-gimbal.md" %}

{{ step_ns("gripper") }}
{% include "assembly/gripper.md" %}

{{ step_ns("final-integration") }}
{% include "assembly/final-integration.md" %}
