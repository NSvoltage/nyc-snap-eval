# `data/policy_corpus/`

Pinned, versioned policy documents used as ground truth for the eval and as the retrieval corpus for the reference implementation.

Per ADR-005, the corpus has three layers (federal, state, NYC city-public) and one explicit exclusion (HRA Policy Directives and Bulletins). [ADR-008](../../docs/decisions/ADR-008-post-obbba-post-mycity-amendments.md) extends the state layer with OTDA GIS messages and corrects two factual claims from ADR-005 (SNAPSB revision date; Screening API auth requirement).

## Structure on disk

```
data/policy_corpus/
├── federal/
│   └── 7-cfr-273/
│       ├── meta.yaml                 # eCFR snapshot date, latest Part 273 amendment date
│       ├── full.xml                  # Full Part 273 as XML (eCFR canonical)
│       ├── full.json                 # Part 273 structure / table of contents
│       └── versions.json             # Amendment history for the part
├── state/
│   ├── otda-snap-source-book/
│   │   ├── meta.yaml                 # "Version: Sept 2025" on cover
│   │   ├── SNAPSB.pdf                # Original PDF (Wayback-served if origin blocked)
│   │   └── extracted/
│   │       └── full.txt              # pypdf-extracted text
│   └── otda-gis/                     # OTDA GIS guidance memoranda (per ADR-008 §3)
│       └── <ID>/                     # e.g. 25DC024, 25DC055, 25DC056, 25DC059, 25DC081
│           ├── meta.yaml
│           ├── <ID>.pdf
│           └── extracted/full.txt
└── nyc/
    ├── hra-public-pages/
    │   ├── meta.yaml                 # Top-level index across all pages
    │   └── pages/
    │       └── <slug>.{html,txt,meta.yaml}   # Per-page artifacts (+ snap_need_to_know.pdf)
    └── benefits-screening-api/
        ├── meta.yaml                 # Auth requirement, server URLs, license
        ├── openapi.yaml              # OpenAPI 1.0.0 spec from CityOfNewYork/screeningapi-docs
        └── sample-requests/
            ├── composite-household-01.json   # Synthetic, non-PII household payload
            └── responses/
                ├── sandbox-noauth-401.json
                └── screeningapi-noauth-401.json
```

`README.md` (this file) is the only top-level README; each subtree has either its own `meta.yaml` or per-artifact metadata as shown above.

## meta.yaml schema

Every corpus directory has a `meta.yaml`. Common fields:

```yaml
source:
  name: "<canonical name>"
  url: "<source URL>"               # e.g. https://otda.ny.gov/programs/snap/SNAPSB.pdf
  fetched_from: "<actual URL>"      # may be a Wayback snapshot if origin was blocked
license: "<license string>"
revision_date: "YYYY-MM-DD"         # When the source document was last amended (when knowable)
retrieval_date: "YYYY-MM-DD"        # When we pulled it into the corpus
retrieval_method: "<one-line description of the script + endpoint used>"
notes: |
  Provenance and caveats. Wayback fallbacks, extraction tool, byte-equality checks, etc.
```

## Refresh discipline

When a corpus source is refreshed:
1. Update `meta.yaml` with the new `revision_date` and `retrieval_date`.
2. Re-generate embeddings if the corpus is materially changed (see `scripts/embed_corpus.py`, planned).
3. Re-run the eval to surface any regressions caused by the policy update.
4. Note the refresh in the next results file.

## Provenance caveat (2026-05-11)

The OTDA host `otda.ny.gov` was unreachable from the network used to pull the Day-1 corpus — both the SNAPSB and the GIS messages were fetched via the Wayback Machine. Each affected artifact's `meta.yaml` records `source.fetched_from` set to the Wayback URL. When a future refresh runs from a network with OTDA reachability, the bytes should be compared against the Wayback-served versions and the meta updated. See [ADR-008 §5](../../docs/decisions/ADR-008-post-obbba-post-mycity-amendments.md).

## What's not here

Per ADR-005, NYC HRA Policy Directives and Policy Bulletins are excluded from v1. They are not publicly published as a canonical corpus. This is a documented limitation, not an oversight.

One identified GIS message — 26DC007, the 200%-of-FPL chart effective 2026-06-01 — is also missing: it has only a placeholder snapshot in the Wayback index and was unreachable directly from this network. Tracked as a follow-up in `scripts/pull_otda_sourcebook.py` (`GIS_INDEX`).
