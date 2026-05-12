"""Pull NYS OTDA SNAP PDFs into the policy corpus.

Originally scoped to the NYS OTDA SNAP Source Book. Extended on 2026-05-11
(per r5-freshness-audit-2026-05-11.md and ADR-008) to also pull OTDA GIS
messages — operational guidance memoranda that OTDA publishes between
Source Book revisions.

The script preserves the OTDA-origin-first / Wayback-fallback pattern across
both modes, because the OTDA host is unreachable from many networks.

Modes:

    # Default: pull the SNAP Source Book.
    uv run python scripts/pull_otda_sourcebook.py

    # Pull a GIS message by ID. Year inferred from the ID prefix (e.g. 25 → 2025).
    uv run python scripts/pull_otda_sourcebook.py --gis 25DC055
    uv run python scripts/pull_otda_sourcebook.py --gis 26DC007

    # Pull an arbitrary OTDA PDF.
    uv run python scripts/pull_otda_sourcebook.py \\
        --url https://otda.ny.gov/programs/snap/some-doc.pdf \\
        --slug some-doc \\
        --target-subdir state/otda-snap/some-doc

    # Pull all GIS messages tracked in the embedded GIS_INDEX list.
    uv run python scripts/pull_otda_sourcebook.py --gis-batch

Writes (SNAPSB mode):
    data/policy_corpus/state/otda-snap-source-book/SNAPSB.pdf
    data/policy_corpus/state/otda-snap-source-book/extracted/full.txt
    data/policy_corpus/state/otda-snap-source-book/meta.yaml

Writes (GIS mode):
    data/policy_corpus/state/otda-gis/<id>/<id>.pdf
    data/policy_corpus/state/otda-gis/<id>/extracted/full.txt
    data/policy_corpus/state/otda-gis/<id>/meta.yaml
"""

from __future__ import annotations

import argparse
import io
import logging
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import httpx
import pypdf
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

SOURCEBOOK_URL = "https://otda.ny.gov/programs/snap/SNAPSB.pdf"
SOURCEBOOK_WAYBACK = "https://web.archive.org/web/2025/https://otda.ny.gov/programs/snap/SNAPSB.pdf"
SOURCEBOOK_TARGET = REPO_ROOT / "data" / "policy_corpus" / "state" / "otda-snap-source-book"

GIS_TARGET_ROOT = REPO_ROOT / "data" / "policy_corpus" / "state" / "otda-gis"

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# GIS messages tracked in v1, identified by r5-freshness-audit-2026-05-11.md.
GIS_INDEX: list[dict[str, str]] = [
    {
        "id": "25DC024",
        "title": "2025-2026 SNAP Income Guidelines",
    },
    {
        "id": "25DC055",
        "title": "Summary of SNAP Changes in the One Big Beautiful Bill",
    },
    {
        "id": "25DC056",
        "title": "Referenced in original ADR-005 as the July 2025 SNAPSB confirmation",
    },
    {
        "id": "25DC059",
        "title": "OTDA-4357-EL form revision",
    },
    {
        "id": "25DC081",
        "title": "OTDA-4357-EL form revision (REV 05/25)",
    },
    {
        "id": "26DC007",
        "title": "200% of Poverty Income Standards Chart, effective 2026-06-01",
    },
]

log = logging.getLogger("pull_otda")


class NotAPdfError(RuntimeError):
    """Raised when a fetch succeeds at HTTP level but the body is not a PDF."""


@dataclass
class PullTarget:
    """A single PDF to pull, with both an origin URL and a Wayback fallback URL."""

    slug: str
    origin_url: str
    wayback_url: str
    target_dir: Path
    canonical_pdf_name: str
    notes_for_meta: list[str]
    kind: str  # "sourcebook" | "gis" | "other"


# ---------------------------------------------------------------------------
# HTTP + parsing
# ---------------------------------------------------------------------------


def download_pdf(url: str, *, ua: str = BROWSER_UA) -> bytes:
    log.info("GET %s", url)
    with httpx.Client(
        headers={"User-Agent": ua, "Accept": "application/pdf,*/*;q=0.8"},
        follow_redirects=True,
        timeout=180.0,
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        body = response.content
        if not body.startswith(b"%PDF"):
            preview = body[:80].decode("utf-8", errors="replace")
            raise NotAPdfError(
                f"{url} returned {len(body)} bytes that do not start with '%PDF'; "
                f"first 80 bytes: {preview!r}"
            )
        return body


def download_with_fallback(target: PullTarget) -> tuple[bytes, str]:
    """Try the origin URL; on any failure, fall back to the Wayback snapshot.

    Returns (bytes, served_from_url) so meta.yaml records true provenance.
    """
    try:
        return download_pdf(target.origin_url), target.origin_url
    except (httpx.HTTPError, httpx.NetworkError, NotAPdfError) as exc:
        log.warning("origin failed (%s); falling back to Wayback", exc)
        return download_pdf(target.wayback_url), target.wayback_url


def extract_text(pdf_bytes: bytes) -> tuple[str, list[str]]:
    """Return the full text (form-feed-joined) and a list of per-page texts."""
    reader = pypdf.PdfReader(stream=io.BytesIO(pdf_bytes))
    pages: list[str] = []
    for i, page in enumerate(reader.pages):
        try:
            pages.append(page.extract_text() or "")
        except Exception as exc:  # pypdf can raise on malformed pages
            log.warning("page %d: extraction failed (%s)", i, exc)
            pages.append("")
    return "\n\n\f\n\n".join(pages), pages


def detect_sourcebook_revision(text_first_page: str) -> str | None:
    """Pull 'Version: <Month> <Year>' from the SNAPSB cover page if present."""
    match = re.search(
        r"Version:\s*([A-Z][a-z]+\.?)\s+(\d{4})", text_first_page, flags=re.IGNORECASE
    )
    if not match:
        return None
    return f"{match.group(1)} {match.group(2)}"


# ---------------------------------------------------------------------------
# Target construction
# ---------------------------------------------------------------------------


def build_sourcebook_target() -> PullTarget:
    return PullTarget(
        slug="otda-snap-source-book",
        origin_url=SOURCEBOOK_URL,
        wayback_url=SOURCEBOOK_WAYBACK,
        target_dir=SOURCEBOOK_TARGET,
        canonical_pdf_name="SNAPSB.pdf",
        notes_for_meta=[
            "Text extracted with pypdf. The Source Book cross-references each section "
            "to both 18 NYCRR Part 387 and the corresponding 7 CFR sections, which makes "
            "the federal-state citation chain explicit. See ADR-005 and ADR-008.",
        ],
        kind="sourcebook",
    )


def build_gis_target(gis_id: str, title: str | None = None) -> PullTarget:
    """Construct a PullTarget for an OTDA GIS message by its ID.

    OTDA's GIS PDFs follow `https://otda.ny.gov/policy/gis/{20YY}/{ID}.pdf`,
    where YY is the two-digit year prefix of the ID (e.g. 25DC055 → 2025).
    """
    gis_id = gis_id.strip().upper()
    if not re.fullmatch(r"\d{2}[A-Z]{2}\d{3}", gis_id):
        raise ValueError(f"GIS ID must match pattern NNAANNN (e.g. 25DC055); got {gis_id!r}")
    year = 2000 + int(gis_id[:2])
    origin = f"https://otda.ny.gov/policy/gis/{year}/{gis_id}.pdf"
    wayback = f"https://web.archive.org/web/2026/{origin}"
    notes = [
        "OTDA GIS (General Information System) message. GIS messages are operational "
        "guidance memoranda issued between Source Book revisions and are part of the "
        "public state-level corpus per ADR-008.",
    ]
    if title:
        notes.insert(0, f"Title: {title}")
    return PullTarget(
        slug=gis_id,
        origin_url=origin,
        wayback_url=wayback,
        target_dir=GIS_TARGET_ROOT / gis_id,
        canonical_pdf_name=f"{gis_id}.pdf",
        notes_for_meta=notes,
        kind="gis",
    )


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def write_outputs(
    target: PullTarget,
    pdf_bytes: bytes,
    text: str,
    pages: list[str],
    retrieval_date: str,
    fetched_from: str,
) -> None:
    target.target_dir.mkdir(parents=True, exist_ok=True)
    (target.target_dir / "extracted").mkdir(exist_ok=True)
    (target.target_dir / target.canonical_pdf_name).write_bytes(pdf_bytes)
    (target.target_dir / "extracted" / "full.txt").write_text(text, encoding="utf-8")

    notes = list(target.notes_for_meta)
    if fetched_from != target.origin_url:
        notes.append(
            f"NOTE: The OTDA origin ({target.origin_url}) was unreachable from the "
            f"pulling network. This artifact was fetched from the Wayback Machine "
            f"snapshot at {fetched_from}. Re-pull from the OTDA origin when network "
            "access permits, and verify byte-equality."
        )

    meta: dict[str, object] = {
        "source": {
            "name": _source_name(target),
            "canonical_url": target.origin_url,
            "fetched_from": fetched_from,
            "kind": target.kind,
        },
        "license": "public (NYS government document)",
        "retrieval_date": retrieval_date,
        "retrieval_method": ("httpx GET; fallback to Wayback Machine if OTDA origin unreachable."),
        "page_count": len(pages),
        "extracted_char_count": len(text),
        "notes": "\n".join(notes),
    }
    if target.kind == "sourcebook":
        meta["revision_label_on_cover"] = detect_sourcebook_revision(pages[0] if pages else "")

    (target.target_dir / "meta.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )


def _source_name(target: PullTarget) -> str:
    if target.kind == "sourcebook":
        return "NYS OTDA SNAP Source Book"
    if target.kind == "gis":
        return f"NYS OTDA GIS message {target.slug}"
    return f"NYS OTDA PDF: {target.slug}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pull NYS OTDA SNAP PDFs.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--gis", metavar="ID", help="Pull a single GIS message by ID (e.g. 25DC055).")
    mode.add_argument(
        "--gis-batch",
        action="store_true",
        help="Pull every GIS message in the embedded GIS_INDEX list.",
    )
    mode.add_argument("--url", help="Pull an arbitrary OTDA PDF from this URL.")

    parser.add_argument("--slug", help="Slug for --url mode (used as directory + file name stem).")
    parser.add_argument(
        "--target-subdir",
        help="Subdirectory under data/policy_corpus for --url mode (e.g. 'state/otda-misc/foo').",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Download and parse, but do not write to disk.",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    targets: list[PullTarget]
    if args.gis_batch:
        targets = [build_gis_target(item["id"], item.get("title")) for item in GIS_INDEX]
    elif args.gis:
        title = next(
            (item.get("title") for item in GIS_INDEX if item["id"] == args.gis.upper()), None
        )
        targets = [build_gis_target(args.gis, title)]
    elif args.url:
        if not args.slug or not args.target_subdir:
            parser.error("--url requires --slug and --target-subdir")
        targets = [
            PullTarget(
                slug=args.slug,
                origin_url=args.url,
                wayback_url=f"https://web.archive.org/web/2026/{args.url}",
                target_dir=REPO_ROOT / "data" / "policy_corpus" / args.target_subdir,
                canonical_pdf_name=f"{args.slug}.pdf",
                notes_for_meta=[f"Ad hoc OTDA pull invoked with --url {args.url}."],
                kind="other",
            )
        ]
    else:
        targets = [build_sourcebook_target()]

    retrieval = date.today().isoformat()
    failures: list[tuple[str, str]] = []

    for target in targets:
        log.info("=== %s (%s) ===", target.slug, target.kind)
        try:
            pdf_bytes, fetched_from = download_with_fallback(target)
        except (httpx.HTTPError, httpx.NetworkError, NotAPdfError) as exc:
            log.error("FAILED to fetch %s: %s", target.slug, exc)
            failures.append((target.slug, str(exc)))
            continue

        log.info("PDF: %d bytes (from %s)", len(pdf_bytes), fetched_from)
        text, pages = extract_text(pdf_bytes)
        log.info("Extracted text: %d chars across %d pages", len(text), len(pages))

        if args.dry_run:
            log.info("Dry run; no files written for %s.", target.slug)
            continue

        write_outputs(
            target=target,
            pdf_bytes=pdf_bytes,
            text=text,
            pages=pages,
            retrieval_date=retrieval,
            fetched_from=fetched_from,
        )
        log.info("Wrote %s to %s", target.slug, target.target_dir)

    if failures:
        log.error("%d target(s) failed:", len(failures))
        for slug, msg in failures:
            log.error("  - %s: %s", slug, msg)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
