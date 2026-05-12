# Architecture Decision Records

Short, dated records of load-bearing decisions. Read these when you wonder "but why did we pick X."

ADRs are immutable once accepted. If a decision changes, write a new ADR that supersedes the old one and update the old one's status to "Superseded by ADR-NNN."

## Status taxonomy

- **Proposed** — under discussion
- **Accepted** — the active decision
- **Deprecated** — no longer followed but kept for history
- **Superseded by ADR-NNN** — replaced by a newer decision

## Index

- [ADR-001](./ADR-001-eval-harness-promptfoo.md) — Eval harness: Promptfoo
- [ADR-002](./ADR-002-eligibility-math-deterministic.md) — Eligibility math is deterministic, not generative
- [ADR-003](./ADR-003-deployment-surface-caseworker.md) — v1 targets caseworker-facing deployment
- [ADR-004](./ADR-004-simulated-baseline-framing.md) — Simulated baseline framing
- [ADR-005](./ADR-005-policy-corpus-sources.md) — Policy corpus sources and exclusions
- [ADR-006](./ADR-006-eval-categories.md) — The seven eval categories
- [ADR-007](./ADR-007-judge-model-and-meta-prompt.md) — Judge model and meta-prompt discipline
- [ADR-008](./ADR-008-post-obbba-post-mycity-amendments.md) — Post-OBBBA, post-MyCity amendments to ADR-005 and project framing

## Template

When writing a new ADR, use this skeleton:

```markdown
# ADR-NNN: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Date:** YYYY-MM-DD
**Decision-makers:** [names]

## Context
What forced this decision? What are we trying to solve?

## Decision
What did we decide? Be specific.

## Consequences
What follows from this — both positive and negative? What does this lock us out of?

## Alternatives considered
What else did we look at, and why did we not pick it?

## References
Links to research reports, prior art, or external documents.
```
