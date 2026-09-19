# Harness fabrication

Build, label and bench-test every cable before installing it.

!!! abstract "At a glance"
    - **Parts:** connectors, loom and USB cables: [Cables and connectors](../bom/cables-and-connectors.md).
    - **Tools:** soldering iron, vise, meter.

The harness is the known weak point: a 0.3–0.4 s CAN (Controller Area Network)
dropout on two arm joints caused a collision on the reference robot.

## Plan every cable

!!! missing "MISSING — SAFETY — Not in the parts list: bulk wire, heat-shrink, GH1.25 CAN mates for RS03/RS04, Ethernet cable for CAN leads, CAN terminators"
    *Owner: electrical lead. Blocks sourcing.*

One row per cable, plus one per motor drop once the daisy-chain order exists
(six per arm or leg bus, four on `can25`, three on `can22`).

| From | To | Gauge | Connectors (A / B) | Length |
| --- | --- | --- | --- | --- |
| Adapter `can9` | Left arm trunk | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Adapter `can21` | Right arm trunk | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Adapter `can22` | Waist / `shoulder_1` trunk | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Adapter `can23` | Right leg trunk | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Adapter `can24` | Left leg trunk | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Adapter `can25` | Camera gimbal trunk | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Pack + | Pack − (series link) | **TODO**{ .dh-missing } | EC5 **UNVERIFIED**{ .dh-unverified } | **TODO**{ .dh-missing } |
| Pack + | Surge protector | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Surge protector | Upper-body power block (48V riser) | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| 48V bus | Lower-body power block | 12 AWG | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Pack − | Upper- and lower-body ground blocks | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| Upper-body power block | 10 A fuse, 48V-to-12V buck | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| 48V-to-12V buck | Onboard computer | 16 AWG | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| 12 V supply (not drawn) | Left gripper servo | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |
| 12 V supply | Right gripper servo | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |

*Gauges: power wiring diagram.*

!!! missing "MISSING — Harness schedule: cable ID, conductor count, connector parts, length with service loop, sleeve size, one row per motor drop; gauge, insulation temperature rating and strand count for every unlabelled run"
    *Owner: electrical lead, measured on a real build. Blocks routing and assembly.*

**Never** run solid or coarse-stranded wire across a joint: it breaks inside the
insulation, causing intermittent dropouts.

## Identify the connector pinouts

Red = positive, black = ground. **Never mate or unmate an XT30 under power.**

| Model | Power | CAN |
| --- | --- | --- |
| RS02 | One XT30(2+2) shell (board XT30PB(2+2)-M.G.B, cable XT30(2+2)-F.G.B): pin 1 +, pin 2 −, pin 3 CAN_L, pin 4 CAN_H | Same shell |
| RS03, RS04 | XT30 (board XT30APW-M, cable XT30UW-F); RS04 leads red +, black − | GH1.25 2-pin (board GH1.25-2PWT, cable GH1.25-T); RS04 leads blue CAN_H, brown CAN_L |
| RS00, RS05, RS06 | **TODO**{ .dh-missing } | **TODO**{ .dh-missing } |

*Source: RobStride manuals.* An RS03 board has two XT30 and two CAN sockets (in,
out). XT30(2+2): 15 A with 18 AWG.

!!! unverified "UNVERIFIED — Actuator connector: XT30(2+2) at RS02 vs XT30 + GH1.25 at RS03/RS04 (manuals); trunk connector unknown. CAN colours: blue/brown (RS04 manual) vs blue/yellow (team photos)"
    *Owner: electrical lead.*

!!! missing "MISSING — Pinouts for RS00, RS05, RS06 and gripper servo; colour and gauge per pin; mating parts; pin-1 orientation"
    *Owner: electrical lead.*

## Solder the XT30 power leads

Do not crimp the XT30 cups.

1. Identify +. Heat-shrink on first. Connector in a vise.
2. Iron about **480 °C**. Tin the wire fully, then the cup until solder wets the
   gold.
3. Reheat the cup, insert the wire, hold still until solid.
4. Check the joint: shiny, no overflow blocking mating, wire exits straight.
5. Shrink over joint and gap. Tug test: nothing moves.

✅ **Check:** continuity, **polarity again**, mates cleanly, no exposed conductor.

## Solder the CAN pairs

1. Power off. Identify CAN_H and CAN_L. Heat-shrink on first.
2. Strip minimally; twist to within 10–15 mm of the joint.
3. Pre-tin, align inline (no stubs), solder quickly; H and L equal length.
4. Shrink, restore the twist.

✅ **Check:** H and L continuous; no H–L short, no short to ground.

### Make a CAN lead from Ethernet cable

1. Strip 2.5 cm of jacket, 8 mm per conductor.
2. Twist the coloured conductors to CAN High (yellow lead), the white ones to CAN
   Low (blue lead).
3. Sleeve with 3/32 in heat-shrink, then 1/4 in over the cable.

!!! unverified "UNVERIFIED — Which runs use the Ethernet CAN lead, and which connector it mates"
    *Owner: electrical lead.*

## Build and test each cable

1. Cut to schedule length (service loop included).
2. Solder, load the shells, check continuity **before** sleeving.
3. Label both ends.

    !!! missing "MISSING — Cable labelling scheme: ID format, label stock, position"
        *Owner: electrical lead.*

4. Bench-test:

    | Test | Pass |
    | --- | --- |
    | Pin-to-pin continuity, both directions | Intended pairs conduct; no others |
    | Insulation between power conductors | **TODO**{ .dh-missing } |
    | Insulation, conductor to sleeve/shield | **TODO**{ .dh-missing } |
    | Flex at each strain relief, meter on | No flicker |

!!! missing "MISSING — Pass criteria for the two insulation tests; pull-out force for a soldered joint; tool, die and strip length for any crimped contact"
    *Owner: electrical lead.*

✅ **Check:** every scheduled cable is built, labelled at both ends, and passes
continuity and the flex test before installation.

## Thread cables before closing limbs

!!! missing "MISSING — Which cables must be threaded before each limb is closed, per assembly step"
    *Owner: electrical lead + assembly lead. Blocks leg, arm, torso and head assembly.*
