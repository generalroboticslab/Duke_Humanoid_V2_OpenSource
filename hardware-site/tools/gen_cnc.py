"""Generate docs/data/cnc-parts.csv + test-fixtures.csv from BOM Sheet2.

Transformations, each of them recorded on bom/index.md:
  * Sheet2's column named UNIT COST is a LINE TOTAL (proved: the 63 rows sum to
    6840.62, which is TOTAL CNC 6389.86 + the 450.76 of rows 16/27/38). It is
    written to total_cost_usd, and a TRUE unit_cost_usd is derived by dividing
    by the quoted lot quantity -- only when the division is exact to the cent.
  * part_id loses its embedded _xN (contract rule 3); the source string is kept
    verbatim in notes so every row stays traceable.
  * The two CNC_leg02 rows collapse to one row carrying both lots.
  * B6_single_leg_tester_plate moves to test-fixtures.csv, out of every total.
"""
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

import csv, os, re
from decimal import Decimal, ROUND_HALF_UP

SRC = str(SOURCE_DIR / "duke-humanoid-v2_BOM_sheet2_cnc-parts.csv")
OUT = str(DATA)

COLS = ["subassembly","class","part_id","description","mpn","vendor","vendor_url",
        "alt_mpn","alt_url","qty_per_robot","unit_cost_usd","total_cost_usd",
        "material","process","tolerance_finish","lead_time_days","priced_as_of","notes"]

LEGACY_NOTE = ("Legacy numbering from the single-leg test rig; not yet reconciled with the "
               "CNC_* scheme. May be an older name for a current part, or a part that is no "
               "longer used. Needs a CAD cross-check before ordering.")
B_NOTE = ("B-series numbering, origin unresolved; B4 is absent from the source sheet. "
          "Needs a CAD cross-check before ordering.")

def money(s):
    return Decimal(s.replace("$","").replace(",","").strip())

def read_rows():
    rows = []
    with open(SRC, newline="", encoding="utf-8-sig") as fh:
        for r in csv.reader(fh):
            if not r or not r[0].strip() or r[0].startswith("#") or r[0] in ("PART","TOTAL CNC"):
                continue
            rows.append((r[0].strip(), money(r[1]), r[2].strip()))
    return rows

def subassembly_of(name):
    if name.startswith("CNC_leg"): return "leg", ""
    if name.startswith("CNC_arm"): return "arm", ""
    if name.startswith("CNC_body"): return "body", ""
    if re.match(r"^\d\d_", name):
        return "leg", LEGACY_NOTE + (" Subassembly read from the 01-22 leg series this row sits in."
                                     if "hip" not in name and "knee" not in name
                                     and "ankle" not in name and "foot" not in name else "")
    if re.match(r"^B\d", name): return "body", B_NOTE
    raise SystemExit("unclassified: " + name)

def describe(part_id):
    """Human-readable name: the part_id with separators turned into spaces.
    No new information is introduced -- this is the source string, re-spaced."""
    s = re.sub(r"^CNC_(leg|arm|body)\d+_", "", part_id)
    s = re.sub(r"^\d\d_", "", s)
    s = re.sub(r"^B\d_", "", s)
    return s.replace("_", " ").strip()

rows = read_rows()
assert len(rows) == 63

merged = {}
order = []
for name, total, qty_raw in rows:
    qty = int(qty_raw.replace("pcs","").strip()) if qty_raw.replace("pcs","").strip() else None
    m = re.search(r"_x(\d+)", name)
    embedded = int(m.group(1)) if m else None
    pid = re.sub(r"_x\d+", "", name)
    if pid not in merged:
        merged[pid] = {"lots": [], "src": [], "embedded": embedded}
        order.append(pid)
    merged[pid]["lots"].append((qty, total))
    merged[pid]["src"].append((name, qty_raw, total))

parts, fixtures = [], []
for pid in order:
    rec = merged[pid]
    src_names = {n for n, _, _ in rec["src"]}
    total = sum(t for _, t in rec["lots"])
    qty = sum(q for q, _ in rec["lots"] if q is not None)
    sub, extra = subassembly_of(pid)

    notes = []
    if len(rec["lots"]) > 1:
        lots = "; ".join(f"{q} pcs at {t}" for q, t in rec["lots"])
        notes.append(
            f"DEDUPED: the source sheet carries this part twice as two separately quoted "
            f"lots ({lots}). Both lots are kept here as one row, so the machined subtotal is "
            f"unchanged, but the per-robot quantity is NOT confirmed -- the source part name "
            f"says _x{rec['embedded']} while the two lots total {qty}.")
    elif rec["embedded"] is not None and qty is not None and rec["embedded"] != qty:
        notes.append(
            f"QUANTITY CONFLICT: the source part name says _x{rec['embedded']} but the source "
            f"quantity column says {qty}. The quantity here is the lot the price was quoted "
            f"for; the per-robot quantity is unverified.")
    if extra:
        notes.append(extra)
    notes.append("Source part ID: " + " / ".join(sorted(src_names)) + ".")

    unit = ""
    if qty:
        exact = (total / Decimal(qty))
        if exact == exact.quantize(Decimal("0.01")):
            unit = f"{exact.quantize(Decimal('0.01'))}"
        else:
            notes.insert(0, f"Quoted lot price {total} does not divide evenly by {qty}; "
                            f"a unit cost to the cent cannot be derived from the source sheet.")

    row = {c: "" for c in COLS}
    row.update({
        "subassembly": sub, "class": "machined", "part_id": pid,
        "description": describe(pid), "qty_per_robot": str(qty) if qty else "",
        "unit_cost_usd": unit, "total_cost_usd": f"{total}",
        "process": "CNC", "notes": " ".join(notes),
    })
    (fixtures if "tester" in pid else parts).append(row)

def write(path, rows_):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows_)

# leg, then arm, then body, stable within group
rank = {"leg": 0, "arm": 1, "body": 2}
parts.sort(key=lambda r: (rank[r["subassembly"]], r["part_id"]))
write(os.path.join(OUT, "cnc-parts.csv"), parts)

for r in fixtures:
    r["subassembly"] = "test_fixture"
    r["description"] = "Single-leg test-rig plate"
    r["notes"] = ("NOT A ROBOT PART. Development fixture for the single-leg test rig. It sits "
                  "inside the machined subtotal of the source spreadsheet; it is held in this "
                  "separate file so that it is visible but excluded from every total this site "
                  "publishes. " + r["notes"])
write(os.path.join(OUT, "test-fixtures.csv"), fixtures)

print("cnc-parts.csv rows:", len(parts), "test-fixtures.csv rows:", len(fixtures))
print("machined total:", sum(Decimal(r["total_cost_usd"]) for r in parts))
for s in ("leg","arm","body"):
    g = [r for r in parts if r["subassembly"] == s]
    print(f"  {s}: {len(g)} rows, {sum(Decimal(r['total_cost_usd']) for r in g)}")
print("fixture total:", sum(Decimal(r["total_cost_usd"]) for r in fixtures))
print("unpriced:", [r["part_id"] for r in parts if not r["total_cost_usd"]])
print("no unit cost:", [r["part_id"] for r in parts if not r["unit_cost_usd"]])
ids = [r["part_id"] for r in parts]
assert len(ids) == len(set(ids)), "duplicate part_id"
assert not any("_x" in i and re.search(r"_x\d", i) for i in ids), "qty left in part_id"
