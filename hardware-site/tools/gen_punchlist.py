"""Generate docs/reference/todo.md from the TODO blocks on the pages themselves.

Why this is generated
---------------------
A punch list maintained by hand drifts away from the pages it tracks within a
week: an item gets closed on its page and lives on in the list, or it gets
opened on a page and never reaches the list. Deriving the list from the pages
makes both impossible. Close a block, re-run this, and the row is gone.

The contract every TODO block follows:

    !!! missing "MISSING — short statement of the gap"
        What is missing, in enough detail that the person who has the answer
        recognises it as theirs.
        *Owner: role who can supply it.*

    !!! unverified "UNVERIFIED — short statement of what is in doubt"
        What is stated, why it is not confirmed, and how to confirm it.
        *Owner: role who can confirm it.*

Both render red and bold (see docs/stylesheets/extra.css). Only boxes whose
title STARTS with MISSING or UNVERIFIED are tracked here. A missing/unverified
box with any other title is a page-level summary of gaps already itemised below
it — it renders the same red, but is not counted twice. ``MISSING — SAFETY``
in the title marks a safety item or something that stops a build outright; this
script reads that as *blocks release*. The
``*Owner:*`` line is mandatory — the script reports any block without one, and
an unowned TODO is a wish rather than a work item.

Usage:  python tools/gen_punchlist.py
"""

from __future__ import annotations

import os
import posixpath
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DOCS = SITE / "docs"
OUT = DOCS / "reference" / "todo.md"

# Pages that are not builder-facing content and carry no punch-list items.
SKIP = {"data/README.md", "reference/todo.md", "assets/MANIFEST.md"}

# Leading whitespace is captured, not forbidden: a TODO block nested inside a
# content tab (``=== "Route B"``) is indented, and anchoring this pattern at
# column zero silently dropped one such block from the published punch list
# while the page still displayed it. Every continuation line is then matched
# against *this block's* indent plus four spaces.
BLOCK_RE = re.compile(r'^([ \t]*)(!!!|\?\?\?\+?)\s+(missing|unverified)\s+"((?:MISSING|UNVERIFIED)[^"]*)"\s*$')
STEP_RE = re.compile(r'\{\{\s*step\(\s*([0-9]+)\s*,\s*"([^"]*)"')
H_RE = re.compile(r'^(#{1,4})\s+(.*)$')
JINJA_RE = re.compile(r'^\s*\{%-?\s*(if|elif|else|endif)\b')

SECTIONS = [
    ("before-you-start/", "Before you start"),
    ("bom/", "Bill of materials"),
    ("fabrication/", "Fabrication"),
    ("assembly/", "Assembly"),
    ("electrical/", "Electrical"),
    ("bringup/", "Bring-up"),
    ("reference/", "Reference"),
    ("", "Top level"),
]

# Pages whose every open item blocks the public release, because the home page's
# "Can you build this robot today?" banner names them as blockers.
BLOCKING_PAGES = {
    "fabrication/cad-downloads.md",
    "bom/fasteners-and-hardware.md",
    "reference/citation-and-license.md",
    "before-you-start/safety.md",
}

ROLES = [
    (r"hardware lead", "Hardware lead"),
    (r"electrical lead|\belectrical\b", "Electrical lead"),
    (r"controls lead|\bcontrols\b", "Controls lead"),
    (r"perception lead|\bperception\b", "Perception lead"),
    (r"\bPI\b", "PI"),
    (r"safety officer|signs off Safety|\bSafety\b", "Safety sign-off"),
    (r"EHS", "Local EHS office"),
    (r"BOM owner", "BOM owner"),
    (r"assembly lead", "Assembly lead"),
    (r"maintains CI", "Whoever maintains CI"),
    (r"performs the first|re-sources the parts|first external",
     "Whoever does the first build / re-sourcing"),
]

SECTION_NOTE = {
    "Assembly": (
        "Almost every row here reads `no`, and that is a reporting artefact rather\n"
        "than an all-clear: the home page names *no torque values and no threadlocker\n"
        "specification* as one single release blocker, and it is these rows, spread\n"
        "across every step of every limb. Treat the section as blocking and the rows\n"
        "as its inventory."
    ),
    "Bring-up": (
        "Bring-up cannot start until Electrical closes the pack-configuration item.\n"
        "Series versus parallel decides the bus voltage, and every current, converter\n"
        "and check below is written against a voltage nobody has confirmed."
    ),
}


# --------------------------------------------------------------------------- #
# extraction
# --------------------------------------------------------------------------- #

def jinja_true(line: str) -> bool | None:
    """Evaluate the two page conditions that depend on files, so a block in the
    branch that MkDocs does not render is not counted as an open item."""
    m = re.search(r'\{%-?\s*if\s+(.+?)\s*-?%\}', line)
    cond = m.group(1) if m else ""
    if cond == "cad_count()":
        p = DOCS / "data" / "cad-files.csv"
        return p.is_file() and len(p.read_text(encoding="utf-8").strip().splitlines()) > 1
    m = re.fullmatch(r'data_file_exists\("([^"]+)"\)', cond)
    if m:
        return (DOCS / "data" / m.group(1)).is_file()
    return None


def extract() -> list[dict]:
    out: list[dict] = []
    for root, _, files in os.walk(DOCS):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = Path(root) / fn
            # POSIX form on every OS: SKIP, SECTIONS and BLOCKING_PAGES are
            # written with '/'. On Windows str() gives backslashes, nothing
            # matches, and the list ends up scanning itself.
            rel = path.relative_to(DOCS).as_posix()
            if rel in SKIP or rel.startswith("data/"):
                continue
            lines = path.read_text(encoding="utf-8").split("\n")
            ctx_heading = ctx_step = ""
            # Context saved at each Jinja `{% if %}`. A heading inside the `if`
            # branch is not rendered when the `else` branch is, so a block in
            # the `else` branch must not link to it.
            jinja_stack: list[tuple[str, str]] = []
            # True/False when the condition is one this script can evaluate
            # (cad_count(), data_file_exists("x.csv")), None when it cannot.
            branch_stack: list[bool | None] = []
            for i, line in enumerate(lines):
                jm = JINJA_RE.match(line)
                if jm:
                    kw = jm.group(1)
                    if kw == "if":
                        jinja_stack.append((ctx_heading, ctx_step))
                        branch_stack.append(jinja_true(line))
                    elif kw in ("elif", "else") and jinja_stack:
                        ctx_heading, ctx_step = jinja_stack[-1]
                        if branch_stack:
                            branch_stack[-1] = None if branch_stack[-1] is None else not branch_stack[-1]
                    elif kw == "endif" and jinja_stack:
                        jinja_stack.pop()
                        branch_stack.pop()
                    continue
                if any(b is False for b in branch_stack):
                    continue   # this branch is not rendered, so its blocks are not open items
                h = H_RE.match(line)
                if h and h.group(1) != "#":
                    ctx_heading, ctx_step = h.group(2).strip(), ""
                s = STEP_RE.search(line)
                if s:
                    ctx_step = f"Step {s.group(1)} — {s.group(2)}"
                m = BLOCK_RE.match(line)
                if not m:
                    continue
                pad = m.group(1) + "    "
                body: list[str] = []
                j = i + 1
                while j < len(lines):
                    cur = lines[j]
                    if cur.strip() == "":
                        k = j
                        while k < len(lines) and lines[k].strip() == "":
                            k += 1
                        if k < len(lines) and lines[k].startswith(pad):
                            body.append("")
                            j = k
                            continue
                        break
                    if not cur.startswith(pad):
                        break
                    body.append(cur[len(pad):])
                    j += 1
                body_txt = "\n".join(body).strip()
                mo = re.search(r"\*Owner:\s*(.+?)\*", body_txt, re.S)
                out.append(dict(
                    file=rel, line=i + 1, kind=m.group(3), title=m.group(4),
                    context=ctx_step or ctx_heading, body=body_txt,
                    owner=" ".join(mo.group(1).split()).rstrip(".") if mo else "",
                ))
    return out


# --------------------------------------------------------------------------- #
# shaping
# --------------------------------------------------------------------------- #

def slug(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_]", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def clean(t: str) -> str:
    t = re.sub(r"\*Owner:.*", "", t, flags=re.S)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\{\s*\.dh-[a-z]+\s*\}", "", t)   # inline red-marker attribute lists
    # Strip emphasis markers only. Underscores inside words (CNC_leg02_...) and
    # anything inside a code span are part numbers and paths, and must survive.
    parts = re.split(r"(`[^`]*`)", t)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<!\w)[*_]{1,2}|[*_]{1,2}(?!\w)", "", parts[i])
    t = "".join(parts)
    t = t.replace("|", "/").replace("\n", " ")
    t = re.sub(r"^\s*[-*]\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


def summarise(item: dict, limit: int = 210) -> str:
    body = item["body"]
    m = re.match(r"(?:MISSING|UNVERIFIED)(?:\s*—\s*SAFETY)?\s*—\s*(.+)", item["title"])
    title_detail = m.group(1).strip() if m else ""
    bullets: list[str] = []
    for line in body.split("\n"):
        if re.match(r"^\s*[-*]\s+", line):
            bullets.append(re.sub(r"^\s*[-*]\s+", "", line).strip())
        elif bullets and line.strip() and not line.strip().startswith("*Owner"):
            bullets[-1] += " " + line.strip()
    if bullets:
        pieces = [clean(b) for b in bullets]
    else:
        pieces = [clean(p) for p in re.split(r"(?<=[.;])\s+", clean(body)) if p.strip()]
    text = ""
    for p in pieces:
        if not p:
            continue
        cand = (text + "; " + p) if text else p
        if len(cand) > limit and text:
            text += " …"
            break
        text = cand
        if len(text) > limit:
            text = text[:limit].rsplit(" ", 1)[0] + " …"
            break
    if title_detail:
        text = title_detail[0].upper() + title_detail[1:] + (" — " + text if text else "")
    if len(text) > limit + 40:
        text = text[:limit].rsplit(" ", 1)[0] + " …"
    return text or clean(item["title"])


def blocking(item: dict) -> bool:
    if "SAFETY" in item["title"]:
        return True
    if item["file"] in BLOCKING_PAGES:
        return True
    return bool(re.search(r"\bblocks?\b|\bblocking\b",
                          item["title"] + " " + item["body"], re.I))


def owner_text(item: dict) -> str:
    o = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", item["owner"])
    for pat in (r"\s*Blocks .*$", r"\s*See .*$", r"\s*Column contract.*$",
                r"\s*This is a safety item.*$"):
        o = re.sub(pat, "", o)
    return o.rstrip(" .") or "unassigned"


def roles(item: dict) -> list[str]:
    found: list[str] = []
    for pat, name in ROLES:
        if re.search(pat, item["owner"], re.I) and name not in found:
            found.append(name)
    return found or ["Unassigned"]


def section_of(f: str) -> str:
    for pref, name in SECTIONS:
        if (f.startswith(pref) if pref else True):
            return name
    return "Top level"


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #

def render(items: list[dict]) -> str:
    total = len(items)
    nblock = sum(1 for i in items if i["_block"])
    npages = len({i["file"] for i in items})
    by_section: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        by_section[section_of(it["file"])].append(it)
    owners: Counter[str] = Counter()
    for it in items:
        for r in it["_roles"]:
            owners[r] += 1

    L: list[str] = []
    w = L.append
    w("# Open items — the punch list")
    w("")
    w(f"Every unresolved item on this site, in one table: **{total} open items** "
      f"across **{npages} pages**, of which **{nblock} block the public release**.")
    w("")
    w("This page is the team's working list. It is generated from the `MISSING` / `UNVERIFIED`")
    w("blocks on the pages themselves, so it cannot drift away from them: close a block")
    w("on its page and it leaves this table when the list is regenerated. Nothing is")
    w("tracked here that is not also marked in place, and nothing is marked in place")
    w("that is not here.")
    w("")
    w('!!! note "How to read a row"')
    w("    **Page** links to the exact section or step the gap sits in — that is where")
    w("    the surrounding facts are, and where the answer must be written. **Who can")
    w("    supply it** is copied from the block's own owner line; it names a role, not")
    w("    a person, because roles survive a graduation. **Blocks release** is `yes`")
    w("    when the title says `MISSING — SAFETY`, when the block itself says what it")
    w("    blocks, or when it sits on a page the home page already names as a blocker")
    w("    (CAD downloads, the fastener schedule, the licence, safety).")
    w("")
    w("## Where the work sits")
    w("")
    w("| Section | Open items | Blocking release |")
    w("| --- | ---: | ---: |")
    for _, name in SECTIONS:
        its = by_section.get(name)
        if not its:
            continue
        w(f"| {name} | {len(its)} | {sum(1 for i in its if i['_block'])} |")
    w(f"| **Total** | **{total}** | **{nblock}** |")
    w("")
    w("## Who is holding what")
    w("")
    w("An item owned jointly counts once against each role, so this column sums to")
    w(f"more than {total}.")
    w("")
    w("| Role | Open items | Of those, blocking |")
    w("| --- | ---: | ---: |")
    for o, c in owners.most_common():
        b = sum(1 for i in items if o in i["_roles"] and i["_block"])
        w(f"| {o} | {c} | {b} |")
    w("")
    w("## The six that stop a build outright")
    w("")
    w("These are the home page's own blocker rows, restated as work. Everything else")
    w("in this list makes a build harder; these make it impossible.")
    w("")
    w("| Blocker | Where it is tracked |")
    w("| --- | --- |")
    w("| No drawings, print plates or native Fusion archive — per-part and whole-robot STEP are published | [CAD downloads](../fabrication/cad-downloads.md) |")
    w("| No fastener schedule — every screw, nut, washer and bearing is one placeholder row | [Fasteners and hardware](../bom/fasteners-and-hardware.md) |")
    w("| No torque values and no threadlocker grade, anywhere | [Assembly](../assembly/index.md), [Tools](../assembly/tools.md) |")
    w("| No hardware licence and no documentation licence | [Citation and licence](citation-and-license.md) |")
    w("| No human-safety procedure: no e-stop doctrine, no power-down order, no bystander distance | [Safety](../before-you-start/safety.md) |")
    w("| No hardware e-stop exists in the design at all — the only stop is a software velocity limit | [Power system](../electrical/power-system.md), [Torso and waist](../assembly/torso-and-waist.md) |")
    w("")

    for _, name in SECTIONS:
        its = by_section.get(name)
        if not its:
            continue
        w(f"## {name}")
        w("")
        if name in SECTION_NOTE:
            w(SECTION_NOTE[name])
            w("")
        w("| Page | What is missing | Who can supply it | Blocks release |")
        w("| --- | --- | --- | :-: |")
        for it in sorted(its, key=lambda x: (x["file"], x["line"])):
            rel = posixpath.relpath(it["file"], "reference")
            ctx = it["context"]
            m = re.match(r"Step (\d+) — (.*)", ctx)
            if m:
                anchor, label = f"#step-{m.group(1)}", f"{m.group(2)} (step {m.group(1)})"
            elif ctx:
                anchor, label = "#" + slug(ctx), clean(ctx)
            else:
                anchor = label = ""
            page = it["file"].split("/")[-1].replace(".md", "")
            text = f"{page} → {label}" if label else page
            flag = "**yes**" if it["_block"] else "no"
            w(f"| [{text}]({rel}{anchor}) | {it['_sum']} | {it['_owner']} | {flag} |")
        w("")

    w("## Items that are not TODO blocks")
    w("")
    w("Three gaps are structural rather than a missing fact, so they have no block on")
    w("a page to generate a row from:")
    w("")
    w("| Gap | What it means | Who can supply it | Blocks release |")
    w("| --- | --- | --- | :-: |")
    w("| `tools.csv` does not exist | The Tools tier on [Bill of materials](../bom/index.md) and the subtotal on [Tools](../assembly/tools.md) both render *not yet published*. A builder cannot budget the tools | hardware lead + assembly lead | no |")
    w("| `optional.csv` does not exist | The third camera module (~$600), spares and upgrades cannot be quoted | hardware lead | no |")
    w("| `print_profiles.csv` does not exist | The per-part table on [Printing guide](../fabrication/printing-guide.md) is gated on the file and does not render at all | hardware lead | **yes** |")
    w("")
    w("## Images")
    w("")
    w("Missing figures are not in this table. They are tracked separately, with the")
    w("exact path and a one-line brief for each, in the")
    w("[image manifest](../assets/MANIFEST.md) — the list to hand to whoever renders")
    w("the exploded views.")
    w("")
    w("## Regenerating this page")
    w("")
    w("This table is derived from the pages, not maintained by hand:")
    w("")
    w("```console")
    w("$ python tools/gen_punchlist.py")
    w("```")
    w("")
    w("Every TODO block in `docs/` has the same shape, and that shape is what makes")
    w("the derivation possible:")
    w("")
    w("```markdown")
    w('!!! missing "MISSING — short statement of the gap"')
    w("    What is missing, in enough detail that the person who has the answer")
    w("    recognises it as theirs.")
    w("    *Owner: role who can supply it.*")
    w("```")
    w("")
    w("For something that is stated but not confirmed, use `!!! unverified` with a")
    w("title starting `UNVERIFIED —`. Both kinds render red and bold. Write")
    w("`MISSING — SAFETY — ...` when the gap is a safety item or stops a build")
    w("outright; the generator reads that as *blocks release*. The")
    w("`*Owner:*` line is mandatory — the generator refuses to run without it, because")
    w("an unowned TODO is a wish rather than a work item.")
    w("")
    return "\n".join(L) + "\n"


def main() -> int:
    items = extract()
    unowned = [i for i in items if not i["owner"]]
    if unowned:
        for i in unowned:
            print(f"ERROR no *Owner:* line — {i['file']}:{i['line']} {i['title']}",
                  file=sys.stderr)
        return 1
    for it in items:
        it["_sum"] = summarise(it)
        it["_block"] = blocking(it)
        it["_owner"] = owner_text(it)
        it["_roles"] = roles(it)
    OUT.write_text(render(items), encoding="utf-8", newline="\n")
    nblock = sum(1 for i in items if i["_block"])
    print(f"{OUT.relative_to(SITE).as_posix()}: {len(items)} open items, {nblock} blocking")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
