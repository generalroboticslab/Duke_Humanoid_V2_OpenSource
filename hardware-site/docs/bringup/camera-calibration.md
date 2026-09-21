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

2. Compare with the robot. At encoder zero the model expects the left camera
   at about 0° azimuth / 0° elevation and the right at about 180° / 0° (it
   faces aft).
3. If they disagree, reset the gimbal zero. `humanoid_set_zero.py` writes the
   current position of every motor in `motor_setup_dict` as its zero; it does
   not drive.
    1. In `humanoid_config.py`, comment out every non-camera entry in
       `motor_setup_dict`, leaving the four `cam_*` joints.
    2. Hand-point both cameras straight forward and level, as the tool prints
       **UNVERIFIED**{ .dh-unverified }. See the gap below for the rear camera.
    3. Run `python humanoid_set_zero.py` and type `yes`.
    4. **Restore the full `motor_setup_dict`.** Skipping this breaks the whole
       stack (joint count no longer matches the model).
    5. Re-run the check.

*Source: deploy repo, `humanoid_gimbal_zero_check.py`, `humanoid_set_zero.py`.*

!!! note "Not measured on the reference robot — gimbal zero tolerance and pointing reference"
    *Owner: perception lead + hardware lead.*

    No source gives the allowed error in degrees or what holds each camera
    "straight forward and level". The tool says to point both cameras forward,
    yet expects the rear camera at about 180° azimuth at zero.

## 3. Calibrate motor-to-camera gear

Needs the camera streaming on its port, motors powered, CAN
(Controller Area Network) up, no `humanoid_real_env.py` or tracker.

1. Hold [`grasp_cube_40mm`](#make-the-fixtures) still in front of the camera
   being calibrated.
2. Run once per gimbal. The tool first drives all four gimbal motors to encoder
   zero, then moves only the chosen gimbal (motor side: 0.4 rad yaw, 0.3 rad
   pitch), then returns to zero.

    ```bash
    python calibrate_cam_gear.py               # left, forward gimbal (port 5555)
    python calibrate_cam_gear.py --side right  # right, rear gimbal (port 5556)
    # gear = -Δmech_pos / Δbearing (motor-rad per camera-rad)
    ```

3. Record the printed `gear ≈` for yaw and pitch. The tool stores nothing;
   `humanoid_camera_point.py` hard-codes `GEAR_RATIO = 5.5` for both gimbals.

!!! note "Not measured on the reference robot — gear-ratio spread across the four gimbal joints"
    *Owner: perception lead.*

    5.5 is only what deploy configures; no CAD or BOM source gives the designed
    ratio. No source gives the allowed spread between axes or between the two
    gimbals.

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

!!! note "Not recorded — the residuals quoted come from example output in SETUP.md, not a recorded solve"
    *Owner: perception lead.*

{{ step(3, "Apply") }}

```bash
python humanoid_monitor.py --handeye-yaml calibration/camera_handeye.yaml
```

✅ **Check:** solve VALID within the table, YAML confirmed loaded.

## Check intrinsics

Use the D436 factory intrinsics. The deploy stack reads fx, fy, ppx and ppy
from each camera's stream profile and skips undistortion for RealSense. Its
chessboard calibration (`perception/camera_utils.py`) serves USB cameras only.
*Source: deploy repo, `perception/camera_realsense_utils.py`.*

## Make the fixtures

All tags are AprilTag `tag36h11`: a 30 mm marker (full 8×8 grid) with a 5 mm
quiet zone on each face.

| Fixture | Used by | Geometry | Tag IDs |
| --- | --- | --- | --- |
| `tag_cube_0` | Hand-eye, left wrist | 40 mm core, 2 mm face slabs on top + 4 sides, no bottom slab | 582–586 |
| `tag_cube_1` | Hand-eye, right wrist | Same as `tag_cube_0` | 577–581 |
| `grasp_cube_40mm` | Gear calibration, hand-held | 40 mm cube, tag on all 6 faces | 501–506 |

1. Take the wrist interface from `v2_wrist_interface.step`. It spans the 12 mm
   below each wrist cube.
2. Take the two-colour wrist-cube meshes `tag_cube_0.obj` / `tag_cube_1.obj`,
   or run `export_cube_obj.py` for separate white (face slabs) and black (core,
   pixels, wrist interface) OBJ files per cube.

*Source: deploy repo, `perception/tagged_bodies/tag_cube/`,
`perception/tagged_bodies/grasp_cube/`, `perception/asset/tag_cube_creation/`.*

!!! note "Yours to print — tag cubes: any rigid 40 mm cube with the tag family below"
    *Owner: perception lead. Blocks [CAD downloads](../fabrication/cad-downloads.md).*

Tag size limits range: 30 mm tags stop decoding beyond about 2 m **UNVERIFIED**{ .dh-unverified }. Keep the cubes within 2 m of the cameras. *Source: deploy repo, `OPERATIONS.md`.*

## Redo calibration

After any `humanoid_set_zero.py` run; after replacing a camera (with section 1).

!!! note "Yours to determine — full re-calibration triggers and interval"
    *Owner: perception lead.*
