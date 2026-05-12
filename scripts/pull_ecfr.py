"""Pull 7 CFR Part 273 from the eCFR API and pin it to a stated revision.

Per ADR-005, the federal layer of the policy corpus is 7 CFR Part 273
(Certification of Eligible Households), retrieved from the eCFR REST API and
saved with a `meta.yaml` recording the revision and retrieval dates.

Usage:
    uv run python scripts/pull_ecfr.py [--date YYYY-MM-DD] [--dry-run]

By default, retrieves the version of Part 273 in effect today. The script
writes:
    data/policy_corpus/federal/7-cfr-273/full.xml
    data/policy_corpus/federal/7-cfr-273/full.json   (structure / table of contents)
    data/policy_corpus/federal/7-cfr-273/versions.json  (amendment history)
    data/policy_corpus/federal/7-cfr-273/meta.yaml
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date
from pathlib import Path

import httpx
import yaml

ECFR_BASE = "https://www.ecfr.gov"
TITLE = 7
PART = "273"

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = REPO_ROOT / "data" / "policy_corpus" / "federal" / "7-cfr-273"

log = logging.getLogger("pull_ecfr")


def fetch_title_up_to_date(client: httpx.Client) -> str:
    """Return the eCFR-reported `up_to_date_as_of` date for the title."""
    url = f"{ECFR_BASE}/api/versioner/v1/titles.json"
    log.info("GET %s", url)
    response = client.get(url, timeout=30.0)
    response.raise_for_status()
    titles = response.json().get("titles", [])
    for title in titles:
        if title.get("number") == TITLE:
            return title["up_to_date_as_of"]
    raise RuntimeError(f"Title {TITLE} not found in eCFR titles index")


def fetch_full_xml(client: httpx.Client, on_date: str) -> str:
    url = f"{ECFR_BASE}/api/versioner/v1/full/{on_date}/title-{TITLE}.xml"
    log.info("GET %s?part=%s", url, PART)
    response = client.get(url, params={"part": PART}, timeout=120.0)
    response.raise_for_status()
    return response.text


def fetch_structure(client: httpx.Client, on_date: str) -> dict:
    url = f"{ECFR_BASE}/api/versioner/v1/structure/{on_date}/title-{TITLE}.json"
    log.info("GET %s", url)
    response = client.get(url, timeout=60.0)
    response.raise_for_status()
    return response.json()


def fetch_versions(client: httpx.Client) -> dict:
    url = f"{ECFR_BASE}/api/versioner/v1/versions/title-{TITLE}.json"
    log.info("GET %s?part=%s", url, PART)
    response = client.get(url, params={"part": PART}, timeout=60.0)
    response.raise_for_status()
    return response.json()


def latest_amendment_date(versions: dict) -> str | None:
    """Walk the versions payload and return the most recent amendment date.

    The eCFR `versions` endpoint returns a list of content versions; each carries
    an `amendment_date`. We take the max across all sections of Part 273.
    """
    dates: list[str] = []
    for entry in versions.get("content_versions", []):
        amendment_date = entry.get("amendment_date")
        part = entry.get("part")
        if amendment_date and (part is None or part == PART):
            dates.append(amendment_date)
    if not dates:
        return None
    return max(dates)


def extract_part_node(structure: dict) -> dict | None:
    """Drill into the title-level structure JSON to find the Part 273 subtree."""
    stack = [structure]
    while stack:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        if node.get("type") == "part" and str(node.get("identifier")) == PART:
            return node
        for child in node.get("children", []) or []:
            stack.append(child)
    return None


def write_outputs(
    target_dir: Path,
    xml_text: str,
    part_structure: dict,
    versions: dict,
    retrieval_date: str,
    revision_date: str,
) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "full.xml").write_text(xml_text, encoding="utf-8")
    (target_dir / "full.json").write_text(
        json.dumps(part_structure, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (target_dir / "versions.json").write_text(
        json.dumps(versions, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    meta = {
        "source": {
            "name": "7 CFR Part 273 — Certification of Eligible Households",
            "url": (
                f"{ECFR_BASE}/current/title-{TITLE}/subtitle-B/chapter-II/subchapter-C/part-{PART}"
            ),
        },
        "license": "public domain",
        "revision_date": revision_date,
        "retrieval_date": retrieval_date,
        "retrieval_method": (
            "eCFR REST API v1; GET /api/versioner/v1/full/{date}/title-7.xml?part=273"
        ),
        "notes": (
            "Pulled via the eCFR API. 'revision_date' is the most recent amendment date "
            "reported by /versioner/v1/versions for Part 273 at retrieval time. "
            "See ADR-005 for source-selection rationale."
        ),
    }
    (target_dir / "meta.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pull 7 CFR Part 273 from the eCFR API.")
    parser.add_argument(
        "--date",
        default=None,
        help=(
            "Point-in-time date for the eCFR snapshot (YYYY-MM-DD). "
            "Defaults to the title's `up_to_date_as_of` reported by /titles.json."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and report sizes, but do not write anything to disk.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=TARGET_DIR,
        help=f"Output directory (default: {TARGET_DIR}).",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    with httpx.Client(headers={"User-Agent": "nyc-snap-eval/0.1 (corpus pull)"}) as client:
        snapshot_date = args.date or fetch_title_up_to_date(client)
        xml_text = fetch_full_xml(client, snapshot_date)
        structure = fetch_structure(client, snapshot_date)
        versions = fetch_versions(client)

    part_structure = extract_part_node(structure) or structure
    revision = latest_amendment_date(versions) or snapshot_date
    retrieval = date.today().isoformat()

    log.info("snapshot_date (up_to_date_as_of): %s", snapshot_date)
    log.info("full.xml: %d bytes", len(xml_text))
    log.info("structure node found: %s", part_structure is not None)
    log.info("revision_date (latest Part 273 amendment): %s", revision)
    log.info("retrieval_date: %s", retrieval)

    if args.dry_run:
        log.info("Dry run; no files written.")
        return 0

    write_outputs(
        target_dir=args.target_dir,
        xml_text=xml_text,
        part_structure=part_structure,
        versions=versions,
        retrieval_date=retrieval,
        revision_date=revision,
    )
    log.info("Wrote corpus to %s", args.target_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
