# Printed parts

Fused-deposition (FDM) and laser-sintered (SLS) parts; `printed-parts.csv` lists three materials, not parts.

| Part ID | Description | Material | Process | Qty | Unit cost | Vendor | Files |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
{% for r in pd_read_csv("data/printed-parts.csv", dtype="str", keep_default_na=False).to_dict("records") %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.material or "**TODO**{ .dh-missing }" }} | {{ r.process or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ r.vendor or "**TODO**{ .dh-missing }" }} | {{ cad_links(r.part_id) }} |
{% endfor %}

!!! missing "MISSING — SAFETY — list of printed parts: one row per part with a CAD-matching ID, FDM or SLS, material grade, structural or not, cost and vendor"
    *Owner: hardware lead.*

## Likely printed parts

Not confirmed against CAD **UNVERIFIED**{ .dh-unverified }:

- **Rendered black in team CAD animations, no row in `cnc-parts.csv`:**
  upper-arm and forearm shells and a square block in the arm; camera-gimbal
  pedestal, neck and two L-shaped arms; torso central spine; front and back
  cover frames and panels.
- **Seen in team build photos:** battery holders with heat-set inserts, an
  X-shaped IMU (inertial measurement unit) bracket, T-brackets holding the
  computer ([Torso and waist](../assembly/torso-and-waist.md)).

Print settings: [Printing guide](../fabrication/printing-guide.md).
