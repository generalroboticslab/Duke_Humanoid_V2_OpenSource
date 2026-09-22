# Open items — the punch list

Every unresolved item on this site, in one table: **10 open items** across **6 pages**, of which **1 block the public release**.

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
| Assembly | 2 | 0 |
| Electrical | 6 | 1 |
| Bring-up | 2 | 0 |
| **Total** | **10** | **1** |

## Who is holding what

An item owned jointly counts once against each role, so this column sums to
more than 10.

| Role | Open items | Of those, blocking |
| --- | ---: | ---: |
| Electrical lead | 7 | 1 |
| Hardware lead | 3 | 0 |
| Safety sign-off | 2 | 1 |
| Controls lead | 2 | 0 |
| BOM owner | 1 | 0 |

## What the release still owes

These are the home page's own blocker rows, read from that page and restated
as work. Everything else in this list makes a build harder; these are the
ones somebody has to close before this counts as a finished release.

| Blocker | Where it is tracked |
| --- | --- |

## Assembly

The home page names *no torque values and no threadlocker specification* as
one single release blocker. It is not one item: it is these rows, spread
across every step of every limb, and each carries the flag in its own right.

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [gripper → Set the open and closed positions (step 7)](../assembly/index.md#step-gripper-7) | The uncalibrated service map reports 90 mm; measure the real gap in step 7 | hardware lead + controls | no |
| [head-and-camera-gimbal → Route the camera cable (step 7)](../assembly/index.md#step-head-and-camera-gimbal-7) | How the camera cable crosses the yaw axis (travel, service loop, retention). | hardware lead | no |

## Electrical

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [harness-fabrication → Identify the connector pinouts](../electrical/index.md#identify-the-connector-pinouts) | Pinouts for RS00, RS05, RS06 and gripper servo; colour and gauge per pin; mating parts; pin-1 orientation | electrical lead | no |
| [power-system → Wire the 48 V bus](../electrical/index.md#wire-the-48-v-bus) | Pack retention in the torso rear bay and lead protection at its exit; balance-lead protection, pack monitoring and shutdown voltage; charge rate, balance-charging procedure and charging location | hardware lead (retention) + electrical lead + safety officer | no |
| [power-system → Wire the 48 V bus](../electrical/index.md#wire-the-48-v-bus) | TVS diodes fitted at each location (BOM: 10) | electrical lead | no |
| [power-system → Wire the 48 V bus](../electrical/index.md#wire-the-48-v-bus) | Surge protector, 4 distribution blocks, 10 A fuse, EC5 connectors: diagram or team log only, not the BOM; no confirmed part numbers | BOM owner + electrical lead | no |
| [power-system → Feed the 12 V rail](../electrical/index.md#feed-the-12-v-rail) | Gripper-servo 12 V supply (source, fuse, wiring), USB hub power and power budget | electrical lead | no |
| [power-system → Protection and disconnect](../electrical/index.md#protection-and-disconnect) | Pack-path fuse (none drawn); surge protector part number and rating | electrical lead + safety officer | **yes** |

## Bring-up

Bring-up cannot start until Electrical closes the pack-configuration item.
Series versus parallel decides the bus voltage, and every current, converter
and check below is written against a voltage nobody has confirmed.

| Page | What is missing | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| [first-power-on → Power the computer only (step 1)](../bringup/index.md#step-first-power-on-1) | How to power the computer alone: the power diagram feeds it from the arm motors' distribution block, no disconnect drawn — Do not improvise. | electrical lead | no |
| [motor-id-and-config → Set an ID](../bringup/index.md#set-an-id) | Whether an ID can only be set with the motor alone on the bus, and what firmware baseline the team ran — The procedure above is the vendor tool's. | controls lead | no |

## Items that are not TODO blocks

These gaps are structural rather than a missing fact, so they have no block
on a page to generate a row from. Their presence here is checked against
`docs/data/` on every run, so a row leaves this table when the file lands.

| Gap | What it means | Who can supply it | Blocks release |
| --- | --- | --- | :-: |
| `print_profiles.csv` does not exist | The per-part profile table on [Printing guide](../fabrication/index.md#printing-guide) is gated on the file and does not render. Material and process per part are published without it, on [Printed parts](../bom/index.md#printed-parts) | hardware lead | no |

## Images

Missing figures are not in this table. They are tracked separately, with the
exact path and a one-line brief for each, in the
[image manifest](IMAGES_NEEDED.md) — the list to hand to whoever renders
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

