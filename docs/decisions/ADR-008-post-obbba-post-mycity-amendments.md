# ADR-008: Post-OBBBA, post-MyCity amendments to ADR-005 and project framing

**Status:** Accepted
**Date:** 2026-05-11
**Decision-makers:** [project lead]
**Supersedes parts of:** ADR-005
**Derived from:** `docs/research/r5-freshness-audit-2026-05-11.md`

## Context

During the Day-1 corpus pull on 2026-05-11, three facts surfaced that ADR-005 and the upstream research reports had not contemplated:

1. **MyCity is no longer deployed.** Mayor Mamdani announced its termination on 2026-01-28; `chat.nyc.gov` showed a beta-ended notice from 2026-02-05 onward. The system the eval's Category A regression set was anchored against is offline.
2. **The federal SNAP statute changed in 2025.** The One Big Beautiful Bill Act (P.L. 119-21, signed 2025-07-04) reshaped ABAWD age bands, removed humanitarian-noncitizen eligibility, shifted federal/state cost share, and more. The implementing regulations at 7 CFR Part 273 have not yet been amended.
3. **Two factual errors in ADR-005 / r4 were surfaced by the corpus pull itself:** the SNAPSB on `otda.ny.gov` is the September 2025 revision (not July 2025 as recorded), and the NYC Benefits Screening API requires Bearer-token authentication (not "open without auth" as r4 reported).

ADR-005 and the research reports are immutable by convention. This ADR records the necessary corrections and corpus additions without rewriting prior decisions.

## Decision

### 1. Correct the SNAPSB revision pin

The pinned NYS OTDA SNAP Source Book revision is **the September 2025 revision** (cover-page text: "Version: Sept 2025"; origin `Last-Modified` header `Wed, 24 Sep 2025 14:21:36 GMT`). ADR-005's reference to a "July 2025 revision, confirmed via OTDA GIS Message 25DC056" remains in the historical record as the originally targeted revision; OTDA appears to have republished the Source Book between GIS 25DC056 (2025-08-21) and our retrieval (2026-05-11). The retrieved artifact is post-OBBBA and is what the eval cites going forward.

### 2. Record the Benefits Screening API authentication requirement

The NYC Benefits Screening API's `/eligibilityPrograms` endpoint requires an `Authorization: Bearer <token>` header. Tokens are issued by `POST /authToken` with registered username/password credentials. Confirmed against both `sandbox.screeningapi.cityofnewyork.us` and `screeningapi.cityofnewyork.us` on 2026-05-11; unauthenticated requests return HTTP 401. The reference implementation (project plan Days 8–10) needs a registered account. ADR-005's claim that the API is "open without auth" is corrected.

### 3. Expand the state-level corpus to include OTDA GIS messages

In addition to the SNAP Source Book, the v1 corpus now includes the following GIS (General Information System) messages, pulled into `data/policy_corpus/state/otda-gis/`:

- **25DC024** — 2025–2026 SNAP Income Guidelines
- **25DC055** — Summary of SNAP Changes in the One Big Beautiful Bill
- **25DC056** — referenced in ADR-005 as the July-2025 SNAPSB confirmation, retained for historical traceability
- **25DC059** — OTDA-4357-EL form revision
- **25DC081** — OTDA-4357-EL form revision (REV 05/25)

26DC007 (the 200%-of-FPL chart effective 2026-06-01) is on the desired list but is not yet available in the Wayback Machine and is unreachable from the pulling network. It is a TODO for the next corpus refresh, recorded in `scripts/pull_otda_sourcebook.py`'s `GIS_INDEX`.

GIS messages are operational guidance memoranda OTDA publishes between Source Book revisions. They are publicly hosted at `otda.ny.gov/policy/gis/{YYYY}/{ID}.pdf`, so they meet ADR-005's "publicly accessible, version-pinned" criteria.

### 4. Frame Category A as a post-mortem regression set

ADR-006 lists Category A as the "MyCity replay" set. The case-authoring methodology does not change — cases are still anchored to The Markup's documented prompts and the statutes the MyCity bot got wrong. What changes is the framing in the project plan and methodology PDF: Category A tests behavior on the prompts that exposed MyCity's failure modes; it is not a live A/B against the system because the system was discontinued in February 2026. This framing is in some ways *stronger* — it positions the eval as the kind of bar the new administration's decision implies the city should have applied. CLAUDE.md, `docs/project-plan.md`, and ADR-006's framing paragraphs are updated to acknowledge this.

### 5. Document the OTDA network-block contingency in the corpus pull tooling

`scripts/pull_otda_sourcebook.py` falls back to the Wayback Machine when the OTDA origin returns either a TLS-level reset or a WAF block-page HTML response on a 200. Both modes were observed during the Day-1 pull. The fallback is recorded in each artifact's `meta.yaml` under `source.fetched_from`. When a future pull runs from a network with OTDA reachability, the artifacts should be byte-compared against the Wayback-served versions and the meta updated. This is a corpus-refresh hygiene item, not an outstanding risk.

## Consequences

**Positive:**
- The corpus on disk reflects post-OBBBA reality at both the state-manual layer (SNAPSB Sept 2025) and the guidance-memo layer (GIS messages).
- The Screening API auth requirement is now known up front, so it is a Days-8-10 sequencing item rather than a Day-9 surprise.
- The Category A framing pivot uses the post-MyCity reality as evidence for the project's thesis, rather than treating it as scope-disruption.
- The OTDA network-block contingency has a documented fallback, so the corpus pull is reproducible from networks that don't have OTDA reachability.

**Negative:**
- The federal-regulations layer (7 CFR Part 273, last amended 2025-01-17) is pre-OBBBA. Cases that test post-OBBBA SNAP rules need to cite the statute and state guidance, not federal regulations alone. The methodology PDF must call this out as a structural limitation.
- One desired GIS message (26DC007) is currently unobtainable; the corpus is incomplete in one identified slot. Tracked as a follow-up.
- Trust in the upstream research reports drops modestly: r4 was wrong about the Screening API auth, and the SNAPSB revision date was stale. The re-audit cadence in r5 §6 mitigates this.

**Cross-impacts on other ADRs:**
- ADR-005 is amended by §§1, 2, 3 of this ADR. The original ADR-005 remains in place as the historical record.
- ADR-006 is amended by §4. The seven categories themselves do not change; Category A's framing does.
- ADR-002 (eligibility math via Screening API) is reinforced — the API is reachable and the spec is sound — but the auth prerequisite is now explicit.

## Alternatives considered

- **Edit ADR-005 in place.** Rejected. ADRs are append-only per `docs/decisions/README.md`. Editing prior records breaks the audit trail.
- **Defer all of this to the Day-13 writeup.** Rejected. The corrections affect what Day 2 case authoring cites (post-OBBBA rules) and what Days-8-10 reference-implementation work needs (Screening API credentials). Deferring would push the work into a worse window.
- **Drop Category A entirely now that MyCity is offline.** Rejected. The published prompts and statutes are still the strongest documented failure-mode set in public-sector benefits AI. The framing change preserves the evidential value.

## References

- `docs/research/r5-freshness-audit-2026-05-11.md` — full audit, with citations.
- ADR-005 — original policy corpus decision.
- ADR-006 — seven eval categories.
- The Markup, "Mamdani to kill the NYC AI chatbot we caught telling businesses to break the law" (2026-01-30): https://themarkup.org/artificial-intelligence/2026/01/30/mamdani-to-kill-the-nyc-ai-chatbot-we-caught-telling-businesses-to-break-the-law
- THE CITY, "Mamdani Targets 'Unusable' AI Chatbot for Termination" (2026-01-30): https://www.thecity.nyc/2026/01/30/mamdani-unusable-ai-chatbot-budget/
- FNS, "SNAP Provisions of the One Big Beautiful Bill Act of 2025 Information Memorandum": https://www.fns.usda.gov/snap/obbb-implementation
- CRS R48552, "SNAP and Related Nutrition Programs in P.L. 119-21": https://www.congress.gov/crs-product/R48552
- NYS OTDA SNAP page (live, but origin currently unreachable from many networks): https://otda.ny.gov/programs/snap/
- NYC Benefits Screening API OpenAPI spec: https://raw.githubusercontent.com/CityOfNewYork/screeningapi-docs/main/dist/resources/benefits_screening_api.yaml
