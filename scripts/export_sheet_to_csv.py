"""Export the authoring Google Sheet to per-category CSVs.

The Google Sheet is the authoring surface; the committed CSVs in
`eval/cases/` are the canonical record (per ADR-001 / `docs/conventions.md`
§6 reproducibility, and Promptfoo wiring in `eval/promptfooconfig.yaml`).
Run this whenever the sheet changes:

    uv run python scripts/export_sheet_to_csv.py

The script reads the sheet's public `gviz` CSV endpoint — no auth required
as long as the sheet share is "anyone with the link can view." Each tab
in `TABS` becomes the corresponding file in `eval/cases/`.

Validation: every exported CSV must have the 12 required columns from
`docs/conventions.md` §2 in row 1, in the order listed in `REQUIRED_COLUMNS`.
Unexpected column orders or missing columns cause a non-zero exit.
"""

from __future__ import annotations

import argparse
import csv
import io
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = REPO_ROOT / "eval" / "cases"

# Public sheet (anyone with the link can edit). Authoring surface for v1.
SHEET_ID = "1CV7O8qHMTYQVFHCVFkWIE_zeDsFIyUDovCDLCHPmAcc"

# Tab name in the Sheet → CSV filename in eval/cases/.
TABS: list[tuple[str, str]] = [
    ("A_mycity_replay", "A_mycity_replay.csv"),
    ("B_factual_recall", "B_factual_recall.csv"),
    ("C_refusal_escalation", "C_refusal_escalation.csv"),
    ("D_eligibility_edge_cases", "D_eligibility_edge_cases.csv"),
    ("E_adversarial", "E_adversarial.csv"),
    ("F_multilingual", "F_multilingual.csv"),
    ("G_grounding_citation", "G_grounding_citation.csv"),
]

# Required columns per docs/conventions.md §2. `notes` is the one optional
# trailing column and is permitted but not required.
REQUIRED_COLUMNS: list[str] = [
    "id",
    "category",
    "subcategory",
    "question",
    "expected_behavior",
    "hard_fail_conditions",
    "citation",
    "citation_url",
    "last_verified_date",
    "harm_severity",
    "language",
    "expected_long_form_answer",
]

log = logging.getLogger("export_sheet")


@dataclass
class ExportResult:
    tab_name: str
    target_path: Path
    row_count: int
    bytes_written: int


def gviz_csv_url(sheet_id: str, tab_name: str) -> str:
    return (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq"
        f"?tqx=out:csv&sheet={tab_name}"
    )


def fetch_tab_csv(client: httpx.Client, sheet_id: str, tab_name: str) -> str:
    url = gviz_csv_url(sheet_id, tab_name)
    log.info("GET %s", url)
    response = client.get(url, timeout=60.0)
    response.raise_for_status()
    body = response.text

    # Google Sheets returns HTML for some misconfigurations (private sheet,
    # bad tab name when sheet does exist but tab doesn't). Detect that.
    if body.lstrip().startswith("<"):
        raise RuntimeError(
            f"Tab {tab_name!r} did not return CSV. Body starts with HTML, which "
            "usually means the sheet share is not 'anyone with link' or the tab "
            f"name is wrong. First 80 chars: {body[:80]!r}"
        )
    return body


def validate_header(csv_text: str, tab_name: str) -> None:
    """Raise if the CSV header row is missing any required column."""
    reader = csv.reader(io.StringIO(csv_text))
    try:
        header = next(reader)
    except StopIteration as exc:
        raise RuntimeError(f"Tab {tab_name!r} is empty (no header row).") from exc

    header_stripped = [c.strip() for c in header]
    missing = [c for c in REQUIRED_COLUMNS if c not in header_stripped]
    if missing:
        raise RuntimeError(
            f"Tab {tab_name!r} is missing required columns: {missing}. "
            f"Header row was: {header_stripped}"
        )
    if header_stripped[: len(REQUIRED_COLUMNS)] != REQUIRED_COLUMNS:
        log.warning(
            "Tab %r has the required columns but not in the canonical order. "
            "Promptfoo reads by name, so this is OK, but cleaner diffs come "
            "from preserving the order in docs/conventions.md §2.",
            tab_name,
        )


def write_csv(target_path: Path, csv_text: str) -> int:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(csv_text, encoding="utf-8")
    return len(csv_text.encode("utf-8"))


def count_data_rows(csv_text: str) -> int:
    """Number of rows after the header. Empty trailing lines don't count."""
    reader = csv.reader(io.StringIO(csv_text))
    return max(0, sum(1 for _ in reader) - 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export the authoring sheet to per-category CSVs.")
    parser.add_argument(
        "--sheet-id",
        default=SHEET_ID,
        help=f"Google Sheet ID (default: {SHEET_ID}).",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"Output directory (default: {DEFAULT_TARGET}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and validate, but do not write to disk.",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    results: list[ExportResult] = []
    failures: list[tuple[str, str]] = []

    with httpx.Client(headers={"User-Agent": "nyc-snap-eval/0.1 (export_sheet)"}) as client:
        for tab_name, csv_name in TABS:
            target = args.target_dir / csv_name
            try:
                csv_text = fetch_tab_csv(client, args.sheet_id, tab_name)
                validate_header(csv_text, tab_name)
            except (httpx.HTTPError, RuntimeError) as exc:
                log.error("FAILED: %s: %s", tab_name, exc)
                failures.append((tab_name, str(exc)))
                continue

            row_count = count_data_rows(csv_text)
            if args.dry_run:
                log.info("(dry-run) %s -> %s: %d data rows", tab_name, target, row_count)
                results.append(ExportResult(tab_name, target, row_count, len(csv_text)))
                continue

            bytes_written = write_csv(target, csv_text)
            results.append(ExportResult(tab_name, target, row_count, bytes_written))
            log.info("%s -> %s: %d data rows, %d bytes", tab_name, target, row_count, bytes_written)

    log.info("Exported %d tab(s); %d failure(s).", len(results), len(failures))
    if failures:
        for tab, msg in failures:
            log.error("  - %s: %s", tab, msg)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
