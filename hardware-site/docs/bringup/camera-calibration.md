# Camera calibration

Calibrate the two RealSense D436 cameras, sections 1–4 in order.

!!! abstract "At a glance"
    - **Parts:** both cameras on USB Hub #1, each on its own two-axis gimbal; [tag cubes](#make-the-fixtures).
    - **Before this:** [Joint zeroing](joint-zeroing.md). No calibration data ships.

| Port | Module | Model site | Gimbal joints |
| --- | --- | --- | --- |
| 5555 | Left, forward-mounted | `cam_left_rgb` | `cam_yaw_left`, `cam_pitch_left` |
| 5556 | Right, rear-mounted | `cam_right_rgb` | `cam_yaw_right`, `cam_pitch_right` |

## Install librealsense

1. Install **2.58.1** or later (D436 support) from this repository. The deploy
   repository pins `pyrealsense2==2.58.1.10581`.

    ```text
    repository: https://librealsense.realsenseai.com/Debian/apt-repo
    key:        https://librealsense.realsenseai.com/Debian/librealsenseai.asc
    packages:   librealsense2 librealsense2-utils librealsense2-dev librealsense2-gl
                librealsense2-udev-rules librealsense2-dbg
    ```

2. Comment out the old Intel repository.
3. Reload udev.

## 1. Bind cameras to ports

Everything binds a camera by **port**. Swapped ports fail silently.

1. Read both serials:

    ```bash
    rs-enumerate-devices -s
    ```

    Without `librealsense2-utils`:

    ```bash
    python -c "import pyrealsense2 as rs; print([d.get_info(rs.camera_info.serial_number) for d in rs.context().query_devices()])"
    ```

2. Set `CAMERA_SERIALS` in `perception/vs_site_local.py`, **left camera first**,
   or pass `--devices <left-serial> <right-serial>` to the camera server (wins).
   `humanoid_site.CAMERA_SERIALS` has no reader.
3. Label each camera with serial and side.

✅ **Check:** the port mapping survives a power cycle and a replug.

## 2. Check gimbal encoder zero

Encoder zero must mean the camera looks straight ahead.

1. Print each camera's predicted azimuth and elevation, drift and noise
   (read-only):

    ```bash
    python humanoid_gimbal_zero_check.py
    ```

    With options:

    ```bash
    python humanoid_gimbal_zero_check.py --robot-ip 127.0.0.1 --seconds 5
    ```

2. Compare with the robot.

!!! missing "MISSING — Procedure and tolerance for setting the gimbal zero"
    *Owner: perception lead + hardware lead.*

## 3. Calibrate motor-to-camera gear

Needs camera on 5555, motors powered, CAN (Controller Area Network) up, no
`humanoid_real_env.py` or tracker.

1. Hold a tagged cube still in front of the forward camera.
2. Run. The tool moves only the forward gimbal (motor side: 0.4 rad yaw,
   0.3 rad pitch), then returns to zero.

    ```bash
    python calibrate_cam_gear.py  # gear = -Δmech_pos / Δbearing (motor-rad per camera-rad)
    ```

!!! missing "MISSING — Rear-gimbal gear calibration, designed ratio, storage, allowed spread"
    *Owner: perception lead.*

## 4. Calibrate hand-eye extrinsics

Run in `<deploy-repo>/control` with telemetry on port 9870, cameras on
5555/5556 and `tag_cube_0` / `tag_cube_1` bolted to the wrists. Full procedure:
[`SETUP.md` §5](https://github.com/generalroboticslab/duke_humanoid_v2_deploy/blob/main/control/docs/SETUP.md).

{{ step(1, "Record") }}

1. Start:

    ```bash
    python humanoid_monitor.py --record-handeye  # 10 s countdown; Ctrl+C saves
    ```

2. Move **both** arms ≥ 30° and ≥ 50 mm at each wrist, **including wrist roll**,
   at moderate speed, ideally with both cubes in one view.
3. Aim for **`n_valid ≥ 100` per port**. Heed observability warnings.

{{ step(2, "Solve") }}

1. Run:

    ```bash
    python humanoid_handeye_calibration.py  # latest recording -> calibration/camera_handeye.yaml
    # other options: --logs --output --subsample (default 5) --dq-thresh --v-link-thresh
    ```

2. Cube twisted on the wrist?

    ```bash
    # warm-start rotation residual > 15°: give a guess in rad
    python humanoid_handeye_calibration.py \
        --obj-rot-inits '{"tag_cube_0": [0.0, 0.0, 0.35]}'
    ```

!!! danger "A failed solve still writes the YAML"
    It carries `calibration_valid: false`, and the monitor silently falls back
    to defaults. Confirm `VALID` in the solver output first.

| Quantity | Reference **UNVERIFIED**{ .dh-unverified } | Fail |
| --- | --- | --- |
| Translation mean / max | 2.3 / 8.1 mm | max > 20 mm |
| Rotation mean / max | 0.21 / 0.89° | max > 5° |
| Valid frames per port | ≥ 100 | < 50 |

!!! unverified "UNVERIFIED — Reference residuals come from example output in SETUP.md, not a recorded solve"
    *Owner: perception lead.*

{{ step(3, "Apply") }}

```bash
python humanoid_monitor.py --handeye-yaml calibration/camera_handeye.yaml
```

✅ **Check:** solve VALID within the table, YAML confirmed loaded.

## Check intrinsics

!!! missing "MISSING — Whether D436 factory intrinsics are trusted or re-estimated"
    *Owner: perception lead.*

## Make the fixtures

!!! missing "MISSING — Tag cubes: geometry, tag family and size, wrist mounts, artwork (not in the bill of materials or CAD)"
    *Owner: perception lead. Blocks [CAD downloads](../fabrication/cad-downloads.md).*

Tag size limits range: 30 mm tags stop decoding beyond about 2 m **UNVERIFIED**{ .dh-unverified }. Keep the cubes within 2 m of the cameras. *Source: deploy repo, `OPERATIONS.md`.*

## Redo calibration

After any `humanoid_set_zero.py` run; after replacing a camera (with section 1).

!!! missing "MISSING — Full re-calibration triggers and interval"
    *Owner: perception lead.*
