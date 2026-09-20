# Open items — the punch list

Every unresolved item on this site, in one table: **184 open items** across **42 pages**, of which **56 block the public release**.

This page is the team's working list. It is generated from the `MISSING` / `UNVERIFIED`
blocks on the pages themselves, so it cannot drift away from them: close a block
on its page and it leaves this table when the list is regenerated. Nothing is
tracked here that is not also marked in place, and nothing is marked in place
that is not here.

!!! note "How to read a row"
    **Page** links to the exact section or step the gap sits in — that is where
    the surrounding facts are, and where the answer must be written. **Who can
    supply it** is copied from the block's own owner line; it names a role, not
    a person, because roles survive a graduation. **Blocks release** is `yes`
    when the title says `MISSING — SAFETY`, when the block itself says what it
    blocks, or when it sits on a page the home page already names as a blocker
    (CAD downloads, the fastener schedule, the licence, safety).

## Where the work sits

| Section | Open items | Blocking release |
| --- | ---: | ---: |
| Before you start | 22 | 15 |
| Bill of materials | 29 | 6 |
| Fabrication | 18 | 6 |
| Assembly | 46 | 5 |
| Electrical | 26 | 12 |
| Bring-up | 25 | 7 |
| Reference | 16 | 5 |
| Top level | 2 | 0 |
| **Total** | **184** | **56** |

## Who is holding what

An item owned jointly counts once against each role, so this column sums to
more than 184.

| Role | Open items | Of those, blocking |
| --- | ---: | ---: |
| Hardware lead | 114 | 31 |
| Electrical lead | 46 | 23 |
| Controls lead | 31 | 7 |
| Perception lead | 8 | 1 |
| PI | 7 | 5 |
| Safety sign-off | 6 | 6 |
| Whoever does the first build / re-sourcing | 5 | 0 |
| BOM owner | 5 | 1 |
| Local EHS office | 3 | 3 |
| Assembly lead | 2 | 1 |
| Unassigned | 1 | 0 |

## The six that stop a build outright

These are the home page's own blocker rows, restated as work. Everything else
in this list makes a build harder; these make it impossible.

| Blocker | Where it is tracked |
| --- | --- |
| No drawings, print plates or native Fusion archive — per-part and whole-robot STEP are published | [CAD downloads](../fabrication/cad-downloads.md) |
| No fastener schedule — the team BOM's bearing and screw lines carry no price, no vendor and no screw quantity | [Fasteners and hardware](../bom/fasteners-and-hardware.md) |
| No torque values and no threadlocker grade, anywhere | [Assembly](../assembly/index.md), [Tools](../assembly/tools.md) |
| No hardware licence and no documentation licence | [Citation and licence](citation-and-license.md) |
| No human-safety procedure: no e-stop doctrine, no power-down order, no bystander distance | [Safety](../before-you-start/safety.md) |
| No hardware e-stop exists in the design at all — the only stop is a software velocity limit | [Power system](../electrical/power-system.md), [Torso and waist](../assembly/torso-and-waist.md) |

## Before you start

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [cost-and-time → Cost](../before-you-start/cost-and-time.md#cost) | A real price: priced fasteners and bearings, printed-part cost, tools tier (with gantry), options tier, shipping/duty/setup allowance, a priced_as_of date per row | hardware lead | **yes** |
| [cost-and-time → Time](../before-you-start/cost-and-time.md#time) | Build time: elapsed time and person-hours per stage (procurement, fabrication, assembly, wiring, bring-up) | whoever performs the first complete build with a stopwatch | no |
| [cost-and-time → Time](../before-you-start/cost-and-time.md#time) | Quoted lead times (cameras, each actuator model, machining), tested alternates for both single-source items, ordering sequence | hardware lead | no |
| [index → Go / no-go](../before-you-start/index.md#go-no-go) | Budget and calendar thresholds, and the last point where a build can stop cheaply | hardware lead | no |
| [safety → Rules](../before-you-start/safety.md#rules) | Lifting specification: gantry rating over 36 kg, lifting points, slings, clearance zone; the gantry is in no parts list | hardware lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Bystander distances: suspended, standing, walking (including fall radius) | hardware lead + local EHS office | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Rest of the PPE list: safety shoes, and whether gloves are required or forbidden | hardware lead + local EHS office | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | E-stop: none in the bill of materials or power diagram, yet the run scripts assume one; mounting, what it cuts, remote or dead-man switch, restart checks — Scripts: `humanoid_nav_step_test.py`, `humanoid_joint_monkey_hw.py`. | electrical lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Physical power-on and power-off order (computer, USB-CAN adapters, motor bus, camera gimbals), with a check at each step, and the software shutdown order before power-off | electrical lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Isolation and lock-out/tag-out procedure, including how to confirm the converters have discharged | electrical lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Which steps need a second person and which need a hoist | hardware lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Numbered mechanical and electrical incident register, like deploy's control-stack register | hardware lead, continuously | **yes** |
| [safety → Power loss means collapse](../before-you-start/safety.md#power-loss-means-collapse) | Collapse behaviour and standoff distance on power loss; safe pose before planned power-down | hardware lead, from a drop test with the robot suspended | **yes** |
| [safety → Lithium-polymer (LiPo) packs](../before-you-start/safety.md#lithium-polymer-lipo-packs) | Battery procedure: charger and charge rate, voltage floor, storage, fire response, disposal, pack-path protection — The team linked an "ISDT ...; DC600Wx2" charger;; the model is UNVERIFIED. | hardware lead with the local EHS office | **yes** |
| [safety → Crush](../before-you-start/safety.md#crush) | Pinch-point diagram (knee, elbow, hip-roll/thigh, waist, gripper jaws, camera gimbals) | hardware lead for the geometry | **yes** |
| [safety → Falls](../before-you-start/safety.md#falls) | Conditions for letting the robot stand free | hardware lead + controls lead | **yes** |
| [safety → Inspect and log before each session](../before-you-start/safety.md#inspect-and-log-before-each-session) | Inspection intervals, pass/fail criteria and owners for the table above | hardware lead | **yes** |
| [skills-and-shop](../before-you-start/skills-and-shop.md) | Prerequisite skills confirmed by an actual build | whoever performs the first external build | no |
| [skills-and-shop → Fabrication](../before-you-start/skills-and-shop.md#fabrication) | Whether 3 axes suffice (any 4/5-axis or turned part), minimum work envelope, FDM substitute for SLS parts, required finishes | hardware lead, from the CAD | **yes** |
| [skills-and-shop → Software](../before-you-start/skills-and-shop.md#software) | GPU machine specification and cost (GPU/VRAM, CPU, RAM, OS, CUDA version, the machine used) | controls lead | no |
| [skills-and-shop → People and space](../before-you-start/skills-and-shop.md#people-and-space) | Bench and floor space used by the reference build | hardware lead | no |
| [what-you-get](../before-you-start/what-you-get.md) | Scope: in or out for teleoperation setup, training workstation, mocap rig, test fixtures, perception cube targets and tripods, charging bench and gantry | hardware lead | no |

## Bill of materials

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [actuators → Which model goes in which joint](../bom/actuators.md#which-model-goes-in-which-joint) | RS05 on wrist_3 and the four camera joints is not checked on the robot | hardware lead + controls lead | no |
| [actuators → Which model goes in which joint](../bom/actuators.md#which-model-goes-in-which-joint) | 2 RS06: this table needs 4 (ankle_2 and shoulder_2 on both sides), the team BOM line `E6` buys 2 | hardware lead | no |
| [actuators → Motor data](../bom/actuators.md#motor-data) | RS00, RS05, RS06 manual data (voltage range, reduction, encoder, `0x7018` range); firmware version and per-joint limits as run on the reference robot | hardware lead + controls lead | no |
| [cables-and-connectors](../bom/cables-and-connectors.md) | Pinout of every custom cable, cut length per run, strain relief and service loops at moving joints | electrical lead | no |
| [cables-and-connectors → Actuator-side connectors](../bom/cables-and-connectors.md#actuator-side-connectors) | Trunk connector (harness pages: XT30(2+2) on every actuator; manuals: XT30 + GH1.25 on RS03/RS04) and CAN wire colours (RS04 manual: blue = CAN_H, brown = CAN_L; team harness, blue/yellow: yellow = CAN_H, blue = CAN_L) | electrical lead | no |
| [cables-and-connectors → Wire gauge](../bom/cables-and-connectors.md#wire-gauge) | Wire gauge of the 48 V riser, the ground returns, the motor branches and the CAN wire | electrical lead | **yes** |
| [cables-and-connectors → Not in this list](../bom/cables-and-connectors.md#not-in-this-list) | Parts-list rows for every connector the harness uses (XT30, XT30(2+2), GH1.25 housings and contacts, EC5), for wire loom or sleeving, Ethernet cable, heat-shrink, bulk wire (gauge, rating, colour, length) and … | electrical lead | no |
| [cables-and-connectors → Not in this list](../bom/cables-and-connectors.md#not-in-this-list) | Two design-log parts with no role: Amazon B0774VBJ3J and connector-housing kit B0BHZTQ1WV | electrical lead | no |
| [cnc-parts → Summary](../bom/cnc-parts.md#summary) | Whether the five rows with no team BOM line are machined parts at all: the team's booklet draws `CNC_arm05`, `CNC_arm06` and `CNC_arm11` as the printed lines `P4`, `P5` and `P6` on p.9, and Fusion has them as … | hardware lead | no |
| [cnc-parts → Summary](../bom/cnc-parts.md#summary) | The unit price of `C25` *Shoulder/Elbow Support* ×4: the team BOM's 57.56 is exactly twice the earlier machining quote's 28.78 for the same part, and the team BOM's is the price shown above — The part itself … | BOM owner | no |
| [electronics → Where each part goes](../bom/electronics.md#where-each-part-goes) | Computer RAM, storage, OS release and rated input power; camera firmware version; physical IMU mounting position and orientation; bring-up peripherals beyond the operator laptop and the GPU machine | electrical lead | no |
| [electronics → Where each part goes](../bom/electronics.md#where-each-part-goes) | IMU mounting screw: M3 (team log) vs Ø2.10 flange holes on 30 × 31 mm centres (vendor drawing) | hardware lead | no |
| [electronics → Power path](../bom/electronics.md#power-path) | 48 V→12 V conversion (power diagram: one buck converter, computer only, no 5 V rail; this list: three); TVS diode (M1.5KE62CA, from the DigiKey link) and how many of the ten sit at each distribution-block pair | electrical lead | **yes** |
| [electronics → Not in this list](../bom/electronics.md#not-in-this-list) | A parts-list row (MPN, qty, link) for the 10 A fuse and holder and for the battery charger, and a manufacturer part number for the surge protector, the four distribution terminals, the USB hubs and the voltage … | electrical lead | no |
| [fasteners-and-hardware](../bom/fasteners-and-hardware.md) | Fastener schedule from CAD: every screw (thread, length, head, drive, qty), bearings and fits per location, dowel pins, retaining rings, shims, threadlocker locations, torque per size and joint, purchase links | hardware lead, from the CAD | **yes** |
| [fasteners-and-hardware → Screwing into an actuator](../bom/fasteners-and-hardware.md#screwing-into-an-actuator) | The 35 × 44 × 5 mm bearing count: team BOM line `H2` buys 18, the Fusion model places 26 `bearing_35x44x5_6707_1.6kN_15g` (at least one of them inside the RobStride 06 actuator model, so not every occurrence … | hardware lead | **yes** |
| [fasteners-and-hardware → Screwing into an actuator](../bom/fasteners-and-hardware.md#screwing-into-an-actuator) | Retaining compound and grease type per bearing and sliding surface | hardware lead | **yes** |
| [index](../bom/index.md) | A unit price for every unpriced team BOM row: all nine bearing and screw lines, every printed part except the ten the sheet prices by weight, and the five machined parts the sheet has no line for — The sheet … | BOM owner | no |
| [index](../bom/index.md) | Allowance for tax, scrap and re-machining in the robot cost | hardware lead | no |
| [printed-parts](../bom/printed-parts.md) | For every printed part: filament or powder grade (the covers only carry a Fusion material name such as `hip3_protection`), structural or cosmetic, print orientation and infill; and a unit cost and vendor for every row the team BOM does not price | hardware lead | **yes** |
| [printed-parts](../bom/printed-parts.md) | Materials: the four torso plates `3DP_body06`–`09` are PLA in the team BOM and `ABS Plastic 60%infill` in Fusion, and the team BOM's PLA is what this table shows; the material of the gripper parts … | hardware lead | no |
| [printed-parts](../bom/printed-parts.md) | Which half of a cover each line is: the booklet draws both halves of a pair but does not say which is A and which is B, so the pairs below are matched as pairs only — `P20`/`P21` Hip 1 Protection A/B and … | hardware lead | no |
| [printed-parts](../bom/printed-parts.md) | Two piece counts: `P15` *AprilTags* ×12 against 16 tiles (booklet p.13 draws eight on one gripper, Fusion has 16), and `P28` *Shank Protection* ×4 against the 2 occurrences Fusion carries (booklet p.6 draws … | hardware lead | no |
| [printed-parts](../bom/printed-parts.md) | STEP and STL of the shank covers `3DP_legP09_shank_cover_a` / `3DP_legP10_shank_cover_b`: the files published under those names are byte-identical to the shoulder covers `3DP_armP05` / `3DP_armP06` (both pairs … | whoever stages the export | no |
| [printed-parts](../bom/printed-parts.md) | Quantities are Fusion occurrence counts, and the left and right arm designs reuse one component name per cover, so one STL may serve both sides or one side may need a mirrored print | hardware lead, from the CAD | no |
| [sourcing](../bom/sourcing.md) | Quoted lead times, with the quote date, for machining, the D436 and the RobStride actuators | hardware lead | no |
| [sourcing → Supply-risk parts](../bom/sourcing.md#supply-risk-parts) | An alternate for the D436 and for each RobStride model, or what a substitution requires | hardware lead + perception lead | no |
| [sourcing → Vendors](../bom/sourcing.md#vendors) | Manufacturer part numbers for the marketplace lines | hardware lead | no |
| [sourcing → Price dates](../bom/sourcing.md#price-dates) | A re-check of each price against its vendor, with the date it was checked | whoever re-sources the parts | no |

## Fabrication

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [cad-downloads](../fabrication/cad-downloads.md) | Redistribution terms of the vendor CAD models (RobStride, Feetech, Intel RealSense, SYD Dynamics, MINISFORUM) included in the whole-robot and module files | PI + hardware lead | **yes** |
| [cad-downloads → Modules](../fabrication/cad-downloads.md#modules) | Module STEP files (one per sub-assembly) are not published yet | hardware lead | **yes** |
| [cad-downloads → Purchased parts (STEP)](../fabrication/cad-downloads.md#purchased-parts-step) | Purchased-part STEP files (motors, servos, camera, IMU, computer) are not published yet | hardware lead | **yes** |
| [cnc-guide → Material and design rules](../fabrication/cnc-guide.md#material-and-design-rules) | Per part: alloy and temper, tolerances on bearing seats, journals, dowel holes and mating faces, finish per face, thread specs, turned or 5-axis | hardware lead, from the CAD and the machining quotations | **yes** |
| [cnc-guide → Known CAD errors](../fabrication/cnc-guide.md#known-cad-errors) | CAD errors: Motor04 shaft and knee need M5 holes, CAD has M4; RS03 shaft bearing retainer above the knee is a design error (enlarged by hand). Whether the released CAD is corrected is unknown | hardware lead | **yes** |
| [cnc-guide → Order the parts](../fabrication/cnc-guide.md#order-the-parts) | Whether the reference parts were ordered from STEP alone or with drawings that were not kept | hardware lead | no |
| [cnc-guide → Order the parts](../fabrication/cnc-guide.md#order-the-parts) | Reference-build machine shop, what it was sent, quote, lead time, setup cost (material was priced with JLCPCB CNC) | hardware lead | no |
| [cnc-guide → Order the parts](../fabrication/cnc-guide.md#order-the-parts) | Which machined parts need spares, and how many | hardware lead | no |
| [cnc-guide → Order the parts](../fabrication/cnc-guide.md#order-the-parts) | Decision on registering the machined parts with one service and publishing its part numbers | hardware lead | no |
| [incoming-inspection → Measure machined parts](../fabrication/incoming-inspection.md#measure-machined-parts) | Nominal and tolerance for every fit-critical feature; until then, record the measured values | hardware lead, once the CNC drawings exist | no |
| [incoming-inspection → Check printed parts](../fabrication/incoming-inspection.md#check-printed-parts) | Pass criteria for printed parts, and which printed parts are structural | hardware lead | no |
| [incoming-inspection → Check actuators](../fabrication/incoming-inspection.md#check-actuators) | Actuator acceptance criteria: firmware baseline per model, bench setup and read-out command, free-rotation feel, mass window, run-in | hardware lead | no |
| [incoming-inspection → Check electronics](../fabrication/incoming-inspection.md#check-electronics) | Battery acceptance voltage and cell balance on arrival, and storage charge | hardware lead | **yes** |
| [incoming-inspection → Record and reject](../fabrication/incoming-inspection.md#record-and-reject) | Measuring instruments and ranges beyond a caliper (micrometers, bore or pin gauges, indicator, thread gauges, multimeter, cell checker) | hardware lead | no |
| [printing-guide → Print profiles](../fabrication/printing-guide.md#print-profiles) | `print_profiles.csv`: material grade, layer height, walls, infill, orientation (which face down, which load the layers must not cross), supports and validated printer for every printed part | hardware lead, from the printer the reference build used | no |
| [printing-guide → Print profiles](../fabrication/printing-guide.md#print-profiles) | Material settings: PLA (filament, nozzle and bed temperature, cooling, speed, enclosure); TPU (shore hardness, temperatures, retraction, speed, extruder type, what the parts are for); SLS (powder grade, bureau, finish, tolerance) | hardware lead | no |
| [printing-guide → Print the parts](../fabrication/printing-guide.md#print-the-parts) | Which parts are FDM or SLS, which are structural, and whether an SLS part can be printed FDM instead | hardware lead | no |
| [printing-guide → Post-process](../fabrication/printing-guide.md#post-process) | Post-processing per part (support removal on mating faces, holes to ream and to what size, heat-set insert size and temperature, annealing) and print time and material mass per part | hardware lead | no |

## Assembly

Almost every row here reads `no`, and that is a reporting artefact rather
than an all-clear: the home page names *no torque values and no threadlocker
specification* as one single release blocker, and it is these rows, spread
across every step of every limb. Treat the section as blocking and the rows
as its inventory.

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [arm](../assembly/arm.md) | Arm parts list, fasteners, torques and fits — No bearing, spacer, printed-part or fastener list.; Per step: screws, torque, Loctite 222 use, bearings, press fits, order, alignment and preload (steps 3, 5). … | hardware lead, from the computer-aided design (CAD) and a photographed build | no |
| [arm → Configure and label the seven actuators (step 1)](../assembly/arm.md#step-1) | Arm hard stops, and the real travel of the four ±180° joints with cabling fitted | hardware lead | no |
| [arm → Build the shoulder-pitch joint (step 2)](../assembly/arm.md#step-2) | Machined-part IDs `arm05`–`arm10`: team list and site list disagree — Steps below use site IDs;; order by part name until settled. … | hardware lead | no |
| [arm → Build the wrist-yaw joint (step 8)](../assembly/arm.md#step-8) | Wrist-to-gripper interface: bolt circle, pilot, keying, servo-cable pass-through | hardware lead | no |
| [arm → Route the harness and close the arm (step 9)](../assembly/arm.md#step-9) | Arm harness: wire gauge, connectors, lengths, service loops — See Harness fabrication. | hardware lead + electrical | no |
| [arm → Build the second arm](../assembly/arm.md#build-the-second-arm) | Which arm parts are handed and which are common — The model's arms differ in `shoulder_2` limits and orientation. | hardware lead, from the CAD | no |
| [final-integration → Support the torso (step 1)](../assembly/final-integration.md#step-1) | Lifting points, sling route and integration stand — None defined; needed before the first lift.; Sling attachment.; What holds the torso (upright or lying down) while limbs go on. … | hardware lead + Safety sign-off | **yes** |
| [final-integration → Attach the first leg (step 2)](../assembly/final-integration.md#step-2) | Hip, shoulder and wrist interfaces: screws, torque, Loctite 222 use, locating features | hardware lead | no |
| [final-integration → Join the harnesses (step 7)](../assembly/final-integration.md#step-7) | Torso harness: connectors, lengths, service loops at hip, shoulder and waist, join order — See Harness fabrication. | electrical lead | no |
| [final-integration → Inspect the whole robot (step 8)](../assembly/final-integration.md#step-8) | Signed inspection checklist keyed to the fastener schedule | hardware lead | no |
| [final-integration → Weigh and hang the robot (step 9)](../assembly/final-integration.md#step-9) | As-built mass by subassembly | whoever performs the first documented build | no |
| [gripper](../assembly/gripper.md) | Gripper parts list, fasteners, torques and fits — Material, process and cost of `base`, both racks and `cnc_flange`.; Pinion, slide parts, fasteners.; Per step: screws, torque, Loctite 222 use, order. … | hardware lead + BOM owner | no |
| [gripper → Configure and label the two servos (step 1)](../assembly/gripper.md#step-1) | Right gripper servo ID: 0 (end-effector service) or 19 (bench script) | controls + hardware lead | no |
| [gripper → Fit the jaw pads (step 4)](../assembly/gripper.md#step-4) | Jaw pads: whether they exist, material, attachment; a thermoplastic polyurethane line in the bill of materials has no part | hardware lead | no |
| [gripper → Apply the AprilTags (step 5)](../assembly/gripper.md#step-5) | AprilTag substrate, adhesive and replacement | perception + hardware lead | no |
| [gripper → Fit the mounting flange (step 6)](../assembly/gripper.md#step-6) | Flange bolt circle, pilot, keying, and jaw clocking relative to `wrist_3` — Document with the arm side (Arm, step 8). | hardware lead | no |
| [gripper → Set the open and closed positions (step 7)](../assembly/gripper.md#step-7) | Jaw opening: 184 mm (model docs) vs 90 mm (uncalibrated service map) — Measure it in step 7. | hardware lead + controls | **yes** |
| [gripper → Set the open and closed positions (step 7)](../assembly/gripper.md#step-7) | Commissioning: open end stop, validated safe torque limit, matching both hands — The zero routine finds only the closed stall, and the torques above are configured values, not a tested limit. | controls + hardware lead | no |
| [head-and-camera-gimbal](../assembly/head-and-camera-gimbal.md) | Gimbal column procedure: fasteners, torques, bearings, hard stops — Per step: screws, torque, Loctite 222 use, order.; Any yaw bearing; neck keying.; How to set and hold the yaw and pitch zeros; hard stops.; … | hardware lead | no |
| [head-and-camera-gimbal → Configure the actuators and record the camera serials (step 1)](../assembly/head-and-camera-gimbal.md#step-1) | Which physical side of the plate carries `cam_yaw_left` (ID 7) and `cam_pitch_left` (ID 8) — Computer-aided design (CAD): left at y = −65 mm;; MuJoCo model: y = +0.065 m.; A swap fails silently. | hardware lead + controls | no |
| [head-and-camera-gimbal → Install the yaw actuator in the mount (step 2)](../assembly/head-and-camera-gimbal.md#step-2) | Gimbal parts are in no bill of materials: material, process, tolerance, cost, bearing, fasteners | hardware lead + BOM owner | no |
| [head-and-camera-gimbal → Install the pitch actuator and the arm (step 4)](../assembly/head-and-camera-gimbal.md#step-4) | `gimbal_arm`: one part or two; `U-joint_type_C_adapter`: mechanical or a USB-C cable adapter | hardware lead | no |
| [head-and-camera-gimbal → Mount the camera (step 5)](../assembly/head-and-camera-gimbal.md#step-5) | The bracket CAD names a D435 body; confirm the D436 fits before machining — The STEP names the camera `IntelRealsense_D435_Multibody`; … | hardware lead | no |
| [head-and-camera-gimbal → Route the camera cable (step 6)](../assembly/head-and-camera-gimbal.md#step-6) | Camera cable across the yaw and pitch axes — Real yaw travel; how the USB-C cable crosses yaw (slip ring, helix or stop).; Cable type, length, bend radius, service loop, retention. … | hardware lead + electrical | **yes** |
| [head-and-camera-gimbal → Bench-test the column (step 7)](../assembly/head-and-camera-gimbal.md#step-7) | Single-column bench harness and written test procedure — The deploy sweep drives all four gimbal motors;; no single-column harness, cycle count or pass criteria exist in the sources. | hardware lead + controls | no |
| [head-and-camera-gimbal → Mount both columns on the top plate (step 9)](../assembly/head-and-camera-gimbal.md#step-9) | Top plate central hole shape: the CAD parse gives only a 64.8 × 59.0 mm bounding box; the CAD animation shows it hexagonal | hardware lead | no |
| [index](../assembly/index.md) | Build order and subassembly boundaries — whether harness branches go into a limb before it closes;; whether `hip_1` and `hip_2` belong to the leg or, as in the computer-aided design (CAD), to the pelvis with the waist; … | hardware lead | no |
| [index → Follow these rules on every page](../assembly/index.md#follow-these-rules-on-every-page) | Build time and crew size per subassembly | whoever performs the first externally documented build | no |
| [leg](../assembly/leg.md) | Leg parts list, fasteners, torques and fits — No printed-part, bearing, spacer or fastener list.; Per step: screws, torque, Loctite 222 use, bearings, press fits, order.; Retainer alignment and preload (steps 3, 8). … | hardware lead, from the computer-aided design (CAD) and a photographed build | no |
| [leg → Configure and label the six actuators (step 1)](../assembly/leg.md#step-1) | Leg mechanical hard stops: whether any exist, and where | hardware lead | no |
| [leg → Build the hip-pitch joint (step 2)](../assembly/leg.md#step-2) | Machined-part counts: `leg02` 7 (team list) or 8 (site list); `leg12` 4 or 5 | hardware lead | no |
| [leg → Build the hip-yaw joint (step 4)](../assembly/leg.md#step-4) | Hip yaw: no machined part is named for it (the CAD shows the waist's flange, ring and coupler) | hardware lead | no |
| [leg → Build the knee joint (step 5)](../assembly/leg.md#step-5) | CAD errors: Motor04 shaft and knee need M5 holes, CAD has M4; design error in the RS03 shaft bearing retainer above the knee — Found at the first-article fit check;; whether the released CAD is fixed is … | hardware lead | no |
| [leg → Fit the foot plate (step 9)](../assembly/leg.md#step-9) | Foot sole or pad: none in the parts list or the CAD | hardware lead | no |
| [leg → Route the harness and close the leg (step 10)](../assembly/leg.md#step-10) | Leg harness: gauge, connectors, lengths, service loops, retention | hardware lead + electrical | no |
| [leg → Build the second leg](../assembly/leg.md#build-the-second-leg) | Which leg parts are handed and which are common — The model's legs differ in `hip_2` limits and orientation. | hardware lead, from the CAD | no |
| [tools](../assembly/tools.md) | Tool list derived from the parts list, not checked against a build | hardware lead, from the first documented build | no |
| [tools → Consumables](../assembly/tools.md#consumables) | Tools that cannot be specified yet: bearing press and arbors, driver sizes, torque range, crimp dies, retaining-ring pliers, zeroing fixtures | hardware lead | no |
| [torso-and-waist](../assembly/torso-and-waist.md) | Torso fasteners, torques, mounts and retention — Per step: screws, torque, Loctite 222 use, plate join order and location, squareness tolerance.; No electronics item has a mount in any parts list. … | hardware lead, from the computer-aided design (CAD) and a photographed build | no |
| [torso-and-waist → Assemble the plate frame (step 2)](../assembly/torso-and-waist.md#step-2) | Machined-part sheet also lists `B1`–`B3` and `B5_body_shelf` plates — Probably duplicates of the `CNC_body` plates: do not order both.; The CAD's internal spine has no `CNC_body` ID. | hardware lead | no |
| [torso-and-waist → Install the waist actuator (step 3)](../assembly/torso-and-waist.md#step-3) | Waist: part IDs of the flange, ring and coupler; whether the ring is a bearing | hardware lead | no |
| [torso-and-waist → Mount the battery packs (step 6)](../assembly/torso-and-waist.md#step-6) | Battery pack retention, swap path and lead protection | hardware lead + electrical | **yes** |
| [torso-and-waist → Mount the IMU (step 8)](../assembly/torso-and-waist.md#step-8) | IMU screws: M3 (team log) vs Ø2.10 mm holes on 30 × 31 mm (vendor drawing) | hardware lead | no |
| [torso-and-waist → Mount the IMU (step 8)](../assembly/torso-and-waist.md#step-8) | IMU physical position relative to the `base_link` origin, which way it faces, and a pass/fail axis-alignment check | hardware lead + controls | no |
| [torso-and-waist → Fit the disconnect and emergency stop (step 9)](../assembly/torso-and-waist.md#step-9) | No e-stop, main disconnect or pre-charge in the BOM or power diagram — The run scripts assume a physical e-stop.; Specify device, what it cuts, rating and location. | hardware lead + electrical + Safety sign-off | **yes** |
| [torso-and-waist → Fit the front and back covers (step 10)](../assembly/torso-and-waist.md#step-10) | Torso covers: material, structural or not, fasteners, what comes off for a pack swap | hardware lead | no |

## Electrical

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [can-bus → Wire and terminate each bus](../electrical/can-bus.md#wire-and-terminate-each-bus) | Per bus: terminator location and type, reference-robot measured value, daisy-chain order and path; CANable PRO termination setting, CAN wire gauge and shielding, stub-length limit, adapter USB retention | electrical lead, from a photographed build | **yes** |
| [can-bus → Name each adapter](../electrical/can-bus.md#name-each-adapter) | CandleLight firmware version on the reference adapters | electrical lead | no |
| [harness-fabrication → Plan every cable](../electrical/harness-fabrication.md#plan-every-cable) | Not in the parts list: bulk wire, heat-shrink, GH1.25 CAN mates for RS03/RS04, Ethernet cable for CAN leads, CAN terminators | electrical lead | **yes** |
| [harness-fabrication → Plan every cable](../electrical/harness-fabrication.md#plan-every-cable) | Harness schedule: cable ID, conductor count, connector parts, length with service loop, sleeve size, one row per motor drop; gauge, insulation temperature rating and strand count for every unlabelled run | electrical lead, measured on a real build | **yes** |
| [harness-fabrication → Identify the connector pinouts](../electrical/harness-fabrication.md#identify-the-connector-pinouts) | Actuator connector: XT30(2+2) at RS02 vs XT30 + GH1.25 at RS03/RS04 (manuals); trunk connector unknown. CAN colours: blue/brown (RS04 manual) vs blue/yellow (team photos) | electrical lead | no |
| [harness-fabrication → Identify the connector pinouts](../electrical/harness-fabrication.md#identify-the-connector-pinouts) | Pinouts for RS00, RS05, RS06 and gripper servo; colour and gauge per pin; mating parts; pin-1 orientation | electrical lead | no |
| [harness-fabrication → Make a CAN lead from Ethernet cable](../electrical/harness-fabrication.md#make-a-can-lead-from-ethernet-cable) | Which runs use the Ethernet CAN lead, and which connector it mates | electrical lead | no |
| [harness-fabrication → Build and test each cable](../electrical/harness-fabrication.md#build-and-test-each-cable) | Cable labelling scheme: ID format, label stock, position | electrical lead | no |
| [harness-fabrication → Build and test each cable](../electrical/harness-fabrication.md#build-and-test-each-cable) | Pass criteria for the two insulation tests; pull-out force for a soldered joint; tool, die and strip length for any crimped contact | electrical lead | no |
| [harness-fabrication → Thread cables before closing limbs](../electrical/harness-fabrication.md#thread-cables-before-closing-limbs) | Which cables must be threaded before each limb is closed, per assembly step | electrical lead + assembly lead | **yes** |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | Series-link connector part number, wire gauge and length | hardware lead | **yes** |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | Pack retention in the torso rear bay and lead protection at its exit; balance-lead protection, pack monitoring and shutdown voltage; charger model, charge rate, balance-charging procedure and charging location | hardware lead (retention) + electrical lead + safety officer | **yes** |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | TVS diodes fitted at each location (BOM: 10) | electrical lead | no |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | Surge protector, 4 distribution blocks, 10 A fuse, EC5 connectors, charger: diagram or team log only, not the BOM; no confirmed part numbers | BOM owner + electrical lead | **yes** |
| [power-system → Feed the 12 V rail](../electrical/power-system.md#feed-the-12-v-rail) | 12 V conversion: power diagram draws one 48V-to-12V buck (computer only); BOM lists three (2 × 48 V→12 V, 1 × 20–60 V→12 V) | electrical lead | no |
| [power-system → Feed the 12 V rail](../electrical/power-system.md#feed-the-12-v-rail) | Gripper-servo 12 V supply (source, fuse, wiring), USB hub power and power budget | electrical lead | no |
| [power-system → Protection, disconnect and e-stop](../electrical/power-system.md#protection-disconnect-and-e-stop) | No e-stop, main disconnect or pre-charge in the power diagram or BOM, though `humanoid_nav_step_test.py` and `humanoid_joint_monkey_hw.py` require a physical e-stop; part, location and what it cuts unspecified | electrical lead + safety officer | **yes** |
| [power-system → Protection, disconnect and e-stop](../electrical/power-system.md#protection-disconnect-and-e-stop) | Pack-path fuse (none drawn); surge protector part number and rating | electrical lead + safety officer | **yes** |
| [power-system → Configured current limits](../electrical/power-system.md#configured-current-limits) | RS00, RS05, RS06 voltage range and constants not checked against a manual; back-EMF basis (rotor or output speed) unknown for all models; scale the reference robot ran (script default 0.6, script comment `04 --> scale=0.55`) | controls lead + hardware lead | no |
| [power-system → Configured current limits](../electrical/power-system.md#configured-current-limits) | Measured bus current (quiescent, standing, walking) and peak inrush at pack connection | electrical lead + controls lead | **yes** |
| [pre-power-checks → B. Test continuity and isolation](../electrical/pre-power-checks.md#b-test-continuity-and-isolation) | Resistance thresholds for B3–B6 from a known-good robot | electrical lead | **yes** |
| [pre-power-checks → D. Bench-test converters](../electrical/pre-power-checks.md#d-bench-test-converters) | Bench supply settings, output tolerance and expected load for D1–D5 | electrical lead | no |
| [pre-power-checks → F. Check packs](../electrical/pre-power-checks.md#f-check-packs) | Pack acceptance thresholds for F1, F2 and F4 | electrical lead + safety officer | **yes** |
| [routing → Route each cable](../electrical/routing.md#route-each-cable) | Routing record for leg, arm, waist, torso, gimbal, gripper: photo, bend radius, service loop and the pose it is sized at, clamp points, pinch clearance | electrical lead, from a photographed build | no |
| [routing → Verify the routing](../electrical/routing.md#verify-the-routing) | Supplies that must be on for the wiggle test: which rails feed CAN polling while the arm motors stay disabled | controls lead + electrical lead | no |
| [routing → Check for trapped cables](../electrical/routing.md#check-for-trapped-cables) | Trapped-cable check after final integration: where to look, without disassembly | electrical lead + assembly lead | no |

## Bring-up

Bring-up cannot start until Electrical closes the pack-configuration item.
Series versus parallel decides the bus voltage, and every current, converter
and check below is written against a voltage nobody has confirmed.

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [acceptance-tests → A0. Check physical conformance](../bringup/acceptance-tests.md#a0-check-physical-conformance) | A0 tolerances; mass breakdown by subassembly; source of the model's 967 g cable mass | hardware lead | no |
| [acceptance-tests → A2. Measure CAN latency](../bringup/acceptance-tests.md#a2-measure-can-latency) | A2 reference latency per bus and the harness-fault threshold | controls lead | no |
| [acceptance-tests → A4. Test per-joint motion](../bringup/acceptance-tests.md#a4-test-per-joint-motion) | A4 motion test for legs, waist, gimbals; reference tracking and current; range-of-motion sweep | controls lead | no |
| [acceptance-tests → A5. Check zero and model fidelity](../bringup/acceptance-tests.md#a5-check-zero-and-model-fidelity) | A5 reference residual per joint measured on the reference robot | controls lead | no |
| [acceptance-tests → A6. Check perception](../bringup/acceptance-tests.md#a6-check-perception) | A6 gimbal tracking test with error and lag figures | perception lead | no |
| [acceptance-tests → A7. Test grippers](../bringup/acceptance-tests.md#a7-test-grippers) | A7 reference no-slip level per side, test-cube size and mass, asymmetry limit, endurance test | controls lead | no |
| [acceptance-tests → A8. Hold whole-body posture](../bringup/acceptance-tests.md#a8-hold-whole-body-posture) | A8 reference motor temperatures and standing current, with fail values | controls lead | no |
| [acceptance-tests → A10. Reach and grasp](../bringup/acceptance-tests.md#a10-reach-and-grasp) | A10 reference grasp success rate over N attempts | controls lead | no |
| [acceptance-tests → A11. Walk](../bringup/acceptance-tests.md#a11-walk) | A11 coast distance and pass threshold; the coast constant was never measured | controls lead | **yes** |
| [acceptance-tests → A11. Walk](../bringup/acceptance-tests.md#a11-walk) | A11 stillness threshold 0.10 rad/s is untested | controls lead | no |
| [camera-calibration → 2. Check gimbal encoder zero](../bringup/camera-calibration.md#2-check-gimbal-encoder-zero) | Gimbal zero tolerance and pointing reference | perception lead + hardware lead | no |
| [camera-calibration → 3. Calibrate motor-to-camera gear](../bringup/camera-calibration.md#3-calibrate-motor-to-camera-gear) | Designed gimbal gear ratio and allowed spread | perception lead | no |
| [camera-calibration → Solve (step 2)](../bringup/camera-calibration.md#step-2) | Reference residuals come from example output in SETUP.md, not a recorded solve | perception lead | no |
| [camera-calibration → Make the fixtures](../bringup/camera-calibration.md#make-the-fixtures) | Tag cubes: print process and material, wrist fasteners, printable `grasp_cube_40mm` file (not in the bill of materials) | perception lead | **yes** |
| [camera-calibration → Redo calibration](../bringup/camera-calibration.md#redo-calibration) | Full re-calibration triggers and interval | perception lead | no |
| [first-power-on → Power the computer only (step 1)](../bringup/first-power-on.md#step-1) | How to power the computer alone: the power diagram feeds it from the arm motors' distribution block, no disconnect drawn — Do not improvise. | electrical lead | **yes** |
| [first-power-on → Energise the motor bus (step 4)](../bringup/first-power-on.md#step-4) | Bench-supply voltage and current limit per stage; what to do without one | electrical lead | **yes** |
| [first-power-on → Energise the motor bus (step 4)](../bringup/first-power-on.md#step-4) | Expected quiescent current, 31 drives powered, none enabled, with tolerance | electrical lead | no |
| [first-power-on → Power down (step 7)](../bringup/first-power-on.md#step-7) | Specified power-on and power-off order of the rails; the order above is unverified | electrical lead + controls lead | **yes** |
| [joint-zeroing → Set zeros](../bringup/joint-zeroing.md#set-zeros) | Zero pose: figure, physical per-joint description for legs, waist and arms, holding method or fixture | hardware lead + controls lead | no |
| [joint-zeroing → Back up zeros](../bringup/joint-zeroing.md#back-up-zeros) | Reading out, backing up and restoring the 31 zero offsets; what to redo after a drive swap | controls lead | no |
| [joint-zeroing → Check accuracy](../bringup/joint-zeroing.md#check-accuracy) | Zeroing accuracy target per joint | controls lead + hardware lead | no |
| [motor-id-and-config → Set an ID](../bringup/motor-id-and-config.md#set-an-id) | Motor ID-setting steps and interface, bus-isolation rule, firmware baseline, label scheme | controls lead + hardware lead | **yes** |
| [motor-id-and-config → Set current limits](../bringup/motor-id-and-config.md#set-current-limits) | 0x7018 range for RS00, RS05, RS06: check the datasheets first | controls lead | no |
| [motor-id-and-config → Confirm directions](../bringup/motor-id-and-config.md#confirm-directions) | Positive direction and mechanical travel limits of all 31 joints: figure, per-joint check — The models disagree on one axis sign: the deployed `robot.xml` sets `left_wrist_2_joint` axis `1 0 0` (line 280), … | controls lead | **yes** |

## Reference

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [citation-and-license → Citation](citation-and-license.md#citation) | Canonical title: CITATION.cff and the BibTeX above give different titles | PI | **yes** |
| [citation-and-license → Citation](citation-and-license.md#citation) | Paper citation (preprint not posted) and which record covers the hardware | PI | **yes** |
| [citation-and-license → Licence](citation-and-license.md#licence) | Hardware licence (e.g. CERN-OHL-S or -W) and documentation licence (e.g. CC-BY-4.0), with the licence file beside the CAD and on the download page; note V1 was MIT | PI + the university's licensing office | **yes** |
| [citation-and-license → Third-party material](citation-and-license.md#third-party-material) | Licence file for the two Unitree G1 URDFs | PI | **yes** |
| [citation-and-license → Third-party material](citation-and-license.md#third-party-material) | Third-party terms: SDKs not vendored here (e.g. the RealSense SDK that deploy imports), component firmware and EULAs, and CAD derived from vendor models | hardware lead | **yes** |
| [faq](faq.md) | Camera module interface for another robot: mounting | hardware lead | no |
| [faq](faq.md) | Issue template, contribution guide, support policy; what to do with an out-of-tolerance part; kits; build-log review | PI + hardware lead | no |
| [full-specifications → Mass properties (Fusion model)](full-specifications.md#mass-properties-fusion-model) | Unspecified: mechanical stops, as-built mass breakdown, measured CoM and inertia, physical foot geometry, current draw and runtime, payload, measured walking speed, measured gimbal range and slew rate, IP rating, robot temperature range, noise | hardware lead + controls lead | no |
| [part-index](part-index.md) | Part index (part ID → description, qty, subassembly, assembly steps) — The parts lists carry the IDs (`CNC_leg01_hip_center_back`, `3DP_legP01_hip3_cover_a`);; the team BOM names its lines by function instead, … | hardware lead for the numbering, then whoever writes the generator | no |
| [part-index](part-index.md) | CNC IDs arm05–arm10 and four quantities differ between the team's 32-part list and this site's list — / ID / Team list / This site / / --- / --- / --- / / arm05 / RS02_back_cover ×4 / RS02_shaft_bearing ×4 / / … | hardware lead | no |
| [part-index → Mass properties](part-index.md#mass-properties) | Inertia about the centre of mass for every part whose `notes` give a ± bound: the export rounds the mass to 0.1 g and these parts sit far from their component origin — The `*_origin` columns are Fusion's exact … | hardware lead, from the CAD (`tools/fusion_export/`) | no |
| [part-index → Mass properties](part-index.md#mass-properties) | Own-part mass, centre of mass and inertia for the parts whose Fusion component carries child components (inserts, magnets, mounted electronics), and the volume of every part until the export's STLs are written … | hardware lead, from the CAD: make those components leaf parts or export their bodies; whoever runs `tools/gen_part_properties.py` once `print/ | no |
| [part-index → Mass properties](part-index.md#mass-properties) | Parts that exist as two or three Fusion components (the left and right arm and leg designs are separate) whose copies differ in size or centre of mass, and parts whose STL bounding box differs from the Fusion … | hardware lead, from the CAD (check the copies for a hidden body, a mirrored placement or construction geometry) | no |
| [revisions](revisions.md) | Hardware changelog: differences between the published model and the robot in the lab, and any V1 parts carried over | hardware lead | no |
| [revisions](revisions.md) | Revision identifier (is it humanoid_v21?), a tagged release pinning code, assets and CAD, the documentation model per revision, and the rule for a new revision | hardware lead + PI | no |
| [troubleshooting](troubleshooting.md) | Entries from real failures: missing or wrong actuator ID, reversed joint, binding after bearing press, misfit part, no depth, high idle current, short pack life, harness failure at a joint | hardware lead, continuously | no |

## Top level

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [software → Robot model](../software.md#robot-model) | Asset READMEs cite paths absent from the export — Whether the files above will be published, and where a builder gets the STEP originals, is not stated. | controls lead | no |
| [software → Robot model](../software.md#robot-model) | Hardware/software contract: per-joint sign check, checkpoint per hardware revision, tested OS, kernel and drivers — Still unknown: the positive rotation direction of each joint as a builder checks it on a … | controls lead | no |

## Items that are not TODO blocks

Three gaps are structural rather than a missing fact, so they have no block on
a page to generate a row from:

| Gap | What it means | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| `tools.csv` does not exist | The Tools tier on [Bill of materials](../bom/index.md) and the subtotal on [Tools](../assembly/tools.md) both render *not yet published*. A builder cannot budget the tools | hardware lead + assembly lead | no |
| `optional.csv` does not exist | The third camera module (~$600), spares and upgrades cannot be quoted | hardware lead | no |
| `print_profiles.csv` does not exist | The per-part table on [Printing guide](../fabrication/printing-guide.md) is gated on the file and does not render at all | hardware lead | **yes** |

## Images

Missing figures are not in this table. They are tracked separately, with the
exact path and a one-line brief for each, in the
[image manifest](../assets/MANIFEST.md) — the list to hand to whoever renders
the exploded views.

## Regenerating this page

This table is derived from the pages, not maintained by hand:

```console
$ python tools/gen_punchlist.py
```

Every TODO block in `docs/` has the same shape, and that shape is what makes
the derivation possible:

```markdown
!!! missing "MISSING — short statement of the gap"
    What is missing, in enough detail that the person who has the answer
    recognises it as theirs.
    *Owner: role who can supply it.*
```

For something that is stated but not confirmed, use `!!! unverified` with a
title starting `UNVERIFIED —`. Both kinds render red and bold. Write
`MISSING — SAFETY — ...` when the gap is a safety item or stops a build
outright; the generator reads that as *blocks release*. The
`*Owner:*` line is mandatory — the generator refuses to run without it, because
an unowned TODO is a wish rather than a work item.

