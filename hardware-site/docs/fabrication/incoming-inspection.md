# Incoming inspection

Log every part on arrival: `part_id`, release tag, quantity received, vendor and batch, measured values, pass / rework / reject. Quarantine a failed part; never fit it.

## Count and record

Count every box against the BOM and log the quantity received. Store by subassembly: leg, arm, body, head, gripper.

## Measure machined parts

Deburr, then measure every bearing bore, shaft journal, dowel hole and mating face against the STEP and the [general tolerance](#material-and-design-rules) — [fit-critical parts](#fit-critical-parts) first, every piece, not a sample. Run a real screw to full depth in every tapped hole. A press fit is not reversible: record every bore and journal before any bearing is pressed.

## Check printed parts

Flat where the part bolts down; holes reamed to size; heat-set inserts flush and square; no delamination on structural parts.

## Check actuators

Do not open an actuator, and do not change its torque limit or protection temperature.

1. Model matches the joint ([Actuators](../bom/index.md#actuators)).
2. Turns freely by hand through a full turn, unpowered.
3. No damage to connectors, output flange or housing.
4. Read the CAN ID and firmware on the bench, one unit at a time; RS03 and RS04 ship at ID 127. Vendor tool: [robstride.com/download](https://www.robstride.com/download) — needs the vendor's USB-CAN module (CH340), not a CANable **UNVERIFIED**{ .dh-unverified }.

## Check electronics

Confirm variants; look for bent pins and cracked connectors. Check each pack for swelling and damaged leads, and log its voltage and cell balance. Power nothing before [Pre-power checks](../electrical/index.md#pre-power-checks).

✅ **Check:** every BOM part is present, inspected and recorded before assembly begins.
