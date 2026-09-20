# Printed parts

Fused-deposition (FDM) and laser-sintered (SLS) parts of our own design, one row per Fusion component: the
torso plates, the wrist and shoulder parts, the end-effector attachment, the covers, the gripper's parts and the
camera-column parts, with three filament and powder rows at the end. Material, process, quantity and
price are the team BOM's where it has a line for the part. **Team ref** is that line in the team BOM
spreadsheet (`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`, 2026-09-19) and the row's `notes` quote it in
full. Print settings: [Printing guide](../fabrication/printing-guide.md).

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/part-index.md#mass-properties).
**Qty** is the Fusion occurrence count per robot; the left and right arm and leg designs are separate, so
their copies of one part are summed. Where the team BOM counts differently, the row's `notes` say both.
The team BOM prices ten printed lines only, so {{ bom_unpriced_count("printed-parts.csv") }} of
{{ bom_row_count("printed-parts.csv") }} rows read **TODO**{ .dh-missing } in **Unit cost** and
**Line total** rather than zero. The printed subtotal below covers the priced rows only.

| Part ID | Description | Material | Process | Team ref | Qty | Unit cost | Line total | Vendor | Mass / size | Files |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/printed-parts.csv", dtype="str", keep_default_na=False).to_dict("records") %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.material or "**TODO**{ .dh-missing }" }} | {{ r.process or "**TODO**{ .dh-missing }" }} | {{ team_ref_cell(r) }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ r.vendor or "**TODO**{ .dh-missing }" }} | {{ "—" if r.part_id.startswith("MAT_") else part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Printed total** | | | | **{{ bom_qty("printed-parts.csv") }}** | | **{{ bom_subtotal("printed-parts.csv") }}** | | | |


!!! missing "MISSING — SAFETY — for every printed part: filament or powder grade (the covers only carry a Fusion material name such as `hip3_protection`), structural or cosmetic, print orientation and infill; and a unit cost and vendor for every row the team BOM does not price"
    *Owner: hardware lead.*

!!! unverified "UNVERIFIED — materials: the four torso plates `3DP_body06`–`09` are PLA in the team BOM and `ABS Plastic 60%infill` in Fusion, and the team BOM's PLA is what this table shows; the material of the gripper parts `3DP_grip01`–`06` and the camera-column parts `3DP_cam01`–`04` is the team BOM's alone (their Fusion material names `rail`, `Base`, `Neck`, `Arm` are not print materials); `3DP_armP03`–`06` and `3DP_armP11` have no team BOM line at all and are listed as printed on their Fusion material name only"
    *Owner: hardware lead.*

!!! unverified "UNVERIFIED — ten open questions on how the team BOM's printed lines map onto the CAD parts: the cover lines are matched to the Fusion covers as groups, by material and piece count, not one by one, and the priced lines are matched by mass"
    - `P20`/`P21` *Hip 1 Protection A/B* and `P24`/`P25` *Hip 3 Protection A/B* → the four
      Fusion `hip3_protection` covers `3DP_legP01`–`P04`. The group is certain (4 lines × 2 =
      8 pieces = the CAD's 3 + 3 + 1 + 1), the line-to-cover assignment is not, and the CAD
      counts do not match the sheet's flat 2 per line. Is there a *Hip 1* cover distinct from
      the hip-yaw ones?
    - `P29`/`P30` *Foot Protection Top/Bot* → `3DP_legP11`/`P12`, which Fusion names
      `ANKLE_1_PROTECTION`. Foot or ankle?
    - `P33`/`P34` *Shoulder 2 Protection A/B* → `3DP_armP07`/`P08`; the four covers
      `3DP_armP03`–`P06` fit the name as well and have no team BOM line at all.
    - `P39` *Arm Roll Shaft Protection* ×8 has no CAD match and is listed under its sheet
      number. Candidates: `3DP_armP03`–`P06` (8 occurrences) or `3DP_armP11` (4).
    - `P28` *Shank Protection* ×4 → `3DP_legP09` + `3DP_legP10`, 1 Fusion occurrence each.
    - `P18` *Gimbal Shaft* vs `P19` *Gimbal Support* → `3DP_cam03_gimbal_arm` and
      `3DP_cam04_gimbal_arm_link`: the pair is certain, which is which is not.
    - `P15` *AprilTags* ×12 → `3DP_grip06_apriltag_tile`, of which Fusion has 16 (eight per
      gripper). 12 or 16?
    - `P11` *Gipper Rack* ×4 → `3DP_grip03_rail`, the only component it can point at while
      the rack itself has no geometry (see below).
    - `P7` *Wrist Housing R* + `P9` *Wrist Housing L* are one Fusion component
      (`3DP_arm14_wrist_block`, 2 occurrences) and are merged into one row here. Are the two
      housings the same part mirrored?
    - `P1` *Body Cover* ×2 → the two fixed torso plates `3DP_body06` + `3DP_body08`, `P2`
      *Front Plate* → `3DP_body07` (Fusion `front_plate_removable`) and `P3` *Back Plate* →
      `3DP_body09` (`back_plate_removable`): matched by the sheet's weight column, which
      equals the Fusion mass of `body06`, `body07` and `body09` (73.9, 96.9 and 113.8 g).
      `body08` (73.2 g) has no weight of its own in the sheet and is priced at `P1`'s rate.
      That column is headed *weight (check urdf)* and states no unit; read as kilograms it
      equals the Fusion mass on eight of the ten priced lines, which is how each price was
      placed. `P5` equals the coupler's STL volume at the density the other nylon lines
      imply, and `P0` (the PC mount) is matched by name and material only: its Fusion mass
      includes the 36 child components on the plate, so the weight cannot be checked.
    *Owner: hardware lead, from the CAD.*

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
