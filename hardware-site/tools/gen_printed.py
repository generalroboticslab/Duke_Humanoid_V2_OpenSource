"""Add the printed parts to docs/data/printed-parts.csv from the Fusion tree.

    python tools/gen_printed.py [path/to/tree.csv]

`gen_sheet1.py` writes the three filament/powder rows the team sheet has; this
script appends one row per printed component found in the Fusion export
(`cad/<export>/tree.csv`, written by tools/fusion_export/). A component is
printed when its Fusion material is a print material (Nylon 12 SLS, ABS) or one
of the team's `*_protection` cover materials. Quantities are the occurrence
counts in the tree. Nothing else is inferred: the filament grade behind a cover
material is not recorded in Fusion and stays a gap on the page.

Run after gen_sheet1.py. `stage_cad_export.py` imports PRINTED to name the files.
"""

from __future__ import annotations

import csv
import glob
import os
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "docs" / "data" / "printed-parts.csv"
COLS = ["subassembly", "class", "part_id", "description", "mpn", "vendor", "vendor_url", "alt_mpn", "alt_url",
        "qty_per_robot", "unit_cost_usd", "total_cost_usd", "material", "process", "tolerance_finish",
        "lead_time_days", "priced_as_of", "notes"]

# (fusion component name, part_id, subassembly, description). Roles of the
# unnamed `ComponentNN` covers come from their Fusion material name only.
PRINTED = [
    ("3DP_arm05_x4_RS02_shaft_bearing_retainer", "3DP_arm05_RS02_shaft_bearing_retainer", "arm", "RS02 shaft bearing retainer"),
    ("3DP_arm11_x2_wrist_roll", "3DP_arm11_wrist_roll", "arm", "Wrist-roll link"),
    ("Component5", "3DP_arm14_wrist_block", "arm", "Wrist block (Fusion `Component5`, next to the wrist-roll link; role not labelled in CAD)"),
    ("Component38", "3DP_armP01_elbow_cover_a", "arm", "Elbow cover, half A (Fusion `Component38`, material `elbow_protection`)"),
    ("Component39", "3DP_armP02_elbow_cover_b", "arm", "Elbow cover, half B (Fusion `Component39`, material `elbow_protection`)"),
    ("Component40", "3DP_armP03_shoulder_cover_a", "arm", "Shoulder cover A (Fusion `Component40`, material `shoulder_protection`)"),
    ("Component41", "3DP_armP04_shoulder_cover_b", "arm", "Shoulder cover B (Fusion `Component41`, material `shoulder_protection`)"),
    ("Component42", "3DP_armP05_shoulder_cover_c", "arm", "Shoulder cover C (Fusion `Component42`, material `shoulder_protection`)"),
    ("Component43", "3DP_armP06_shoulder_cover_d", "arm", "Shoulder cover D (Fusion `Component43`, material `shoulder_protection`)"),
    ("Component34", "3DP_armP07_shoulder_cover_e", "arm", "Shoulder cover E (Fusion `Component34`, material `measured_shoulder_protection`)"),
    ("Component35", "3DP_armP08_shoulder_cover_f", "arm", "Shoulder cover F (Fusion `Component35`, material `measured_shoulder_protection`)"),
    ("Component36", "3DP_armP09_shoulder_yaw_cover_a", "arm", "Shoulder-yaw cover A (Fusion `Component36`, material `shoulder_yaw_protection`)"),
    ("Component37", "3DP_armP10_shoulder_yaw_cover_b", "arm", "Shoulder-yaw cover B (Fusion `Component37`, material `shoulder_yaw_protection`)"),
    ("3DP_body_06_x1_front_plate_fixed", "3DP_body06_front_plate", "body", "Torso front plate"),
    ("3DP_body_08_x1_back_plate_fixed", "3DP_body08_back_plate", "body", "Torso back plate"),
    ("Component194|leg", "3DP_legP01_hip3_cover_a", "leg", "Hip-yaw cover A (Fusion `Component194`, material `hip3_protection`)"),
    ("Component195|leg", "3DP_legP02_hip3_cover_b", "leg", "Hip-yaw cover B (Fusion `Component195`, material `hip3_protection`)"),
    ("Component198|leg", "3DP_legP03_hip3_cover_c", "leg", "Hip-yaw cover C (Fusion `Component198`, material `hip3_protection`)"),
    ("Component199|leg", "3DP_legP04_hip3_cover_d", "leg", "Hip-yaw cover D (Fusion `Component199`, material `hip3_protection`)"),
    ("Component196|leg", "3DP_legP05_hip2_cover_a", "leg", "Hip-roll cover A (Fusion `Component196`, material `hip2_protection`)"),
    ("Component197|leg", "3DP_legP06_hip2_cover_b", "leg", "Hip-roll cover B (Fusion `Component197`, material `hip2_protection`)"),
    ("Component44|leg", "3DP_legP07_knee_cover_a", "leg", "Knee cover A (Fusion `Component44`, material `knee protection`)"),
    ("Component45|leg", "3DP_legP08_knee_cover_b", "leg", "Knee cover B (Fusion `Component45`, material `knee protection`)"),
    ("Component42|leg", "3DP_legP09_shank_cover_a", "leg", "Shank cover A (Fusion `Component42` in the lower body, material `shank protection`)"),
    ("Component43|leg", "3DP_legP10_shank_cover_b", "leg", "Shank cover B (Fusion `Component43` in the lower body, material `shank protection`)"),
    ("symmetric_sole", "3DP_leg19_sole", "leg", "Foot sole (Fusion `symmetric_sole`, material `foot_protection`)"),
    ("foot_front", "3DP_leg20_foot_front", "leg", "Foot front cap (Fusion `foot_front`, material `foot_protection`)"),
]

PROCESS = {"Nylon 12": "SLS", "ABS": "FDM"}


def find_tree(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    trees = sorted(glob.glob(str(SITE.parent / "cad" / "*" / "tree.csv")), key=os.path.getmtime)
    if not trees:
        sys.exit("no cad/*/tree.csv found; run tools/fusion_export in Fusion first")
    return Path(trees[-1])


def load_tree(path: Path) -> dict[str, list[dict]]:
    by: dict[str, list[dict]] = {}
    with open(path, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["kind"] != "part":
                continue
            by.setdefault(r["fusion_name"], []).append(r)
    return by


def pick(by: dict[str, list[dict]], key: str) -> list[dict]:
    name, _, scope = key.partition("|")
    rows = by.get(name, [])
    if scope == "leg":
        return [r for r in rows if r["path"].startswith("v2.1_lower_body")]
    if name.startswith("Component"):
        return [r for r in rows if not r["path"].startswith("v2.1_lower_body")]
    return rows


def main() -> int:
    tree = load_tree(find_tree(sys.argv[1] if len(sys.argv) > 1 else None))
    with open(OUT, encoding="utf-8-sig", newline="") as fh:
        keep = [r for r in csv.DictReader(fh) if r["part_id"].startswith("MAT_")]
    rows = []
    for key, pid, sub, desc in PRINTED:
        occ = pick(tree, key)
        if not occ:
            print(f"WARNING {pid}: {key} not in tree", file=sys.stderr)
            continue
        mat = occ[0]["material"]
        proc = next((p for k, p in PROCESS.items() if k in mat), "")
        material = ("Nylon 12, SLS (Formlabs Fuse 1)" if "Nylon 12" in mat
                    else "ABS, 60 % infill" if "60%" in mat
                    else "ABS" if "ABS" in mat else "")
        qty = sum(int(r["qty"]) for r in occ)
        mass = occ[0]["mass_g"]
        notes = f"From the Fusion tree ({occ[0]['fusion_name']}, {qty} occurrence(s), {mass} g each)."
        if not material:
            notes += f" Fusion material name `{mat}`: filament and print settings not recorded in CAD."
        rows.append({c: "" for c in COLS} | dict(
            subassembly=sub, **{"class": "printed"}, part_id=pid, description=desc, qty_per_robot=qty,
            material=material, process=proc, notes=notes))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows + keep)
    print(f"{OUT.relative_to(SITE).as_posix()}: {len(rows)} printed parts + {len(keep)} material rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
