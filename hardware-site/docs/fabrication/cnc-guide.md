# CNC guide

Have the machined parts made and check a first article.

!!! abstract "At a glance"
    - **You will:** order the parts and measure a first article.
    - **Parts:** [CNC parts](../bom/cnc-parts.md).
    - **Before this:** [CAD downloads](cad-downloads.md).

## Material and design rules

| Item | Value |
| --- | --- |
| Material | Aluminium, 6061 or 7075 (repo comments suggest hard-anodized 6061) |
| General tolerance | 0.03 mm on radius and length, 0.06 mm on diameter; ± or total band not stated **UNVERIFIED**{ .dh-unverified } |
| Walls | ≥ 1 mm; structural walls ≥ 4 mm |
| Blind holes | End in a standard cone |
| Tapped holes | ≥ 4 mm usable thread, 6 mm preferred |
| Edges | No sharp internal corners; chamfers, not fillets |

*Source: team design log, "Material Choice" and CNC checklist.*

!!! missing "MISSING — SAFETY — per part: alloy and temper, tolerances on bearing seats, journals, dowel holes and mating faces, finish per face, thread specs, turned or 5-axis"
    *Owner: hardware lead, from the CAD and the machining quotations.*

!!! unverified "UNVERIFIED — aluminium grade: 6061 or 7075"
    *Owner: hardware lead.*

## Known CAD errors

<figure markdown>
  ![CAD render of an actuator and its output shaft part](../assets/photos/tolerance-cad-m4-vs-m5.webp){ loading=lazy }
  <figcaption>"Motor04 Shaft NEEDS m5 holes, but the cad has m4 holes. Same in the knee motor."</figcaption>
</figure>

The reference build's first article found both (below); check the CAD before
ordering.

!!! unverified "UNVERIFIED — CAD errors: Motor04 shaft and knee need M5 holes, CAD has M4; RS03 shaft bearing retainer above the knee is a design error (enlarged by hand). Whether the released CAD is corrected is unknown"
    *Owner: hardware lead. Blocks `hw-1.0.0`.*

## Fit-critical parts

Shafts, couplers, bearing housings, retainers; measure these reviewed
interfaces first:

| Part | Interface |
| --- | --- |
| `CNC_leg02` RS03 shaft coupler | Some diameters at 0.03 mm instead of 0.06 mm |
| `CNC_leg03` RS03 shaft bearing retainer | Mating feature with the motor |
| `CNC_leg08` knee front bearing retainer | Faces meeting the motor and RS03 shaft; bearing outer diameter |
| `CNC_leg09` knee back | Interface with the RS03 shaft |
| `CNC_leg10` knee output shank | Circular pattern on the RS04 side (missing at review) |
| `CNC_leg11` knee support shank | Top/bottom symmetry |
| `CNC_leg13`, `CNC_leg14` ankle pitch front and back | Clearance fit to the RS06; screw-hole size |

## Order the parts

1. **Freeze the revision:** make every part from one release tag.
2. **Send one archive:** STEP per part, PDF drawings (unpublished:
   [CAD downloads](cad-downloads.md)), a parts table (ID,
   quantity, material, finish) and a cover sheet (general tolerance, default
   finish, deadline, contact).

    !!! missing "MISSING — reference-build machine shop, what it was sent, quote, lead time, setup cost (material was priced with JLCPCB CNC)"
        *Owner: hardware lead.*

3. **Ask for a first article:** one piece of each fit-critical part before the
   batch runs. Measure it yourself.
4. **Get the measurement report:** measured values on toleranced features, for
   [incoming inspection](incoming-inspection.md).
5. **Order spares on the same setup.**

    !!! missing "MISSING — which machined parts need spares, and how many"
        *Owner: hardware lead.*

✅ **Check:** each fit-critical first article is measured against the drawing
before the full batch is released.

!!! missing "MISSING — decision on registering the machined parts with one service and publishing its part numbers"
    *Owner: hardware lead.*
