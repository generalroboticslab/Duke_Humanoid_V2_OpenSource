import os
from pathlib import Path

# Repo-relative so this runs on any checkout. BOM_SOURCE_DIR points at the
# directory holding the two source spreadsheets exported as CSV; it defaults to
# ../../reference/bom next to this repository.
_TOOLS = Path(__file__).resolve().parent
SITE = _TOOLS.parent
SOURCE_DIR = Path(os.environ.get(
    "BOM_SOURCE_DIR", SITE.parent / "reference" / "bom"))
DATA = SITE / "docs" / "data"

import csv, re
from decimal import Decimal

src = str(SOURCE_DIR / "duke-humanoid-v2_BOM_sheet2_cnc-parts.csv")
rows = []
with open(src, newline="", encoding="utf-8-sig") as fh:
    for r in csv.reader(fh):
        if not r or r[0].startswith("#") or r[0] in ("PART", "TOTAL CNC") or not r[0].strip():
            continue
        rows.append(r)
print("data rows:", len(rows))

def money(s):
    return Decimal(s.replace("$", "").replace(",", "").strip())

vals = [money(r[1]) for r in rows]
print("sum all 63      :", sum(vals))
blocks = [(1,15),(17,26),(28,37),(39,63)]
tot = Decimal(0)
for a,b in blocks:
    s = sum(vals[a-1:b])
    print(f"rows {a}-{b}: {s}")
    tot += s
print("sum of 4 blocks :", tot)
skipped = [16,27,38]
print("skipped rows:", [(rows[i-1][0], vals[i-1]) for i in skipped])
print("gap:", sum(vals[i-1] for i in skipped))
b6 = [v for r,v in zip(rows,vals) if r[0]=="B6_single_leg_tester_plate"][0]
print("all63 minus B6  :", sum(vals)-b6)

# qty conflicts
conf = 0
for r, v in zip(rows, vals):
    name = r[0]
    q = r[2].strip().replace("pcs","")
    m = re.search(r"_x(\d+)", name)
    embedded = int(m.group(1)) if m else None
    qty = int(q) if q else None
    if embedded is not None and qty is not None and embedded != qty:
        conf += 1
print("qty conflicts:", conf)
