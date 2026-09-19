"""mkdocs-macros module for the Duke Humanoid V2 hardware site.

Why this file exists
--------------------
Every cost figure on this site must be *computed from a CSV in ``docs/data/``*,
never hand-typed into prose. Hand-typed subtotals drift the moment a part is
re-sourced, and a drifting cost table is exactly the defect this release is
trying to fix. Pages therefore call ``bom_subtotal()`` / ``bom_total()`` and get
a formatted figure back.

The CSV column contract is documented in ``docs/data/README.md``. This module
reads only the columns it needs and is deliberately tolerant: if a CSV is not
present yet, the macros return a visible "not yet published" marker rather than
breaking the build. That is intentional — the site is published with honest
holes, not with invented numbers.
"""

from __future__ import annotations

import csv
import os
from typing import Any, Callable, Iterable

# Rendered in place of a number whenever the underlying CSV is missing or has no
# priced rows. Must stay visually obvious; never substitute a guess.
PENDING = '<strong class="pending-figure">NOT YET PUBLISHED</strong>'

# Columns the cost macros rely on. See docs/data/README.md for the full contract.
COL_QTY = "qty_per_robot"
COL_UNIT = "unit_cost_usd"
COL_TOTAL = "total_cost_usd"
COL_SUB = "subassembly"
COL_CLASS = "class"
COL_ID = "part_id"

# Files in docs/data/ that are NOT robot parts and must never land in a
# whole-robot total. Historically this bit us twice: a bare ``bom_total()``
# swept in the single-leg test fixture and silently added $101.38 of
# development tooling to the price of a robot, and the same call would have
# swept in the tools tier the day it lands. A whole-robot figure means "parts
# that end up in the machine", so the default total is everything in the data
# directory that carries the parts schema, minus this set.
NON_ROBOT_FILES = {
    "test-fixtures.csv",   # development fixtures — see docs/bom/cnc-parts.md
    "tools.csv",           # tools tier, priced separately
    "optional.csv",        # third camera module, spares, upgrades
    "spares.csv",          # reserved
}

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def _data_dir(env) -> str:
    """Absolute path of the BOM data directory (``docs/data`` by default)."""
    rel = env.conf["extra"].get("bom_data_dir", "data")
    return os.path.join(env.conf["docs_dir"], rel)


def _read(path: str) -> list[dict[str, str]]:
    if not os.path.isfile(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return [row for row in csv.DictReader(fh)]


def _header(path: str) -> list[str]:
    """Column names of a CSV, or ``[]`` if it is missing or empty."""
    if not os.path.isfile(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.reader(fh):
            return [c.strip() for c in row]
    return []


def _is_parts_file(path: str) -> bool:
    """True if this CSV follows the parts schema in ``docs/data/README.md``.

    Guards the default of ``bom_total()``: ``bom-reconciliation.csv`` (an audit
    table) already lives in the same directory and ``print_profiles.csv`` (print
    settings) will when it lands; neither carries a ``part_id`` or a cost
    column, so they are excluded by shape rather than by being listed one by
    one.
    """
    cols = set(_header(path))
    return COL_ID in cols and bool(cols & {COL_UNIT, COL_TOTAL})


def _robot_csv_names(directory: str) -> list[str]:
    """Every parts CSV whose rows belong in a whole-robot total."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        f for f in os.listdir(directory)
        if f.endswith(".csv")
        and f not in NON_ROBOT_FILES
        and _is_parts_file(os.path.join(directory, f))
    )


def _num(value: Any) -> float | None:
    """Parse a cell that may carry ``$``, thousands separators or blanks."""
    if value is None:
        return None
    text = str(value).strip().replace("$", "").replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _row_total(row: dict[str, str]) -> float | None:
    """Line total: the explicit column if present, else qty x unit cost."""
    total = _num(row.get(COL_TOTAL))
    if total is not None:
        return total
    qty, unit = _num(row.get(COL_QTY)), _num(row.get(COL_UNIT))
    if qty is None or unit is None:
        return None
    return qty * unit


def _select(
    rows: Iterable[dict[str, str]],
    subassembly: str | None = None,
    part_class: str | None = None,
    exclude_ids: Iterable[str] = (),
    where: Callable[[dict[str, str]], bool] | None = None,
) -> list[dict[str, str]]:
    excluded = {i.strip().lower() for i in exclude_ids}
    out = []
    for row in rows:
        if subassembly and row.get(COL_SUB, "").strip().lower() != subassembly.lower():
            continue
        if part_class and row.get(COL_CLASS, "").strip().lower() != part_class.lower():
            continue
        if row.get(COL_ID, "").strip().lower() in excluded:
            continue
        if where and not where(row):
            continue
        out.append(row)
    return out


def define_env(env):
    """mkdocs-macros entry point."""

    # ----------------------------------------------------------------- #
    # cost macros
    # ----------------------------------------------------------------- #

    @env.macro
    def money(amount: float | None) -> str:
        """Format a USD figure the one way this site formats USD figures."""
        if amount is None:
            return PENDING
        return f"${amount:,.2f}"

    @env.macro
    def bom_subtotal(
        csv_name: str,
        subassembly: str | None = None,
        part_class: str | None = None,
        exclude_ids: Iterable[str] = (),
    ) -> str:
        """Formatted subtotal of one CSV in ``docs/data/``.

        ``bom_subtotal("leg.csv", part_class="machined")`` -> ``$1,234.56``.
        Rows whose cost cannot be parsed are skipped and reported separately by
        ``bom_unpriced()``; a subtotal is never silently completed with a guess.
        """
        rows = _select(
            _read(os.path.join(_data_dir(env), csv_name)),
            subassembly, part_class, exclude_ids,
        )
        totals = [t for t in (_row_total(r) for r in rows) if t is not None]
        if not totals:
            return PENDING
        return money(sum(totals))

    @env.macro
    def bom_total(csv_names: Iterable[str] | None = None,
                  exclude_ids: Iterable[str] = ()) -> str:
        """Formatted grand total across several parts CSVs.

        Called with no arguments — the form every page should use — this is the
        **whole-robot parts total**: every parts CSV in ``docs/data/`` except the
        files in ``NON_ROBOT_FILES`` (test fixtures, tools, options). Pass an
        explicit list only to total a deliberate subset; passing the full list by
        hand on each page is how three pages came to disagree about what "total"
        meant.
        """
        directory = _data_dir(env)
        if csv_names is None:
            csv_names = _robot_csv_names(directory)
            if not csv_names:
                return PENDING
        totals: list[float] = []
        for name in csv_names:
            rows = _select(_read(os.path.join(directory, name)), exclude_ids=exclude_ids)
            totals += [t for t in (_row_total(r) for r in rows) if t is not None]
        if not totals:
            return PENDING
        return money(sum(totals))

    @env.macro
    def bom_count(csv_name: str, subassembly: str | None = None,
                  part_class: str | None = None) -> str:
        """Number of part rows matching the filter, as a string."""
        rows = _select(_read(os.path.join(_data_dir(env), csv_name)),
                       subassembly, part_class)
        return str(len(rows)) if rows else PENDING

    @env.macro
    def bom_qty(csv_name: str, subassembly: str | None = None,
                part_class: str | None = None) -> str:
        """Total piece count (sum of ``qty_per_robot``) matching the filter."""
        rows = _select(_read(os.path.join(_data_dir(env), csv_name)),
                       subassembly, part_class)
        qtys = [q for q in (_num(r.get(COL_QTY)) for r in rows) if q is not None]
        if not qtys:
            return PENDING
        return f"{sum(qtys):g}"

    @env.macro
    def bom_unpriced(csv_name: str) -> str:
        """Comma-separated ``part_id`` list of rows with no usable cost.

        Pages print this so a reader can see exactly which parts are missing a
        price instead of trusting a subtotal that quietly skipped them.
        """
        rows = _read(os.path.join(_data_dir(env), csv_name))
        missing = [r.get(COL_ID, "?") for r in rows if _row_total(r) is None]
        if not rows:
            return PENDING
        return ", ".join(missing) if missing else "none"

    @env.macro
    def bom_priced_as_of(csv_name: str) -> str:
        """Newest ``priced_as_of`` date in the file, so prices carry a date."""
        rows = _read(os.path.join(_data_dir(env), csv_name))
        dates = sorted({r.get("priced_as_of", "").strip() for r in rows} - {""})
        return dates[-1] if dates else PENDING

    @env.macro
    def data_file_exists(csv_name: str) -> bool:
        """True once a content agent has landed this CSV. Use to gate prose."""
        return os.path.isfile(os.path.join(_data_dir(env), csv_name))

    # ----------------------------------------------------------------- #
    # downloadable CAD files: docs/files/, indexed by tools/gen_cad_manifest.py
    # ----------------------------------------------------------------- #

    def _cad_rows() -> list[dict[str, str]]:
        return _read(os.path.join(_data_dir(env), "cad-files.csv"))

    def _from_page(path: str) -> str:
        """Make a docs-root path relative to the Markdown file being rendered."""
        src = env.page.file.src_path.replace("\\", "/") if env.page else ""
        return "../" * src.count("/") + path

    def _link(row: dict[str, str], text: str) -> str:
        attr = "" if row["format"] == "PDF" else '{ download="" }'
        return f"[{text}]({_from_page(row['path'])}){attr}"

    @env.macro
    def cad_links(part_id: str) -> str:
        """Download links for one part (STEP · 3MF/STL · PDF), or a red TODO."""
        order = {"step": 0, "print": 1, "drawings": 2}
        rows = sorted(
            (r for r in _cad_rows() if r["part_id"] == part_id and r["kind"] in order),
            key=lambda r: order[r["kind"]],
        )
        if not rows:
            return "**TODO**{ .dh-missing }"
        return " · ".join(_link(r, r["format"]) for r in rows)

    @env.macro
    def cad_table(kind: str | None = None) -> str:
        """A table of every published file of one kind, each a download link."""
        rows = [r for r in _cad_rows() if kind is None or r["kind"] == kind]
        if not rows:
            return PENDING
        out = ["| File | Part | Format | Size |", "| --- | --- | --- | ---: |"]
        for r in rows:
            name = r["path"].rsplit("/", 1)[-1]
            out.append(f"| {_link(r, name)} | `{r['part_id']}` | {r['format']} | {int(r['bytes']) / 2**20:.1f} MB |")
        return "\n".join(out)

    @env.macro
    def cad_count(kind: str | None = None) -> int:
        return sum(1 for r in _cad_rows() if kind is None or r["kind"] == kind)

    # ----------------------------------------------------------------- #
    # assembly page furniture
    # ----------------------------------------------------------------- #

    @env.macro
    def step(number: int | str, title: str) -> str:
        """Numbered assembly-step heading with a badge.

        ``{{ step(3, "Press the hip-roll bearing") }}`` renders an ``<h3>`` that
        the table of contents picks up, with a circled step number in front.
        """
        anchor = f"step-{number}"
        return (
            f'<h3 class="step" id="{anchor}">'
            f'<span class="step-badge">{number}</span>{title}'
            f'<a class="headerlink" href="#{anchor}" title="Permanent link">¶</a>'
            f"</h3>"
        )

    @env.macro
    def checkpoint(text: str) -> str:
        """A must-pass verification gate between steps.

        Rendered as a Material admonition of type ``checkpoint`` (styled in
        ``docs/stylesheets/extra.css``). Use for anything a builder must confirm
        before continuing, not for general advice.
        """
        return (
            '<div class="admonition checkpoint">'
            '<p class="admonition-title">Checkpoint</p>'
            f"<p>{text}</p></div>"
        )
