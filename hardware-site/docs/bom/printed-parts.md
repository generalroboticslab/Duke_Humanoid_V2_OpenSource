# Printed parts

Fused-deposition (FDM) and laser-sintered (SLS) parts of our own design, one row per Fusion component: the
torso plates, the wrist and shoulder parts, the end-effector attachment, the covers, the gripper's parts and the
camera-column parts, with three filament and powder rows at the end. Material, process, quantity and
price are the team BOM's where it has a line for the part. **Team ref** is that line in the team BOM
spreadsheet (`reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`, 2026-09-19) and the row's `notes` quote it in
full. Which CAD part each team ref is, and what settles it, is one row per team BOM line in
[team-map.csv](../data/team-map.csv). Print settings: [Printing guide](../fabrication/printing-guide.md).

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/part-index.md#mass-properties).
**Qty** is the Fusion occurrence count per robot; the left and right arm and leg designs are separate, so
their copies of one part are summed. Where the team BOM counts differently, the row's `notes` say both.
The team BOM prices ten printed lines only, so {{ bom_unpriced_count("printed-parts.csv") }} of
{{ bom_row_count("printed-parts.csv") }} rows read **TODO**{ .dh-missing } in **Unit cost** and
**Line total** rather than zero. The printed subtotal below covers the priced rows only.

| Team ref | Part ID | Description | Material | Process | Qty | Unit cost | Line total | Vendor | Mass / size | Files |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/printed-parts.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.material or "**TODO**{ .dh-missing }" }} | {{ r.process or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ r.vendor or "**TODO**{ .dh-missing }" }} | {{ "—" if r.part_id.startswith("MAT_") else part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Printed total** | | | **{{ bom_qty("printed-parts.csv") }}** | | **{{ bom_subtotal("printed-parts.csv") }}** | | | |


!!! missing "MISSING — SAFETY — for every printed part: filament or powder grade (the covers only carry a Fusion material name such as `hip3_protection`), structural or cosmetic, print orientation and infill; and a unit cost and vendor for every row the team BOM does not price"
    *Owner: hardware lead.*

!!! unverified "UNVERIFIED — materials: the four torso plates `3DP_body06`–`09` are PLA in the team BOM and `ABS Plastic 60%infill` in Fusion, and the team BOM's PLA is what this table shows; the material of the gripper parts `3DP_grip01`–`06` and the camera-column parts `3DP_cam01`–`04` is the team BOM's alone (their Fusion material names `rail`, `Base`, `Neck`, `Arm` are not print materials); `3DP_armP11` has no team BOM line at all and is listed as printed on its Fusion material name only"
    *Owner: hardware lead.*

Every printed line of the team BOM is matched to its CAD part by the team's exploded-view booklet, which
labels each assembly with the spreadsheet's own ids and is reproduced on the
[assembly pages](../assembly/index.md).
What is left open is which half of a two-piece cover each *A*/*B* line is, and two piece counts.

!!! unverified "UNVERIFIED — which half of a cover each line is: the booklet draws both halves of a pair but does not say which is A and which is B, so the pairs below are matched as pairs only"
    - `P20`/`P21` *Hip 1 Protection A/B* and `P24`/`P25` *Hip 3 Protection A/B* → the four
      Fusion covers `3DP_legP01`–`P04`. Booklet p.6 draws four covers on one leg, over the
      hip-1 and the hip-3 motor: 4 lines × 2 = 8 pieces = the CAD's 8 occurrences. In the
      2026-09-19 export those four are one two-piece design (identical mass and box) placed
      at four motors and all named after the hip-pitch motor, while the booklet's four covers
      do not all look alike. Whether *Hip 1* has a cover of its own, which line is which
      cover, and which pair is *Hip 1*, is open.
    - `P22`/`P23` hip 2, `P26`/`P27` knee, `P29`/`P30` ankle roll, `P33`/`P34` shoulder
      pitch, `P35`/`P36` arm roll, `P37`/`P38` elbow: pair confirmed on booklet p.6 and
      p.10, half not. `P35` is labelled twice at the shoulder end of the arm and `P36` twice
      at the forearm end, so those two lines may split by joint rather than by half.
    *Owner: hardware lead.*

!!! unverified "UNVERIFIED — two piece counts: `P15` *AprilTags* ×12 against 16 tiles (booklet p.13 draws eight on one gripper, Fusion has 16), and `P28` *Shank Protection* ×4 against the 2 occurrences Fusion carries (booklet p.6 draws two straps on one leg, and the CAD holds the pair on the right leg only)"
    The table above shows the Fusion count, so `P15` reads 16 and `P28` reads 1 per cover.
    *Owner: hardware lead.*

The ten priced lines are matched by the sheet's weight column, not by the booklet: read as kilograms it
equals the Fusion mass on eight of them (`P1` *Body Cover* 73.9 g = `3DP_body06`, whose twin `3DP_body08`
is 73.2 g and is priced at the same rate; `P2` 96.9 g = `3DP_body07`; `P3` 113.8 g = `3DP_body09`).
`P5` equals the coupler's STL volume at the density the other nylon lines imply, and `P0` *PC Mount* has no
checkable mass because the Fusion component carries 36 children. The column is headed *weight (check urdf)*
and states no unit.

The gripper's rack teeth are cut along the slide arm `3DP_grip03_rail` (`P11`, booklet p.13), so the empty
Fusion component `double_helix_rack_30teeth_6mm v2` is a placeholder with no body, no STEP and no STL.

!!! missing "MISSING — STEP and STL of the shank covers `3DP_legP09_shank_cover_a` / `3DP_legP10_shank_cover_b`: the files published under those names are byte-identical to the shoulder covers `3DP_armP05` / `3DP_armP06` (both pairs are named `Component42` / `Component43` in Fusion, and the earlier export wrote one file per component name)"
    The export of 2026-09-19 16:46 writes one file per component (`Component42` / `Component43` for the shank
    covers, `Component42~2`, `~3` / `Component43~2`, `~3` for the shoulder covers of the left and right arm);
    re-staging it with `tools/stage_cad_export.py` closes this.
    *Owner: whoever stages the export.*

!!! unverified "UNVERIFIED — quantities are Fusion occurrence counts, and the left and right arm designs reuse one component name per cover, so one STL may serve both sides or one side may need a mirrored print"
    *Owner: hardware lead, from the CAD.*

## Not in this list

Seen in team build photos but absent from the Fusion tree **UNVERIFIED**{ .dh-unverified }: battery holders
with heat-set inserts; the X-shaped IMU (inertial measurement unit) bracket; the T-brackets
holding the computer. In Fusion the batteries, IMU, computer and relay sit directly under
`3DP_body_05_x1_interior_plate` with no bracket components ([Torso and waist](../assembly/torso-and-waist.md)).

In the Fusion tree but not listed, because the material does not say the part is printed
**UNVERIFIED**{ .dh-unverified }: `Hub` inside the `Vention USB Hub` assembly (Bambu `PAHT-CF` filament material,
33 g: a printed hub mount or housing, or a vendor model given a filament material); `ankle_top_cover` (material
Steel, right leg only, with one child component); the own body of the gripper root component
`dovetail_umi_gripper` (material `rail`, role not labelled). The export writes their STEP and STL, but they are
not staged for download.
