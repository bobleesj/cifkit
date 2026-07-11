#!/usr/bin/env python3
"""End-to-end checks for the Jupyter Book HTML tree (CI + local).

Exit 0 only if the built site has the agent/human entry points, critical
pages, citations, and a few content anchors. Run after:

    jupyter-book build docs
    python scripts/docs_e2e_check.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "docs" / "_build" / "html"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if not HTML.is_dir():
        fail(f"missing build tree {HTML}")

    required_files = [
        "intro.html",
        "install.html",
        "llms.txt",
        "robots.txt",
        "sitemap.txt",
        "_static/CITATION.txt",
        "_static/oled.csv",
        "_static/oled_table.html",
        "_static/gdsb_polyhedron.html",
        "_static/custom.css",
        "_static/llms.txt",
        "tutorials/physical-features.html",
        "tutorials/statistics-many-cifs.html",
        "tutorials/oled.html",
        "api/index.html",
        "api/quick-reference.html",
        "api/cif.html",
        "api/cif-ensemble.html",
        "api/oliynyk.html",
        "api/formula.html",
    ]
    for rel in required_files:
        path = HTML / rel
        if not path.is_file():
            fail(f"missing {rel}")
        if path.stat().st_size < 50:
            fail(f"too small {rel} ({path.stat().st_size} bytes)")

    checks = {
        "llms.txt": [
            "How to credit",
            "Lee2024OLED",
            "Lee2024cifkit",
            "from cifkit.sources.oliynyk import Oliynyk, Property",
            "UNPARIED_E",
            "compute_CN",
            "filter_by_formulas",
            "to_dataframe",
            "parsed_formula",
        ],
        "intro.html": [
            "Parse physical features",
            "Statistics over many CIFs",
            "OLED",
            "llms.txt",
            "OLED table",
            "Data in Brief",
            "10.21105/joss.07205",
            "10.1016/j.dib.2024.110178",
        ],
        "tutorials/oled.html": [
            "What each property means",
            "CITATION.txt",
            "Lee2024OLED",
            "atomic_weight",
            "cohesive_energy",
            "oled-table",
            "76",
            "curated elemental property table",
        ],
        "tutorials/physical-features.html": [
            "shortest_distance",
            "compute_CN",
            "CN_best_methods",
            "how each is determined",
            "largest gap",
            "gdsb_polyhedron.html",
            "10.21105/joss.07205",
            "Data in Brief",
        ],
        "api/quick-reference.html": [
            "UNPARIED_E",
            "filter_by_formulas",
            "CN_max_gap_per_site",
            "to_csv",
        ],
        "_static/CITATION.txt": [
            "10.1016/j.dib.2024.110178",
            "10.21105/joss.07205",
            "Lee2024OLED",
            "Lee2024cifkit",
            "S2352340925008595",
            "d6dd00121a",
        ],
        "robots.txt": ["Allow: /", "llms.txt", "Sitemap:"],
    }

    for rel, needles in checks.items():
        text = (HTML / rel).read_text(errors="replace")
        for needle in needles:
            if needle not in text:
                fail(f"{rel} missing content: {needle!r}")

    # No stale class-named tutorial pages
    for stale in (
        "tutorials/cif.html",
        "tutorials/coordination.html",
        "tutorials/cif_ensemble.html",
        "tutorials/elemental_data.html",
    ):
        if (HTML / stale).exists():
            fail(f"stale tutorial page still built: {stale}")

    # Secondary sidebar should not appear (CSS + theme option)
    intro = (HTML / "intro.html").read_text(errors="replace")
    if "custom.css" not in intro:
        fail("intro.html does not load custom.css")

    print("docs e2e check: PASS")
    print(f"  html root: {HTML}")
    print(f"  files checked: {len(required_files)}")
    print(f"  content anchors: {sum(len(v) for v in checks.values())}")


if __name__ == "__main__":
    main()
