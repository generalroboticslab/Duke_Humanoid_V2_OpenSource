"""Stage a Fusion export (from tools/fusion_export/) into docs/files/.

    python tools/stage_cad_export.py ../cad/humanoid_2.1_latest_<stamp> [--rev 01] [--apply]

Reads <export>/tree.csv and the part IDs in docs/data/*.csv, matches Fusion
component names to part IDs (the site IDs are the Fusion names without the
`_x<qty>` token), and prints the mapping. With --apply it copies:

    <export>/step/<fusion>.step   -> docs/files/step/<part_id>_rev<NN>.step
    <export>/print/<fusion>.stl   -> docs/files/print/<part_id>_rev<NN>.stl   (printed parts only)
    <export>/assembly/*.step/.f3z -> docs/files/assembly/<design>_rev<NN>.*

Only parts the site lists (machined and printed) are staged: vendor parts
(actuators, bearings, screws) are not redistributed. Run gen_cad_manifest.py
afterwards. Nothing here edits a page.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "docs" / "data"
FILES = SITE / "docs" / "files"

# Site IDs that were truncated or renamed relative to the Fusion component names.
ALIASES = {
    "CNC_arm01_shoulder_roll_front_bearing": "CNC_arm01_shoulder_roll_front_bearing_retainer",
    "CNC_arm02_shoulder_roll_back_bearing": "CNC_arm02_shoulder_roll_back_bearing_retainer",
    "CNC_arm04_shoulder_roll_support_shaft": "CNC_arm04_shoulder_elbow_support_shaft",
    "CNC_arm07_elbow_front_bearing": "CNC_arm07_elbow_front_bearing_retainer",
    "CNC_arm08_elbow_back_bearing": "CNC_arm08_elbow_back_bearing_retainer",
    "CNC_leg12_lower_leg_bearing": "CNC_leg12_lower_leg_bearing_cap",
    "CNC_arm09_elbow_output_shaft": "CNC_arm09_elbow_roll_output_shaft",
}
PRINTED_PREFIX = "3DP_"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_printed import PRINTED  # noqa: E402  (fusion name, part_id, ...)
ALIASES.update({pid: name.split("|")[0] for name, pid, _, _ in PRINTED})
PRINTED_IDS = {pid for _, pid, _, _ in PRINTED}
MAX_FILE = 95 * 1024 * 1024


def strip_qty(name: str) -> str:
    return re.sub(r"_x\d+(?=_)", "", name)


def site_ids() -> dict[str, str]:
    out = {}
    for f in ("cnc-parts.csv", "printed-parts.csv"):
        with open(DATA / f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                pid = r["part_id"].strip()
                if pid and not pid.startswith("MAT_"):
                    out[pid] = f
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--rev", default="01")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    exp = Path(a.export)
    with open(exp / "tree.csv", encoding="utf-8", newline="") as fh:
        tree = [r for r in csv.DictReader(fh) if r["kind"] == "part"]
    by_stripped: dict[str, list[dict]] = {}
    for r in tree:
        by_stripped.setdefault(strip_qty(r["file_name"]), []).append(r)
        if r["fusion_name"] != r["file_name"]:
            by_stripped.setdefault(r["fusion_name"], []).append(r)

    plan, missing = [], []
    for pid in site_ids():
        key = ALIASES.get(pid, pid)
        cands = by_stripped.get(key) or by_stripped.get(strip_qty(key), [])
        if not cands:
            missing.append(pid)
            continue
        src = cands[0]["file_name"]
        printed = pid in PRINTED_IDS or key.startswith(PRINTED_PREFIX)
        plan.append((pid, src, printed, sum(int(c["qty"]) for c in cands)))

    print(f"{len(plan)} site parts matched to Fusion components, {len(missing)} not in the CAD:")
    for pid in missing:
        print(f"  NOT IN CAD  {pid}")
    for pid, src, printed, qty in plan:
        tag = "3DP" if printed else "CNC"
        print(f"  {tag}  {pid:45} <- {src}  (qty {qty})")

    fusion_only = sorted(k for k in by_stripped if k.startswith(("CNC_", "3DP_"))
                         and k not in {ALIASES.get(p, p) for p in site_ids()})
    if fusion_only:
        print(f"{len(fusion_only)} CNC/3DP components in the CAD with no site row:")
        for k in fusion_only:
            print(f"  NOT ON SITE {k}")

    if not a.apply:
        print("\n(dry run; add --apply to copy)")
        return 0

    copied, absent = 0, []
    for pid, src, printed, _ in plan:
        pairs = [("step", ".step", "step")]
        if printed:
            pairs.append(("print", ".stl", "print"))
        for sub, ext, dst_sub in pairs:
            s = exp / sub / (src + ext)
            if not s.is_file():
                absent.append(str(s.relative_to(exp)))
                continue
            d = FILES / dst_sub / f"{pid}_rev{a.rev}{ext}"
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
            copied += 1
    for s in sorted((exp / "assembly").glob("*")):
        if s.suffix.lower() not in (".step", ".stp", ".f3z") or s.name.endswith(".f3z.f3d"):
            continue
        d = FILES / "assembly" / f"{s.stem}_rev{a.rev}{s.suffix.lower()}"
        if s.stat().st_size > MAX_FILE:
            if s.suffix.lower() in (".step", ".stp"):
                import zipfile
                with zipfile.ZipFile(str(d) + ".zip", "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                    z.write(s, d.name)
                print(f"  zipped (over 95 MB): {d.name}.zip")
            else:
                print(f"  skipped (over 95 MB, publish as a release asset): {s.name}")
            continue
        shutil.copy2(s, d)
        copied += 1
    print(f"\ncopied {copied} files into docs/files/")
    for x in absent:
        print(f"  export missing: {x}")
    print("now run: python tools/gen_cad_manifest.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
