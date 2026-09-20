"""Generate the six parts-list CSVs from the team's BOM spreadsheet.

    python tools/gen_bom.py [path/to/Duke_Humanoid_V2_BOM_WIP.xlsx] [path/to/tree.csv]

The team's spreadsheet ``reference/bom/Duke_Humanoid_V2_BOM_WIP.xlsx`` (one
sheet, 100 part lines) is THE source for every parts list on this site. It
replaces the two exported CSVs the retired ``gen_sheet1.py`` / ``gen_cnc.py``
read; where the two disagree, the spreadsheet wins.

    Category    rows          -> CSV
    Electronics E0-E20 (21)   -> actuators.csv (E1-E6), cables-connectors.csv
                                 (E9), electronics.csv (the rest)
    CNC         C0-C29 (30)   -> cnc-parts.csv
    3DP         P0-P39 (40)   -> printed-parts.csv
    Hardware    H0-H8  (9)    -> fasteners.csv

Every CSV carries the column contract of ``docs/data/README.md`` plus a last
column ``team_ref``: the spreadsheet's ``#`` value (``E3``, ``C21``, ``P20``,
``H1``) the row came from, blank for a row the spreadsheet has no line for.

What this script will not do
----------------------------
* **No invented price.** A blank or ``0`` unit cost becomes a *blank*
  ``unit_cost_usd`` and the note "Team BOM: no price yet", so the cost macros
  skip it and the pages print a red TODO. 39 of the 100 lines are unpriced: the
  30 unpriced 3DP lines and all 9 Hardware lines.
* **No invented mapping.** The CNC and 3DP rows of the spreadsheet carry no
  part IDs, so ``CNC_MAP`` / ``PRINTED_MAP`` below map them to the CAD-derived
  ``part_id``s the rest of the release keys on (``docs/files/<kind>/<part_id>_
  rev<NN>.*``, the viewer, ``part-properties.csv``). Every entry carries its
  evidence in a comment and, where the evidence is a group of parts rather
  than one part, the row itself says so and is marked UNVERIFIED.
* **No dropped CAD part.** A printed or machined part that is in the CAD but
  not in the spreadsheet is kept, unpriced, with the note "not in the team
  BOM". A spreadsheet row with no CAD match keeps its ``team_ref`` as its
  ``part_id`` and says "no CAD match yet".

Run order: ``gen_bom.py`` (this file, writes all six CSVs, reads the newest
``cad/*/tree.csv`` for the printed parts) then ``gen_cad_manifest.py``,
``gen_punchlist.py``, ``gen_image_manifest.py``. ``gen_printed.py`` is now the
``PRINTED`` mapping module (Fusion component -> ``part_id``) that this script,
``stage_cad_export.py``, ``build_viewer.py`` and ``gen_part_properties.py``
import; it no longer writes a CSV.
"""

from __future__ import annotations

import csv
import os
import re
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_printed import PRINTED, find_tree, load_tree, material_of, pick  # noqa: E402

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "docs" / "data"
SOURCE = Path(os.environ.get("BOM_SOURCE_DIR", SITE.parent / "reference" / "bom"))
XLSX = SOURCE / "Duke_Humanoid_V2_BOM_WIP.xlsx"

# The spreadsheet's own date: the file the team handed over on 2026-09-19.
PRICED_AS_OF = "2026-09-19"

COLS = ["subassembly", "class", "part_id", "description", "mpn", "vendor", "vendor_url",
        "alt_mpn", "alt_url", "qty_per_robot", "unit_cost_usd", "total_cost_usd",
        "material", "process", "tolerance_finish", "lead_time_days", "priced_as_of",
        "notes", "team_ref"]

NO_PRICE = "Team BOM: no price yet."
NOT_IN_BOM = "Not in the team BOM (Duke_Humanoid_V2_BOM_WIP.xlsx, 2026-09-19): no price and no quantity from it."
RS_ALT = ("SUPPLY RISK, no alternate published. A different actuator model changes the "
          "mounting interface, the shaft and the CAN configuration, so it is not a drop-in "
          "substitution.")

# Link domain -> vendor name. A domain that is not here keeps its host name and
# is reported, so no vendor is ever guessed silently.
VENDORS = {
    "amazon.com": "Amazon",
    "aliexpress.us": "AliExpress",
    "digikey.com": "DigiKey",
    "aifitlab.com": "AiFitLab",
    "waveshare.com": "Waveshare",
    "robotshop.com": "RobotShop",
    "store.realsenseai.com": "RealSense Store",
    "zeeebattery.com": "Zeee",
    "epowerhobby.com": "ePowerHobby",
}

# --------------------------------------------------------------------------- #
# purchased parts: Electronics (E0-E20) and Hardware (H0-H8)
#
# (team_ref, csv, part_id, subassembly, description, mpn, extra note). The
# part_ids of rows that were already published keep their IDs (gen_vendor_map.py
# and docs/assets/viewer/vendor-map.json key on them); new rows follow the same
# scheme. `description` is the curated English name where the item is unchanged,
# the spreadsheet's own text where it is new; the spreadsheet's text is in the
# notes of every row either way.
# --------------------------------------------------------------------------- #
ACT_FILE, EL_FILE, CAB_FILE, FAS_FILE = (
    "actuators.csv", "electronics.csv", "cables-connectors.csv", "fasteners.csv")

PURCHASED: list[tuple[str, str, str, str, str, str, str]] = [
    # --- actuators ---------------------------------------------------------
    ("E1", ACT_FILE, "ACT_RS00", "actuators", "RobStride 00 quasi-direct-drive actuator", "RobStride 00", RS_ALT),
    ("E2", ACT_FILE, "ACT_RS02", "actuators", "RobStride 02 quasi-direct-drive actuator", "RobStride 02", RS_ALT),
    ("E3", ACT_FILE, "ACT_RS03", "actuators", "RobStride 03 quasi-direct-drive actuator", "RobStride 03", RS_ALT),
    ("E4", ACT_FILE, "ACT_RS04", "actuators", "RobStride 04 quasi-direct-drive actuator", "RobStride 04", RS_ALT),
    ("E5", ACT_FILE, "ACT_RS05", "actuators", "RobStride 05 quasi-direct-drive actuator", "RobStride 05",
     "Quoted below the RS 02 and the RS 00, which does not follow the model numbering; "
     "re-check with the vendor before ordering. " + RS_ALT),
    ("E6", ACT_FILE, "ACT_RS06", "actuators", "RobStride 06 quasi-direct-drive actuator", "RobStride 06",
     "QUANTITY CONFLICT: the team BOM lists 2, but the robot has four RS06 joints (ankle_2 and "
     "shoulder_2 on both sides, from `deploy/control/humanoid_config.py` and the CAN bus list), "
     "so two more are needed than the team BOM buys. UNVERIFIED. " + RS_ALT),
    # --- electronics -------------------------------------------------------
    ("E0", EL_FILE, "EL_COMPUTE_MINIPC", "electronics", "MINISFORUM X1-470 mini PC (onboard computer)", "X1-470",
     "Module (III) on the hardware overview figure. The 2026-09-19 link is the X1-Pro-470 listing; "
     "the model on the site is the X1-470 **UNVERIFIED**."),
    ("E7", EL_FILE, "EL_BATTERY_6S", "electronics", "Zeee 6S LiPo battery, 10000 mAh, 22.2 V, 2-pack", "",
     "Priced as one 2-pack, which is how the team BOM records it (its item text ends in x2). "
     "Whether both packs are carried at once is not stated there."),
    ("E8", EL_FILE, "EL_TVS_DIODE", "electronics", "TVS diode, 53 V working / 85 V clamping", "M1.5KE62CA",
     "Manufacturer part number read from the DigiKey link. Where the ten diodes are installed "
     "is not documented in the team BOM."),
    ("E10", EL_FILE, "EL_SERVO_DRIVER", "electronics", "Waveshare serial bus servo driver board, ST/SC series", "",
     "Two boards for the two Feetech bus servos."),
    ("E11", EL_FILE, "EL_BUCK_12V_ENC", "electronics", "DC 20-60 V to 12 V encased buck converter", "", ""),
    ("E12", EL_FILE, "EL_BUCK_48V_12V", "electronics", "48 V to 12 V buck converter", "", ""),
    ("E13", EL_FILE, "EL_CAN_ADAPTER", "electronics", "CANable PRO V2.0 USB-CAN controller", "CANable PRO V2.0",
     "Six adapters, one per CAN bus."),
    ("E14", EL_FILE, "EL_CAM_D436", "electronics", "Intel RealSense D436 depth camera", "D436",
     "SUPPLY RISK, no alternate published. One per camera gimbal. The workspace study assumes "
     "this camera's 90x65 degree RGB field of view, so a substitute changes the result the "
     "design was optimised for."),
    ("E15", EL_FILE, "EL_SERVO_FEETECH", "electronics", "Feetech HL-3915-C001 12 V servo, 14.2 kg-cm",
     "HL-3915-C001", "One servo per gripper."),
    ("E16", EL_FILE, "EL_USB_HUB", "electronics", "Vention USB hub", "", ""),
    ("E17", EL_FILE, "EL_IMU_TM171", "electronics", "SYD Dynamics TransducerM TM171 9-axis AHRS, dual-port",
     "TM171", "Listed in the team BOM only as \"IMU\"; the model is read from the vendor link."),
    ("E18", EL_FILE, "EL_SURGE_PROTECTOR", "electronics", "TTocas surge protector", "",
     "New in the 2026-09-19 team BOM. The power wiring diagram puts a surge protector in the "
     "pack lead before the 48 V bus; that this is that part is **UNVERIFIED**, and the link is "
     "a vendor storefront, not one product."),
    ("E19", EL_FILE, "EL_DIST_BLOCK", "electronics", "Power distribution block terminals", "",
     "New in the 2026-09-19 team BOM. Four off, which matches the two power + ground pairs "
     "drawn on the power wiring diagram; that the drawn blocks are this part is **UNVERIFIED**."),
    ("E20", EL_FILE, "EL_VOLTAGE_CHECKER", "electronics", "LiPo voltage checker, 1-8S, with case", "",
     "New in the 2026-09-19 team BOM. Two off; where they sit on the robot is not stated."),
    # --- cables and connectors --------------------------------------------
    ("E9", CAB_FILE, "CBL_USBA_USBC_BELKIN", "harness", "Belkin USB-A to USB-C cable, 6.6 ft, 2-pack", "",
     "Grouped under Electronics in the team BOM; filed here with the rest of the cabling. "
     "Quantity 2 means two 2-packs."),
    # --- fasteners and bearings -------------------------------------------
    ("H0", FAS_FILE, "FAS_BEARING_45X58X7", "fasteners", "Ball bearing, 45 x 58 x 7 mm", "", ""),
    ("H1", FAS_FILE, "FAS_BEARING_50X65X7", "fasteners", "Ball bearing, 50 x 65 x 7 mm", "",
     "The team design log calls the 50 x 65 x 7 mm bearing the main bearing and models "
     "McMaster-Carr 6656K229; the team BOM gives no part number or link."),
    ("H2", FAS_FILE, "FAS_BEARING_35X44X5", "fasteners", "Ball bearing, 35 x 44 x 5 mm", "", ""),
    ("H3", FAS_FILE, "FAS_BEARING_35X47X7", "fasteners", "Ball bearing, 35 x 47 x 7 mm", "", ""),
    ("H4", FAS_FILE, "FAS_BEARING_30X37X4", "fasteners", "Ball bearing, 30 x 37 x 4 mm", "", ""),
    ("H5", FAS_FILE, "FAS_BEARING_10X15X4", "fasteners", "Ball bearing, 10 x 15 x 4 mm", "", ""),
    ("H6", FAS_FILE, "FAS_SCREW_M3X10_TORX_BH", "fasteners", "M3 x 10 Torx button-head screw", "",
     "The team BOM gives no quantity. It also conflicts with the team design log, which "
     "specifies M3x12 (McMaster-Carr 90991A115) **UNVERIFIED**."),
    ("H7", FAS_FILE, "FAS_SCREW_M4X8_TORX_BH", "fasteners", "M4 x 8 Torx button-head screw", "",
     "The team BOM gives no quantity."),
    ("H8", FAS_FILE, "FAS_SCREW_M4X10_TORX_BH", "fasteners", "M4 x 10 Torx button-head screw", "",
     "The team BOM gives no quantity. It also conflicts with the team design log, which "
     "specifies M4x12 (McMaster-Carr 90991A123) **UNVERIFIED**."),
]

# --------------------------------------------------------------------------- #
# CNC rows C0-C29 -> the CAD-derived part_id.
#
# Evidence per line: the spreadsheet's item name and unit cost x quantity, and
# the same figures in the superseded machining quote
# (reference/bom/duke-humanoid-v2_BOM_sheet2_cnc-parts.csv), whose part names
# ARE the CAD names. Every price below matches that quote's line total divided
# by its lot, which is what ties a team name such as "Foot" to `CNC_leg18`.
# --------------------------------------------------------------------------- #
CNC_MAP: list[tuple[str, str, str]] = [
    # team_ref, part_id, note beyond the price/quantity match
    ("C0", "CNC_body03_top_plate", ""),                      # Body Plate - Top 64.53 x1 = quote CNC_body03_x1_top_plate 64.53
    ("C1", "CNC_body01_bottom_plate", ""),                   # Body Plate - Bottom 64.03 x1 = quote CNC_body01_x1_bottom_plate
    ("C2", "CNC_body02_side_plate", ""),                     # Body Plate - Side 109.14 x2 = quote CNC_body02_x2_side_plate
    ("C3", "CNC_body04_front_plate", ""),                    # Body Plate - Front/Back 47.08 x4 = quote CNC_body04_x4_front_plate
    ("C4", "CNC_leg03_RS03_shaft_bearing_retainer", ""),     # Robstride 03 Bearing Retainer 49.34 x5 = quote CNC_leg03_x5 49.34 x5
    ("C5", "CNC_leg02_RS03_shaft_coupler",
     "The quote carries this part as two lots (6 pcs at 274.02 and 2 pcs at 100.26, 374.28 for 8); "
     "the team BOM prices it at 46.785 each, which is that 374.28 divided by 8, for 7 pieces."),
    # Robstride 03 Output Shaft 46.785 x7; quote name CNC_leg02_x7_RS03_shaft_coupler
    ("C6", "CNC_leg01_hip_center_back", ""),                 # Hip 1 Motor Bracket 81.59 x2 = quote CNC_leg01_x2_hip_center_back
    ("C7", "CNC_leg04_hip_roll_front_bearing_retainer", ""), # Hip 2 Motor Bracket 48.59 x2 = quote CNC_leg04_x2
    ("C8", "CNC_leg05_hip_roll_back_bearing_retainer", ""),  # Hip 2 Bearing Retainer 68.02 x2 = quote CNC_leg05_x2
    ("C9", "CNC_leg06_hip_roll_output_shaft", ""),           # Hip 3 Output Shaft 59.96 x2 = quote CNC_leg06_x2
    ("C10", "CNC_leg07_hip_roll_support_shaft", ""),         # Hip 3 Supporting Shaft 57.43 x2 = quote CNC_leg07_x2
    ("C11", "CNC_leg08_knee_front_bearing_retainer", ""),    # Knee Motor Bracket 54.81 x2 = quote CNC_leg08_x2
    ("C12", "CNC_leg09_knee_motor_back_cover", ""),          # Knee Bearing Retainer 81.35 x2 = quote CNC_leg09_x2
    ("C13", "CNC_leg10_knee_output_shank", ""),              # Shank Shaft 113.29 x2 = quote CNC_leg10_x2
    ("C14", "CNC_leg11_knee_support_shank", ""),             # Shank Support 50.05 x2 = quote CNC_leg11_x2
    ("C15", "CNC_leg12_lower_leg_bearing",
     "The quote's name says x4 and its lot was 5 pieces; the team BOM says 4."),
    # Shank Joint Cap 16.50 x4 = quote CNC_leg12_x4_lower_leg_bearing 16.50
    ("C16", "CNC_leg13_ankle_pitch_front", ""),              # Ankle Motor Bracket 78.82 x2 = quote CNC_leg13_x2
    ("C17", "CNC_leg14_ankle_pitch_back", ""),               # Ankle Bearing Retainer 95.85 x2 = quote CNC_leg14_x2
    ("C18", "CNC_leg15_RS06_shaft_bearing_retainer", ""),    # Robstride 06 Bearing Retainer 37.81 x2 = quote CNC_leg15_x2
    ("C19", "CNC_leg16_ankle_roll_output_shaft", ""),        # Foot Shaft 39.40 x2 = quote CNC_leg16_x2
    ("C20", "CNC_leg17_ankle_roll_support_shaft", ""),       # Foot Support 34.60 x2 = quote CNC_leg17_x2
    ("C21", "CNC_leg18_foot_plate", ""),                     # Foot 53.76 x2 = quote CNC_leg18_x2_foot_plate
    ("C22", "CNC_arm01_shoulder_roll_front_bearing", ""),    # Shoulder Motor Bracket 46.69 x2 = quote CNC_arm01_x2
    ("C23", "CNC_arm02_shoulder_roll_back_bearing", ""),     # Shoulder Bearing Retainer 99.24 x2 = quote CNC_arm02_x2
    ("C24", "CNC_arm03_shoulder_roll_output_shaft", ""),     # Shoulder Shaft 31.72 x2 = quote CNC_arm03_x2
    ("C25", "CNC_arm04_shoulder_roll_support_shaft",
     "MATCHED ON NAME AND QUANTITY ONLY: the quote prices this part (CNC_arm04_x4_shoulder_roll_support_shaft) "
     "at 28.78 each for 4, exactly half the team BOM's 57.56 each for 4. Which of the two unit prices "
     "holds is UNVERIFIED; the team BOM's is used here."),
    # Shoulder/Elbow Support 57.56 x4
    ("C26", "CNC_arm09_elbow_output_shaft", ""),             # Elbow Shaft 31.42 x2 = quote CNC_arm09_x2
    ("C27", "CNC_arm10_r03_back_cover",
     "The team BOM calls it a coupler, the CAD name is a back cover; price and quantity are the "
     "quote's CNC_arm10_x4_r03_back_cover exactly. UNVERIFIED."),
    # Shoulder/Elbow Coupler 54.25 x4 = quote CNC_arm10_x4 54.25 x4
    ("C28", "CNC_arm07_elbow_front_bearing", ""),            # Elbow Motor Bracket 57.94 x2 = quote CNC_arm07_x2
    ("C29", "CNC_arm08_elbow_back_bearing", ""),             # Elbow Bearing Retainer 65.65 x2 = quote CNC_arm08_x2
]

# Machined parts the release already publishes that the team BOM has no row
# for. They keep their IDs because the assembly pages, docs/files/ and the
# viewer use them; they lose the superseded quote's price.
# (part_id, subassembly, description, note)
CNC_EXTRA: list[tuple[str, str, str, str]] = [
    ("CNC_arm05_RS02_shaft_bearing", "arm", "RS02 shaft bearing",
     "In Fusion this part is the SLS nylon `3DP_arm05_RS02_shaft_bearing_retainer` (see Printed parts)."),
    ("CNC_arm06_RS02_shaft_coupler", "arm", "RS02 shaft coupler",
     "In Fusion this part is the SLS nylon `3DP_arm06_RS02_shaft_coupler` (see Printed parts)."),
    ("CNC_arm11_wrist_roll", "arm", "wrist roll",
     "In Fusion this part is the SLS nylon `3DP_arm11_wrist_roll` (see Printed parts)."),
    ("CNC_arm12_wrist_pitch", "arm", "wrist pitch",
     "Not in the Fusion model either: no CAD file, no mass."),
    ("CNC_arm13_RS05_shaft_coupler", "arm", "RS05 shaft coupler",
     "In Fusion it is the gripper's machined mounting flange inside `dovetail_umi_gripper` "
     "(the code repo's `cnc_flange`, Aluminium 6061)."),
]

# --------------------------------------------------------------------------- #
# 3DP rows P0-P39 -> the CAD-derived part_id(s).
#
# (team_refs, part_ids, note). Several refs on one part = the spreadsheet
# splits one CAD component into left/right or A/B lines; several parts on one
# ref = one spreadsheet line covers several CAD components. The quantity
# written to the CSV is always the Fusion occurrence count, and the row says so
# when the spreadsheet's count differs.
#
# Eight of the ten priced rows are matched by MASS: the spreadsheet's `weight`
# column times its `price per unit weight` is its unit cost, and that weight, read
# as kilograms, equals the Fusion mass of the component in tree.csv to 0.1 g
# (with its child components for body07/body09). P5 matches by STL volume at the
# Nylon 12 density the other nylon lines imply; P0 matches by name and material
# only. Every row's note says which case it is (`weight_check`). The unpriced
# rows have no weight, so they are matched by Fusion material group, piece count
# and name.
# --------------------------------------------------------------------------- #
PRINTED_MAP: list[tuple[tuple[str, ...], tuple[str, ...], str]] = [
    # ---- priced rows: mass-matched ---------------------------------------
    (("P0",), ("3DP_body05_interior_plate",),
     "Matched by name and material: the plate that carries the PC, and the only `3DP_` component "
     "with a PLA material in Fusion. Its weight cannot be checked against the export (see below). "
     "UNVERIFIED."),  # PC Mount, PLA x1; weight 0.3175725 -> 317.6 g; Fusion mass 4637.4 g includes 36 children
    (("P1",), ("3DP_body06_front_plate", "3DP_body08_back_plate"),
     "One team BOM line of 2 pieces: its weight (73.888 g) is the CAD mass of the front plate "
     "(73.9 g); the back plate is 73.2 g and is priced at the same rate here."),
    (("P2",), ("3DP_body07_front_plate_removable",),
     ""),  # Front Plate, PLA x1; weight 0.096876586 -> 96.9 g = CAD mass of body07
    (("P3",), ("3DP_body09_back_plate_removable",),
     ""),  # Back Plate, PLA x1; weight 0.113809991 -> 113.8 g = CAD mass of body09
    (("P4",), ("3DP_arm05_RS02_shaft_bearing_retainer",),
     ""),  # Arm Shaft Cover, Nylon 12 x4; weight 70.62 g = CAD 70.6 g, 4 occurrences
    (("P5",), ("3DP_arm06_RS02_shaft_coupler",),
     "The weight (64.6 g) is this part's STL volume in part-properties.csv (63.67 cm3) at the "
     "density the other Nylon 12 lines imply (1.014 g/cm3); the Fusion mass, 67.5 g, includes "
     "the component's 6 child components."),  # Elbow Shaft Coupler, Nylon 12 x2; 2 occurrences
    (("P6",), ("3DP_arm11_wrist_roll",),
     ""),  # Wrist Shaft, Nylon 12 x2; weight 72.10 g = CAD 72.1 g, 2 occurrences
    (("P7", "P9"), ("3DP_arm14_wrist_block",),
     "The team BOM splits this component into a right-hand and a left-hand line of one piece each "
     "(Wrist Housing R and L); both carry the same weight, 138.0 g, which is this part's CAD mass."),
    (("P8",), ("3DP_arm15_end_effector_attachment",),
     ""),  # Wrist Output, Nylon 12 x2; weight 130.22 g = CAD 130.2 g, 2 occurrences
    # ---- unpriced rows: matched on material group, count and name ---------
    (("P10",), ("3DP_grip01_base",),
     ""),  # Gripper Housing, PLA x2 = the 2 gripper bases
    (("P11",), ("3DP_grip03_rail",),
     "The team BOM calls it a rack; the only matching CAD component is the gripper's slide rail "
     "(4 off). The rack itself has no geometry in Fusion. UNVERIFIED."),
    (("P12",), ("3DP_grip05_pinion",),
     ""),  # Gear, Nylon 12 x2 = the 2 double-helix pinions
    (("P13",), ("3DP_grip02_finger",),
     ""),  # UMI Fingers, TPU x4 = the 4 gripper fingers
    (("P14",), ("3DP_grip04_apriltag_holder",),
     ""),  # AprilTag Housing, PLA x4 = the 4 AprilTag holders
    (("P15",), ("3DP_grip06_apriltag_tile",),
     "The team BOM lists 12 tiles; Fusion has 16 (eight per gripper). UNVERIFIED."),
    (("P16",), ("3DP_cam01_gimbal_mount",),
     ""),  # Gimbal Base, PLA x2 = the 2 camera-column bases
    (("P17",), ("3DP_cam02_gimbal_neck",),
     ""),  # Gimbal Neck, PLA x2 = the 2 camera-column necks
    (("P18", "P19"), ("3DP_cam03_gimbal_arm", "3DP_cam04_gimbal_arm_link"),
     "The team BOM's two remaining camera-column lines (Gimbal Shaft and Gimbal Support, 2 pieces "
     "each) cover these two components (2 each). Which line is which part is UNVERIFIED."),
    (("P20", "P21", "P24", "P25"),
     ("3DP_legP01_hip3_cover_a", "3DP_legP02_hip3_cover_b", "3DP_legP03_hip3_cover_c", "3DP_legP04_hip3_cover_d"),
     "The team BOM's Hip 1 and Hip 3 protection lines (4 lines, 8 pieces) cover the four Fusion "
     "components that carry the material `hip3_protection` (8 occurrences: 3, 3, 1, 1). Which line "
     "is which cover, and the per-cover counts, are UNVERIFIED."),
    (("P22", "P23"), ("3DP_legP05_hip2_cover_a", "3DP_legP06_hip2_cover_b"),
     "The team BOM's Hip 2 protection A and B (2 pieces each) are the two Fusion components with "
     "the material `hip2_protection` (2 occurrences each). Which line is A and which is B is UNVERIFIED."),
    (("P26", "P27"), ("3DP_legP07_knee_cover_a", "3DP_legP08_knee_cover_b"),
     "The team BOM's Knee protection A and B (2 pieces each) are the two Fusion components with "
     "the material `knee protection` (2 occurrences each). Which line is A and which is B is UNVERIFIED."),
    (("P28",), ("3DP_legP09_shank_cover_a", "3DP_legP10_shank_cover_b"),
     "One team BOM line of 4 pieces over the two Fusion components with the material `shank "
     "protection`, which have 1 occurrence each. The count is UNVERIFIED."),
    (("P29", "P30"), ("3DP_legP11_ankle_cover_a", "3DP_legP12_ankle_cover_b"),
     "The team BOM's Foot Protection Top and Bot (2 pieces each) are matched to the two Fusion "
     "components with the material `ANKLE_1_PROTECTION` (2 occurrences each), the only leg covers "
     "left once the sole and the front cap are matched. UNVERIFIED."),
    (("P31",), ("3DP_leg20_foot_front",),
     ""),  # Foot Protection - Front, TPU x2 = Fusion `foot_front`, 2 occurrences
    (("P32",), ("3DP_leg19_sole",),
     ""),  # Foot Protection - Sole, TPU x2 = Fusion `symmetric_sole`, 2 occurrences
    (("P33", "P34"), ("3DP_armP07_shoulder_cover_e", "3DP_armP08_shoulder_cover_f"),
     "The team BOM's Shoulder 2 protection A and B (2 pieces each) are matched to the two Fusion "
     "components with the material `measured_shoulder_protection` (2 occurrences each). The four "
     "`shoulder_protection` covers are the other candidate and have no team BOM line at all. UNVERIFIED."),
    (("P35", "P36"), ("3DP_armP09_shoulder_yaw_cover_a", "3DP_armP10_shoulder_yaw_cover_b"),
     "The team BOM's Arm Roll protection Front and Back (4 pieces each) are the two Fusion "
     "components with the material `shoulder_yaw_protection` and 4 occurrences each. Which line "
     "is front and which is back is UNVERIFIED."),
    (("P37", "P38"), ("3DP_armP01_elbow_cover_a", "3DP_armP02_elbow_cover_b"),
     "The team BOM's Elbow protection A and B (2 pieces each) are the two Fusion components with "
     "the material `elbow_protection` (2 occurrences each). Which line is A and which is B is UNVERIFIED."),
    # P39 "Arm Roll Shaft Protection, TPU" x8 has no CAD match; it is emitted below
    # as its own row. Candidates, neither confirmed: the four `shoulder_protection`
    # covers (3DP_armP03-P06, 8 occurrences) or 3DP_armP11 (4 occurrences).
]

# Sheet rows with no CAD match: part_id = team_ref.
PRINTED_NO_CAD = {
    "P39": ("arm", "Arm-roll shaft protection (team BOM name)",
            "No CAD match yet. The Fusion components left without a team BOM line are the four "
            "`shoulder_protection` covers `3DP_armP03`-`3DP_armP06` (8 occurrences, which is this "
            "line's 8 pieces) and `3DP_armP11` (4 occurrences); neither is confirmed."),
}

# The three filament / powder rows. The team BOM has no line for them, but it
# does carry a price per unit weight per material, which is recorded here.
MATERIAL_ROWS = [
    ("MAT_TPU", "TPU filament (printed parts)", "TPU", "FDM", "34.99"),
    ("MAT_PLA", "PLA filament (printed parts)", "PLA", "FDM", "12.47"),
    ("MAT_SLS_NYLON", "Nylon 12 powder for SLS (printed parts)", "Nylon 12", "SLS", "99.9"),
]


# --------------------------------------------------------------------------- #
# spreadsheet
# --------------------------------------------------------------------------- #
class Sheet:
    """The spreadsheet's part rows, keyed by the `#` column (E0, C21, P20, H1)."""

    def __init__(self, path: Path):
        import openpyxl  # imported here so the module can be read without it

        ws = openpyxl.load_workbook(path, data_only=True)["Sheet1"]
        self.rows: dict[str, dict] = {}
        self.order: list[str] = []
        self.sum_total = self.sum_qty = None
        for cells in ws.iter_rows(min_row=2, values_only=True):
            category, ref, item, link, unit, qty, total = (cells + (None,) * 7)[:7]
            weight, per_weight = cells[8], cells[9]
            if category == "SUM":
                self.sum_total, self.sum_qty = _dec(unit), _dec(qty)
                continue
            if not ref or not item:
                continue
            self.rows[str(ref).strip()] = dict(
                ref=str(ref).strip(), category=str(category).strip(), item=str(item).strip(),
                link=(link or "").strip(), unit=_dec(unit), qty=_dec(qty), total=_dec(total),
                weight=_dec(weight), per_weight=_dec(per_weight))
            self.order.append(str(ref).strip())

    def __getitem__(self, ref: str) -> dict:
        return self.rows[ref]

    def of_category(self, category: str) -> list[dict]:
        return [self.rows[r] for r in self.order if self.rows[r]["category"] == category]


def _dec(value) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except Exception:
        return None


def _plain(value: Decimal | None) -> str:
    """Decimal -> the digits the CSV carries, without exponent or trailing zeros."""
    if value is None:
        return ""
    text = format(value.normalize(), "f")
    return text


def vendor_of(link: str, seen_unknown: set[str]) -> str:
    if not link:
        return ""
    host = re.sub(r"^https?://", "", link).split("/")[0].lower()
    host = host[4:] if host.startswith("www.") else host
    for domain, name in VENDORS.items():
        if host == domain or host.endswith("." + domain):
            return name
    seen_unknown.add(host)
    return host


def price_note(row: dict, cad: tuple[str, str] | None = None) -> list[str]:
    """The note a row gets for its price and its weight column.

    `cad` is (mass_g, children) of the Fusion component the row maps to, so the
    sheet's weight is checked against the export rather than asserted to match.
    """
    notes = []
    if row["unit"] is None or row["unit"] == 0:
        notes.append(NO_PRICE)
    if row["weight"] is not None:
        grams = row["weight"] * 1000
        notes.append(
            f"Team BOM weight {_plain(row['weight'])} and price per unit weight "
            f"{_plain(row['per_weight'])}; their product is the unit cost. The sheet states no "
            f"unit for the weight (its column is headed `weight (check urdf)`); read as "
            f"kilograms it is {grams:.1f} g, " + weight_check(grams, cad))
    elif row["per_weight"] is not None:
        notes.append(f"Team BOM price per unit weight {_plain(row['per_weight'])}, no weight.")
    return notes


def weight_check(grams: Decimal, cad: tuple[str, str] | None) -> str:
    """How the sheet's weight compares with the Fusion mass of the mapped component."""
    if not cad or not cad[0]:
        return "which no Fusion mass is available to check."
    mass, children = Decimal(cad[0]), int(cad[1] or 0)
    close = abs(grams - mass) <= Decimal("0.15")
    if close and not children:
        return f"which equals the Fusion mass of the component ({mass} g)."
    if close:
        return (f"which equals the Fusion mass of the component with its {children} child "
                f"component(s) ({mass} g).")
    if children:
        return (f"which cannot be checked against the export: the Fusion mass ({mass} g) includes "
                f"{children} child component(s) and the component's own mass is not exported.")
    return f"which does NOT equal the Fusion mass of the component ({mass} g). UNVERIFIED."


def joined(notes: list[str]) -> str:
    """Notes as one sentence stream, each sentence once, in the order given."""
    seen, out = set(), []
    for n in notes:
        n = n.strip()
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return " ".join(out)


def new_row(**kw) -> dict:
    row = {c: "" for c in COLS}
    row.update(kw)
    return row


def costs(row: dict) -> dict:
    """unit_cost_usd / priced_as_of for a spreadsheet row, blank when unpriced."""
    if row["unit"] is None or row["unit"] == 0:
        return dict(unit_cost_usd="", priced_as_of="")
    return dict(unit_cost_usd=_plain(row["unit"]), priced_as_of=PRICED_AS_OF)


# --------------------------------------------------------------------------- #
# builders
# --------------------------------------------------------------------------- #
def build_purchased(sheet: Sheet, unknown_hosts: set[str]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {ACT_FILE: [], EL_FILE: [], CAB_FILE: [], FAS_FILE: []}
    for ref, csv_name, pid, sub, desc, mpn, extra in PURCHASED:
        src = sheet[ref]
        notes = [f"Team BOM {ref}: \"{src['item']}\"."]
        if extra:
            notes.append(extra)
        notes += price_note(src)
        out[csv_name].append(new_row(
            subassembly=sub, **{"class": "off_the_shelf"}, part_id=pid, description=desc, mpn=mpn,
            vendor=vendor_of(src["link"], unknown_hosts), vendor_url=src["link"],
            qty_per_robot=_plain(src["qty"]), **costs(src),
            notes=joined(notes), team_ref=ref))
    return out


def build_cnc(sheet: Sheet) -> list[dict]:
    rows = []
    for ref, pid, extra in CNC_MAP:
        src = sheet[ref]
        notes = [f"Team BOM {ref}: \"{src['item']}\", {_plain(src['qty'])} off."]
        if extra:
            notes.append(extra)
        notes += price_note(src)
        rows.append(new_row(
            subassembly=subassembly_of(pid), **{"class": "machined"}, part_id=pid,
            description=src["item"], qty_per_robot=_plain(src["qty"]), **costs(src),
            process="CNC", notes=joined(notes), team_ref=ref))
    for pid, sub, desc, extra in CNC_EXTRA:
        rows.append(new_row(
            subassembly=sub, **{"class": "machined"}, part_id=pid, description=desc,
            process="CNC", notes=joined([NOT_IN_BOM, extra]), team_ref=""))
    rank = {"leg": 0, "arm": 1, "body": 2}
    rows.sort(key=lambda r: (rank[r["subassembly"]], r["part_id"]))
    return rows


def subassembly_of(part_id: str) -> str:
    for key in ("leg", "arm", "body"):
        if part_id.startswith("CNC_" + key):
            return key
    raise SystemExit("unclassified machined part: " + part_id)


SHEET_MATERIALS = [("Nylon 12", "SLS"), ("TPU", "FDM"), ("PLA", "FDM")]


def sheet_material(item: str) -> tuple[str, str]:
    """Material and process from the 3DP item name's suffix, e.g. `..., TPU`."""
    for needle, process in SHEET_MATERIALS:
        if re.search(r"[,\s]" + re.escape(needle) + r"\s*$", item):
            return needle, process
    return "", ""


def build_printed(sheet: Sheet, tree: dict[str, list[dict]]) -> tuple[list[dict], list[str]]:
    """One row per CAD printed part, then the sheet rows with no CAD part."""
    cad = {pid: (key, sub, desc) for key, pid, sub, desc in PRINTED}
    mapped: dict[str, tuple[tuple[str, ...], str]] = {}
    for refs, pids, note in PRINTED_MAP:
        for pid in pids:
            if pid not in cad:
                raise SystemExit(f"PRINTED_MAP points at {pid}, which gen_printed.PRINTED has no entry for")
            mapped[pid] = (refs, note)

    rows, warnings = [], []
    for key, pid, sub, desc in PRINTED:
        occ = pick(tree, key)
        if not occ:
            warnings.append(f"{pid}: Fusion component `{key}` is not in the tree; row skipped")
            continue
        first = occ[0]
        qty = sum(int(r["qty"]) for r in occ)
        cad_material, cad_process = material_of(first["material"])
        fusion_name = re.sub(r" \(\d+\)$", "", first["fusion_name"])
        cad_note = (f"Fusion component `{fusion_name}`, material `{first['material']}`, "
                    f"{qty} occurrence(s), {first['mass_g'] or '?'} g each in CAD.")

        refs, map_note = mapped.get(pid, ((), ""))
        notes: list[str] = []
        material, process, unit, priced = cad_material, cad_process, "", ""
        if refs:
            src = [sheet[r] for r in refs]
            items = "; ".join(f"{r['ref']} \"{r['item']}\" x{_plain(r['qty'])}" for r in src)
            notes.append(f"Team BOM {items}.")
            if map_note:
                notes.append(map_note)
            sheet_qty = sum((r["qty"] or 0) for r in src)
            if len(mapped_ids(pid)) == 1 and sheet_qty != qty:
                notes.append(f"The team BOM says {_plain(sheet_qty)} pieces, the Fusion model {qty}. UNVERIFIED.")
            material, process = sheet_material(src[0]["item"])
            if cad_material and material and material.lower() not in cad_material.lower():
                notes.append(f"MATERIAL CONFLICT: the team BOM says {material}, Fusion says "
                             f"`{first['material']}` ({cad_material}). UNVERIFIED.")
            elif not cad_material:
                notes.append(f"Material from the team BOM line only; the Fusion material name "
                             f"`{first['material']}` is not a print material.")
            unit_costs = {_plain(r["unit"]) for r in src if r["unit"]}
            if len(unit_costs) > 1:
                notes.append(f"The team BOM prices its lines differently ({', '.join(sorted(unit_costs))}); "
                             f"no unit cost is written here. UNVERIFIED.")
            elif unit_costs:
                unit, priced = unit_costs.pop(), PRICED_AS_OF
            else:
                notes.append(NO_PRICE)
            for r in src:
                notes += [n for n in price_note(r, (first["mass_g"], first["children"])) if n != NO_PRICE]
        else:
            notes.append(NOT_IN_BOM)
        notes.append(cad_note)
        if int(first["children"]):
            notes.append(f"The Fusion component carries {first['children']} child component(s): "
                         f"its CAD mass includes them.")
        rows.append(new_row(
            subassembly=sub, **{"class": "printed"}, part_id=pid, description=desc,
            qty_per_robot=str(qty), unit_cost_usd=unit, priced_as_of=priced,
            material=material, process=process, notes=joined(notes),
            team_ref=", ".join(refs)))

    for ref, (sub, desc, note) in PRINTED_NO_CAD.items():
        src = sheet[ref]
        material, process = sheet_material(src["item"])
        notes = [f"Team BOM {ref}: \"{src['item']}\", {_plain(src['qty'])} off.", note]
        notes += price_note(src)
        rows.append(new_row(
            subassembly=sub, **{"class": "printed"}, part_id=ref, description=desc,
            qty_per_robot=_plain(src["qty"]), **costs(src), material=material, process=process,
            notes=joined(notes), team_ref=ref))

    for pid, desc, material, process, per_weight in MATERIAL_ROWS:
        rows.append(new_row(
            subassembly="printed", **{"class": "consumable"}, part_id=pid, description=desc,
            material=material, process=process, team_ref="",
            notes=(f"The team BOM has no line for the filament or powder itself; it prices the "
                   f"{material} parts at {per_weight} per unit weight (no unit stated). Grade, "
                   f"vendor and quantity are not recorded anywhere in the release.")))
    return rows, warnings


def mapped_ids(part_id: str) -> tuple[str, ...]:
    """The CAD part_ids the same team BOM line(s) as `part_id` cover."""
    for _, pids, _ in PRINTED_MAP:
        if part_id in pids:
            return pids
    return (part_id,)


# --------------------------------------------------------------------------- #
def write(name: str, rows: list[dict]) -> Decimal:
    ids = [r["part_id"] for r in rows]
    assert len(ids) == len(set(ids)), f"{name}: duplicate part_id"
    with open(DATA / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows([{k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()} for r in rows])
    total = sum((Decimal(r["unit_cost_usd"]) * Decimal(r["qty_per_robot"])
                 for r in rows if r["unit_cost_usd"] and r["qty_per_robot"]), Decimal(0))
    unpriced = [r["part_id"] for r in rows if not r["unit_cost_usd"]]
    print(f"{name:24s} rows={len(rows):3d}  unpriced={len(unpriced):3d}  subtotal={total:12.4f}")
    if unpriced:
        print(f"{'':26s}no price: {', '.join(unpriced)}")
    return total


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    xlsx = Path(sys.argv[1]) if len(sys.argv) > 1 else XLSX
    if not xlsx.is_file():
        sys.exit(f"team BOM not found: {xlsx}")
    sheet = Sheet(xlsx)
    tree = load_tree(find_tree(sys.argv[2] if len(sys.argv) > 2 else None))

    unknown_hosts: set[str] = set()
    bought = build_purchased(sheet, unknown_hosts)
    cnc = build_cnc(sheet)
    printed, warnings = build_printed(sheet, tree)

    grand = Decimal(0)
    for name, rows in ((ACT_FILE, bought[ACT_FILE]), (EL_FILE, bought[EL_FILE]),
                       (CAB_FILE, bought[CAB_FILE]), (FAS_FILE, bought[FAS_FILE]),
                       ("cnc-parts.csv", cnc), ("printed-parts.csv", printed)):
        grand += write(name, rows)

    # Which spreadsheet rows ended up where, and what the arithmetic says.
    used = {r["team_ref"] for rows in (list(bought.values()) + [cnc, printed]) for r in rows} - {""}
    used = {ref.strip() for group in used for ref in group.split(",")}
    unused = [r for r in sheet.order if r not in used]
    sheet_total = sum((sheet[r]["total"] or 0) for r in sheet.order)
    sheet_qty = sum((sheet[r]["qty"] or 0) for r in sheet.order)

    print(f"\nsite subtotal (6 CSVs):      {grand:12.4f}")
    print(f"team BOM, sum of Total Cost: {sheet_total:12.4f}   (its SUM cell: {sheet.sum_total})")
    print(f"team BOM, sum of Quantity:   {sheet_qty:12.0f}   (its SUM cell: {sheet.sum_qty})")
    print(f"difference:                  {grand - sheet_total:12.4f}")
    print(f"\nteam BOM rows: {len(sheet.order)}, used: {len(used)}, not used: {unused or 'none'}")
    if unknown_hosts:
        print(f"vendor name not in VENDORS, host used as the name: {', '.join(sorted(unknown_hosts))}")
    for w in warnings:
        print("WARNING " + w, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
