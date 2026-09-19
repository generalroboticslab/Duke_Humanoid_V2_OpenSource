"""Fusion 360 script: export the Duke Humanoid V2 release CAD in one run.

Run it from Fusion 360 with the robot design (humanoid_2.1_latest) open:
  UTILITIES > ADD-INS > Scripts and Add-Ins > Scripts > fusion_export > Run

It asks for an output folder, then writes:

  <out>/tree.csv                 every component: path, name, qty, bodies, material,
                                 mass, bounding box, linked?, out-of-date?  (always)
  <out>/assembly/<design>.step   whole-robot STEP                            (full run)
  <out>/assembly/<design>.f3z    native Fusion archive, linked designs included
  <out>/step/<component>.step    one STEP per leaf component (part), deduplicated
  <out>/print/<component>.stl    one high-resolution STL per leaf component
  <out>/export.log               what was written, what failed, Fusion version

File names are the Fusion component names, sanitised. Rename the files (or the
components) to the `part_id` used in hardware-site/docs/data/*.csv, then copy
them into hardware-site/docs/files/{assembly,step,print}/ as
<part_id>_rev01.<ext> and run tools/gen_cad_manifest.py.

Nothing here modifies the design. Out-of-date linked components are reported,
not updated: use Get Latest in the browser before a release export.
"""

import csv
import datetime
import os
import re
import traceback

import adsk.core
import adsk.fusion

_app = None
_ui = None
_log_lines = []


def log(msg):
    _log_lines.append(msg)


def safe_name(name):
    name = re.sub(r"\s*v\d+$", "", name.strip())          # drop Fusion's " v12" version suffix
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return name.strip("_") or "unnamed"


def bbox_mm(comp):
    try:
        bb = comp.boundingBox
        return [round((bb.maxPoint.x - bb.minPoint.x) * 10, 1),
                round((bb.maxPoint.y - bb.minPoint.y) * 10, 1),
                round((bb.maxPoint.z - bb.minPoint.z) * 10, 1)]
    except Exception:
        return ["", "", ""]


def mass_g(comp):
    try:
        return round(comp.physicalProperties.mass * 1000, 1)
    except Exception:
        return ""


def materials(comp):
    names = []
    for b in comp.bRepBodies:
        try:
            n = b.material.name
        except Exception:
            n = ""
        if n and n not in names:
            names.append(n)
    return "; ".join(names)


def walk(root):
    """Collect every component once, with qty = number of occurrences and the first path."""
    comps = {}
    for occ in root.allOccurrences:
        comp = occ.component
        key = comp.id if hasattr(comp, "id") else comp.name
        entry = comps.get(key)
        if entry is None:
            entry = dict(
                comp=comp,
                name=comp.name,
                path=occ.fullPathName,
                qty=0,
                children=comp.occurrences.count,
                bodies=comp.bRepBodies.count,
                linked=occ.isReferencedComponent,
                out_of_date="",
                visible=occ.isVisible,
            )
            for attr in ("isOutOfDate",):
                try:
                    entry["out_of_date"] = bool(getattr(occ, attr))
                except Exception:
                    pass
            comps[key] = entry
        entry["qty"] += 1
    return list(comps.values())


def write_tree(entries, out):
    path = os.path.join(out, "tree.csv")
    cols = ["fusion_name", "file_name", "kind", "qty", "bodies", "children", "material",
            "mass_g", "bbox_x_mm", "bbox_y_mm", "bbox_z_mm", "linked", "out_of_date", "path"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for e in sorted(entries, key=lambda e: e["path"]):
            kind = "part" if e["children"] == 0 and e["bodies"] > 0 else (
                "subassembly" if e["children"] else "empty")
            bx, by, bz = bbox_mm(e["comp"])
            w.writerow([e["name"], safe_name(e["name"]), kind, e["qty"], e["bodies"], e["children"],
                        materials(e["comp"]) if kind == "part" else "",
                        mass_g(e["comp"]), bx, by, bz, e["linked"], e["out_of_date"], e["path"]])
    log("wrote %s (%d components)" % (path, len(entries)))
    return path


def export_step(em, comp, path):
    opts = em.createSTEPExportOptions(path, comp)
    return em.execute(opts)


def export_stl(em, comp, path):
    opts = em.createSTLExportOptions(comp, path)
    opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    opts.isBinaryFormat = True
    return em.execute(opts)


def export_archive(em, design, path):
    opts = em.createFusionArchiveExportOptions(path)
    return em.execute(opts)


def run(context):
    global _app, _ui
    _app = adsk.core.Application.get()
    _ui = _app.userInterface
    try:
        design = adsk.fusion.Design.cast(_app.activeProduct)
        if not design:
            _ui.messageBox("Open the robot design first.")
            return
        root = design.rootComponent
        design_name = safe_name(_app.activeDocument.name)

        dlg = _ui.createFolderDialog()
        dlg.title = "Choose the export folder (a new dated subfolder is created inside)"
        if dlg.showDialog() != adsk.core.DialogResults.DialogOK:
            return
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        out = os.path.join(dlg.folder, "%s_%s" % (design_name, stamp))
        for sub in ("assembly", "step", "print"):
            os.makedirs(os.path.join(out, sub), exist_ok=True)

        log("Fusion %s, design %s, root %s" % (_app.version, _app.activeDocument.name, root.name))
        entries = walk(root)
        stale = [e["name"] for e in entries if e["out_of_date"] is True]
        if stale:
            log("OUT OF DATE linked components: " + ", ".join(stale))
        write_tree(entries, out)

        parts = [e for e in entries if e["children"] == 0 and e["bodies"] > 0]
        choice = _ui.messageBox(
            "%d components, %d leaf parts.\n%s\n\n"
            "YES = full export (whole-robot STEP + f3z, STEP and STL per part).\n"
            "NO  = tree.csv only.\n\nOutput: %s"
            % (len(entries), len(parts),
               ("WARNING: %d linked components are out of date. Use Get Latest first for a release export." % len(stale))
               if stale else "No out-of-date linked components detected.", out),
            "Duke Humanoid V2 export", adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType)
        if choice == adsk.core.DialogResults.DialogCancel:
            return
        if choice == adsk.core.DialogResults.DialogYes:
            em = design.exportManager
            prog = _ui.createProgressDialog()
            prog.isCancelButtonShown = True
            prog.show("Exporting", "Whole robot STEP", 0, len(parts) * 2 + 2)

            for label, fn in (("whole-robot STEP", lambda: export_step(em, root, os.path.join(out, "assembly", design_name + ".step"))),
                              ("Fusion archive", lambda: export_archive(em, design, os.path.join(out, "assembly", design_name + ".f3z")))):
                prog.message = label
                try:
                    log("%s: %s" % (label, "ok" if fn() else "FAILED"))
                except Exception:
                    log("%s: EXCEPTION %s" % (label, traceback.format_exc().splitlines()[-1]))
                prog.progressValue += 1
                adsk.doEvents()

            for e in parts:
                if prog.wasCancelled:
                    log("cancelled by user")
                    break
                fname = safe_name(e["name"])
                for kind, sub, ext, fn in (("STEP", "step", ".step", export_step), ("STL", "print", ".stl", export_stl)):
                    prog.message = "%s %s" % (kind, fname)
                    path = os.path.join(out, sub, fname + ext)
                    try:
                        ok = fn(em, e["comp"], path)
                        log("%s %s: %s" % (kind, fname, "ok" if ok else "FAILED"))
                    except Exception:
                        log("%s %s: EXCEPTION %s" % (kind, fname, traceback.format_exc().splitlines()[-1]))
                    prog.progressValue += 1
                    adsk.doEvents()
            prog.hide()

        with open(os.path.join(out, "export.log"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(_log_lines) + "\n")
        failed = sum(1 for l in _log_lines if "FAILED" in l or "EXCEPTION" in l)
        _ui.messageBox("Done. %d problems (see export.log).\n%s" % (failed, out))
    except Exception:
        if _ui:
            _ui.messageBox("Failed:\n" + traceback.format_exc())
