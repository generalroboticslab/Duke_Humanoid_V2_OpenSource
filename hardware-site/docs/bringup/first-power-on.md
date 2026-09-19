# First power-on

Energise the robot and prove all 31 actuators answer, **without enabling any**.

!!! abstract "At a glance"
    - **Tools:** bench supply, e-stop (emergency stop), two people.
    - **Operator:** connects power, runs commands, reads output aloud; never touches the robot.
    - **Safety:** holds the e-stop, watches, calls the abort; never touches the keyboard.
    - **Before this:** [Pre-power checks](../electrical/pre-power-checks.md) passed and signed. Robot hung from a rated hoist, legs straight, clear space below.

## Prepare the host

Ubuntu 22.04; adapter firmware, udev names, IMU (inertial measurement unit)
output, RealSense driver: [Software](../software.md).

1. Remove `brltty`:

    ```bash
    sudo apt remove brltty  # grabs USB-serial devices; /dev/ttyUSB0 never appears
    ```

2. Join `netdev`:

    ```bash
    sudo adduser $USER netdev  # bring CAN interfaces up without sudo
    ```

3. Join `dialout`:

    ```bash
    sudo adduser $USER dialout  # serial access
    ```

4. Log out and back in.
5. Update:

    ```bash
    sudo apt update
    ```

6. Install CAN (Controller Area Network) tools:

    ```bash
    sudo apt install can-utils libsocketcan-dev
    ```

7. Driver present?

    ```bash
    modinfo gs_usb  # CAN adapter driver
    ```

8. Driver loaded?

    ```bash
    lsmod | grep can
    ```

??? info "Find a new USB device's node"
    ```bash
    ls -1 /dev > before.txt
    # plug the device in
    ls -1 /dev > after.txt
    diff before.txt after.txt
    ```

## Know when to abort

Cut power, and do not restart to retry, on:

- smell, smoke or heat;
- current limit;
- unexpected motion;
- wrong ID or bus;
- ERROR-WARNING or error frames;
- anyone calling abort.

Fault came and went? Run the
[dropout probe](../electrical/can-bus.md#bus-health-and-fault-diagnosis) before
any power cycle.

!!! missing "No e-stop is specified; every step assumes one"
    Tracked on [Power system](../electrical/power-system.md#protection-disconnect-and-e-stop).
    *Owner: electrical lead.*

## Power up

{{ step(1, "Power the computer only") }}

!!! unverified "UNVERIFIED — SAFETY — How to power the computer alone: the power diagram feeds it from the arm motors' distribution block, no disconnect drawn"
    Do not improvise. *Owner: electrical lead.*

1. Leave the motor bus disconnected.
2. Boot and log in.

{{ step(2, "Inventory the USB devices") }}

| Hub | Devices |
| --- | --- |
| USB Hub #1 | Two RealSense D436, IMU |
| USB Hub #2 | CANable PRO V2.0 adapters |
| USB Hub #3 | Two gripper servo driver boards |

*Source: team data wiring diagram*; hub power not drawn. First D436, `can9`,
`can25`: via hub or direct **UNVERIFIED**{ .dh-unverified }.

1. Devices:

    ```bash
    lsusb  # everything present?
    ```

2. USB speed: `480M` is USB 2; replug until `5000M`, else fix the hub or
   [routing](../electrical/routing.md).

    ```bash
    lsusb -t  # each RealSense must show 5000M, not 480M
    ```

3. CAN interfaces:

    ```bash
    ip link show type can  # six CAN interfaces present (still down)
    ```

4. Cameras; record the serials:

    ```bash
    rs-enumerate-devices -s  # two cameras, with serial numbers
    ```

5. Gripper boards:

    ```bash
    ls -la /dev/ttyACMservo*  # both gripper driver boards
    ```

{{ step(3, "Bring up the CAN buses") }}

1. Go to `control/`:

    ```bash
    cd <deploy-repo>/control
    ```

2. Bring the buses up:

    ```bash
    python humanoid_setup_can.py
    ```

3. Read each state:

    ```bash
    for c in can9 can21 can22 can23 can24 can25; do
      echo -n "$c: "; ip -details link show $c | grep -o "can state [A-Z-]*" | head -1
    done
    ```

4. Fix a dead bus (adapter, udev, USB) before adding motor power.

✅ **Check:** all six buses report ERROR-ACTIVE, motor bus unpowered.

??? info "Inspect a bus"
    Stop `candump` before any tool that transmits.

    ```bash
    ip -details -statistic link show can22  # one bus: state and error counters
    ```

    ```bash
    candump any,0:0,#FFFFFFFF -extA  # every bus, error frames included
    ```

{{ step(4, "Energise the motor bus") }}

Use a **current-limited bench supply**, not the packs: a fault then trips the
limit, not a fire. Packs: two 6S LiPo (lithium polymer) in series, 44.4 V
nominal, 50.4 V full.

!!! missing "MISSING — SAFETY — Bench-supply voltage and current limit per stage; what to do without one"
    *Owner: electrical lead.*

1. Safety holds the e-stop.
2. Current limit set, raise the supply to bus voltage.
3. Watch the current, not the robot.
4. Current limit hit: short, **cut power**, back to
   [Pre-power checks](../electrical/pre-power-checks.md) group B.

✅ **Check:** current steady and low (value **TODO**{ .dh-missing }).

!!! missing "MISSING — Expected quiescent current, 31 drives powered, none enabled, with tolerance"
    *Owner: electrical lead.*

{{ step(5, "Read every motor") }}

```bash
python humanoid_motor_temps.py  # read-only; humanoid_real_env.py stopped
```

| Check | Pass |
| --- | --- |
| Rows | 31, none *no feedback yet* |
| ID and bus | Match the [actuator map](../electrical/can-bus.md#the-actuator-map); fix in hardware |
| Bus voltage | Supply voltage on every motor. Low means a bad conductor |
| Temperature | Near ambient. Tool flags > 60 °C |

✅ **Check:** all 31 pass; none is enabled.

{{ step(6, "Profile the bus at 1 % torque") }}

```bash
python humanoid_profile_motor_latency.py  # latency per motor and bus
```

✅ **Check:** pass values in [A2](acceptance-tests.md#a2-measure-can-latency).

{{ step(7, "Power down") }}

1. Stop every tool talking to the motors.
2. Take the buses down:

    ```bash
    python humanoid_setup_can.py --down
    ```

3. Shut the computer down.
4. Remove motor bus power.
5. Disconnect the supply or packs.

!!! missing "MISSING — SAFETY — Specified power-on and power-off order of the rails; the order above is unverified"
    *Owner: electrical lead + controls lead.*
