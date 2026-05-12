# Project plan

The v2 build plan, distilled. Day-by-day sequencing for the two-week build.

## Where we are (updated 2026-05-11)

> Aggregate in-flight / blocked / done / forward-milestones view: [`docs/status.md`](status.md). The day-by-day plan below is the canonical sequencing; `status.md` is the cross-day aggregate.

**Days 1 and 2 are complete.** Corpus is pulled and pinned, Promptfoo config validates, and the Category A (MyCity replay) case set is authored and committed. The state-of-the-world findings from Day 1 are recorded in the Day-1 freshness audit ([`r5`](research/r5-freshness-audit-2026-05-11.md)) and [ADR-008](decisions/ADR-008-post-obbba-post-mycity-amendments.md):

- MyCity chatbot was discontinued by the Mamdani administration on 2026-02-05 → Category A is a post-mortem regression set.
- The One Big Beautiful Bill Act of 2025-07-04 reshaped federal SNAP statute, but 7 CFR Part 273 has not been amended since 2025-01-17 → cases that hinge on post-OBBBA rules must cite the statute and state guidance, not federal regulations alone.
- The NYS OTDA SNAP Source Book on disk is the **September 2025** revision (not July 2025 as originally pinned). OTDA GIS messages 25DC024, 25DC055, 25DC056, 25DC059, 25DC081 are also in the corpus; 26DC007 is a follow-up.
- The NYC Benefits Screening API **requires Bearer-token authentication**. A registered account is a Days-8–10 prerequisite.
- The `otda.ny.gov` origin was unreachable from the pulling network; SNAPSB and GIS messages were Wayback-served. Byte-comparison against the origin is a corpus-refresh hygiene item.

Day-2 added one new finding of the same shape (parallel to ADR-008 §5):

- The **state and city legislative-codifier sites** (`nysenate.gov`, `codelibrary.amlegal.com`, `law.justia.com`, `codes.findlaw.com`) all return Cloudflare bot-protection challenges (HTTP 403) from the corpus-pull network, even with full browser-class headers. Canonical URLs *do* resolve in real browsers and *do* contain the cited statute text — the constraint is bot detection, not link rot. Per-row Wayback fallback URLs (verified 2026-05-11) are recorded in the `notes` column of [`eval/cases/A_mycity_replay.csv`](../eval/cases/A_mycity_replay.csv); the framing decisions and full contingency are in [`docs/handoffs/day-2-category-a-authoring-notes.md`](handoffs/day-2-category-a-authoring-notes.md). Day-14 `verify_citations.py` will need a browser-class fetcher (Playwright or `curl-impersonate`) and an NY Open Legislation API key to satisfy hard rule #1 from CI.

**Pick up here:** Day 3 — seed-case authoring for Categories B (factual recall), C (refusal/escalation), D (eligibility edge cases), and G (citation/grounding) per the day-by-day below. These seeds become the inputs to the Days 4–7 synthetic-expansion pipeline. Each new tab in the [authoring sheet](https://docs.google.com/spreadsheets/d/1CV7O8qHMTYQVFHCVFkWIE_zeDsFIyUDovCDLCHPmAcc/edit) needs first-time setup (header row in row 1) per [`eval/cases/README.md`](../eval/cases/README.md#first-time-sheet-setup-one-off) before authoring; the Day-2 export already validated that workflow end-to-end. Day-2 stretch goal **not yet done**: first Promptfoo run against bare Claude Sonnet 4.5 to establish the Category-A floor. Roll into Day 3 or sequence as Day 3 prerequisite.

Open Day-1 items still pending (drafts ready at [`docs/outreach/`](outreach/)): SME-reviewer outreach send (target end of Day 3 to keep the Days-4–7 SME-review window) and the NYC Benefits Screening API account request submission (Days-8–10 prerequisite; lead time unknown).

## Thesis

The MyCity chatbot failed because there was no published, statute-grounded, measurable bar that the system was held to before it shipped. Mayor Mamdani took office on 2026-01-01 and discontinued MyCity on 2026-02-05, citing operating cost and the documented failure modes The Markup and THE CITY had reported. This project demonstrates what a bar of that shape looks like for one program (SNAP) in one jurisdiction (New York) at one point in time, on one deployment surface (caseworker-facing). Approximately seventy cases across seven categories, a published grader, a validated judge, and a narrow reference implementation that runs against the same suite. With MyCity offline, Category A is a post-mortem regression set rather than a live A/B (per ADR-008 §4); the rest of the methodology is unaffected.

## Deliverables

1. **Eval suite** — ~70 cases across seven categories, authored in a public Google Sheet, consumed by Promptfoo, every case anchored to a 7 CFR or NYS OTDA citation.
2. **Published grader** — Claude Opus 4.5 as judge with the full meta-prompt versioned at `eval/graders/llm_judge_meta_prompt.md`. Validation against SME-labeled gold examples reported as Cohen's κ.
3. **Reference implementation** — Claude Sonnet 4.5 with RAG over federal and state SNAP policy, deterministic eligibility via the NYC Benefits Screening API, mandatory inline citations, hard refusal on legal advice, deployed at a Vercel URL.
4. **Simulated baseline** — a deliberately under-scaffolded configuration (RAG-light, no eligibility tool, weak system prompt) for delta comparison. Labeled "simulation, not replication" every time it appears.
5. **Methodology PDF** — twelve to fifteen pages, structured like an Anthropic research note. Section structure in `docs/conventions.md`.
6. **README** — applies the tone checklist; credits Propel, The Markup, and others in the first 1,000 words.
7. **Blog post** — single post in the Propel three-part register.
8. **Architecture Decision Records** — every load-bearing design choice has a dated ADR.

## The seven eval categories

Settled per ADR-006. Approximate case counts in parens.

- **A. MyCity replay** (~15) — known-failure regression set, anchored to The Markup's documented prompts and the specific statutes the MyCity bot got wrong. Stochastic-consistency metric: N=10 per case to detect run-to-run instability.
- **B. Policy-grounded factual recall** (~15) — anchored to 7 CFR Part 273 (latest amendment 2025-01-17, pre-OBBBA), the September 2025 NYS OTDA SNAP Source Book (post-OBBBA), and OTDA GIS message 25DC055 (OBBBA summary). Cases that hinge on post-OBBBA SNAP rules must cite the statute and state guidance, not federal regulations alone (see ADR-008 §3).
- **C. Refusal and escalation** (~8) — calibration on legal-advice-shaped requests. Tests both under-refusal (giving advice we shouldn't) and over-refusal (gating on legitimate questions).
- **D. Eligibility edge cases** (~12) — mixed-status families, ABAWD work requirements, formerly incarcerated, elderly LEP, gig income, students, fleeing-felon rules.
- **E. Adversarial inputs** (~8) — prompt injection, persona attacks, many-shot patterns. Only public attack patterns; no novel jailbreaks.
- **F. Multilingual consistency** (~10) — same case translated by certified translators across English, Spanish, and one Asian language. Parity-of-answer grading.
- **G. Citation and grounding** (~10) — GOV.UK Chat-style metrics: factual precision, factual recall, relevancy, groundedness. Citation URLs must resolve and contain the cited text.

## Day-by-day sequencing

### Day 1 — Repo scaffold and corpus pull
- [x] Wire up Promptfoo with `promptfooconfig.yaml` (validated; CSV paths point at `eval/cases/`)
- [x] Pull 7 CFR Part 273 from the eCFR API; pinned to 2026-05-08 snapshot (latest Part 273 amendment 2025-01-17, pre-OBBBA — see ADR-008 §3)
- [x] Pull the September 2025 NYS OTDA SNAP Source Book to `data/policy_corpus/state/otda-snap-source-book/` (Wayback fallback used because OTDA origin was unreachable from this network — see ADR-008 §5)
- [x] Pull OTDA GIS messages 25DC024, 25DC055, 25DC056, 25DC059, 25DC081 to `data/policy_corpus/state/otda-gis/` (26DC007 unavailable in Wayback at retrieval; tracked as a follow-up)
- [x] Smoke-test the NYC Benefits Screening API; OpenAPI spec saved and auth requirement documented in `data/policy_corpus/nyc/benefits-screening-api/meta.yaml`. Endpoint **requires** Bearer-token auth — see ADR-008 §2.
- [x] Scrape 10 NYC HRA public SNAP guidance pages to `data/policy_corpus/nyc/hra-public-pages/`
- [x] Conduct a freshness audit; record findings in `docs/research/r5-freshness-audit-2026-05-11.md` and decisions in ADR-008
- [ ] Send one outreach email to find an SME reviewer (Legal Aid, LSNY, or a benefits navigator at Single Stop / Hispanic Federation)
- [ ] Create public GitHub repo — deferred to Day 14 per the polish-and-publish sequence

### Day 2 — Author the MyCity replay set (Category A)
- [x] Pull every documented prompt from The Markup's March 2024 and April 2024 articles, plus AP and Entrepreneur follow-ups (13 verbatim from r2 §4 + 2 paraphrases on the Section-8 stochastic-inconsistency case and the food-adulteration highest-harm case)
- [x] For each, write: the prompt, the source URL, the actual statute citation, the expected behavior, the hard-fail conditions (refusal-and-redirect framing per ADR-003 + ADR-008 §4; framing decisions and per-case harm rationale recorded in [`docs/handoffs/day-2-category-a-authoring-notes.md`](handoffs/day-2-category-a-authoring-notes.md))
- [x] All 15 cases authored in the Google Sheet and exported to [`eval/cases/A_mycity_replay.csv`](../eval/cases/A_mycity_replay.csv)
- [ ] First Promptfoo run against bare Claude Sonnet 4.5 — establishes the floor *(Day-2 stretch; rolled to Day 3 prerequisite)*

### Day 3 — Seed cases for B, C, D, G
- [ ] 3–4 hand-written factual recall cases pinned to specific 7 CFR sections
- [ ] 2–3 refusal/escalation cases covering legal advice, immigration enforcement risk, out-of-scope
- [ ] 2–3 eligibility edge cases (one mixed-status, one ABAWD, one self-employed)
- [ ] 2–3 citation-grounding cases
- [ ] These are seeds for synthetic expansion in days 4–7

### Days 4–7 — Synthetic expansion pipeline
- [ ] Implement the hybrid generation pipeline per `docs/research/r3-synthetic-data.md` §"Test case expansion"
- [ ] Six scenario axes × three subtopics × four cases per cell, plus the categories not covered by that grid (E, F)
- [ ] Three-tier verification: rule-based structural checks, statute-grounded LLM judging in both orderings, SME spot-check
- [ ] ROUGE-L deduplication against seed cases
- [ ] Publish the full generation prompt in `eval/graders/`
- [ ] SME reviewer engaged for cases requiring expert review; track and report disagreement

### Days 8–10 — Reference implementation and simulated baseline
- [ ] Stand up Next.js + Vercel AI SDK demo
- [ ] Implement RAG over the policy corpus (pgvector on Supabase, voyage-3 embeddings)
- [ ] Implement `check_eligibility` tool calling the NYC Benefits Screening API
- [ ] Implement `retrieve_policy` and `escalate` tools
- [ ] System prompt with citation enforcement and refusal patterns
- [ ] Deploy to Vercel
- [ ] Author the simulated baseline configuration (same model, weak system prompt, naive retrieval, no tools) — label clearly
- [ ] Run the full eval against: (a) reference implementation, (b) bare Sonnet 4.5, (c) GPT-4o, (d) Gemini 2.5 Pro, (e) simulated baseline
- [ ] Generate per-case results with 95% CIs

### Days 11–13 — Writeup
- [ ] Methodology PDF, twelve to fifteen pages, structured per `docs/conventions.md`
- [ ] README, applying the tone checklist
- [ ] Blog post, single post in Propel's three-part register
- [ ] Recruit one external reader to flag jargon and marketing tells
- [ ] Recruit one SME for technical review of the writeup

### Day 14 — Polish and publish
- [ ] Verify every claim has a citation or a confidence interval
- [ ] Verify every public-facing document credits Propel, The Markup, GOV.UK GDS, Nava Labs, CfA, Stanford RegLab in the first 1,000 words
- [ ] Run the tone checklist end-to-end on README and blog post
- [ ] Confirm every URL in every citation field resolves
- [ ] Make the repo public
- [ ] Publish the blog post
- [ ] Email the recruiter with three links and a 100-word pitch

## Forward work, explicitly not in v1

These are framed as future work in the methodology PDF and README. Do not let scope creep pull them into v1.

- **Applicant-facing rubrics** — plain-language Flesch-Kincaid gates, categorical refusal patterns, trauma-informed framing, no-PII solicitation tests, disclaimer integrity. The MyCity failure was specifically about lay users acting on illegal-action-inducing model output. v2 has to solve harder problems and is sized accordingly.
- **Native-language generation rubrics** — v1 ships multilingual consistency tests, not native-language quality grading.
- **Live caseworker user study** — RCT-style field evaluation à la Nava's Imagine LA work. Out of scope.
- **Cross-program transfer** — Medicaid, TANF, WIC, LIHEAP. Discussed as a hypothesis, not tested.
- **NYC HRA Policy Directive / Policy Bulletin grounding** — the corpus isn't publicly canonical, so we exclude cases that would require it.

## The unresolved tensions

Named honestly in the methodology PDF:
1. **SME pool is small.** If reviewers can't agree on a case, it's documented as contested rather than scored.
2. **Simulated baseline is not MyCity.** It's a known-bad-pattern anchor.
3. **Applicant-facing v2 is the more important problem.** We're not shipping it. Framed as sequencing, not lack of ambition.
