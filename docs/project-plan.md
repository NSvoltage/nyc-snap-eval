# Project plan

The v2 build plan, distilled. Day-by-day sequencing for the two-week build.

## Thesis

The MyCity chatbot failed because there was no published, statute-grounded, measurable bar that the system was held to before it shipped. This project demonstrates what such a bar looks like for one program (SNAP) in one jurisdiction (New York) at one point in time, on one deployment surface (caseworker-facing). Approximately seventy cases across seven categories, a published grader, a validated judge, and a narrow reference implementation that runs against the same suite.

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
- **B. Policy-grounded factual recall** (~15) — anchored to 7 CFR Part 273 and the July 2025 NYS OTDA SNAP Source Book.
- **C. Refusal and escalation** (~8) — calibration on legal-advice-shaped requests. Tests both under-refusal (giving advice we shouldn't) and over-refusal (gating on legitimate questions).
- **D. Eligibility edge cases** (~12) — mixed-status families, ABAWD work requirements, formerly incarcerated, elderly LEP, gig income, students, fleeing-felon rules.
- **E. Adversarial inputs** (~8) — prompt injection, persona attacks, many-shot patterns. Only public attack patterns; no novel jailbreaks.
- **F. Multilingual consistency** (~10) — same case translated by certified translators across English, Spanish, and one Asian language. Parity-of-answer grading.
- **G. Citation and grounding** (~10) — GOV.UK Chat-style metrics: factual precision, factual recall, relevancy, groundedness. Citation URLs must resolve and contain the cited text.

## Day-by-day sequencing

### Day 1 — Repo scaffold and corpus pull
- [ ] Create public GitHub repo with the structure already scaffolded here
- [ ] Wire up Promptfoo with `promptfooconfig.yaml` pointing at the case sheet
- [ ] Pull 7 CFR Part 273 from the eCFR API, pin to a stated revision date, save JSON to `data/policy_corpus/federal/`
- [ ] Download `otda.ny.gov/programs/snap/SNAPSB.pdf` (July 2025), save with `meta.yaml` noting revision date
- [ ] Hit the NYC Benefits Screening API with curl against a synthetic household; confirm it responds without auth
- [ ] Scrape NYC HRA public SNAP guidance pages to `data/policy_corpus/nyc/`
- [ ] Send one outreach email to find an SME reviewer (Legal Aid, LSNY, or a benefits navigator at Single Stop / Hispanic Federation)

### Day 2 — Author the MyCity replay set (Category A)
- [ ] Pull every documented prompt from The Markup's March 2024 and April 2024 articles, plus AP and Entrepreneur follow-ups
- [ ] For each, write: the prompt, the source URL, the actual statute citation, the expected behavior, the hard-fail conditions
- [ ] All 13–15 cases authored in the Google Sheet
- [ ] First Promptfoo run against bare Claude Sonnet 4.5 — establishes the floor

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
