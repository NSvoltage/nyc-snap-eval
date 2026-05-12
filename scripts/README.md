# `scripts/`

Utility scripts that are too small for their own modules but get re-run frequently.

## Planned scripts

- **`pull_ecfr.py`** — Pull 7 CFR Part 273 from the eCFR API, save XML and JSON, update `data/policy_corpus/federal/7-cfr-273/meta.yaml`
- **`pull_otda_sourcebook.py`** — Download the OTDA SNAP Source Book PDF, extract text, save with `meta.yaml`
- **`scrape_hra_pages.py`** — Scrape NYC HRA public SNAP pages, save HTML and extracted text
- **`verify_corpus.py`** — Re-check that every source in `data/policy_corpus/` still resolves and matches the recorded revision date. Run before each eval run.
- **`verify_citations.py`** — Day-14 check: every `citation_url` in every case CSV resolves and contains the cited text. Used in CI.
- **`embed_corpus.py`** — Generate voyage-3 embeddings for the chunked corpus and upsert to pgvector. Re-run when the corpus is refreshed.
- **`export_sheet_to_csv.py`** — Pull the latest version of the authoring Google Sheet and write CSVs to `eval/cases/`. The CSVs are the canonical record; the sheet is the authoring surface.

## Conventions

- All scripts are Python 3.11+, formatted with `ruff format`, type-hinted
- All scripts have a `--dry-run` flag where they can plausibly cause side effects
- All scripts log to stderr; stdout is reserved for structured output
- Scripts that modify the repo (corpus pulls, CSV exports) commit their changes only with a `--commit` flag
