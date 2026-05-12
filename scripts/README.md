# `scripts/`

Utility scripts that are too small for their own modules but get re-run frequently.

Python 3.11+, managed via `uv` (see `pyproject.toml` at the repo root). Run any script with `uv run python scripts/<name>.py …`. All scripts have a `--dry-run` flag where they can plausibly cause side effects.

## Built in v1

- **`pull_ecfr.py`** — Pulls 7 CFR Part 273 from the eCFR REST API and pins to the title's reported `up_to_date_as_of` date.
  - Writes XML, structure JSON, versions JSON, and `meta.yaml` to `data/policy_corpus/federal/7-cfr-273/`.
  - Records the most-recent Part 273 amendment date (from `/versioner/v1/versions`) as `revision_date`.
- **`pull_otda_sourcebook.py`** — Pulls NYS OTDA SNAP PDFs. Originally scoped to the Source Book; extended on 2026-05-11 (per ADR-008 §3) to also pull OTDA GIS messages and arbitrary OTDA PDFs.
  - Default invocation pulls SNAPSB to `data/policy_corpus/state/otda-snap-source-book/`.
  - `--gis 25DC055` pulls a single GIS message by ID to `data/policy_corpus/state/otda-gis/<ID>/`.
  - `--gis-batch` pulls every ID in the embedded `GIS_INDEX` list.
  - `--url <URL> --slug <NAME> --target-subdir <PATH>` pulls an arbitrary OTDA PDF.
  - All modes fall back to the Wayback Machine when the OTDA origin is unreachable. The Wayback fallback is recorded in each artifact's `meta.yaml`.
- **`scrape_hra_pages.py`** — Fetches the canonical NYC HRA public SNAP pages (URL list discovered by crawling internal links from the main SNAP page on 2026-05-11).
  - Writes raw HTML, extracted text (BeautifulSoup, chrome-stripped), per-page meta YAML, and a top-level `meta.yaml` index to `data/policy_corpus/nyc/hra-public-pages/`.
  - Includes the published `snap_need_to_know.pdf` from NYC HRA.

## Planned (not yet built)

- **`verify_corpus.py`** — Re-check that every source in `data/policy_corpus/` still resolves and matches the recorded revision date. Run before each eval run.
- **`verify_citations.py`** — Day-14 check: every `citation_url` in every case CSV resolves and contains the cited text. Used in CI.
- **`embed_corpus.py`** — Generate voyage-3 embeddings for the chunked corpus and upsert to pgvector. Re-run when the corpus is refreshed.
- **`export_sheet_to_csv.py`** — Pull the latest version of the authoring Google Sheet and write CSVs to `eval/cases/`. The CSVs are the canonical record; the sheet is the authoring surface.

## Conventions

- All scripts are Python 3.11+, formatted with `ruff format`, type-hinted. Run `uv run ruff check scripts/` and `uv run ruff format scripts/` before committing.
- All scripts have a `--dry-run` flag where they can plausibly cause side effects.
- All scripts log to stderr; stdout is reserved for structured output.
- Scripts that modify the repo (corpus pulls, CSV exports) commit their changes only with a `--commit` flag (planned).
- The Wayback-fallback pattern in `pull_otda_sourcebook.py` is a deliberate hedge: when `otda.ny.gov` is unreachable from the running network, the corpus pull still succeeds via the Wayback snapshot. The provenance is recorded in `meta.yaml` so future refreshes from networks with OTDA reachability can byte-compare and update.
