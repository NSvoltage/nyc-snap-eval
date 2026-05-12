# Conventions

How we write code and prose in this repo. Hard rules, with rationale where useful.

## 1. Code style

### Python (graders, scripts, RAG pipeline)
- Python 3.11+
- `ruff` for formatting and linting (`ruff format`, `ruff check`)
- Type hints on every function signature
- Docstrings in Google style for public functions
- `pytest` for tests
- No more than ~100 lines per module without justification; if it grows past that, split it

### TypeScript (demo)
- Next.js 15 (App Router)
- TypeScript strict mode
- `prettier` for formatting
- `eslint` with the Next.js config
- Server actions over API routes where possible

### Naming
- File names: kebab-case (`mycity-replay-cases.csv`, not `MyCityReplayCases.csv`)
- Python: `snake_case` everywhere
- TypeScript: `camelCase` for variables, `PascalCase` for components and types
- ADRs: `ADR-NNN-short-slug.md` (zero-padded three-digit number)

## 2. Eval case schema

Every row in the authoring sheet has these columns. No exceptions.

| Column | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Stable identifier, format `A-001`, `B-014`, etc. Category letter + zero-padded number. |
| `category` | enum | yes | One of A/B/C/D/E/F/G per `docs/project-plan.md`. |
| `subcategory` | string | yes | Free-text, e.g., "ABAWD work requirements" or "Section 8 source-of-income." |
| `question` | string | yes | The prompt under test. |
| `expected_behavior` | string | yes | What a passing answer does. Prose, not a regex. |
| `hard_fail_conditions` | string | yes | What automatically fails. Prose. |
| `citation` | string | yes | Statute or policy citation, e.g., "7 CFR 273.5(b)(8)" or "NYS SNAP Source Book §10.D, rev. 7/2025". |
| `citation_url` | string | yes | A URL that resolves and contains the cited text. Day-14 check verifies this. |
| `last_verified_date` | ISO date | yes | When the citation was last confirmed accurate. |
| `harm_severity` | enum | yes | `low` / `medium` / `high` — how bad is a wrong answer here. `high` = illegal action induced, benefits denied to eligible person, or similar. |
| `language` | string | yes | ISO 639-1, defaults to `en`. |
| `expected_long_form_answer` | string | optional | Reference answer for LLM-judge grading. |
| `notes` | string | optional | Free-text. SME comments, ambiguity flags, contested status. |

If you ever feel the urge to add a column, surface it. Schema changes go through an ADR.

## 3. Voice

This is the most important section in the file. The artifact is judged on voice as much as on technical merit.

### The twenty-item tone checklist (run before publishing any public-facing document)

1. Is the user, caseworker, or institution the grammatical subject of action sentences more often than "Claude" or "our system"?
2. Has every "Claude does X" been replaced with "Claude can be used to X" or "X allows the user to Y"?
3. Have you removed every instance of "the correct architecture," "the right approach," "the right way to"?
4. Has every "unlike [Org]" or "outperforms [Org]" been replaced with "complements," "builds on," or "is one approach among others, including [Org]'s"?
5. Are Propel, Code for America, Nava Labs, and the Markup reporters named and credited substantively in the first 1,000 words?
6. Have you credited journalists and advocates who originally surfaced MyCity's failure modes, by name where possible?
7. Does each substantive empirical claim have an accompanying limitation in an adjacent sentence?
8. Is there an explicit Limitations section enumerating five or more specific constraints?
9. Have you used "may," "might," or "we expect ... we have not tested" for any cross-program or cross-population claim?
10. Have you stated at least one thing that would change your mind about the reference implementation?
11. Is the reference implementation framed as a probe for the eval suite, not as a product proposal?
12. Have you removed every superlative ("most accurate," "best-in-class," "state-of-the-art") about your own work?
13. Where you report numbers, do you include confidence intervals or note run variance?
14. Have you cited Anthropic's High-Risk Use Case Requirements or analogous frameworks when discussing what production would require beyond the prototype?
15. Does the README include a specific channel for feedback — repo issues, a named email — not just "reach out"?
16. Are the eval set, grader prompts, judge meta-prompt, and scoring code open-sourced, and is this stated?
17. Have you used a "we welcome" or "we invite" sentence with a stated purpose ("so that ... can reproduce / extend / critique")?
18. Are headers in sentence case, descriptive-noun phrases (not questions, not marketing taglines)?
19. Have you removed every emoji, every rocket, every "we're excited to announce" lead?
20. Does the closing sentence acknowledge what is unfinished or unresolved, not a CTA or victory lap?

### Specific patterns to mirror

- **Augmentation, never replacement.** "Claude can be used to support caseworker policy lookup," not "Claude handles policy lookup for caseworkers."
- **Disagreement without criticism.** Describe failure modes without naming vendors when avoidable. "The MyCity chatbot failure," not "Nuvalence's failure."
- **Limitations are operationalized.** Not "the eval has limitations" but "the eval pins to 7 CFR Part 273 as of [date]; revalidation is required when regulations change."
- **Generous attribution.** Name people, not just orgs. "Dave Guarino and Propel," "Colin Lecher's reporting at The Markup," "the GOV.UK Government Digital Service team."
- **Invitations include a channel and a reason.** "We welcome issues and PRs from practitioners adapting this to adjacent programs, so the methodology can be stress-tested across contexts."

### Methodology PDF section structure

Mirror Anthropic research notes. In order:
1. Title (short noun phrase, colon, descriptor)
2. Abstract (4–6 sentences: question → method → validation → demonstrations → limitations → governance framing)
3. Introduction (one-sentence stakes; gap paragraph; numbered contributions; roadmap)
4. Related work (compact, citation-dense, by sub-theme)
5. Method (numbered subsections; pipeline diagram; metrics defined before results)
6. Evaluations (per-experiment subsections: setup, metric, table, one-paragraph interpretation)
7. Validation / grader reliability (Cohen's κ, per-sample and aggregate)
8. Qualitative examples (`Human:` / `Assistant:` transcripts of representative success/failure cases)
9. Discussion (what the results imply and explicitly do not)
10. Limitations (3–5 paragraphs minimum; specific not abstract)
11. Acknowledgments (named individuals)
12. References

### Words and phrases to avoid

- "Revolutionary," "groundbreaking," "first-of-its-kind"
- "Solving" anything (we're not solving benefits AI)
- "Best practices" (whose?)
- "Robust" (overused; say what you mean)
- "Safe," "trustworthy," "ethical AI" (vague; say what specifically is true)
- "Production-ready" (we are not)
- "Game-changing," "next-generation"
- Any emoji
- "We're excited to" / "we're thrilled to" / "we're proud to"

### Words and phrases to use

- "We contribute," "we report," "we found," "we observed"
- "Statute-grounded," "regression set," "refusal calibration," "citation-grounding"
- "We expect ... we have not tested"
- "This approach is one of several; others include..."
- "Forward work," "out of scope," "future iterations"
- "Limitations include..."
- "We welcome feedback at..."

## 4. Citation discipline

- Every factual claim in any public-facing document has a citation, a URL that resolves, or a confidence interval — or it gets cut.
- Every statute reference uses the canonical form: `7 CFR 273.X(y)(z)` for federal, `18 NYCRR 387.X(y)` for state regulations, "NYS SNAP Source Book §X.Y, rev. M/YYYY" for the OTDA manual.
- URLs include a retrieval date in `citation_url` metadata: `https://www.ecfr.gov/... (retrieved 2026-MM-DD)`.

## 5. Commit hygiene

- Conventional Commits format: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Reference ADRs when a commit implements one: `feat(eval): implement category A regression runner per ADR-006`
- Don't commit secrets. `.env` is gitignored. Use `.env.example` for required variables with placeholder values.
- Don't commit large binaries to the repo. Policy PDFs go in `data/policy_corpus/` with `.gitattributes` configured for Git LFS if they exceed 5MB.

## 6. Reproducibility

- Every eval run produces a results file in `eval/results/YYYY-MM-DD-<short-slug>/` containing: model versions, prompt template hashes, judge prompt hash, per-case results, aggregate statistics, run timestamp, environment notes.
- Random seeds are pinned where the model supports it.
- Embeddings are regenerated when the corpus version changes; the corpus version is recorded in the results file.
