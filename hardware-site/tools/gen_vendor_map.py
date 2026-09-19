"""Map the vendor components of the Fusion model to the BOM -> docs/data/vendor-parts.csv
and docs/assets/viewer/vendor-map.json.

    python tools/gen_vendor_map.py ../cad/<export>            (needs <export>/tree.csv with file_name)

A *vendor/other* component is every component with bodies in tree.csv that is
not one of the site's own parts (docs/data/cnc-parts.csv, printed-parts.csv,
resolved the way stage_cad_export.py resolves them). Each gets one row in
vendor-parts.csv; `part_id` is filled only when a rule below matches.

Matching is by explicit rules (RULES) tested against the component's own Fusion
name first and then against each ancestor in its occurrence path, nearest first:
an actuator's rotor, stator core or PCB is matched through its `Robstride 0N`
parent, a RealSense lens through `IntelRealsense_D435...`. `note` says which
ancestor carried the match and what the model and the BOM disagree on (model
name vs BOM model number, modelled count vs BOM quantity). Fasteners, bearings,
the wiring lumps, the power distribution blocks and the site's own unlisted
parts (gripper prints, covers under `protections`) are left unmatched with a
note that says why: the BOM has no row for them (fasteners.csv holds only the
placeholder row). Nothing is guessed from a name that no rule covers.

vendor-map.json holds the matched components only:
    {"<file_name>": {"part_id", "bom_file", "description", "qty_in_model", "via"}}

Prints per BOM row the modelled count of the matched assemblies against
`qty_per_robot`, and the unmatched components above 20 g.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "docs" / "data"
OUT_CSV = DATA / "vendor-parts.csv"
OUT_JSON = SITE / "docs" / "assets" / "viewer" / "vendor-map.json"
BOM_FILES = ("actuators.csv", "electronics.csv", "cables-connectors.csv", "fasteners.csv")
COLS = ["file_name", "fusion_name", "qty_in_model", "part_id", "bom_file", "description", "mpn", "vendor",
        "vendor_url", "note"]
REPORT_MIN_G = 20.0

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stage_cad_export import (FASTENER, base_name, is_fastener, load_tree, mass_of,  # noqa: E402
                              resolve_site_parts, vendor_rows)

ACTUATOR = re.compile(r"robstride[ _-]*0*(\d)(?!\d)", re.I)
ACTUATOR_IDS = {"0": "ACT_RS00", "2": "ACT_RS02", "3": "ACT_RS03", "4": "ACT_RS04", "5": "ACT_RS05", "6": "ACT_RS06"}

# (regex on a Fusion component name, part_id, note). Tested on the component
# itself, then on its ancestors nearest first; the first hit wins.
RULES: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"^FEETECH[ _-]*HL[ _-]*3915", re.I), "EL_SERVO_FEETECH", ""),
    (re.compile(r"^wa[rv]eshare[ _-]*st[ _-]*servo", re.I), "EL_SERVO_DRIVER",
     "Fusion name `wareshare_st_servo_controller`; BOM row is the Waveshare bus servo driver"),
    (re.compile(r"^IntelRealsense[ _-]*D435", re.I), "EL_CAM_D436",
     "Fusion component is the Intel RealSense D435 model; the BOM row is the D436"),
    (re.compile(r"^IMU[ _-]*syd[ _-]*dynamics[ _-]*TM171", re.I), "EL_IMU_TM171", ""),
    (re.compile(r"^CAN[ _-]*Isolated", re.I), "EL_CAN_ADAPTER",
     "Fusion name `CAN_Isolated`; BOM row is the CANable PRO V2.0"),
    (re.compile(r"^USB-C[ _-]*Cable$", re.I), "CBL_USBA_USBC",
     "Fusion material `USB C to A`; 12 modelled (2 per CAN adapter) vs 6 in the BOM"),
    (re.compile(r"^MINISFORUM", re.I), "EL_COMPUTE_MINIPC",
     "Fusion name `MINISFORUM_AI_X1`; BOM row is the X1-470"),
    (re.compile(r"^battery[ _-]*zeee", re.I), "EL_BATTERY_6S",
     "2 packs modelled; the BOM counts one 2-pack"),
    (re.compile(r"^Vention[ _-]*USB[ _-]*Hub", re.I), "EL_USB_HUB", ""),
    (re.compile(r"^VEMONT[ _-]*USB-C[ _-]*Hub", re.I), "EL_USB_HUB",
     "Fusion names it a VEMONT USB-C hub; the BOM row (qty 3) is a Vention hub — 1 Vention + 2 VEMONT are modelled"),
    (re.compile(r"^buck[ _-]*converter[ _-]*48[ _-]*to[ _-]*12", re.I), "EL_BUCK_48V_12V", ""),
]

# Why a component stays unmatched (regex on its own name; first hit wins).
UNMATCHED_NOTES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^150A[ _-]*relay", re.I), "no BOM row: the 150 A relay (power page: main disconnect gap)"),
    (re.compile(r"^battery[ _-]*tester", re.I), "no BOM row"),
    (re.compile(r"^(lumped[ _-]*wires|Small[ _-]*Wires|cables|8AWG)", re.I),
     "wiring harness lump; no single BOM row (see cables-connectors.csv and the wiring pages)"),
    (re.compile(r"^(power[ _-]*block|block|casing|6x10-7holes)$", re.I),
     "power distribution block; no BOM row (missing from the BOM, see the power page)"),
    (re.compile(r"^(schematics|.*cross_section|.*_face)", re.I), "sketch/section carrier; no manufacturing content"),
    (re.compile(r"bearing", re.I), "bearing; fasteners.csv has only the placeholder row"),
    (re.compile(r"^apriltag", re.I), "AprilTag fiducial / holder of the gripper; no BOM row"),
    (re.compile(r"^(gimbal_|U-joint|Component92)", re.I),
     "camera gimbal column part (`twincities_v2_nolock`); no BOM row"),
    (re.compile(r"^(custom_umi_gripper|rail|base|dovetail_umi_gripper|Component9)$", re.I),
     "gripper part designed for this robot; no row in printed-parts.csv or cnc-parts.csv"),
    (re.compile(r"^v15_right_end_effector_attachment", re.I),
     "wrist end-effector attachment (Nylon 12); no row in printed-parts.csv"),
    (re.compile(r"^ankle_top_cover", re.I), "cover under `protections` (Fusion material Steel); not in printed-parts.csv"),
]


def segments(path: str) -> list[str]:
    """Occurrence path -> component names, nearest ancestor first, self excluded."""
    names = [re.sub(r":\d+$", "", s) for s in path.split("+")]
    return list(reversed(names[:-1]))


def match(name: str) -> tuple[str, str] | None:
    m = ACTUATOR.search(name)
    if m and m.group(1) in ACTUATOR_IDS:
        return ACTUATOR_IDS[m.group(1)], ""
    for rx, pid, note in RULES:
        if rx.search(name):
            return pid, note
    return None


def match_row(r: dict) -> tuple[str, str, str]:
    """(part_id, via, note) for one tree row: own name first, then the ancestors."""
    hit = match(r["fusion_name"])
    if hit:
        return hit[0], "", hit[1]
    for anc in segments(r["path"]):
        hit = match(anc)
        if hit:
            return hit[0], anc, hit[1]
    return "", "", ""


def unmatched_note(r: dict, top: str) -> str:
    n = base_name(r["file_name"])
    if FASTENER.search(r["fusion_name"]):
        return "fastener; fasteners.csv has only the placeholder row"
    for rx, note in UNMATCHED_NOTES:
        if rx.search(n) or rx.search(r["fusion_name"]):
            return note
    if "protection" in r["material"].lower() or "+protections" in r["path"]:
        return "cover under `protections`; not in printed-parts.csv"
    if mass_of(r) < 3:
        return "no BOM row; under 3 g"
    return f"no BOM row; Fusion material `{r['material']}`, under `{top}`"


def load_bom() -> dict[str, dict]:
    bom = {}
    for f in BOM_FILES:
        p = DATA / f
        if not p.is_file():
            continue
        with open(p, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                bom[row["part_id"].strip()] = row | {"bom_file": f}
    return bom


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    exp = Path(sys.argv[1])
    tree = load_tree(exp)
    _, owner = resolve_site_parts(tree)
    bom = load_bom()
    rows, vmap = [], {}
    per_bom: dict[str, dict] = {}
    for r in vendor_rows(tree, owner):
        pid, via, note = match_row(r)
        top = r["path"].split("+")[0].split(":")[0]
        b = bom.get(pid)
        if pid and b is None:
            print(f"WARNING rule points at {pid} which is in no BOM CSV ({r['file_name']})", file=sys.stderr)
            pid = ""
        if pid:
            note = "; ".join(x for x in (f"via `{via}`" if via else "", note) if x)
            rows.append(dict(file_name=r["file_name"], fusion_name=r["fusion_name"], qty_in_model=r["qty"],
                             part_id=pid, bom_file=b["bom_file"], description=b["description"], mpn=b["mpn"],
                             vendor=b["vendor"], vendor_url=b["vendor_url"], note=note))
            vmap[r["file_name"]] = {"part_id": pid, "bom_file": b["bom_file"], "description": b["description"],
                                    "qty_in_model": int(r["qty"]), "via": via}
            per_bom.setdefault(pid, {"components": 0})["components"] += 1
        else:
            rows.append(dict(file_name=r["file_name"], fusion_name=r["fusion_name"], qty_in_model=r["qty"],
                             part_id="", bom_file="", description="", mpn="", vendor="", vendor_url="",
                             note=unmatched_note(r, top)))

    # Modelled count of each matched assembly root: a component whose OWN name matches,
    # that is not empty (the `*_cross_section` sketches) and has no ancestor matching
    # the same BOM row (an actuator inside an actuator would count twice).
    roots: dict[str, int] = {}
    for r in tree:
        hit = match(r["fusion_name"])
        if not hit or hit[0] not in per_bom or r["kind"] == "empty":
            continue
        if any((match(a) or ("",))[0] == hit[0] for a in segments(r["path"])):
            continue
        roots[hit[0]] = roots.get(hit[0], 0) + int(r["qty"])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(vmap, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    matched = [r for r in rows if r["part_id"]]
    print(f"{OUT_CSV.relative_to(SITE).as_posix()}: {len(rows)} vendor/other components with bodies, "
          f"{len(matched)} matched to {len(per_bom)} BOM rows, {len(rows) - len(matched)} unmatched")
    print(f"{OUT_JSON.relative_to(SITE).as_posix()}: {len(vmap)} entries")
    print("\nBOM row               components  modelled  bom_qty")
    for pid in sorted(per_bom):
        q = bom[pid]["qty_per_robot"]
        flag = "" if str(roots.get(pid, "")) == q else "   <- differs"
        print(f"  {pid:20} {per_bom[pid]['components']:>10}  {roots.get(pid, 0):>8}  {q:>7}{flag}")
    unmatched_bom = sorted(p for p in bom if p not in per_bom)
    print(f"\nBOM rows with no component in the model: {', '.join(unmatched_bom)}")
    big = [(r, mass_of(t)) for r in rows for t in tree
           if not r["part_id"] and t["file_name"] == r["file_name"] and mass_of(t) > REPORT_MIN_G]
    print(f"\nunmatched components over {REPORT_MIN_G:.0f} g ({len(big)}):")
    for r, m in sorted(big, key=lambda x: -x[1]):
        print(f"  {m:7.1f} g  x{r['qty_in_model']:<3} {r['file_name']:45} {r['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
