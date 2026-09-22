# CNC guide

Order the machined parts from the STEP files. There are no per-part drawings.

## Material and design rules

| Item | Value |
| --- | --- |
| Material | Aluminium 6061 (the Fusion material on every `CNC_` part) |
| General tolerance | 0.03 mm on radius and length, 0.06 mm on diameter; ± or total band not stated **UNVERIFIED**{ .dh-unverified } |
| Walls | ≥ 1 mm; structural walls ≥ 4 mm |
| Blind holes | End in a standard cone |
| Tapped holes | ≥ 4 mm usable thread, 6 mm preferred |
| Edges | No sharp internal corners; chamfers, not fillets |

## Fit-critical parts

Measure these interfaces first:

| Part | Interface |
| --- | --- |
| `CNC_leg02` RS03 shaft coupler | Some diameters at 0.03 mm instead of 0.06 mm |
| `CNC_leg03` RS03 shaft bearing retainer | Mating feature with the motor |
| `CNC_leg08` knee front bearing retainer | Faces meeting the motor and RS03 shaft; bearing outer diameter |
| `CNC_leg09` knee back | Interface with the RS03 shaft |
| `CNC_leg10` knee output shank | Circular pattern on the RS04 side |
| `CNC_leg11` knee support shank | Top/bottom symmetry |
| `CNC_leg13`, `CNC_leg14` ankle pitch front and back | Clearance fit to the RS06; screw-hole size |

## Order the parts

1. Make every part from one release tag.
2. Send the shop one archive: a STEP per part, a parts table (ID, quantity, material, finish) and a cover sheet with the general tolerance and the deadline.
3. Ask for a first article of each fit-critical part before the batch, and measure it yourself.
4. Ask for the measurement report on toleranced features.
5. Order spares of the fit-critical parts on the same setup.

✅ **Check:** each fit-critical first article measures within tolerance before the batch is released.
