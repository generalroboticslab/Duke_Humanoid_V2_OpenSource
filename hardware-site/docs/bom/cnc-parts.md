# CNC parts

{{ bom_count("cnc-parts.csv") }} machined part rows, {{ bom_subtotal("cnc-parts.csv") }};
**Qty** is the lot each price was quoted for, not a count checked against CAD
**UNVERIFIED**{ .dh-unverified }.

## Leg

{{ bom_count("cnc-parts.csv", subassembly="leg") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}.

| Part ID | Description | Qty | Unit cost | Line total | Flags | Files |
| --- | --- | ---: | ---: | ---: | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "leg" %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }}{{ " **UNVERIFIED**{ .dh-unverified }" if ("QUANTITY CONFLICT" in r.notes or "DEDUPED" in r.notes) else "" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ money(r.total_cost_usd|float) }} | {{ (("qty conflict; " if "QUANTITY CONFLICT" in r.notes else "") ~ ("not in team list; " if ("Legacy numbering" in r.notes or "B-series" in r.notes) else "") ~ ("no unit cost; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Leg subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="leg") }}** | | |

## Arm

{{ bom_count("cnc-parts.csv", subassembly="arm") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}.

| Part ID | Description | Qty | Unit cost | Line total | Flags | Files |
| --- | --- | ---: | ---: | ---: | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "arm" %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }}{{ " **UNVERIFIED**{ .dh-unverified }" if ("QUANTITY CONFLICT" in r.notes or "DEDUPED" in r.notes) else "" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ money(r.total_cost_usd|float) }} | {{ (("qty conflict; " if "QUANTITY CONFLICT" in r.notes else "") ~ ("not in team list; " if ("Legacy numbering" in r.notes or "B-series" in r.notes) else "") ~ ("no unit cost; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Arm subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="arm") }}** | | |

## Body

{{ bom_count("cnc-parts.csv", subassembly="body") }} rows,
{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}.

| Part ID | Description | Qty | Unit cost | Line total | Flags | Files |
| --- | --- | ---: | ---: | ---: | --- | --- |
{% for r in pd_read_csv("data/cnc-parts.csv", dtype="str", keep_default_na=False).to_dict("records") if r.subassembly == "body" %}| `{{ r.part_id }}` | {{ r.description }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }}{{ " **UNVERIFIED**{ .dh-unverified }" if ("QUANTITY CONFLICT" in r.notes or "DEDUPED" in r.notes) else "" }} | {{ money(r.unit_cost_usd|float) if r.unit_cost_usd else "**TODO**{ .dh-missing }" }} | {{ money(r.total_cost_usd|float) }} | {{ (("qty conflict; " if "QUANTITY CONFLICT" in r.notes else "") ~ ("not in team list; " if ("Legacy numbering" in r.notes or "B-series" in r.notes) else "") ~ ("no unit cost; " if not r.unit_cost_usd else "")).rstrip("; ") or "—" }} | {{ cad_links(r.part_id) }} |
{% endfor %}| | **Body subtotal** | | | **{{ bom_subtotal("cnc-parts.csv", subassembly="body") }}** | | |

## Summary

**Machined total: {{ bom_subtotal("cnc-parts.csv") }}.** Raw data, every column:
[cnc-parts.csv](../data/cnc-parts.csv). Make them with the
[CNC guide](../fabrication/cnc-guide.md); check them with
[Incoming inspection](../fabrication/incoming-inspection.md).

!!! missing "MISSING — per-robot quantity of every row checked against CAD, and one part-ID scheme matching the CAD filenames"
    *Owner: hardware lead, from the CAD.*

**Flags:**

- *qty conflict*: the source part name gives a different count.
- *not in team list*: absent from the team's 32-part CNC list; may duplicate a current part.
- *no unit cost*: the lot price does not divide evenly.

!!! unverified "UNVERIFIED — this list vs the team's 32-part CNC list: arm05–arm10 name the same parts shifted by one ID; counts (team vs this list) leg02 7 vs 8, leg12 4 vs 5, arm07 4 vs 2, arm10 2 vs 4; arm11–arm13 and the *not in team list* rows are absent from it"
    *Owner: hardware lead, from the CAD.*
