# Printed parts

Fused-deposition (FDM) and laser-sintered (SLS) parts, one row per Fusion component, with the three
filament/powder rows from the team sheet at the end. Print settings: [Printing guide](../fabrication/printing-guide.md).

| Part ID | Description | Material | Process | Qty | Unit cost | Vendor | Files |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
{% for r in pd_read_csv("data/printed-parts.csv", dtype="str", keep_default_na=False).to_dict("records") %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.material or "**TODO**{ .dh-missing }" }} | {{ r.process or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ r.vendor or "**TODO**{ .dh-missing }" }} | {{ cad_links(r.part_id) }} |
{% endfor %}

!!! missing "MISSING — SAFETY — for every printed part: filament or powder grade (the covers only carry a Fusion material name such as `hip3_protection`), structural or cosmetic, print orientation and infill, cost and vendor"
    *Owner: hardware lead.*

!!! unverified "UNVERIFIED — quantities are Fusion occurrence counts, and left and right copies of a cover share one component name, so one STL may serve both sides or one side may need a mirrored print"
    *Owner: hardware lead, from the CAD.*

## Not in this list

Seen in team build photos but carrying no print material in Fusion **UNVERIFIED**{ .dh-unverified }:
the camera-gimbal pedestal, neck and L-shaped arms; the torso central spine; battery holders with
heat-set inserts; the X-shaped IMU (inertial measurement unit) bracket; the T-brackets holding the
computer ([Torso and waist](../assembly/torso-and-waist.md)).
