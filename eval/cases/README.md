# `eval/cases/`

Eval cases, exported from the authoring Google Sheet, one CSV per category. Promptfoo reads from this directory directly — see `eval/promptfooconfig.yaml`.

## Authoring surface

The Google Sheet at https://docs.google.com/spreadsheets/d/1CV7O8qHMTYQVFHCVFkWIE_zeDsFIyUDovCDLCHPmAcc/edit is the editing surface. Anyone with the link can edit. **The committed CSVs in this directory are the canonical record** — if the sheet and the CSV diverge, the CSV wins, and the next export resets the discrepancy.

One tab per category. Tab names match the CSV filenames below.

## Schema

Every CSV uses the schema defined in `docs/conventions.md` §2. All twelve required columns plus the optional `notes`. No deviations without an ADR. The header row is validated on every export.

## Files

- `A_mycity_replay.csv` — Category A, ~15 cases anchored to documented MyCity failures (post-mortem regression set per ADR-008 §4)
- `B_factual_recall.csv` — Category B, ~15 cases anchored to 7 CFR Part 273, the September 2025 NYS OTDA SNAP Source Book, and OTDA GIS 25DC055 (OBBBA summary)
- `C_refusal_escalation.csv` — Category C, ~8 cases testing refusal calibration
- `D_eligibility_edge_cases.csv` — Category D, ~12 cases on structural complexity (post-OBBBA ABAWD, noncitizen sunset, etc.)
- `E_adversarial.csv` — Category E, ~8 cases using public attack patterns only
- `F_multilingual.csv` — Category F, ~10 cases translated by certified translators
- `G_grounding_citation.csv` — Category G, ~10 cases on factual precision/recall/relevancy/groundedness

## Authoring workflow

1. Edit the relevant tab in the authoring sheet (link above).
2. Run `uv run python scripts/export_sheet_to_csv.py` to refresh the CSVs and validate the header row.
3. Commit the changed CSVs. Use a Conventional Commits message like `feat(cases): add 5 Category-A cases per r2 §"MyCity prompts"` so the commit ties cases back to the research file or ADR that grounded them.

## Adding a new case

Required: all twelve schema columns populated, including a `citation_url` that resolves and contains the cited text. The Day-14 verification script (`scripts/verify_citations.py`, planned) re-checks every URL.

If you can't cite it, you don't test it. Per the hard rule in `CLAUDE.md` and `docs/conventions.md`.

## First-time sheet setup (one-off)

If the sheet ever needs to be rebuilt from scratch (new sheet ID, accidental column deletion, etc.):

1. Rename `Sheet1` to `A_mycity_replay`; add six more tabs with the remaining category names from the table in `docs/conventions.md` §2.
2. In each tab, paste this exact line into cell A1:

   ```
   id,category,subcategory,question,expected_behavior,hard_fail_conditions,citation,citation_url,last_verified_date,harm_severity,language,expected_long_form_answer,notes
   ```

3. Freeze row 1 (`View → Freeze → 1 row`) so the headers stay visible while scrolling.
4. Run `uv run python scripts/export_sheet_to_csv.py --dry-run` to confirm every tab validates clean.
