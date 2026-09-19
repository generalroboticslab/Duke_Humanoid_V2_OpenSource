# Software

| Repository | Use |
| --- | --- |
| [`duke_humanoid_v2`](https://github.com/generalroboticslab/duke_humanoid_v2) | Umbrella: README, citation, licence, submodules |
| [`duke_humanoid_v2_simulation`](https://github.com/generalroboticslab/duke_humanoid_v2_simulation) | Training, paper reproduction, robot model |
| [`duke_humanoid_v2_deploy`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy) | Control stack on the robot |

```bash
git submodule update --init --recursive   # umbrella cloned without submodules
```

The cuRobo plan/MPC (model-predictive control) server needs a separate GPU
machine, not in the bill of materials. The robot computer needs no CUDA.

## Robot computer setup

1. Flash each CANable PRO V2.0 with **candleLight** (`gs_usb`) using the ElmueSoft
   [CANable Firmware Update](https://netcult.ch/elmue/CANable%20Firmware%20Update/)
   tool: press the adapter button for flash mode and connect it directly to the
   computer. Firmware version **UNVERIFIED**{ .dh-unverified }.
2. Prepare the host and name the adapters. Bus map:
   [CAN (Controller Area Network) bus](electrical/can-bus.md).

    ```bash
    # Ubuntu 22.04; log out and back in after adduser
    sudo apt remove brltty            # else /dev/ttyUSB0 never appears
    sudo adduser $USER netdev         # CAN up without sudo
    sudo adduser $USER dialout        # serial devices
    sudo apt install can-utils libsocketcan-dev
    modinfo gs_usb; lsmod | grep can  # candleLight driver present and loaded
    sudo dmesg                        # each adapter's USB serial (or lsusb -v, usb-devices)
    # write /etc/udev/rules.d/99-candlelight.rules (below); humanoid_setup_can.py reads it
    sudo udevadm control --reload-rules && sudo systemctl restart systemd-udevd && sudo udevadm trigger
    # then unplug and replug every adapter
    ```

    ```text
    # One line per name: for a duplicated name the setup script keeps the last line.
    # Optional on each line: ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="606f"
    SUBSYSTEM=="net", ACTION=="add", ATTRS{serial}=="<adapter-serial>", NAME="can9"
    SUBSYSTEM=="net", ACTION=="add", ATTRS{serial}=="<adapter-serial>", NAME="can21"
    SUBSYSTEM=="net", ACTION=="add", ATTRS{serial}=="<adapter-serial>", NAME="can22"
    SUBSYSTEM=="net", ACTION=="add", ATTRS{serial}=="<adapter-serial>", NAME="can23"
    SUBSYSTEM=="net", ACTION=="add", ATTRS{serial}=="<adapter-serial>", NAME="can24"
    SUBSYSTEM=="net", ACTION=="add", ATTRS{serial}=="<adapter-serial>", NAME="can25"
    SUBSYSTEM=="net", KERNEL=="can[0-9]*", GROUP="can", MODE="0660"
    ```

3. Configure the TransducerM TM171 inertial measurement unit in the vendor's
   ImuAssistant (Windows):

    ```text
    Output data        Composite + Status only
    Output data rate   800 Hz
    Port               USB (UART off)
    Sensors            gyro, accelerometer, magnetometer on
    Boot mode          Auto
    GyroErrFilter      on
    Self-adapt filter  on
    Accel / mag gain   2.08 / 1.00
    # deploy imu.hpp opens USB at 4000000 baud and parses only the Combo packet
    ```

4. Install librealsense2 **2.58.1** (`librealsense2`, `-utils`, `-dev`, `-gl`,
   `-udev-rules`, `-dbg`) from `librealsense.realsenseai.com`, old Intel
   repository commented out; reload udev rules. Deploy pins
   `pyrealsense2==2.58.1.10581`.
5. Build `deploy/control` with CMake, vcpkg and Ninja presets (nanobind
   bindings).

Before the robot moves, read [Safety](before-you-start/safety.md), then deploy's
[`OPERATIONS.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/OPERATIONS.md),
[`auto_operator_incidents.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/auto_operator_incidents.md)
and `auto_operator_safety_contract.md`.

!!! missing "MISSING — Whether deploy has lower-body gravity compensation and stable-stand control"
    *Owner: controls lead.*

## Robot model

`simulation/asset/duke_v2/`: `humanoid_v21/`, `head_cam/`, `parallel_gripper/`.

!!! missing "MISSING — Asset READMEs cite paths absent from the export"
    *Owner: controls lead.*

The model sets joint order, directions and link masses. Never machine from its
meshes; see [CAD downloads](fabrication/cad-downloads.md).

!!! missing "MISSING — Hardware/software contract: joint vector (index, name, sign), checkpoint per revision, tested OS and drivers, fresh install"
    *Owner: controls lead.*

Code is Apache-2.0; see [Citation and licence](reference/citation-and-license.md).
