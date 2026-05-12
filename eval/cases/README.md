# `eval/cases/`

Eval cases, exported from the authoring Google Sheet, one CSV per category.

## Schema

Every CSV uses the schema defined in `docs/conventions.md` §2. All twelve required columns. No deviations without an ADR.

## Files

- `A_mycity_replay.csv` — Category A, ~15 cases anchored to documented MyCity failures
- `B_factual_recall.csv` — Category B, ~15 cases anchored to 7 CFR Part 273 and the NYS OTDA SNAP Source Book
- `C_refusal_escalation.csv` — Category C, ~8 cases testing refusal calibration
- `D_eligibility_edge_cases.csv` — Category D, ~12 cases on structural complexity
- `E_adversarial.csv` — Category E, ~8 cases using public attack patterns only
- `F_multilingual.csv` — Category F, ~10 cases translated by certified translators
- `G_grounding_citation.csv` — Category G, ~10 cases on factual precision/recall/relevancy/groundedness

## Authoring workflow

1. Add or edit a row in the public Google Sheet (URL recorded in `docs/conventions.md` once provisioned)
2. Export the relevant tab as CSV and commit it here
3. The CSV is the canonical record; the sheet is the authoring surface

## Adding a new case

Required: all twelve schema columns populated, including a `citation_url` that resolves and contains the cited text. The Day-14 verification script (`scripts/verify_citations.py`) re-checks every URL.

If you can't cite it, you don't test it. Per the hard rule in `CLAUDE.md` and `docs/conventions.md`.
