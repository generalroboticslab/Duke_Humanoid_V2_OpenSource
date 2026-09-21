# Bring-up

Do the stages in order; each assumes the previous one passed.

!!! abstract "At a glance"
    - **Tools:** `control/` of the deploy repository.
    - **Before this:** [Pre-power checks](../electrical/index.md#pre-power-checks) passed and signed; control stack built on the robot computer ([Robot computer setup](#robot-computer-setup)).
    - **Read:**
      [`SETUP.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/SETUP.md)
      (install),
      [`OPERATIONS.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/OPERATIONS.md)
      (operator runbook) and
      [`auto_operator_incidents.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/auto_operator_incidents.md)
      (past incidents and their safeguards).

0. [Robot computer setup](#robot-computer-setup) — once, before any bus is touched.
1. [First power-on](#first-power-on)
2. [Motor ID and config](#motor-id-and-config)
3. [Joint zeroing](#joint-zeroing)
4. [Camera calibration](#camera-calibration)
5. [Acceptance tests](#acceptance-tests)

!!! danger "Hang the robot, legs straight, for all of bring-up"
    The joints are quasi-direct-drive: cutting power drops the robot. A bent-leg
    hang tilts the torso and corrupts the body-frame geometry.

## Keep one owner per CAN bus

Stop `humanoid_real_env.py` before any tool that talks to the motors: two
clients on one CAN (Controller Area Network) bus look like a harness fault.

{% include "bringup/robot-computer-setup.md" %}

{{ step_ns("first-power-on") }}
{% include "bringup/first-power-on.md" %}

{{ step_ns("motor-id-and-config") }}
{% include "bringup/motor-id-and-config.md" %}

{{ step_ns("joint-zeroing") }}
{% include "bringup/joint-zeroing.md" %}

{{ step_ns("camera-calibration") }}
{% include "bringup/camera-calibration.md" %}

{{ step_ns("acceptance-tests") }}
{% include "bringup/acceptance-tests.md" %}
