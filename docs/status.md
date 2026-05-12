# Status

The in-flight + blocked + done view across the whole effort. The day-by-day plan lives in [`project-plan.md`](project-plan.md); the per-day handoff briefs live in [`handoffs/`](handoffs/); this file is the aggregate.

**Update cadence.** Refresh end-of-day, or whenever (a) something moves between sections, (b) a new blocker surfaces, or (c) a milestone date should shift. Commit alongside the work that caused the change with a `docs(status):` Conventional Commits prefix. The `Last touched` line below is the freshness signal.

**Last touched:** 2026-05-11 (Day 2 close)

---

## In flight (Day 3 — 2026-05-12)

| Item | Owner | Notes |
|---|---|---|
| Promptfoo Category-A floor run against bare Claude Sonnet 4.5 | Claude Code | Day-2 stretch carried over; Day-3 sequencing prerequisite. Save results to `eval/results/2026-05-12-cat-a-floor/`. Per [day-3-kickoff §4.0](handoffs/day-3-kickoff.md#40-carry-over-first-promptfoo-run-on-category-a-sequencing-prerequisite). |
| Category B seed authoring (3–4 cases) | Claude Code + human paste | Pin post-OBBBA cases to OBBBA / OTDA SNAPSB / OTDA GIS 25DC055, not 7 CFR alone. Per [day-3-kickoff §4.1](handoffs/day-3-kickoff.md#41-category-b--policy-grounded-factual-recall-34-seeds). |
| Category C seed authoring (2–3 cases) | Claude Code + human paste | Tests both under-refusal and over-refusal. Per [day-3-kickoff §4.2](handoffs/day-3-kickoff.md#42-category-c--refusalescalation-23-seeds). |
| Category D seed authoring (2–3 cases) | Claude Code + human paste | LLM never computes eligibility math (hard rule #3, ADR-002). Per [day-3-kickoff §4.3](handoffs/day-3-kickoff.md#43-category-d--eligibility-edge-cases-23-seeds). |
| Category G seed authoring (2–3 cases) | Claude Code + human paste | GOV.UK Chat-style metrics: precision/recall/relevancy/groundedness. Per [day-3-kickoff §4.4](handoffs/day-3-kickoff.md#44-category-g--citationgrounding-23-seeds). |
| Send SME outreach (first batch) | Human | Drafts at [`outreach/sme-outreach.md`](outreach/sme-outreach.md). Three open variables to fill before sending. **Send by end of Day 3** to keep within the Days-4–7 SME-review window. |
| Submit NYC Benefits Screening API account request | Human | Draft at [`outreach/screening-api-account-request.md`](outreach/screening-api-account-request.md). Submit via the [eepurl form](http://eepurl.com/gfLTuH); fall back to `products@nycopportunity.nyc.gov` only if no response in ~5 business days. |

## Blocked / waiting

| Item | Waiting on | First needed by | Mitigation if late |
|---|---|---|---|
| SME reviewer engagement | Response to outreach (sent end of Day 3) | Day 4 | Days-4–7 synthetic-expansion uses LLM-judge validation only; SME pass becomes a Day-13/14 hygiene item rather than the inter-rater Cohen's κ source. Methodology PDF flags reduced validation strength explicitly. |
| NYC Benefits Screening API credentials | NYC OTI account approval | Day 8 | Per [ADR-008 §2](decisions/ADR-008-post-obbba-post-mycity-amendments.md#2-record-the-benefits-screening-api-authentication-requirement) the fallback is the deterministic Python port of OTDA tables. Days-8–10 still ships, but the demo loses the live-API branch. |
| OTDA `otda.ny.gov` byte-compare against Wayback artifacts | Network access from a host with OTDA reachability | Day 14 (corpus-refresh hygiene) | Acceptable to ship v1 against the Wayback-served SNAPSB; flagged in methodology PDF limitations. |
| OTDA GIS 26DC007 (200% FPL chart, eff. 2026-06-01) | Wayback availability or OTDA reachability | Day 4 (Category B post-OBBBA seeds may want it) | Cite GIS 25DC024 (FY26 baseline income guidelines) instead and note 26DC007 as forward-update. |
| `verify_citations.py` (Day 14) needs Playwright/`curl-impersonate` + NY Open Legislation API key | Implementation work + API key request | Day 14 | Manual spot-check of the ~70 `citation_url` fields if automation isn't ready; track in [day-2-category-a-authoring-notes.md §2](handoffs/day-2-category-a-authoring-notes.md#2-citation-url-contingency-parallel-to-adr-008-5-otda-pattern) follow-ups. |

## Forward milestones

Dates are derived from [`project-plan.md`](project-plan.md). Anchored against today (2026-05-11) so slip is visible.

| Date | Milestone | What must be true |
|---|---|---|
| 2026-05-12 | Day 3 close | Promptfoo Category-A floor recorded; 9–12 seeds across B/C/D/G committed; SME outreach sent; Screening API form submitted. |
| 2026-05-13 | Days 4–7 begin | Synthetic-expansion pipeline implementation per [r3 §"Test case expansion"](research/r3-propel-positioning-synthetic-data-voice.md). |
| ~2026-05-14 | SME reviewer ideally engaged | Inside the 4-day Days-4–7 review window for synthetic cases. |
| 2026-05-18 | Days 8–10 begin | Reference implementation (Next.js + RAG + Screening API tool). Screening API credentials must be in hand. |
| ~2026-05-22 | Days 11–13 writeup begins | All eval results runnable; methodology PDF, README, blog post drafting. |
| 2026-05-24 | Day 14 polish + publish | Repo public, blog post live, recruiter email sent. |

## Done

Rolling done log, most recent first. Each entry: date — short description (commit short-SHA).

- **2026-05-11** — Day 2 close: project plan updated; first Promptfoo run + SME send + Screening API form rolled to Day 3 (`102339b`)
- **2026-05-11** — Day 2: 15 Category-A MyCity-replay cases authored, exported, committed; refusal-and-redirect framing + citation-URL contingency captured in [day-2-category-a-authoring-notes.md](handoffs/day-2-category-a-authoring-notes.md) (`4764639`)
- **2026-05-11** — r2 substantive content paste-in (`1a24bb7`)
- **2026-05-11** — Day-2 kickoff brief drafted (`92d4b50`)
- **2026-05-11** — Authoring-sheet → CSV export wired (`fdfa84b`)
- **2026-05-11** — SME outreach + Screening API account drafts (`0a8fc8c`)
- **2026-05-11** — Day-1 close: freshness audit + ADR-008 amendments to ADR-005 (`f9da5b1`)
- **2026-05-11** — Day 1: SNAP policy corpus pulled per ADR-005 + ADR-008 (federal 7 CFR 273, NYS OTDA SNAPSB Sept 2025, OTDA GIS 25DC024/055/056/059/081, NYC HRA pages, Screening API spec) (`d557107`)
