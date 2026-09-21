# CAN bus

Connect all 31 actuators to six CAN (Controller Area Network) buses at
**1 Mbit/s**.

!!! abstract "At a glance"
    - **You will:** wire, name and bring up each bus.
    - **Parts:** six CANable PRO V2.0 USB-CAN adapters (candleLight / `gs_usb`), [Electronics](../bom/electronics.md).

<figure markdown>
  ![Data wiring diagram, Duke Humanoid V2](../assets/wiring/data-wiring-v2.webp){ loading=lazy }
</figure>

[Full-size diagram](../assets/wiring/data-wiring-v2.png). USB hubs: #1 cameras
and IMU (inertial measurement unit), #2 CAN adapters, #3 gripper servo boards.
Whether the first D436, `can9` and `can25` plug into the hub or the computer is
**UNVERIFIED**{ .dh-unverified }.

## The actuator map

??? info "Full actuator map (URDF order)"
    | # | Joint | CAN ID | Bus | Model |
    | --- | --- | --- | --- | --- |
    | 0 | `waist` | 1 | `can22` | RS03 |
    | 1 | `left_hip_1` | 31 | `can24` | RS03 |
    | 2 | `left_hip_2` | 32 | `can24` | RS03 |
    | 3 | `left_hip_3` | 33 | `can24` | RS03 |
    | 4 | `left_knee` | 34 | `can24` | RS04 |
    | 5 | `left_ankle_1` | 35 | `can24` | RS03 |
    | 6 | `left_ankle_2` | 36 | `can24` | RS06 |
    | 7 | `right_hip_1` | 41 | `can23` | RS03 |
    | 8 | `right_hip_2` | 42 | `can23` | RS03 |
    | 9 | `right_hip_3` | 43 | `can23` | RS03 |
    | 10 | `right_knee` | 44 | `can23` | RS04 |
    | 11 | `right_ankle_1` | 45 | `can23` | RS03 |
    | 12 | `right_ankle_2` | 46 | `can23` | RS06 |
    | 13 | `left_shoulder_1` | 10 | `can22` | RS03 |
    | 14 | `left_shoulder_2` | 11 | `can9` | RS06 |
    | 15 | `left_shoulder_3` | 12 | `can9` | RS02 |
    | 16 | `left_elbow` | 13 | `can9` | RS02 |
    | 17 | `left_wrist_1` | 14 | `can9` | RS02 |
    | 18 | `left_wrist_2` | 15 | `can9` | RS00 |
    | 19 | `left_wrist_3` | 16 | `can9` | RS05 |
    | 20 | `right_shoulder_1` | 20 | `can22` | RS03 |
    | 21 | `right_shoulder_2` | 21 | `can21` | RS06 |
    | 22 | `right_shoulder_3` | 22 | `can21` | RS02 |
    | 23 | `right_elbow` | 23 | `can21` | RS02 |
    | 24 | `right_wrist_1` | 24 | `can21` | RS02 |
    | 25 | `right_wrist_2` | 25 | `can21` | RS00 |
    | 26 | `right_wrist_3` | 26 | `can21` | RS05 |
    | 27 | `cam_yaw_left` | 7 | `can25` | RS05 |
    | 28 | `cam_pitch_left` | 8 | `can25` | RS05 |
    | 29 | `cam_yaw_right` | 5 | `can25` | RS05 |
    | 30 | `cam_pitch_right` | 6 | `can25` | RS05 |

    *Source: `control/humanoid_config.py` (index = `motor_setup_dict`
    order; the deployed MJCF `robot.xml` and the policy's `controlled_joints`
    list the same order, left camera first). Ignore the stale `#27`–`#30`
    comments on the camera lines there.*

- Program IDs per [Motor ID and config](../bringup/motor-id-and-config.md).
  IDs are unique robot-wide; keep them so.
- `can22` spans both blocks: waist on lower-body power, both `shoulder_1` on
  upper-body power.
- `can12` and `can19` in `humanoid_config.py` are unused.

## Wire and terminate each bus

1. Daisy-chain each bus: no ring, no stubs
   ([connectors and pinouts](harness-fabrication.md#identify-the-connector-pinouts)).
2. Fit 120 Ω at each physical end. No terminator is in the parts list.

!!! note "Not measured on the reference robot — per-bus terminator location and measured resistance"
    *Owner: electrical lead, from a photographed build. Blocks pre-power checks.*

✅ **Check:** a finished, unpowered bus reads **about 60 Ω** across CAN_H–CAN_L.

## Name each adapter

1. Flash **candleLight** with the ElmueSoft
   [CANable Firmware Update](https://netcult.ch/elmue/CANable%20Firmware%20Update/)
   tool: adapter plugged directly into the computer, button pressed for flash
   mode.
2. Find each adapter's USB serial:

    ```bash
    udevadm info --attribute-walk --path=/sys/class/net/can0 | grep 'ATTRS{serial}'
    # or: sudo dmesg (after plugging in), lsusb -v, usb-devices
    ```

3. Bind each serial to its name, one line each:

    ```text
    # /etc/udev/rules.d/99-candlelight.rules
    SUBSYSTEM=="net", ACTION=="add", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="606f", ATTRS{serial}=="<adapter-serial>", NAME="can21"
    SUBSYSTEM=="net", KERNEL=="can[0-9]*", GROUP="can", MODE="0660"
    ```

4. Keep **exactly one rule per `NAME`**: `humanoid_setup_can.py` USB-resets the
   adapter on the **last** matching line. Delete or `#`-comment retired adapters.
5. Reload, then replug every adapter and label it:

    ```bash
    sudo udevadm control --reload-rules && sudo systemctl restart systemd-udevd && sudo udevadm trigger
    ```

!!! note "Not recorded — candleLight firmware version on the reference adapters"
    *Owner: electrical lead.*

## Bring the buses up

After **every** power cycle ([host setup](../bringup/first-power-on.md)):

1. Run `humanoid_setup_can.py`; it USB-resets failures and lists what to replug.

    ```bash
    cd <deploy-repo>/control
    python humanoid_setup_can.py        # needs iproute2, usbutils (usbreset), sudo
    for c in can9 can21 can22 can23 can24 can25; do
      echo -n "$c: "; ip -details link show $c | grep -o "can state [A-Z-]*" | head -1
    done   # all six ERROR-ACTIVE
    ```

2. No interfaces in `ip link`? Load the driver:

    ```bash
    sudo modprobe can can_raw gs_usb
    modinfo gs_usb; lsmod | grep can   # driver present and loaded
    ```

✅ **Check:** from a cold power cycle all six buses are ERROR-ACTIVE, all 31
actuators answer at their mapped ID and bus, and adapter labels match the udev
rules.

## Diagnose bus faults { #bus-health-and-fault-diagnosis }

1. Stop `humanoid_real_env.py` first: two clients on one bus look exactly like
   a harness fault.
2. Read state, frames and load (motor loop 200 Hz; reference bus load:
   **TODO**{ .dh-missing }):

    ```bash
    ip -details -statistic link show can22   # state and error counters
    candump any,0:0,#FFFFFFFF -extA          # all frames, error frames included
    canbusload can22@1000000 -cbr            # bus load, second terminal
    ```

3. Pick a script:

    | Tool | Use |
    | --- | --- |
    | `humanoid_motor_temps.py` | Read-only joint, CAN ID, temperature and bus voltage (`v_bus`) |
    | `humanoid_profile_motor_latency.py` | Per-motor round-trip latency, 1 % torque ceiling |
    | `humanoid_wiggle_watch.py` | Live dropout alarm while you press connectors |
    | `humanoid_dropout_probe.py` | Link break or motor reboot, after an event |

    ```bash
    cd <deploy-repo>/control
    python humanoid_motor_temps.py   # read-only: joint, CAN ID, temperature, v_bus
    ```

4. After a dropout, probe before any restart (the host writes `5000` to
   `0x7028` at startup):

    | Reading | Meaning |
    | --- | --- |
    | `5000` | Link break: harness or solder joint |
    | Other | Motor rebooted: power dip or firmware crash |
    | No answer | Break still open: wiggle the harness while probing |

Recurring error frames or ERROR-WARNING: inspect the harness before running.
