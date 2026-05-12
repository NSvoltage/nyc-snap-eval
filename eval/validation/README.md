# `eval/validation/`

SME-labeled gold examples and inter-rater agreement analysis. Per ADR-007, this is where the judge model is validated against expert human labels, and Cohen's κ is reported.

## What lives here

- **`sme_labels.csv`** — A sampled subset of cases (target n ≥ 30, drawn proportionally from all seven categories) labeled by an SME reviewer. Schema: `case_id`, `sme_verdict`, `sme_reasoning`, `sme_id`, `label_date`.
- **`judge_labels.csv`** — The judge model's verdicts on the same subset.
- **`kappa.ipynb`** — Notebook that computes per-category and overall Cohen's κ, with confidence intervals.
- **`disagreement_log.md`** — Cases where SMEs disagree with the judge or with each other. The methodology PDF cites this honestly: "X cases are flagged as contested by inter-rater disagreement and excluded from aggregate metrics."

## The validation workflow

Per ADR-007:

1. SME reviewer is recruited (target: Legal Aid Society, LSNY, or a benefits navigator at Single Stop, Hispanic Federation, or similar CBO)
2. Sampled subset of cases is drawn — proportional stratified sampling across the seven categories
3. SME labels each case independently of the judge
4. Judge runs against the same subset
5. Cohen's κ computed per-category and overall
6. Target: κ ≥ 0.7 per category. If below, the judge meta-prompt is iterated until it clears, or the category is flagged as low-agreement
7. Disagreements are documented in `disagreement_log.md` and discussed in the methodology PDF

## What good looks like

The κ discipline is the part of this project that materially extends Propel's and GOV.UK Chat's published methodology. Neither publishes inter-rater agreement against expert humans. This is where we are most rigorous.

It is also where the project is most vulnerable to the SME pool being small. If we can recruit only one reviewer, the κ analysis becomes thinner. The methodology PDF says so explicitly per the third unresolved tension in `docs/project-plan.md`.

## Files committed at the end of v1

- `sme_labels.csv` — committed with SME identifiers anonymized to `SME-01`, `SME-02`, etc.
- `judge_labels.csv` — committed
- `kappa.ipynb` — committed, rendered to HTML in the results folder
- `disagreement_log.md` — committed
