# Research Report 5 — Freshness audit

A point-in-time re-audit of the policy landscape that the eval suite and reference implementation depend on, conducted while pulling the Day-1 corpus on 2026-05-11. Extends [`r4-corpus-access-verification.md`](r4-corpus-access-verification.md), which audited *access* but assumed sources were current.

## Summary

The post-2025 landscape has shifted in three ways that the prior research reports and ADR-005 did not contemplate:

1. The system the eval is anchored to — NYC's MyCity chatbot — was discontinued on 2026-02-05 by the incoming Mamdani administration.
2. The federal SNAP statute changed substantially when the One Big Beautiful Bill Act (OBBBA, P.L. 119-21) was signed on 2025-07-04, but the implementing regulations at 7 CFR Part 273 have not yet been amended, so the regulatory and statutory layers of our corpus are not aligned.
3. Two factual errors in ADR-005 and r4 were surfaced by the corpus pull itself: the NYS OTDA SNAP Source Book on disk is the September 2025 revision (not July 2025 as recorded), and the NYC Benefits Screening API requires an Authorization header (not "open without auth" as r4 reported).

None of these findings invalidate the project. They sharpen its framing — the eval becomes the bar that *would have* caught MyCity before the new administration shut it down, and the bar that post-OBBBA caseworker tooling needs to clear. This document records what changed, what we have, and what we still need.

## 1. MyCity chatbot was discontinued

- **Status as of 2026-05-11:** discontinued. `chat.nyc.gov` shows a "beta test has ended" notice directing visitors to NYC.gov. ([THE CITY, 2026-01-30](https://www.thecity.nyc/2026/01/30/mamdani-unusable-ai-chatbot-budget/))
- **Sequence of events:** Mayor Mamdani took office 2026-01-01. At a 2026-01-28 press conference he announced the termination, citing operating costs of approximately half a million dollars and the 2024 reporting by The Markup and THE CITY that documented illegal-action-inducing responses. The system was taken offline 2026-02-05. ([Futurism](https://futurism.com/artificial-intelligence/ai-chatbot-mamdani), [Vice](https://www.vice.com/en/article/zohran-mamdani-discontinues-nycs-troubled-chatbot/), [StateScoop](https://statescoop.com/mamdani-kill-nyc-ai-chatbot/))
- **The Markup's continued coverage:** Colin Lecher's follow-up piece confirmed the new administration's decision and re-referenced the original reporting. ([The Markup, 2026-01-30](https://themarkup.org/artificial-intelligence/2026/01/30/mamdani-to-kill-the-nyc-ai-chatbot-we-caught-telling-businesses-to-break-the-law))

**Implication for the eval.** Category A (MyCity replay, ~15 cases) was originally framed as a known-failure regression set anchored to The Markup's documented prompts. The chatbot is no longer available to test against directly, but this was already implicit — the case authoring uses Lecher's published prompts and the statutes the MyCity bot got wrong, not live API calls. The framing tightens: the eval becomes a post-mortem regression suite. The simulated baseline (ADR-004) is the only live comparator for the failure modes; the reference implementation demonstrates what the eval can be used to validate.

## 2. The One Big Beautiful Bill Act changed federal SNAP

- **Signed:** 2025-07-04. P.L. 119-21. ([FNS implementation index](https://www.fns.usda.gov/snap/obbb-implementation))
- **Provisions relevant to caseworker-facing tooling:**
  - ABAWD age band expanded to 18–64 (from 18–54). NYC implementation effective 2026-03-01 for approximately 123,000 NYC ABAWDs. ([THE CITY, 2026-02-27](https://www.thecity.nyc/2026/02/27/snap-work-requirements-trump/), [Healthbeat](https://www.healthbeat.org/newyork/2026/03/02/snap-work-requirements/))
  - Veterans, individuals experiencing homelessness, and youth aged out of foster care lost the ABAWD exemptions that had been added in the 2023 Fiscal Responsibility Act.
  - Humanitarian-noncitizen SNAP eligibility (refugees, asylees, trafficking survivors during first five years) sunsets 2026-04-09. ([FNS alien-eligibility memo](https://www.fns.usda.gov/snap/obbb-alien-eligibility))
  - Federal share of administrative costs drops from 50% to 25%, effective FY27 (2026-10-01).
  - Beginning FY28, states with SNAP payment-error rates ≥6% pay a share of benefit costs from state budgets — up to 15% if error rate ≥10%. ([CRS R48552](https://www.congress.gov/crs-product/R48552))
- **CBO estimate:** monthly SNAP participation falls by approximately 2.4 million.

**Implication for the corpus.** The federal *statute* changed substantially; the federal *regulations* at 7 CFR Part 273 have not. The eCFR API reports the most recent amendment to Part 273 as 2025-01-17 (pre-OBBBA). This is normal — implementation rulemaking follows statute. For our purposes it means:

| Layer | Source | Post-OBBBA? |
|---|---|---|
| Federal statute | OBBBA / P.L. 119-21 | yes (by definition) |
| Federal regulations | 7 CFR Part 273 (eCFR snapshot 2026-05-08, amended 2025-01-17) | **no** |
| State manual | NYS OTDA SNAP Source Book, Sept 2025 cover | yes (Source Book republished post-OBBBA) |
| State guidance memos | OTDA GIS messages | partially — see §4 |
| NYC public pages | HRA SNAP pages (retrieved 2026-05-11) | yes (e.g., ABAWD page reflects 2026-03-01 effective date) |

Cases that test post-OBBBA SNAP rules need to cite the statute, the OTDA Source Book, and the relevant GIS messages — not 7 CFR alone. The methodology PDF should call out this regulatory lag explicitly.

## 3. Corrections to ADR-005

Two factual errors surfaced during the Day-1 corpus pull:

### 3a. SNAPSB revision is Sept 2025, not July 2025

ADR-005 states "Pin: July 2025 revision, confirmed via OTDA GIS Message 25DC056." The PDF at `https://otda.ny.gov/programs/snap/SNAPSB.pdf` displays "Version: Sept 2025" on its cover page. The Wayback snapshot's `x-archive-orig-last-modified` header is `Wed, 24 Sep 2025 14:21:36 GMT`. OTDA appears to have republished the Source Book post-OBBBA (signed 2025-07-04) and post-GIS-25DC056 (issued 2025-08-21). We retrieved the live version, which is the September 2025 revision. ADR-008 records the correction.

### 3b. The NYC Benefits Screening API requires authentication

ADR-005 and r4 both state "Auth required: None for basic use." The OpenAPI specification at `https://raw.githubusercontent.com/CityOfNewYork/screeningapi-docs/main/dist/resources/benefits_screening_api.yaml` defines a `securitySchemes.ApiKeyAuth` and requires `Authorization: Bearer <token>` on `/eligibilityPrograms`. The token is issued by `POST /authToken` with registered username/password credentials. Smoke tests on 2026-05-11 against both `sandbox.screeningapi.cityofnewyork.us` and `screeningapi.cityofnewyork.us` returned `HTTP 401 {"message":"Unauthorized"}` for unauthenticated requests, including with a syntactically valid composite household payload (see `data/policy_corpus/nyc/benefits-screening-api/sample-requests/`).

This is a Days-8-10 prerequisite: the reference implementation needs a registered Screening API account. ADR-008 records the correction.

## 4. GIS messages worth adding to the corpus

Identified during the audit. None are in the v1 corpus yet; ADR-008 covers the corpus expansion.

| ID | Title | Notes |
|---|---|---|
| 25DC055 | Summary of SNAP Changes in the One Big Beautiful Bill | Issued 2025-Q3. Load-bearing for any case that tests post-OBBBA rules. |
| 25DC024 | 2025–2026 SNAP Income Guidelines | FY26 baseline income standards. |
| 25DC056 | Already referenced in ADR-005 as the July-2025 confirmation. We retain the reference for the historical record even though the September 2025 revision supersedes the July 2025 revision it described. |
| 25DC059, 25DC081 | OTDA-4357-EL form revisions | Useful for procedural cases (Category D). |
| 26DC007 | 200% of Poverty Income Standards Chart, effective 2026-06-01 | Used in expedited-issuance eligibility. |

Source: OTDA GIS index at `https://otda.ny.gov/policy/gis/` (currently unreachable from the pulling network; reached via Wayback or direct GIS URLs).

## 5. What we have on disk after Day 1

| Path | Source | Revision | Retrieved | Provenance |
|---|---|---|---|---|
| `data/policy_corpus/federal/7-cfr-273/` | eCFR API | 2025-01-17 amendment, 2026-05-08 snapshot | 2026-05-11 | direct |
| `data/policy_corpus/state/otda-snap-source-book/` | NYS OTDA | Version: Sept 2025 | 2026-05-11 | **Wayback fallback** — OTDA origin blocked from pulling network |
| `data/policy_corpus/nyc/hra-public-pages/` | NYC HRA | live | 2026-05-11 | direct, 10 pages |
| `data/policy_corpus/nyc/benefits-screening-api/` | NYC OTI | OpenAPI 1.0.0 spec via GitHub | 2026-05-11 | spec direct from `CityOfNewYork/screeningapi-docs`; live endpoints confirmed reachable but require auth |

The OTDA-origin block is a network-level rejection from this specific pulling environment (RST at TLS layer, then HTML WAF page on retry). It is not a property of OTDA's servers. When the corpus is refreshed from a network with OTDA reachability, the SNAPSB.pdf should be byte-compared against the Wayback artifact and the meta.yaml updated.

## 6. Re-audit cadence

The corpus is point-in-time. SNAP policy is changing faster in 2026 than the project plan assumed. Recommended re-audit triggers:

- Before any public-facing claim about results (Day 11 onward).
- When a new OTDA GIS message is published in the SNAP series (subscribe to `otda.ny.gov/policy/gis/`).
- When FNS publishes a final or interim rule implementing OBBBA SNAP provisions.
- When the eCFR `versions` endpoint reports a new amendment to 7 CFR Part 273.
- When HRA materially changes the published ABAWD or eligibility pages.

`scripts/verify_corpus.py` (planned in `scripts/README.md`) should be implemented to automate the first four checks.

## Verification methodology

Conducted on 2026-05-11. Inputs:

- Direct fetches and HTTP smoke tests by the Day-1 corpus pull scripts in `scripts/`.
- Web searches against news sources, federal and state agency sites, and primary-source repositories. Results triangulated across at least two independent reports per claim.
- Wayback Machine for OTDA artifacts where the origin was unreachable.

This audit does not replace SME review. The SME engagement scheduled for Day 1 of the project plan is still needed to validate the policy substance behind any specific case.
