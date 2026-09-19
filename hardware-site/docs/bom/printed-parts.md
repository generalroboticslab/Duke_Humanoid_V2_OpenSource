# Printed parts

Fused-deposition (FDM) and laser-sintered (SLS) parts of our own design, one row per Fusion component: the
torso plates, the wrist and shoulder parts, the end-effector attachment, the covers, the gripper's parts and the
camera-column parts, with the three filament/powder rows from the team sheet at the end. Print settings:
[Printing guide](../fabrication/printing-guide.md).

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/part-index.md#mass-properties).
**Qty** is the Fusion occurrence count per robot; the left and right arm and leg designs are separate, so
their copies of one part are summed.

| Part ID | Description | Material | Process | Qty | Unit cost | Vendor | Mass / size | Files |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/printed-parts.csv", dtype="str", keep_default_na=False).to_dict("records") %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.material or "**TODO**{ .dh-missing }" }} | {{ r.process or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ r.vendor or "**TODO**{ .dh-missing }" }} | {{ "—" if r.part_id.startswith("MAT_") else part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}

!!! missing "MISSING — SAFETY — for every printed part: filament or powder grade (the covers only carry a Fusion material name such as `hip3_protection`), structural or cosmetic, print orientation and infill, cost and vendor"
    *Owner: hardware lead.*

!!! unverified "UNVERIFIED — the gripper parts `3DP_grip01`–`06`, the camera-column parts `3DP_cam01`–`04` and the shoulder-yaw cover C `3DP_armP11` are listed as printed on the strength of their Fusion appearance (a plastic) and custom material names (`rail`, `Base`, `Neck`, `Arm`, `Plastic, Opaque White`, `shoulder_yaw_protection`) only; material and process are not recorded in CAD"
    *Owner: hardware lead.*

!!! missing "MISSING — geometry of the gripper's rack: Fusion `double_helix_rack_30teeth_6mm v2` holds only the empty component `Component115` (no body), so no STEP or STL of the rack exists; whether the teeth are cut into the finger (`3DP_grip02_finger`) or the rack is a bought part is not recorded"
    *Owner: hardware lead, from the CAD.*

!!! missing "MISSING — STEP and STL of the shank covers `3DP_legP09_shank_cover_a` / `3DP_legP10_shank_cover_b`: the files published under those names are byte-identical to the shoulder covers `3DP_armP05` / `3DP_armP06` (both pairs are named `Component42` / `Component43` in Fusion, and the earlier export wrote one file per component name)"
    The export of 2026-09-19 16:46 writes one file per component (`Component42` / `Component43` for the shank
    covers, `Component42~2`, `~3` / `Component43~2`, `~3` for the shoulder covers of the left and right arm);
    re-staging it with `tools/stage_cad_export.py` closes this.
    *Owner: whoever stages the export.*

!!! unverified "UNVERIFIED — quantities are Fusion occurrence counts, and the left and right arm designs reuse one component name per cover, so one STL may serve both sides or one side may need a mirrored print"
    *Owner: hardware lead, from the CAD.*

## Not in this list

Seen in team build photos but absent from the Fusion tree **UNVERIFIED**{ .dh-unverified }: the torso central
spine; battery holders with heat-set inserts; the X-shaped IMU (inertial measurement unit) bracket; the T-brackets
holding the computer. In Fusion the batteries, IMU, computer and relay sit directly under
`3DP_body_05_x1_interior_plate` with no bracket components ([Torso and waist](../assembly/torso-and-waist.md)).

In the Fusion tree but not listed, because the material does not say the part is printed
**UNVERIFIED**{ .dh-unverified }: `Hub` inside the `Vention USB Hub` assembly (Bambu `PAHT-CF` filament material,
33 g: a printed hub mount or housing, or a vendor model given a filament material); `ankle_top_cover` (material
Steel, right leg only, with one child component); the own body of the gripper root component
`dovetail_umi_gripper` (material `rail`, role not labelled). The export writes their STEP and STL, but they are
not staged for download.
