# Research Report 2 — Eval methodology and MyCity post-mortem

> **To paste in:** the artifact titled *"Building an Anthropic-Quality Benefits-AI Evaluation Suite for NYC SNAP"* from the planning conversation. This is the substantive technical report whose nine sections cover: executive summary, Anthropic publication template, gold standard for public-sector AI evals, MyCity post-mortem, recommended eval taxonomy, reference implementation architecture, project blueprint, open questions and risks, and pitch / interview framing.

## What this report contributes to the project

This is the load-bearing report. Three sections do the most work:

- **§2 The Anthropic publication template** — drives the methodology PDF's structure and voice. The twenty-item tone checklist in `docs/conventions.md` is distilled from this section's reading of Anthropic's published research.
- **§3 The gold standard for public-sector AI evals** — drives the eval design discipline. Propel's `snap-eval`, GOV.UK Chat's four metrics, Stanford RegLab's hallucination methodology, Nava Labs' Imagine LA RCT design, the Beeck Center Policy2Code findings — these are the peer artifacts the project is in conversation with.
- **§4 The MyCity post-mortem** — drives Category A (the regression set). The documented prompts, the statute citations, the timeline, and the technical-architecture inferences are the raw material for the ~15 cases in that category.

## How ADRs cite this report

- ADR-001 (eval harness) cites §3 for the public-sector eval landscape
- ADR-004 (simulated baseline) cites §4 for the MyCity context
- ADR-006 (eval categories) cites §5 for the taxonomy rationale
- ADR-007 (judge model) cites §2 for Anthropic's published patterns
