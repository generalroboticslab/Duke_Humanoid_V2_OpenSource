# Sourcing

Order these first:

| Item | Why |
| --- | --- |
| {{ bom_count("cnc-parts.csv") }} machined parts, {{ bom_subtotal("cnc-parts.csv") }} | Large custom order; lead time not quoted |
| Intel RealSense D436 ×2 | Supply risk: the RealSense line has had availability gaps |
| RobStride actuators, {{ bom_qty("actuators.csv") }} units, {{ bom_subtotal("actuators.csv") }} | Supply risk |

!!! missing "MISSING — quoted lead times, with the quote date, for machining, the D436 and the RobStride actuators"
    *Owner: hardware lead.*

## Supply-risk parts

{% set risky = pd_read_csv("data/actuators.csv", dtype="str", keep_default_na=False).to_dict("records") + pd_read_csv("data/electronics.csv", dtype="str", keep_default_na=False).to_dict("records") %}
| Part ID | Description | Qty | Alternate | Vendor |
| --- | --- | ---: | --- | --- |
{% for r in risky if "SUPPLY RISK" in r.notes %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot }} | {{ r.alt_mpn or "**TODO**{ .dh-missing } none published" }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}

No substitute is drop-in. Another actuator changes the mounting interface, the
shaft and the Controller Area Network (CAN) configuration. Another camera changes
the gimbal mount, the perception bridge and the 90° × 65° RGB field of view the
design assumes.

!!! missing "MISSING — an alternate for the D436 and for each RobStride model, or what a substitution requires"
    *Owner: hardware lead + perception lead.*

## Vendors

{% set bought = pd_read_csv("data/actuators.csv", dtype="str", keep_default_na=False).to_dict("records") + pd_read_csv("data/electronics.csv", dtype="str", keep_default_na=False).to_dict("records") + pd_read_csv("data/cables-connectors.csv", dtype="str", keep_default_na=False).to_dict("records") %}
| Vendor | Lines | Part IDs |
| --- | ---: | --- |
{% for vendor, items in bought | selectattr("vendor") | groupby("vendor") %}| {{ vendor }} | {{ items | length }} | {{ items | map(attribute="part_id") | join(", ") }} |
{% endfor %}

Machining vendor: [CNC guide](../fabrication/cnc-guide.md#order-the-parts).

!!! missing "MISSING — manufacturer part numbers for the marketplace lines"
    *Owner: hardware lead.*

## Price dates

Every price on this site is the team BOM's, dated
{{ bom_priced_as_of("actuators.csv") }}.

!!! missing "MISSING — a re-check of each price against its vendor, with the date it was checked"
    *Owner: whoever re-sources the parts.*
