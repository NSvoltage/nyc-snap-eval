# Research Report 4 — Corpus access verification

> **Superseded in part by [r5](r5-freshness-audit-2026-05-11.md) (2026-05-11).** Two factual claims below were corrected by the Day-1 corpus pull: the NYS OTDA SNAP Source Book is now the **September 2025** revision (not July 2025), and the NYC Benefits Screening API **requires Bearer-token authentication** (not "open without auth" as recorded below). r5 also records the discontinuation of the MyCity chatbot and the post-OBBBA statutory landscape. The corrections are formalized in [ADR-008](../decisions/ADR-008-post-obbba-post-mycity-amendments.md). The original text is retained below as the historical record.

A verification audit of the policy sources the eval suite and reference implementation depend on. Conducted on 2026-05-11.

## Summary

All load-bearing sources are publicly accessible without authentication. One layer (NYC HRA Policy Directives and Bulletins) is not canonically published; ADR-005 excludes it from v1 scope.

## Sources confirmed accessible

### 7 CFR Part 273 — Certification of Eligible Households

- **URL:** https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273
- **API:** https://www.ecfr.gov/developers/documentation/api/v1
- **Bulk data:** GPO bulk XML
- **License:** Public domain (federal regulations)
- **Auth required:** None
- **Pinning:** eCFR API supports point-in-time access via revision date; we pin to a stated revision at corpus-pull time and record it in `data/policy_corpus/federal/meta.yaml`
- **Notes:** This is the cleanest source we have. Daily-updated, version-controlled, parseable XML/JSON, no rate limiting documented for normal use. The Part 273 structure (Subparts A–H, Sections 273.1–273.32) maps directly to the taxonomy in the OTDA Source Book, which makes citation chains trivial.

### NYS OTDA SNAP Source Book

- **URL:** https://otda.ny.gov/programs/snap/SNAPSB.pdf
- **License:** Public (NYS government document)
- **Auth required:** None
- **Pinning:** Latest revision is July 2025, confirmed via OTDA GIS Message 25DC056 (Aug 21, 2025) at https://www.otda.ny.gov/policy/gis/2025/25DC056.pdf
- **Notes:** Maps each section to both 18 NYCRR Part 387 and the corresponding 7 CFR sections. This is what makes the federal-state citation chain clean: a Source Book section comes with both citations pre-attached. Updated periodically; the GIS Message system at `otda.ny.gov/policy/gis/` provides change notifications.

### NYC Benefits Screening API

- **API docs:** https://screeningapidocs.cityofnewyork.us
- **Source repo:** https://github.com/CityOfNewYork/screeningapi-docs
- **Implementation:** https://github.com/NYCOpportunity/benefits-screening-api
- **Rules engine source:** https://github.com/NYCOpportunity/ACCESS-NYC-Rules (Drools BRMS)
- **License:** Open / public
- **Auth required:** None for basic use; rate limits documented at the docs URL
- **Notes:** Covers 35+ programs including SNAP, Cash Assistance, WIC, HEAP, Fair Fares, and Medicaid. Hosted on AWS Lambda by NYC Office of Technology and Innovation. This is the load-bearing tool for the reference implementation's deterministic eligibility computation (per ADR-002). The rules are auditable in the public Drools repo.

### NYC HRA public SNAP guidance

- **Primary URL:** https://www.nyc.gov/site/hra/help/snap-benefits-food-program.page
- **Related public pages:** SNAP FAQ, ABAWD page, ACCESS HRA help content
- **License:** Public (NYC government website)
- **Auth required:** None
- **Pinning:** Scraped on a specific date recorded in `data/policy_corpus/nyc/meta.yaml`
- **Notes:** Plain HTML pages, easily scrapable. Content includes the November 2025 implementation of ABAWD requirements (effective March 2026) and other operational details that don't appear in the federal/state corpus.

### NYS LDSS forms

- **URL:** https://otda.ny.gov/programs/applications/
- **Specific forms:** LDSS-4826 (SNAP application), LDSS-3421 (HEAP), LDSS-5208, others
- **License:** Public PDFs
- **Auth required:** None
- **Notes:** Useful for grounding cases that test procedural questions ("what forms does the applicant need," "what information is on the recertification form").

## Source explicitly excluded from v1

### NYC HRA Policy Directives and Policy Bulletins

- **Status:** Not canonically published on `nyc.gov`
- **What they are:** HRA's internal worker-facing operational policy documents that interpret state and federal SNAP policy for NYC-specific implementation
- **Where they surface:** FOIL responses, benefits-attorney practice guides (Empire Justice Center, CSS-NY's Benefits Plus Learning Center reference manual), HRA training materials
- **Why excluded:** Cannot pin to a canonical revision, cannot ground citations in a public URL that reliably resolves
- **Decision:** ADR-005 excludes this layer from v1. Cases whose correct answer requires HRA-specific guidance are deferred to forward work. The methodology PDF documents this as a limitation.

## Day 1 corpus-pull checklist

This is the action list derived from this audit, also reproduced in `docs/project-plan.md`:

- [ ] Pull all of 7 CFR Part 273 via the eCFR API, pin to a stated revision date, save JSON to `data/policy_corpus/federal/`
- [ ] Download `otda.ny.gov/programs/snap/SNAPSB.pdf` (July 2025 revision), save to `data/policy_corpus/state/` with `meta.yaml` recording revision date
- [ ] Hit the NYC Benefits Screening API with curl against a synthetic household; confirm it responds without auth; save the response schema to `data/policy_corpus/nyc/benefits-screening-api/`
- [ ] Scrape NYC HRA's public SNAP pages (FAQ, ABAWD, SNAP Benefits) to `data/policy_corpus/nyc/`
- [ ] Note in the methodology that HRA Policy Directives and Policy Bulletins are out of scope and document why

## Verification methodology

This audit consisted of:
1. Web searches for each candidate source by name
2. Direct retrieval of each URL to confirm it resolved
3. Confirmation that no authentication or registration was required for read access
4. Confirmation that the source had a stable URL structure suitable for pinning
5. For dynamic sources (eCFR, NYC pages), confirmation of an update-notification mechanism

The audit was conducted on 2026-05-11. Re-verification is recommended before each corpus refresh and is automated as part of the eval CI (see `scripts/verify_corpus.py` once implemented).
