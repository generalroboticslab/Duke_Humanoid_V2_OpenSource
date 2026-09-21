# Robot computer setup

Do this once, before any bus is touched.

1. Flash each CANable PRO V2.0 with **candleLight** (`gs_usb`) using the ElmueSoft
   [CANable Firmware Update](https://netcult.ch/elmue/CANable%20Firmware%20Update/)
   tool: press the adapter button for flash mode and connect it directly to the
   computer.
2. Prepare the host and name the adapters. Bus map:
   [CAN (Controller Area Network) bus](../electrical/index.md#can-bus).

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

Before the robot moves, read deploy's
[`OPERATIONS.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/OPERATIONS.md),
[`auto_operator_incidents.md`](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/auto_operator_incidents.md)
and `auto_operator_safety_contract.md`.
