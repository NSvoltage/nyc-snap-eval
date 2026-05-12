# ADR-005: Policy corpus sources and exclusions

**Status:** Accepted; amended by [ADR-008](./ADR-008-post-obbba-post-mycity-amendments.md) (2026-05-11)
**Date:** 2026-05-11
**Decision-makers:** [project lead]

> ADR-008 corrects two factual claims in this ADR: the SNAP Source Book pin is the **September 2025** revision (not July 2025), and the NYC Benefits Screening API **requires Bearer-token authentication** (not "open without auth" as recorded below). ADR-008 also expands the state-level corpus to include OTDA GIS messages and reframes Category A as a post-mortem regression set after the MyCity chatbot was discontinued on 2026-02-05. The original text below is retained as the historical record.

## Context

The eval suite anchors every case to a public statute or policy citation. The reference implementation grounds its retrieval in the same corpus. The corpus must be:
- Publicly accessible (anyone can re-verify a citation)
- Version-pinned (so the eval can be re-run against the same source-of-truth)
- Hierarchically clean (federal → state → city, with citations that map across layers)

Corpus access was verified before this ADR was written.

## Decision

### Included in the v1 corpus

**Federal level — 7 CFR Part 273 (Certification of Eligible Households).**
- Source: eCFR REST API (https://www.ecfr.gov/developers/documentation/api/v1)
- License: public domain (federal regulations)
- Pin: a specific revision date recorded in `data/policy_corpus/federal/meta.yaml`
- Pull mechanism: scripted via the eCFR API; both XML and JSON saved

**State level — NYS OTDA SNAP Source Book.**
- Source: https://otda.ny.gov/programs/snap/SNAPSB.pdf
- License: public (NYS government document)
- Pin: July 2025 revision, confirmed via OTDA GIS Message 25DC056
- Citation discipline: the Source Book maps each section to both 18 NYCRR Part 387 and the corresponding 7 CFR sections, which makes the federal-state citation chain explicit

**City level — NYC HRA public SNAP guidance.**
- Source: https://www.nyc.gov/site/hra/help/snap-benefits-food-program.page and related public pages
- License: public (NYC government website)
- Pin: scraped on a specific date recorded in `data/policy_corpus/nyc/meta.yaml`
- Limited to public-facing pages

**City level — NYC Benefits Screening API documentation.**
- Source: https://screeningapidocs.cityofnewyork.us
- License: open / public
- Pin: API version recorded in the reference implementation's tool definition
- Used as the eligibility computation tool, not retrieved as text

### Explicitly excluded from the v1 corpus

**NYC HRA Policy Directives and Policy Bulletins (PD/PB).**

These are HRA's internal worker-facing policy documents. They are not publicly published as a canonical corpus on `nyc.gov`. Fragments surface in FOIL responses, in benefits-attorney practice guides (Empire Justice Center, CSS-NY's Benefits Plus Learning Center), and in HRA training materials, but there is no comprehensive public source.

We exclude them from v1 because:
- We cannot pin to a canonical revision
- We cannot ground citations in a public URL that reliably resolves
- The methodology PDF would have to caveat every HRA-specific citation, which is worse than excluding the layer

This is documented as a limitation in the README and methodology PDF. Cases whose correct answer turns on HRA-specific guidance are deferred to forward work.

## Consequences

**Positive:**
- Every citation in the suite resolves to a publicly verifiable source
- The federal–state citation chain is clean (7 CFR ↔ 18 NYCRR ↔ OTDA Source Book section)
- The corpus is small enough to pull, pin, and ship reproducibly
- The Day-14 citation-validity check (every `citation_url` resolves and contains the cited text) is feasible

**Negative:**
- We exclude an entire layer of operational guidance that real NYC caseworkers actually use. The methodology PDF must frame this honestly: the eval grounds in the layers we can publicly cite, and cases requiring HRA-specific knowledge are out of scope for v1.
- Some realistic caseworker questions cannot be tested in this version because their answers depend on HRA's internal interpretation of state policy.

## Alternatives considered

- **Include FOIL'd PD/PBs.** Rejected. They are not canonical, not version-controlled, and we can't guarantee a public URL.
- **Include third-party summaries (Empire Justice, CSS-NY).** Rejected as primary sources. These are excellent secondary sources but pinning to them introduces an editorial layer we can't audit.
- **Exclude NYC entirely; ship a federal+state-only eval.** Considered. Rejected because the project's positioning is explicitly NYC-focused (the MyCity context) and because the public-facing HRA pages and the Benefits Screening API give us enough city-level grounding for v1.

## References

- eCFR API documentation: https://www.ecfr.gov/reader-aids/ecfr-developer-resources/rest-api-interactive-documentation
- NYS OTDA SNAP Source Book: https://otda.ny.gov/programs/snap/SNAPSB.pdf
- OTDA GIS Message 25DC056 (Aug 21, 2025): https://www.otda.ny.gov/policy/gis/2025/25DC056.pdf
- NYC Benefits Screening API: https://screeningapidocs.cityofnewyork.us
- `docs/research/r4-corpus-access-verification.md` for the full corpus access audit
