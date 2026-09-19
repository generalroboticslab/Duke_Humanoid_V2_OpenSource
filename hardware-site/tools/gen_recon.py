"""bom-reconciliation.csv -- the audit of the source spreadsheet's own arithmetic.

Deliberately has NO unit_cost_usd / total_cost_usd / qty_per_robot columns, so the
cost macros ignore it. The numbers in it are quotations of a defective source, not
cost claims this site makes; they belong in data rather than in page prose so that
nobody has to retype them.
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

import csv
OUT = str(DATA / "bom-reconciliation.csv")
COLS = ["Figure", "Amount (USD)", "Where it comes from", "Verdict"]
ROWS = [
 ("Source sheet GRAND TOTAL", "$14,881.99",
  "The bought-parts rows ($8,492.13) plus the sheet's own TOTAL CNC ($6,389.86).",
  "Do not publish. It is four machining quotations plus the bought parts, not the parts list."),
 ("Source sheet TOTAL CNC", "$6,389.86",
  "Four quotation subtotals recorded in the machined sheet: 2,076.98 + 1,374.19 + 1,317.87 + 1,620.82.",
  "Do not publish. The four quotations cover 60 of the 63 machined rows."),
 ("Rows the four quotations skip", "$450.76",
  "CNC_arm13 RS05 shaft coupler 109.80 + CNC_arm11 wrist roll 239.58 + the single-leg tester plate 101.38.",
  "Explains the gap exactly. Rows added to the sheet after the quotations and never folded back in."),
 ("All 63 machined rows", "$6,840.62",
  "Sum of the machined sheet's 63 rows.",
  "Correct sum of the parts list, but it still counts the single-leg test fixture."),
 ("Single-leg test fixture", "$101.38",
  "B6_single_leg_tester_plate, one row of the machined sheet.",
  "Removed. Development tooling, not a robot part. Held in test-fixtures.csv."),
 ("Machined parts, this site", "$6,739.24",
  "All 63 machined rows, less the test fixture. Computed from cnc-parts.csv.",
  "Published. This is the machined figure every page on this site uses."),
 ("Machined sheet, unit cost x quantity", "$16,009.04",
  "What the machined sheet gives if its UNIT COST column is read as a unit cost.",
  "Meaningless. It is 2.5x the machined total, which is how that column is known to hold line totals."),
]
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(COLS); w.writerows(ROWS)
print("wrote", OUT, len(ROWS), "rows")
