# Part index

!!! missing "MISSING — Part index (part ID → description, qty, subassembly, assembly steps), blocked until one of the three machined-part naming schemes is chosen"
    Schemes in use: `CNC_leg01`, `01_m03_shaft`, `B1_body_base_plate`. See [CNC parts](../bom/cnc-parts.md).
    *Owner: hardware lead for the numbering, then whoever writes the generator.*

Team labels read *kind_regionNN_xCount* (+ `L`/`R`); kind is `CNC`, `ELEC`,
`MTR`, `HWR` (hardware) or `DIY` (printed). Example: `CNC_leg02_x7`,
RS03_shaft_coupler.

!!! unverified "UNVERIFIED — CNC IDs arm05–arm10 and four quantities differ between the team's 32-part list and this site's list"
    | ID | Team list | This site |
    | --- | --- | --- |
    | arm05 | RS02_back_cover ×4 | RS02_shaft_bearing ×4 |
    | arm06 | RS02_shaft_bearing_retainer ×4 | RS02_shaft_coupler ×4 |
    | arm07 | RS02_shaft_coupler ×4 | elbow_front_bearing ×2 |
    | arm08 | elbow_front_bearing_retainer ×2 | elbow_back_bearing ×2 |
    | arm09 | elbow_back_bearing_retainer ×2 | elbow_output_shaft ×2 |
    | arm10 | elbow_output_shaft ×2 | r03_back_cover ×4 |
    | leg02, leg12 | ×7, ×4 | ×8, ×5 |

    Site-only: arm11 wrist_roll, arm12 wrist_pitch, arm13 RS05_shaft_coupler.
    Confirm each row against the CAD before ordering.
    *Owner: hardware lead. See [CNC parts](../bom/cnc-parts.md).*
