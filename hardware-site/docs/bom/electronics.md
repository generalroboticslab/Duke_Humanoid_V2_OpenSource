# Electronics

Computer, battery, power conversion, Controller Area Network (CAN) and sensing:
{{ bom_subtotal("electronics.csv") }} across {{ bom_count("electronics.csv") }}
lines (MPN: manufacturer part number).

| Team ref | Part ID | Description | MPN | Qty | Unit cost | Line total | Vendor |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
{% for r in pd_read_csv("data/electronics.csv", dtype="str", keep_default_na=False).to_dict("records") %}| {{ team_ref_cell(r) }} | `{{ r.part_id }}` | {{ r.description }} | {{ r.mpn or "**TODO**{ .dh-missing }" }} | {{ r.qty_per_robot or "**TODO**{ .dh-missing }" }} | {{ money_cell(r.unit_cost_usd) }} | {{ line_total_cell(r) }} | [{{ r.vendor }}]({{ r.vendor_url }}) |
{% endfor %}| | | | | | **Total** | **{{ bom_subtotal("electronics.csv") }}** | |
