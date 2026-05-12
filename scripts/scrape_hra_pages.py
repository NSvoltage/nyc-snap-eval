"""Scrape NYC HRA's public SNAP guidance pages.

Per ADR-005, the city-public layer of the policy corpus consists of HRA's
public-facing SNAP pages (NOT the internal Policy Directives / Bulletins,
which are excluded from v1).

The URL list below was discovered by following internal links from the main
SNAP page (/site/hra/help/snap-benefits-food-program.page) on the retrieval
date. Re-run periodically; expect the set to drift as HRA reorganizes content.

Usage:
    uv run python scripts/scrape_hra_pages.py [--dry-run]

Writes:
    data/policy_corpus/nyc/hra-public-pages/pages/<slug>.html
    data/policy_corpus/nyc/hra-public-pages/pages/<slug>.txt
    data/policy_corpus/nyc/hra-public-pages/pages/<slug>.meta.yaml
    data/policy_corpus/nyc/hra-public-pages/meta.yaml      (top-level)
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import httpx
import yaml
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = REPO_ROOT / "data" / "policy_corpus" / "nyc" / "hra-public-pages"

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Canonical SNAP-relevant HRA pages. Discovered by crawling internal links
# from the main SNAP page on 2026-05-11; verified to return HTTP 200.
HRA_URLS: list[str] = [
    "https://www.nyc.gov/site/hra/help/snap-benefits-food-program.page",
    "https://www.nyc.gov/site/hra/help/snap-faq.page",
    "https://www.nyc.gov/site/hra/help/snap-application-frequently-asked-questions.page",
    "https://www.nyc.gov/site/hra/help/snap-nondiscrimination.page",
    "https://www.nyc.gov/site/hra/help/able-bodied-adults-without-dependents.page",
    "https://www.nyc.gov/site/hra/help/access-hra-resources.page",
    "https://www.nyc.gov/site/hra/help/food-assistance.page",
    "https://www.nyc.gov/site/hra/help/ebt-card-services.page",
    "https://www.nyc.gov/site/hra/help/benefitreplacement.page",
    "https://www.nyc.gov/assets/hra/downloads/pdf/services/snap/snap_need_to_know.pdf",
]

log = logging.getLogger("scrape_hra")


def slugify(url: str) -> str:
    """Return a filesystem-safe slug derived from the URL path."""
    path = urlparse(url).path.rstrip("/")
    name = path.rsplit("/", 1)[-1] or "index"
    name = re.sub(r"\.(page|html|pdf)$", "", name)
    return re.sub(r"[^A-Za-z0-9._-]", "-", name)


def extract_text(html: str) -> str:
    """Strip HTML chrome and return human-readable text."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    return re.sub(r"\n{3,}", "\n\n", main.get_text(separator="\n", strip=True))


def fetch(client: httpx.Client, url: str) -> httpx.Response:
    log.info("GET %s", url)
    response = client.get(url, timeout=60.0)
    response.raise_for_status()
    return response


def page_meta(url: str, response: httpx.Response, sha256: str) -> dict:
    return {
        "url": url,
        "final_url": str(response.url),
        "status": response.status_code,
        "content_type": response.headers.get("content-type"),
        "content_length": len(response.content),
        "last_modified": response.headers.get("last-modified"),
        "etag": response.headers.get("etag"),
        "sha256": sha256,
    }


def write_outputs(
    target_dir: Path, fetched: list[tuple[str, httpx.Response, str]], retrieval_date: str
) -> None:
    pages_dir = target_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    page_records: list[dict] = []
    for url, response, slug in fetched:
        body = response.content
        sha256 = hashlib.sha256(body).hexdigest()
        is_pdf = url.lower().endswith(".pdf")
        ext = "pdf" if is_pdf else "html"

        (pages_dir / f"{slug}.{ext}").write_bytes(body)

        if not is_pdf:
            text = extract_text(body.decode(response.encoding or "utf-8", errors="replace"))
            (pages_dir / f"{slug}.txt").write_text(text, encoding="utf-8")

        per_page = page_meta(url, response, sha256)
        per_page["slug"] = slug
        (pages_dir / f"{slug}.meta.yaml").write_text(
            yaml.safe_dump(per_page, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        page_records.append(per_page)

    top_meta = {
        "source": {
            "name": "NYC HRA public SNAP guidance",
            "scope": (
                "Public-facing HRA SNAP pages reachable from "
                "/site/hra/help/snap-benefits-food-program.page"
            ),
        },
        "license": "public (NYC government website)",
        "retrieval_date": retrieval_date,
        "retrieval_method": (
            "httpx GET with a browser User-Agent; HTML parsed with BeautifulSoup; "
            "URL set discovered by following internal links from the main SNAP page."
        ),
        "excluded_from_corpus": (
            "HRA Policy Directives and Policy Bulletins are NOT canonically published "
            "on nyc.gov and are excluded from v1 per ADR-005."
        ),
        "page_count": len(page_records),
        "pages": page_records,
    }
    (target_dir / "meta.yaml").write_text(
        yaml.safe_dump(top_meta, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scrape NYC HRA public SNAP guidance pages.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and report; no writes.")
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

    fetched: list[tuple[str, httpx.Response, str]] = []
    with httpx.Client(
        headers={"User-Agent": BROWSER_UA, "Accept": "*/*"},
        follow_redirects=True,
    ) as client:
        for url in HRA_URLS:
            response = fetch(client, url)
            fetched.append((url, response, slugify(url)))
            log.info(
                "  -> %d bytes (%s)",
                len(response.content),
                response.headers.get("content-type"),
            )

    if args.dry_run:
        log.info("Dry run; no files written.")
        return 0

    retrieval = date.today().isoformat()
    write_outputs(args.target_dir, fetched, retrieval)
    log.info("Wrote %d pages to %s", len(fetched), args.target_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
