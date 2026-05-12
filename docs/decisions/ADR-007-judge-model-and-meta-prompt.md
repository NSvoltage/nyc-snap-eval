# ADR-007: Judge model and meta-prompt discipline

**Status:** Accepted
**Date:** 2026-05-11
**Decision-makers:** [project lead]

## Context

LLM-as-judge is the primary grading mechanism for most categories in this suite. The published peer work in this space has a recurring gap: Propel does not publish its judge model or meta-prompt; GOV.UK Chat does not publish the prompts behind its four metrics; Hippocratic AI's evals are similarly opaque. This is a place we can meaningfully extend the published methodology by being transparent about exactly what we're doing.

The choice of judge also matters. Letting a model grade its own outputs is a well-documented failure mode (positional bias, self-preference). Using a different model class — or at minimum a different model from the same family — partially addresses this.

## Decision

### Judge model

Claude Opus 4.5 is the judge for all categories that use LLM-as-judge grading. The judge is pinned by exact model identifier in `promptfooconfig.yaml`. Model upgrades require a new ADR and a re-run of the validation set.

This mirrors the pattern in Anthropic's `political-neutrality-eval`, which uses Opus to grade Sonnet outputs.

When the system under test is Claude Opus 4.5 itself (likely for at least one comparison run), we additionally report results graded by GPT-4o as a cross-model sanity check on that subset.

### Meta-prompt

The full judge meta-prompt lives at `eval/graders/llm_judge_meta_prompt.md`. It is versioned, and changes are tracked in the commit history. Any change to the meta-prompt requires:
- A diff in a PR
- A re-run of the SME-labeled validation set
- A note in the methodology PDF if the change is non-trivial

The meta-prompt is published in the README's "How grading works" section in full, not just linked.

### Positional bias mitigation

Following Nemotron-4 340B's pattern: for any pairwise grading, we run the judge in both orderings (A-then-B and B-then-A) and report disagreement. If the judge's verdict flips based on ordering, the case is flagged as positionally ambiguous and excluded from aggregate metrics.

### SME validation

A subset of cases (target n ≥ 30, drawn proportionally from the seven categories) is labeled by an SME reviewer. We compute Cohen's κ between the SME labels and the judge labels. Target κ ≥ 0.7. If κ falls below 0.7 on a category, the judge meta-prompt is iterated until it clears the threshold or the category is flagged as low-agreement in the results.

This mirrors the validation pattern in Perez et al. 2022 "Discovering Language Model Behaviors with Model-Written Evaluations" (crowdworker agreement on a sampled subset).

### Reporting

For every published eval run:
- Judge model identifier and version
- Meta-prompt hash
- Per-category κ between judge and SME labels
- Count of positionally-ambiguous cases excluded from aggregates
- Per-case results in addition to aggregate metrics

## Consequences

**Positive:**
- Extends the published methodology in a place peer artifacts (Propel, GOV.UK Chat) leave opaque
- Makes the eval reproducible by anyone with API credits
- Surfaces judge limitations honestly via reported κ rather than burying them
- Aligns with Anthropic's published research patterns

**Negative:**
- Opus calls are more expensive than Sonnet; for ~70 cases × multiple systems under test × 10 runs for Category A consistency × both orderings, the compute cost is non-trivial but manageable (estimated low hundreds of dollars for a full run)
- The κ discipline means a low-agreement category can't ship cleanly; we accept this as a feature

## Alternatives considered

- **Claude Sonnet 4.5 as judge.** Considered. Rejected because Sonnet is the primary system under test; self-grading is a known failure mode.
- **GPT-4o as primary judge.** Considered. Rejected because the artifact is positioned around Anthropic's published methodology and Claude family models; using GPT-4o as the canonical judge would create an inconsistent story. GPT-4o is retained as the cross-model sanity check when Opus itself is under test.
- **No SME validation; trust the judge.** Rejected. The point of this project is to extend the published methodology by validating what others assume.
- **Multiple judges with majority vote.** Considered. Deferred to v2 — adds compute and complexity without clearly improving on a single pinned judge with reported κ for v1's scope.

## References

- Anthropic, `political-neutrality-eval`: https://github.com/anthropics/political-neutrality-eval
- Perez et al. 2022, "Discovering Language Model Behaviors with Model-Written Evaluations" (arXiv:2212.09251)
- NVIDIA, Nemotron-4 340B Technical Report (arXiv:2406.11704), §"both response orderings"
- `docs/research/r3-propel-positioning-synthetic-data-voice.md` §"Synthetic data methodology"
