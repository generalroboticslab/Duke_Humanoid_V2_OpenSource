# Electrical

Work packs dry — connect only at [Pre-power checks](#pre-power-checks), under
[First power-on](../bringup/index.md#first-power-on), robot suspended.

## Work in this order

1. [Power system](#power-system) ([diagram](../assets/wiring/power-supply-v2.png))
2. [CAN bus](#can-bus) ([diagram](../assets/wiring/data-wiring-v2.png))
3. [Harness fabrication](#harness-fabrication)
4. [Routing](#routing), in step with [Assembly](../assembly/index.md)
5. [Pre-power checks](#pre-power-checks)

## What the system carries

| Load | Qty | Interface |
| --- | --- | --- |
| RobStride actuators | 31 | CAN (Controller Area Network), 1 Mbit/s, six buses |
| Feetech HL-3915-C001 gripper servos (12 V) | 2 | USB serial via Waveshare ST/SC boards (CH340) |
| Intel RealSense D436 depth cameras | 2 | USB 3; must link at 5 Gbit/s |
| SYD Dynamics TransducerM TM171 IMU (inertial measurement unit) | 1 | USB |
| MINISFORUM X1-470 mini PC | 1 | 12 V power |
| USB hubs | 3 | USB |

*Source: [deploy repository](https://github.com/generalroboticslab/duke_humanoid_v2_deploy)
`control/humanoid_config.py`, `docs/SETUP.md`; bill of materials.*

{% include "electrical/power-system.md" %}

{% include "electrical/can-bus.md" %}

{% include "electrical/harness-fabrication.md" %}

{% include "electrical/routing.md" %}

{% include "electrical/pre-power-checks.md" %}
