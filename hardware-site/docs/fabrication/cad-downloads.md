# CAD downloads

Download the CAD at the level you need: the whole robot, one module, or one part (machined, printed
or purchased).

!!! abstract "At a glance"
    - **You will:** download the files for what you are making or checking, and verify each one.
    - **Three levels:** [whole robot](#whole-robot) · [modules](#modules) (one sub-assembly each) · [parts](#parts) (one component each, machined, printed or purchased).
    - **Parts lists:** [CNC parts](../bom/index.md#cnc-parts) · [Printed parts](../bom/index.md#printed-parts).
    - **Before this:** [Bill of materials](../bom/index.md).

!!! note "Yours to check — redistribution terms of the vendor CAD models you download"
    *Owner: PI + hardware lead.*

## Find a part on the robot

<div class="dh-viewer-block">
<model-viewer id="dh-viewer" data-base="../../" src="../../assets/viewer/robot.glb" camera-controls
  camera-orbit="35deg 75deg auto" min-camera-orbit="auto auto 0.3m" max-camera-orbit="auto auto 6m"
  interaction-prompt="none" shadow-intensity="0.6" exposure="1.1" loading="eager"
  alt="Duke Humanoid V2, every component in its Fusion 360 appearance">
  <button slot="hotspot-x" class="dh-axis dh-axis-x" type="button" tabindex="-1" data-position="0m 0m 0m" aria-label="X axis">X</button>
  <button slot="hotspot-y" class="dh-axis dh-axis-y" type="button" tabindex="-1" data-position="0m 0m 0m" aria-label="Y axis">Y</button>
  <button slot="hotspot-z" class="dh-axis dh-axis-z" type="button" tabindex="-1" data-position="0m 0m 0m" aria-label="Z axis">Z</button>
</model-viewer>
<div class="dh-viewer-bar">
  <button id="dh-viewer-reset" class="md-button" type="button">Show all</button>
  <span class="dh-viewer-legend"><span>Colours are the Fusion appearances</span><span><i class="dh-sw-amber"></i>hovered row</span><span><i class="dh-sw-red"></i>selected</span></span>
  <div id="dh-viewer-info" hidden></div>
</div>
<p class="dh-viewer-note">Axes are the STEP file axes (right-handed, Z up).</p>
</div>

1. Click **Preview** in a row below: that file's part or module turns red and the camera frames it; a whole-robot file shows the complete robot.
2. Click a component on the robot: the info box names it, lists its module chain and its downloads, and the page jumps to its row.
3. The selected part shows through other parts as a translucent red ghost. **Hide selected** takes it out of the
   view, like the eye in Fusion, so you can see what sits behind it; **Show hidden** brings everything back.
4. Drag to orbit, scroll to zoom, **Show all** to reset.

## Files

{% if cad_count() %}
Part files are named `<part_id>_rev<NN>`, matching the parts lists; left and right parts are separate files.
Module and purchased-part files carry the Fusion 360 component name.

### Whole robot

Assembly STEP, and the Fusion 360 archive (`.f3z`) for editing. Both contain every module and part below.

{{ cad_table("assembly") }}

### Modules

One STEP per sub-assembly, its parts assembled, in the sub-assembly's own coordinates: lower body, torso, arms, gripper, legs, camera
columns, wrists, the hip, knee, shoulder and elbow modules, the electronics tray, and the vendor assemblies
used at those levels. Use these to rebuild one joint or to check fits. Depth 0 is directly under the robot.

{% if cad_count("modules") %}
{{ cad_table_modules() }}
{% else %}
!!! note "Not published — per-sub-assembly module STEP files; the whole-robot and per-part STEPs cover the build"
    *Owner: hardware lead.*
{% endif %}

### Parts

One file per component, in the component's own coordinates.

#### Machined and printed parts (STEP)

For machining, or to edit or re-mesh a part.

{{ cad_table("step") }}

#### Printable meshes (3MF / STL)

Open in your slicer. Units are millimetres.

{{ cad_table("print") }}

#### Purchased parts (STEP)

Vendor models as placed in the Fusion design (motors, servos, camera, IMU, computer, bearings, fasteners).
Buy these parts; the files are for fit checks only.

{% if cad_count("vendor") %}
{{ cad_table("vendor", "Component") }}
{% else %}
!!! note "The vendors' to distribute — purchased-part STEP files (motors, servos, camera, IMU, computer)"
    *Owner: hardware lead.*
{% endif %}

#### Drawings (PDF)

Two documents: the whole-robot overall dimensions, and the exploded-view booklet
(`duke_humanoid_v2_exploded_views_rev01.pdf`, 15 pages) whose part labels are the team BOM ids
used in the [parts lists](../bom/index.md) and reproduced on the [Assembly](../assembly/index.md) pages.
There are no per-part drawings, so machined parts are ordered from the STEP files with the shop's
default tolerances.

{{ cad_table("drawings") }}

#### Ready-to-print plates

Slicer projects with orientation, supports and settings already set.

{{ cad_table("plates") }}

Checksums for every file: [SHA256SUMS.txt](../files/SHA256SUMS.txt){ download="" }.
{% else %}
!!! missing "MISSING — SAFETY — no manufacturing CAD published: per-part STEP, printable 3MF/STL, PDF drawings, whole-robot STEP and Fusion 360 archive"
    *Owner: hardware lead. Blocks release.*
{% endif %}

All STEP files are AP214 (`AUTOMOTIVE_DESIGN`), written by Fusion 360 build 2705.1.15 from the
`humanoid_2.1_latest` design. The whole-robot STEP is zipped because it is over GitHub's file-size limit.

The native Fusion 360 archive is too large for this repository and is published as a release asset:

| File | Size | SHA-256 |
| --- | ---: | --- |
| [humanoid_2.1_latest.f3z](https://github.com/rivery927/Duke_Humanoid_V2_OpenSource/releases/download/cad-v2.1-rc1/humanoid_2.1_latest.f3z) (101 linked designs included, release `cad-v2.1-rc1`) | 319 MB | `f440621df68f0775f521c87d02f8a644ae0a65f64ef76b385fdd2bc22a04d420` |

Known CAD errors are listed in the [CNC guide](#known-cad-errors). The
hardware design files, this documentation and the figures all ship under
[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0); see
[Citation and licence](../reference/index.md#citation-and-licence) and the
[`LICENSE`](../files/LICENSE){ download="" } file at the top of the downloads
folder.

## Not manufacturing files

The code repository also holds simulation meshes (`simulation/asset/duke_v2/`) and camera-calibration
fixtures (`deploy/perception/asset/*.step`). Meshes carry no tolerance, thread, finish or material:
**never send them to a shop**. `cartesian_hand_v3/` is not on this robot.

## Check a download

1. Hash the file:

    ```bash
    shasum -a 256 <file>
    ```

2. Compare the result with that file's line in `SHA256SUMS.txt`. If it differs, download the file again.

3. Write the `_revNN` of every file you use into your build log.

✅ **Check:** every file matches its checksum before anything goes to a shop.
