# `data/policy_corpus/`

Pinned, versioned policy documents used as ground truth for the eval and as the retrieval corpus for the reference implementation.

Per ADR-005, the corpus has three layers (federal, state, NYC city-public) and one explicit exclusion (HRA Policy Directives and Bulletins).

## Structure

```
data/policy_corpus/
├── federal/
│   ├── 7-cfr-273/                    # Pulled from eCFR API
│   │   ├── meta.yaml                 # Revision date, retrieval date, source URL
│   │   ├── full.json                 # Full Part 273 as JSON
│   │   ├── full.xml                  # Full Part 273 as XML (eCFR canonical)
│   │   └── by-subpart/               # Pre-chunked by subpart for retrieval
│   └── README.md
├── state/
│   ├── otda-snap-source-book/
│   │   ├── meta.yaml                 # Rev. 7/2025, retrieval date, source URL
│   │   ├── SNAPSB.pdf                # Original PDF as published
│   │   └── extracted/                # Text-extracted version for retrieval
│   └── README.md
├── nyc/
│   ├── hra-public-pages/
│   │   ├── meta.yaml
│   │   └── pages/                    # Scraped public HRA SNAP pages
│   ├── benefits-screening-api/
│   │   ├── meta.yaml
│   │   ├── openapi.yaml              # API spec
│   │   └── sample-requests/          # Example calls and responses
│   └── README.md
└── README.md (this file)
```

## meta.yaml schema

Every corpus directory has a `meta.yaml` with:

```yaml
source:
  name: "7 CFR Part 273"
  url: "https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273"
license: "public domain"
revision_date: "2026-04-24"     # The date the source document was last amended
retrieval_date: "2026-05-12"    # When we pulled it into the corpus
retrieval_method: "eCFR REST API v1, GET /api/versioner/v1/full/{date}/title-7.xml?part=273"
notes: |
  Pulled via the eCFR API. The 'revision_date' is the eCFR's reported 'up_to_date_as_of'
  for Part 273 at retrieval time. See ADR-005 for the source-selection rationale.
```

## Refresh discipline

When a corpus source is refreshed:
1. Update `meta.yaml` with the new `revision_date` and `retrieval_date`
2. Re-generate embeddings if the corpus is materially changed (see `scripts/embed_corpus.py`)
3. Re-run the eval to surface any regressions caused by the policy update
4. Note the refresh in the next results file

## What's not here

Per ADR-005, NYC HRA Policy Directives and Policy Bulletins are excluded from v1. They are not publicly published as a canonical corpus. This is a documented limitation, not an oversight.
