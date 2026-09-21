# Printed parts

Fused-deposition (FDM) and laser-sintered (SLS) parts of our own design, one row per Fusion component: the
torso plates, the wrist and shoulder parts, the end-effector attachment, the covers, the gripper's parts and the
camera-column parts, with three filament and powder rows at the end. Material, process, quantity and
price are the team BOM's where it has a line for the part. **Team ref** is that line. Print settings: [Printing guide](../fabrication/index.md#printing-guide).

**Mass / size** is each part's CAD mass and bounding box from the Fusion model, not a measurement.
Volume, centre of mass and inertia for every part: [Mass properties](../reference/index.md#mass-properties).
**Qty** is the Fusion occurrence count per robot; the left and right arm and leg designs are separate, so
their copies of one part are summed. Where the team BOM counts differently, the row's `notes` say both.
The team BOM prices ten printed lines only, so {{ bom_unpriced_count("printed-parts.csv") }} of
{{ bom_row_count("printed-parts.csv") }} rows read **TODO**{ .dh-missing } in **Unit cost** and
**Line total** rather than zero. The printed subtotal below covers the priced rows only.

| Team ref | Part ID | Description | Material | Process | Qty | Unit cost | Line total | Vendor | Mass / size | Files |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
{% for r in pd_read_csv("data/printed-parts.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.material or "**TODO**{ .dh-missing }" }} | {{ r.process or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | {{ r.vendor or "**TODO**{ .dh-missing }" }} | {{ "—" if r.part_id.startswith("MAT_") else part_props(r.part_id) }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | | **Printed total** | | | **{{ bom_qty("printed-parts.csv") }}** | | **{{ bom_subtotal("printed-parts.csv") }}** | | | |


!!! note "Read off the model — Fusion material name per printed part"
    Take it from the published model — see [CAD downloads](../fabrication/index.md#cad-downloads).
    *Owner: hardware lead.*

!!! note "Build to the model — torso plates `3DP_body06`–`09`: PLA in the team sheet, ABS in Fusion"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    *Owner: hardware lead.*

Every printed line of the team BOM is matched to its CAD part by the team's exploded-view booklet, which
labels each assembly with the spreadsheet's own ids and is reproduced on the
[assembly pages](../assembly/index.md).
What is left open is which half of a two-piece cover each *A*/*B* line is, and two piece counts.

!!! note "Build to the model — which half of a cover pair each line is"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    - `P20`/`P21` *Hip 1 Protection A/B* and `P24`/`P25` *Hip 3 Protection A/B* → the four
      Fusion covers `3DP_legP01`–`P04`. Booklet p.6 draws four covers on one leg, over the
      hip-1 and the hip-3 motor: 4 lines × 2 = 8 pieces = the CAD's 8 occurrences. In the
      CAD export those four are one two-piece design (identical mass and box) placed
      at four motors and all named after the hip-pitch motor, while the booklet's four covers
      do not all look alike. Whether *Hip 1* has a cover of its own, which line is which
      cover, and which pair is *Hip 1*, is open.
    - `P22`/`P23` hip 2, `P26`/`P27` knee, `P29`/`P30` ankle roll, `P33`/`P34` shoulder
      pitch, `P35`/`P36` arm roll, `P37`/`P38` elbow: pair confirmed on booklet p.6 and
      p.10, half not. `P35` is labelled twice at the shoulder end of the arm and `P36` twice
      at the forearm end, so those two lines may split by joint rather than by half.
    *Owner: hardware lead.*

!!! note "Build to the model — `P15` and `P28` piece counts differ from the booklet"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
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

The shank covers and the shoulder covers are distinct files, despite sharing
Fusion component names (`Component42` / `Component43`): the shank covers span
261 × 66 × 25 mm, the shoulder covers 82 × 47 × 11 mm. Each pair's two halves
are mirrors of each other, so they carry the same triangle count and the same
bounding box and differ in file content.

!!! note "Build to the model — quantities are Fusion occurrence counts"
    The published model is what you build to; the team's spreadsheet is a working document and differs here.
    *Owner: hardware lead, from the CAD.*

## Not in this list { #printed-parts-not-in-this-list }

Seen in team build photos but absent from the Fusion tree **UNVERIFIED**{ .dh-unverified }: battery holders
with heat-set inserts; the X-shaped IMU (inertial measurement unit) bracket; the T-brackets
holding the computer. In Fusion the batteries, IMU, computer and relay sit directly under
`3DP_body_05_x1_interior_plate` with no bracket components ([Torso and waist](../assembly/index.md#torso-and-waist)).

In the Fusion tree but not listed, because the material does not say the part is printed
**UNVERIFIED**{ .dh-unverified }: `Hub` inside the `Vention USB Hub` assembly (Bambu `PAHT-CF` filament material,
33 g: a printed hub mount or housing, or a vendor model given a filament material); `ankle_top_cover` (material
Steel, right leg only, with one child component); the own body of the gripper root component
`dovetail_umi_gripper` (material `rail`, role not labelled). The export writes their STEP and STL, but they are
not staged for download.
