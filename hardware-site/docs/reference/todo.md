# Open items — the punch list

Every unresolved item on this site, in one table: **27 open items** across **15 pages**, of which **9 block the public release**.

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
    only when the block's own owner line says `Blocks release.` — it is declared,
    never inferred from wording, so a row carries that weight only because
    somebody decided it should.

## Where the work sits

| Section | Open items | Blocking release |
| --- | ---: | ---: |
| Before you start | 3 | 3 |
| Bill of materials | 8 | 1 |
| Fabrication | 2 | 2 |
| Assembly | 4 | 0 |
| Electrical | 6 | 1 |
| Bring-up | 2 | 0 |
| Reference | 2 | 2 |
| **Total** | **27** | **9** |

## Who is holding what

An item owned jointly counts once against each role, so this column sums to
more than 27.

| Role | Open items | Of those, blocking |
| --- | ---: | ---: |
| Electrical lead | 13 | 3 |
| Hardware lead | 11 | 3 |
| Controls lead | 4 | 0 |
| BOM owner | 2 | 0 |
| Safety sign-off | 2 | 1 |
| PI | 2 | 2 |
| Whoever stages the CAD export | 1 | 1 |

## What stops a build outright

These are the home page's own blocker rows, read from that page and restated
as work. Everything else in this list makes a build harder; these make it
impossible.

| Blocker | Where it is tracked |
| --- | --- |
| No per-part drawings, print plates or native Fusion archive (part and whole-robot STEP are published) | [CAD downloads](../fabrication/cad-downloads.md) |
| No fastener schedule | [Fasteners](../bom/fasteners-and-hardware.md) |
| No torque values (threadlocker: Loctite 222) | [Assembly](../assembly/index.md) |
| No hardware or documentation licence | [Citation and licence](citation-and-license.md) |
| No human-safety procedure | [Safety](../before-you-start/safety.md) |
| No e-stop, pack fuse or main disconnect | [Power system](../electrical/power-system.md) |
| No hardware/software contract | [Software](../software.md) |

## Before you start

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [safety → Rules](../before-you-start/safety.md#rules) | Lifting points on the robot, sling route and clearance zone — The gantry itself is specified above;; where to attach to the robot is not. | hardware lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | E-stop: none in the bill of materials or power diagram, yet the run scripts assume one; mounting, what it cuts, remote or dead-man switch, restart checks — Scripts: `humanoid_nav_step_test.py`, `humanoid_joint_monkey_hw.py`. | electrical lead | **yes** |
| [safety → Rules](../before-you-start/safety.md#rules) | Physical power-on and power-off order (computer, USB-CAN adapters, motor bus, camera gimbals), with a check at each step, and the software shutdown order before power-off | electrical lead | **yes** |

## Bill of materials

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [actuators → Which model goes in which joint](../bom/actuators.md#which-model-goes-in-which-joint) | 2 RS06: this table needs 4 (ankle_2 and shoulder_2 on both sides), the team BOM line `E6` buys 2 | hardware lead | no |
| [actuators → Motor data](../bom/actuators.md#motor-data) | RS00, RS05, RS06 manual data (voltage range, reduction, encoder, `0x7018` range); firmware version and per-joint limits as run on the reference robot | hardware lead + controls lead | no |
| [cables-and-connectors → Actuator-side connectors](../bom/cables-and-connectors.md#actuator-side-connectors) | Trunk connector (harness pages: XT30(2+2) on every actuator; manuals: XT30 + GH1.25 on RS03/RS04) and CAN wire colours (RS04 manual: blue = CAN_H, brown = CAN_L; team harness, blue/yellow: yellow = CAN_H, blue = CAN_L) | electrical lead | no |
| [electronics → Where each part goes](../bom/electronics.md#where-each-part-goes) | IMU mounting screw: M3 (team log) vs Ø2.10 flange holes on 30 × 31 mm centres (vendor drawing) | hardware lead | no |
| [electronics → Power path](../bom/electronics.md#power-path) | 48 V→12 V conversion (power diagram: one buck converter, computer only, no 5 V rail; this list: three); TVS diode (M1.5KE62CA, from the DigiKey link) and how many of the ten sit at each distribution-block pair | electrical lead | no |
| [electronics → Not in this list](../bom/electronics.md#not-in-this-list) | A parts-list row (MPN, qty, link) for the 10 A fuse and holder and for the battery charger, and a manufacturer part number for the surge protector, the four distribution terminals, the USB hubs and the voltage … | electrical lead | no |
| [index](../bom/index.md) | A unit price for every unpriced team BOM row: all nine bearing and screw lines, every printed part except the ten the sheet prices by weight, and the five machined parts the sheet has no line for — The sheet … | BOM owner | no |
| [printed-parts](../bom/printed-parts.md) | STEP and STL of the shank covers `3DP_legP09_shank_cover_a` / `3DP_legP10_shank_cover_b`: the files published under those names are byte-identical to the shoulder covers `3DP_armP05` / `3DP_armP06` (both pairs … | whoever stages the export | **yes** |

## Fabrication

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [cnc-guide → Known CAD errors](../fabrication/cnc-guide.md#known-cad-errors) | CAD errors: Motor04 shaft and knee need M5 holes, CAD has M4; RS03 shaft bearing retainer above the knee is a design error (enlarged by hand). Whether the released CAD is corrected is unknown | hardware lead | **yes** |
| [printing-guide → Print the parts](../fabrication/printing-guide.md#print-the-parts) | Which parts are FDM or SLS, which are structural, and whether an SLS part can be printed FDM instead | hardware lead | **yes** |

## Assembly

The home page names *no torque values and no threadlocker specification* as
one single release blocker. It is not one item: it is these rows, spread
across every step of every limb, and each carries the flag in its own right.

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [gripper → Set the open and closed positions (step 7)](../assembly/gripper.md#step-7) | The uncalibrated service map reports 90 mm; measure the real gap in step 7 | hardware lead + controls | no |
| [head-and-camera-gimbal → Configure the actuators and record the camera serials (step 1)](../assembly/head-and-camera-gimbal.md#step-1) | The CAD mirrors this, putting `cam_yaw_left` at y = −65 mm — A swap fails silently.; Confirm against the robot before wiring. | hardware lead + controls | no |
| [head-and-camera-gimbal → Mount the camera (step 5)](../assembly/head-and-camera-gimbal.md#step-5) | The bracket CAD names a D435 body; confirm the D436 fits before machining — The STEP names the camera `IntelRealsense_D435_Multibody`; … | hardware lead | no |
| [head-and-camera-gimbal → Route the camera cable (step 6)](../assembly/head-and-camera-gimbal.md#step-6) | Camera cable across the yaw and pitch axes — Real yaw travel; how the USB-C cable crosses yaw (slip ring, helix or stop).; Cable type, length, bend radius, service loop, retention. … | hardware lead + electrical | no |

## Electrical

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [harness-fabrication → Identify the connector pinouts](../electrical/harness-fabrication.md#identify-the-connector-pinouts) | Pinouts for RS00, RS05, RS06 and gripper servo; colour and gauge per pin; mating parts; pin-1 orientation | electrical lead | no |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | Pack retention in the torso rear bay and lead protection at its exit; balance-lead protection, pack monitoring and shutdown voltage; charger model, charge rate, balance-charging procedure and charging location | hardware lead (retention) + electrical lead + safety officer | no |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | TVS diodes fitted at each location (BOM: 10) | electrical lead | no |
| [power-system → Wire the 48 V bus](../electrical/power-system.md#wire-the-48-v-bus) | Surge protector, 4 distribution blocks, 10 A fuse, EC5 connectors, charger: diagram or team log only, not the BOM; no confirmed part numbers | BOM owner + electrical lead | no |
| [power-system → Feed the 12 V rail](../electrical/power-system.md#feed-the-12-v-rail) | Gripper-servo 12 V supply (source, fuse, wiring), USB hub power and power budget | electrical lead | no |
| [power-system → Protection, disconnect and e-stop](../electrical/power-system.md#protection-disconnect-and-e-stop) | Pack-path fuse (none drawn); surge protector part number and rating | electrical lead + safety officer | **yes** |

## Bring-up

Bring-up cannot start until Electrical closes the pack-configuration item.
Series versus parallel decides the bus voltage, and every current, converter
and check below is written against a voltage nobody has confirmed.

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [first-power-on → Power the computer only (step 1)](../bringup/first-power-on.md#step-1) | How to power the computer alone: the power diagram feeds it from the arm motors' distribution block, no disconnect drawn — Do not improvise. | electrical lead | no |
| [motor-id-and-config → Set an ID](../bringup/motor-id-and-config.md#set-an-id) | Whether an ID can only be set with the motor alone on the bus, and what firmware baseline the team ran — The procedure above is the vendor tool's. | controls lead | no |

## Reference

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [citation-and-license → Licence](citation-and-license.md#licence) | Hardware licence (e.g. CERN-OHL-S or -W) and documentation licence (e.g. CC-BY-4.0), with the licence file beside the CAD and on the download page; note V1 was MIT | PI + the university's licensing office | **yes** |
| [citation-and-license → Third-party material](citation-and-license.md#third-party-material) | Licence file for the two Unitree G1 URDFs | PI | **yes** |

## Items that are not TODO blocks

These gaps are structural rather than a missing fact, so they have no block
on a page to generate a row from. Their presence here is checked against
`docs/data/` on every run, so a row leaves this table when the file lands.

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

