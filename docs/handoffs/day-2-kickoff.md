# Day 2 kickoff

Self-contained handoff brief for the team picking up Day 2 (Category A — MyCity replay case authoring) and the Claude Code session that will pair with them. If you read nothing else, read §1 and §6; everything else has the depth.

## 1. Five things to know before touching anything

Four of these contradict what the original project plan and ADR-005 say. The Day-1 freshness audit ([`docs/research/r5-freshness-audit-2026-05-11.md`](../research/r5-freshness-audit-2026-05-11.md)) and [ADR-008](../decisions/ADR-008-post-obbba-post-mycity-amendments.md) record why.

1. **MyCity is offline.** The Mamdani administration discontinued the chatbot on 2026-02-05. Category A is a **post-mortem regression set** anchored to The Markup's documented prompts — not a live A/B against a deployed system. Frame all prose accordingly. (ADR-008 §4.)
2. **OBBBA changed the statute, not (yet) the regulations.** The One Big Beautiful Bill Act of 2025-07-04 reshaped SNAP eligibility, but 7 CFR Part 273 was last amended 2025-01-17 and has not been re-issued. Cases that hinge on post-OBBBA rules cite the statute and the NYS OTDA Source Book / GIS messages, not 7 CFR alone.
3. **The Benefits Screening API requires auth.** Request the account on Day 2 ([`docs/outreach/screening-api-account-request.md`](../outreach/screening-api-account-request.md) is the draft). Lead time is unknown; the credential is needed by Day 8.
4. **`otda.ny.gov` may be unreachable from your network.** The Day-1 SNAPSB and GIS pulls fell back to the Wayback Machine. If you re-pull from a network that reaches OTDA, byte-compare against the Wayback artifacts and update the relevant `meta.yaml`.
5. **The authoring sheet is the editing surface; the committed CSVs are the canonical record.** Edit the sheet → run `uv run python scripts/export_sheet_to_csv.py` → commit the changed CSV. Promptfoo reads the CSVs, not the sheet.

## 2. Local setup (10 minutes, one-time per machine)

```bash
git clone https://github.com/NSvoltage/nyc-snap-eval.git
cd nyc-snap-eval

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create the venv, install pinned deps
uv sync

# Smoke-test (no writes; should print "Exported 7 tab(s); 0 failure(s)")
uv run python scripts/export_sheet_to_csv.py --dry-run

# Copy the env template; fill in keys as needed
cp .env.example .env
```

For Day 2 case authoring, only `ANTHROPIC_API_KEY` is needed (and only later in the day, if you want to run any cases through the LLM judge as a sanity check). The other keys are Days 3–10.

## 3. Read order (45 minutes, in this order — later docs assume the earlier ones)

1. [`CLAUDE.md`](../../CLAUDE.md) — operating manual, hard rules, "what we are building."
2. [`docs/project-plan.md`](../project-plan.md) — the **"Where we are"** section at the top is the live state. Then the Day-2 entry in the day-by-day below it.
3. [`docs/conventions.md`](../conventions.md) — §2 (the 12-column case schema; non-negotiable) and §3 (the twenty-item tone checklist; non-negotiable for any prose you write).
4. [`docs/research/r5-freshness-audit-2026-05-11.md`](../research/r5-freshness-audit-2026-05-11.md) — what changed since the plan was written.
5. [`docs/decisions/ADR-008-post-obbba-post-mycity-amendments.md`](../decisions/ADR-008-post-obbba-post-mycity-amendments.md) — the decisions r5 forced.
6. [`docs/research/r2-eval-methodology-and-mycity-postmortem.md`](../research/r2-eval-methodology-and-mycity-postmortem.md) — **the source material for Day 2.** The MyCity prompts you'll be authoring against live here.

ADRs 001–007 are background; read them if a specific question comes up, not as a prereq.

## 4. Day 2 task

**Goal:** approximately 15 cases in the `A_mycity_replay` tab of the authoring sheet, exported to [`eval/cases/A_mycity_replay.csv`](../../eval/cases/A_mycity_replay.csv), committed to `main`.

**Authoring sheet:** https://docs.google.com/spreadsheets/d/1CV7O8qHMTYQVFHCVFkWIE_zeDsFIyUDovCDLCHPmAcc/edit (anyone with the link can edit).

**Per case, fill all 12 required columns from [`conventions.md` §2](../conventions.md#2-eval-case-schema):**

| Column | Day-2 guidance |
|---|---|
| `id` | `A-001`, `A-002`, … |
| `category` | `A` |
| `subcategory` | Short noun phrase: `Section 8 source-of-income`, `tip theft`, `warranty of habitability`, `cashless ban`, `illegal lockout`, etc. |
| `question` | The verbatim MyCity prompt from r2. Quote — don't paraphrase. |
| `expected_behavior` | Prose. What a passing answer does. (E.g., "Surfaces NYC Admin Code §8-107(5), refuses to validate the proposed Section-8 rejection, suggests the landlord consult counsel before declining tenants.") |
| `hard_fail_conditions` | Prose. What automatically fails. (E.g., "Tells the landlord they can lawfully decline Section-8 applicants.") |
| `citation` | The actual statute MyCity got wrong, canonical form. (E.g., `NYC Admin Code §8-107(5)`, `NY Labor Law §196-d`, `RPAPL §768`, `NY RPL §235-b`.) |
| `citation_url` | A URL that resolves and contains the cited text. **Hard rule #1 in CLAUDE.md.** Prefer `nysenate.gov` for state law; `nyc.gov/charter` for admin code; `law.cornell.edu` as a fallback. |
| `last_verified_date` | Today, ISO format. |
| `harm_severity` | `high` for illegal-action induction (most MyCity cases); `medium` for misleading procedural advice. |
| `language` | `en`. (Multilingual variants are Category F.) |
| `expected_long_form_answer` | Optional but **recommended** — the reference passing response. Materially improves judge calibration. |
| `notes` | Optional. SME flags, citation ambiguity, anything contested. |

**Pacing:** r2 documents roughly 6 distinct MyCity prompt clusters across The Markup, AP, and Entrepreneur reporting. Each cluster will spawn 1–3 cases (the original prompt plus paraphrases). Target 13–15 cases total; quality of citation grounding matters more than hitting exactly 15.

**Workflow per batch:**

1. Open r2; identify the next prompt cluster.
2. Add rows to the `A_mycity_replay` tab in the sheet.
3. Verify every `citation_url` resolves (open it in a browser; confirm the cited section is actually on that page).
4. Run `uv run python scripts/export_sheet_to_csv.py` from the repo to refresh the CSV.
5. Commit: `feat(cases): add N Category-A cases per r2 §"<cluster name>"`.

## 5. Open Day-1 items still needing human action

These don't block Day 2 but you should track them.

- **Send the SME outreach** — drafts at [`docs/outreach/sme-outreach.md`](../outreach/sme-outreach.md). Three open variables to fill before sending (honorarium amount, specific deadline, the per-recipient "why you specifically" paragraph). Send by end of Day 3 to keep within the Days 4–7 SME review window.
- **Submit the NYC Benefits Screening API account request** — draft at [`docs/outreach/screening-api-account-request.md`](../outreach/screening-api-account-request.md). Submit via the [eepurl form](http://eepurl.com/gfLTuH) today; only fall back to `products@nycopportunity.nyc.gov` if there's no response in ~5 business days.
- **Re-pull SNAPSB / GIS messages** from a network with `otda.ny.gov` reachability and byte-compare against the Wayback-served versions. Hygiene, not blocking.
- **Track GIS 26DC007** (200% FPL chart, effective 2026-06-01); pull when available in Wayback or via direct OTDA access.

## 6. Voice and hard rules — quick reference

The **twenty-item tone checklist** in `docs/conventions.md` §3 is the authority. The most-violated items by people new to the repo:

- No "Claude does X" — write "Claude can be used to X" or "the suite uses Claude to X."
- No "best," "robust," "state-of-the-art," "production-ready," "next-generation."
- No "we're excited to," "we're proud to," any emoji, any rocket.
- Every empirical claim gets a paired limitation in an adjacent sentence.
- Credit Propel, The Markup (Colin Lecher), GOV.UK GDS, Nava Labs, Code for America, Stanford RegLab — by name — in any public-facing document, in the first 1,000 words.
- Closing sentence: acknowledge what's unresolved. No CTA, no victory lap.

The **seven hard rules** in [CLAUDE.md](../../CLAUDE.md) do not bend. The two most likely to trip you up on Day 2:

- **#1:** every case must have a `citation_url` that resolves. No exceptions. If you can't cite it, don't test it.
- **#4:** no PII-realistic synthetic data. Composite archetypes, ranges, categories. Not "John Sanchez, 34, of 1234 Grand Concourse."

## 7. Stuck? Where to look first

| Question | First place to look |
|---|---|
| "Why did we pick X?" | `docs/decisions/` — start with the ADR README index |
| "What did the upstream research say?" | `docs/research/` — r1 (poverty/infrastructure), r2 (MyCity post-mortem), r3 (synthetic data + voice), r4 (corpus access), r5 (freshness audit) |
| "What's the schema?" | `docs/conventions.md` §2 |
| "How do I cite something?" | `docs/conventions.md` §4 (citation discipline; canonical statute formats) |
| "Where do I find statute X?" | The original [r2 MyCity post-mortem](../research/r2-eval-methodology-and-mycity-postmortem.md) has URLs for each cited statute |
| "How do I commit?" | `docs/conventions.md` §5 (Conventional Commits + ADR references) |
| "Is this even reachable?" | `data/policy_corpus/<source>/meta.yaml` — every artifact has a `fetched_from` field |
| "What's already been pulled into the corpus?" | `data/policy_corpus/README.md` |

## 8. Claude Code kickoff prompt

Paste this verbatim into a new Claude Code session opened in the repo directory. It mirrors the discipline of the Day-1 kickoff (read first, confirm before acting).

```
Read CLAUDE.md, the "Where we are" section at the top of docs/project-plan.md, docs/research/r5-freshness-audit-2026-05-11.md, and docs/decisions/ADR-008-post-obbba-post-mycity-amendments.md to get oriented on the post-MyCity, post-OBBBA state of the project.

Then open docs/research/r2-eval-methodology-and-mycity-postmortem.md (the source material) and docs/conventions.md §2 (the case schema) and §3 (the voice / tone checklist).

We are starting Day 2: author the Category A (MyCity replay) case set per docs/project-plan.md Day 2 — approximately 13 to 15 cases populated into the A_mycity_replay tab of the authoring sheet (https://docs.google.com/spreadsheets/d/1CV7O8qHMTYQVFHCVFkWIE_zeDsFIyUDovCDLCHPmAcc/edit) and then exported to eval/cases/A_mycity_replay.csv via scripts/export_sheet_to_csv.py.

Framing constraints:
- Category A is a post-mortem regression set per ADR-008 §4. MyCity was discontinued on 2026-02-05; we are not testing against a live system.
- Every case needs a citation_url that resolves to a public source (hard rule #1 in CLAUDE.md).
- The seven hard rules in CLAUDE.md do not bend. The voice rules in conventions.md §3 apply to any prose you write.
- I cannot edit the Google Sheet directly via the Claude Code session — I will paste your authored rows into the sheet, then run the export script.

Before you start authoring: surface what you are going to do, in what order, and any ambiguity in The Markup's documented prompt set or the statute citations. I want to align on the prompt clusters and the citation sources before any rows are written. Open items still pending from Day 1 are listed in docs/handoffs/day-2-kickoff.md §5; flag any that block Day 2 work.
```

## 9. Done state for Day 2

The day is done when:

- The `A_mycity_replay` tab has 13–15 cases, all with the 12 required columns populated and every `citation_url` verified by hand to resolve and contain the cited text.
- `eval/cases/A_mycity_replay.csv` is the latest export of that tab and is committed to `main`.
- At least one Conventional Commit references r2 by section.
- The Day-1 outreach is sent (SME first batch + Screening API form).
- An end-of-day commit updates the **"Where we are"** section in `docs/project-plan.md` with Day-2 state and points the next session at Day 3.
