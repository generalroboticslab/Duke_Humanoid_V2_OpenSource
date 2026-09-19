"""Generate actuators / electronics / cables-connectors / fasteners / printed-parts
CSVs from BOM Sheet1. Every description, link, price and quantity below is
transcribed from duke-humanoid-v2_BOM_sheet1_main.csv. Nothing is added.
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

import csv, os
from decimal import Decimal

OUT = str(DATA)
COLS = ["subassembly","class","part_id","description","mpn","vendor","vendor_url",
        "alt_mpn","alt_url","qty_per_robot","unit_cost_usd","total_cost_usd",
        "material","process","tolerance_finish","lead_time_days","priced_as_of","notes"]

PROVISIONAL = ""   # stated once per page instead of once per row
RS_ALT = ("SUPPLY RISK, no alternate published. A different actuator model changes the "
          "mounting interface, the shaft and the CAN configuration, so it is not a drop-in "
          "substitution.")

def R(sub, cls, pid, desc, qty, unit, vendor, url, mpn="", notes="", **kw):
    row = {c: "" for c in COLS}
    row.update(subassembly=sub, **{"class": cls}, part_id=pid, description=desc,
               mpn=mpn, vendor=vendor, vendor_url=url,
               qty_per_robot=str(qty) if qty is not None else "",
               unit_cost_usd=unit if unit is not None else "",
               notes=notes)
    row.update(kw)
    return row

# --------------------------------------------------------------- actuators
ACT = [
    R("actuators","off_the_shelf","ACT_RS00","RobStride 00 quasi-direct-drive actuator",2,"125.00",
      "RobStride","https://www.robstride.com/products/robStride00","RobStride 00", RS_ALT),
    R("actuators","off_the_shelf","ACT_RS02","RobStride 02 quasi-direct-drive actuator",6,"145.00",
      "RobStride","https://www.robstride.com/products/robStride02","RobStride 02", RS_ALT),
    R("actuators","off_the_shelf","ACT_RS03","RobStride 03 quasi-direct-drive actuator",11,"225.00",
      "RobStride","https://www.robstride.com/products/robStride03","RobStride 03", RS_ALT),
    R("actuators","off_the_shelf","ACT_RS04","RobStride 04 quasi-direct-drive actuator",2,"255.00",
      "RobStride","https://www.robstride.com/products/robStride04","RobStride 04", RS_ALT),
    R("actuators","off_the_shelf","ACT_RS05","RobStride 05 quasi-direct-drive actuator",6,"110.00",
      "RobStride","https://www.robstride.com/products/robStride05","RobStride 05",
      "Quoted below the RS 02 and the RS 00 in the source sheet, which does not follow the "
      "model numbering; re-check with the vendor before ordering. " + RS_ALT),
    R("actuators","off_the_shelf","ACT_RS06","RobStride 06 quasi-direct-drive actuator",4,"210.00",
      "RobStride","https://www.robstride.com/products/robStride06","RobStride 06", RS_ALT),
]

# ------------------------------------------------------------- electronics
AMZ, ALI = "Amazon", "AliExpress"
ELE = [
    R("electronics","off_the_shelf","EL_COMPUTE_MINIPC","MINISFORUM X1-470 mini PC (onboard computer)",1,"1295.00",
      AMZ,"https://www.amazon.com/MINISFORUM-Desktop-Computer-HDMI2-1-Graphics/dp/B0GM43XCGT","X1-470",
      "Module (III) on the hardware overview figure. Source link was recorded without a scheme; "
      "https:// added. "),
    R("electronics","off_the_shelf","EL_BATTERY_6S","Zeee 6S LiPo battery, 10000 mAh, 22.2 V, 2-pack",1,"306.00",
      AMZ,"https://www.amazon.com/dp/B0BHQX8XQX","",
      "Priced as one 2-pack, which is how the source sheet records it. How many packs one robot "
      "needs, and whether both cells are carried at once, is not stated in the source. "),
    R("electronics","off_the_shelf","EL_CAM_D436","Intel RealSense D436 depth camera",2,"354.00",
      "RealSense Store","https://store.realsenseai.com/buy-intel-realsense-depth-camera-d436.html","D436",
      "SUPPLY RISK, no alternate published. One per camera gimbal. The workspace study assumes "
      "this camera's 90x65 degree RGB field of view, so a substitute changes the result the "
      "design was optimised for. "),
    R("electronics","off_the_shelf","EL_IMU_TM171","SYD Dynamics TransducerM TM171 9-axis AHRS, dual-port",1,"57.00",
      "RobotShop","https://www.robotshop.com/products/syd-dynamics-transducerm-tm171-9-axis-ahrs-w-dual-port-communication","TM171",
      "Listed in the source sheet only as \"IMU\"; the model is read from the vendor link. "),
    R("electronics","off_the_shelf","EL_CAN_ADAPTER","CANable PRO V2.0 USB-CAN controller",6,"20.80",
      AMZ,"https://www.amazon.com/Macrobase-PRO-V2-0-Controller-transceiver/dp/B0GJSRZLBV/","CANable PRO V2.0",
      "Six adapters; the bus topology that needs six is not documented in the source sheet and "
      "is not inferred here. "),
    R("electronics","off_the_shelf","EL_BUCK_12V_ENC","DC 20-60 V to 12 V encased buck converter",1,"18.99",
      AMZ,"https://www.amazon.com/gp/product/B0G2SV9PFY","", PROVISIONAL),
    R("electronics","off_the_shelf","EL_BUCK_48V_12V","48 V to 12 V buck converter",2,"2.70",
      ALI,"https://www.aliexpress.us/item/3256809688561615.html","", PROVISIONAL),
    R("electronics","off_the_shelf","EL_TVS_DIODE","TVS diode, 53 V working / 85 V clamping",10,"3.56",
      "DigiKey","https://www.digikey.com/en/products/detail/microchip-technology/M1-5KE62CA/4349574","",
      "Manufacturer part number not transcribed: the source records only the DigiKey link. "
      "Where the ten diodes are installed is not documented. "),
    R("electronics","off_the_shelf","EL_SERVO_DRIVER","Waveshare serial bus servo driver board, ST/SC series",2,"4.99",
      "Waveshare","https://www.waveshare.com/product/robotics/drivers-sensors/drivers/bus-servo-adapter-a.htm","",
      "Two boards for the two Feetech bus servos. "),
    R("electronics","off_the_shelf","EL_SERVO_FEETECH","Feetech HL-3915-C001 12 V servo, 14.2 kg-cm",2,"50.00",
      "AiFitLab","https://aifitlab.com/products/feetech-hl-3915-servo-motor","HL-3915-C001",
      "The role of these two servos is not stated in the source sheet. The robot has four camera "
      "gimbal axes (two gimbals x yaw and pitch), so two servos do not cover them on their own. "),
    R("electronics","off_the_shelf","EL_USB_HUB","Vention USB hub",3,"12.99",
      AMZ,"https://www.amazon.com/VENTION-Splitter-Expander-Chromebook-Surface/dp/B0D2XWJ99H","", PROVISIONAL),
]

# ------------------------------------------------------ cables & connectors
CAB = [
    R("harness","off_the_shelf","CBL_XT30_2P2","Amass XT30(2+2) connector, 5-piece pack (select the first colour option, XT30U(2+2)-F)",4,"5.00",
      ALI,"https://www.aliexpress.us/item/3256807585110718.html","",
      "Source text records the option as \"XT30U(2 2)-F\"; transcribed as written. "),
    R("harness","off_the_shelf","CBL_XT30_SET","XT30 male/female connector set, 30 pairs (Frienda)",1,"14.99",
      AMZ,"https://www.amazon.com/Connectors-Female-Pieces-Shrink-Battery/dp/B0BB2XF5SQ","", PROVISIONAL),
    R("harness","off_the_shelf","CBL_LOOM_025","Alex Tech cord protector / wire loom, 1/4 inch, 25 ft",1,"13.99",
      AMZ,"https://www.amazon.com/Alex-Tech-10ft-Protector-Sleeving/dp/B07FW86XV6/","",
      "The source describes this as 25 ft but its link reads 10 ft; confirm the length before "
      "ordering. "),
    R("harness","off_the_shelf","CBL_LOOM_038","Alex Tech cord protector / wire loom, 3/8 inch, 25 ft",1,"15.98",
      AMZ,"https://www.amazon.com/Alex-Tech-25ft-Protector-Sleeving/dp/B07FW4M7Z8/","", PROVISIONAL),
    R("harness","off_the_shelf","CBL_USBC_EXT","Duttek short USB-C extension cable, 40 Gbps",2,"9.76",
      AMZ,"https://www.amazon.com/dp/B0CWGW3LTJ","", PROVISIONAL),
    R("harness","off_the_shelf","CBL_USBA_USBC","USB-A to USB-C 3.1 Gen 2 cable",6,"9.99",
      AMZ,"https://www.amazon.com/Transfer-Charging-Samsung-SanDisk-Portable/dp/B09H2LLXPN","",
      "Six of these and six CANable adapters is consistent with one cable per adapter, but the "
      "source sheet does not say so. "),
    R("harness","off_the_shelf","CBL_USBC_RA","USB-C cable, 1 ft, right-angle plug",1,"12.99",
      AMZ,"https://www.amazon.com/Afterplug-Right-Angle-Charging-Ultra-Flexible-Silicone/dp/B0G2LVGZ39","", PROVISIONAL),
    R("harness","off_the_shelf","CBL_USBA_USBC_BELKIN","Belkin USB-A to USB-C cable, 6.6 ft, 2-pack",2,"14.99",
      AMZ,"https://www.amazon.com/Belkin-USB-Cable-2-Pack-6-6ft/dp/B0F63XNWN3","",
      "Grouped under ELECTRONICS in the source sheet; filed here with the rest of the cabling. "
      "Quantity 2 means two 2-packs. "),
]

# ---------------------------------------------------------------- fasteners
FAS = [
    R("fasteners","off_the_shelf","FAS_PLACEHOLDER",
      "PLACEHOLDER ROW -- the entire fastener, bearing and hardware schedule",
      None, None, "", "", "",
      "The source spreadsheet carries one row reading \"example: fasteners, nuts\", priced at "
      "$0.00 with no vendor and no quantity. Every screw, nut, washer, bearing, dowel pin and "
      "threadlocker in a 31-DoF, 36 kg machine is behind that one row. The $0.00 is replaced "
      "here by a blank so that it is skipped by the cost macros instead of being silently "
      "summed as zero: the true fastener cost is unknown, not nil."),
]

# ----------------------------------------------------------- printed parts
PRN = [
    R("printed","consumable","MAT_TPU","TPU filament (printed parts)",None,None,"","","",
      "No cost, quantity, grade, vendor or shore hardness in the source sheet. Which parts are "
      "printed in TPU is not recorded anywhere in the release.", material="TPU"),
    R("printed","consumable","MAT_PLA","PLA filament (printed parts)",None,None,"","","",
      "No cost, quantity, grade, vendor or printer in the source sheet. Whether this is plain "
      "PLA or a filled grade such as PLA-CF is not recorded.", material="PLA"),
    R("printed","consumable","MAT_SLS_NYLON","Nylon powder for SLS (printed parts)",None,None,"","","",
      "No cost, quantity, grade, vendor or service bureau in the source sheet. The polymer grade "
      "(PA11 vs PA12) is not recorded.", material="Nylon (SLS powder)", process="SLS"),
]

def write(name, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows([{k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()} for r in rows])
    tot = sum(Decimal(r["unit_cost_usd"]) * Decimal(r["qty_per_robot"])
              for r in rows if r["unit_cost_usd"] and r["qty_per_robot"])
    print(f"{name:26s} rows={len(rows):3d}  subtotal={tot}")
    return tot

grand = Decimal(0)
for n, rs in (("actuators.csv", ACT), ("electronics.csv", ELE),
              ("cables-connectors.csv", CAB), ("fasteners.csv", FAS),
              ("printed-parts.csv", PRN)):
    grand += write(n, rs)
print("sheet1-derived subtotal:", grand)
print("expected (sheet1 priced rows, fastener $0.00 row now blank):", Decimal("8492.13"))
