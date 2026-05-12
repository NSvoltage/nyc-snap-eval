# Research Report 3 — Propel positioning, synthetic data, and voice

> **To paste in:** the artifact titled *"Benefits AI Evaluation Suite: Caseworker-Facing v1 Build Plan Extending Propel's snap-eval"* from the planning conversation. Five sections: what we learned from Propel, caseworker/applicant positioning, synthetic data methodology, Anthropic voice deep-dive, and the integrated v2 plan.

## What this report contributes to the project

This is the design-tightening report — the one that refined v1 from "an Anthropic-style eval" into "a caseworker-facing eval that extends Propel and is sequenced after the May 2026 CfA–Anthropic partnership." Four sections do specific work:

- **§1 What we learned from Propel** — drives the authoring affordances (Google Sheet, three-column schema extended), the discipline of releasing ~70 cases as illustrative rather than comprehensive, and the README's attribution language.
- **§2 Caseworker/applicant positioning** — drives ADR-003. The v1/v2 split, the principal-basis framing under OMB M-25-21, the shared eval scaffolding with different rubrics.
- **§3 Synthetic data methodology** — drives the test case expansion pipeline (six axes × three subtopics × four cases per cell, three-tier verification), the simulated baseline framing (per ADR-004), and the synthetic persona discipline (composite archetypes from cited demographic research, never PII-realistic).
- **§4 Anthropic voice deep-dive** — drives the twenty-item tone checklist in `docs/conventions.md` and the before/after rewrites that informed every public-facing paragraph in the README.

## How ADRs cite this report

- ADR-003 (deployment surface) cites §2 directly
- ADR-004 (simulated baseline) cites §3 §"Baseline simulation: how to do it responsibly"
- ADR-007 (judge model) cites §3 for the Nemotron-style pairwise grading discipline
- The voice rules in `docs/conventions.md` are distilled from §4
