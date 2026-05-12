# ADR-001: Eval harness — Promptfoo

**Status:** Accepted
**Date:** 2026-05-11
**Decision-makers:** [project lead]

## Context

We need an eval harness that lets SMEs author cases without writing code, runs the same cases against multiple model providers, supports both code-based and LLM-as-judge grading, and produces results we can publish. The closest published artifact in this space — Propel's `snap-eval` — uses Promptfoo, and our project is explicitly building on that work.

## Decision

Use Promptfoo as the primary eval harness. Author cases in a public Google Sheet consumed directly by Promptfoo. Pin the judge model in the `promptfooconfig.yaml` and publish the meta-prompt at `eval/graders/llm_judge_meta_prompt.md`.

## Consequences

**Positive:**
- SMEs can author cases without engineering involvement; this preserves Propel's core authoring affordance
- Provider-agnostic: same config runs against Claude, GPT, Gemini, or a local simulated baseline
- Fast to demo; the entire infra is a YAML file and a sheet URL
- Mirrors the published artifact we're building on, which makes the methodology PDF's "we extend Propel's pattern" claim concrete

**Negative:**
- Promptfoo's default behavior is to use OpenAI as judge; we must explicitly pin Claude Opus 4.5 and document this
- Less programmatic control than Inspect AI for agentic / multi-turn evals; we accept this trade-off for v1
- Google Sheets dependency for authoring; CSVs are committed to the repo as the canonical record

## Alternatives considered

- **Inspect AI (UK AISI):** Python-first, more programmatic, used by UK AI Safety Institute. Considered as a stretch goal for re-implementing a subset (MyCity replay + citation grounding) to demonstrate compatibility with the AISI-aligned harness. Deferred to forward work; if v1 has time, we add it.
- **MLflow:** Wrong category of tool. MLflow is for tracking training runs and managing model artifacts. Using it here would be tracking-theatre for a problem we don't have.
- **LangSmith:** Commercial; tightly coupled to LangChain; not the right shape for a public open-source artifact.
- **DeepEval:** Pytest-shaped; would push us toward code-first authoring and lose the SME affordance.
- **Custom harness:** Considered briefly. Rejected as scope creep.

## References

- Propel's `snap-eval`: https://github.com/propelinc/snap-eval
- Propel's three-part eval blog series: https://www.propel.app/insights/
- `docs/research/r2-eval-methodology-and-mycity-postmortem.md` §"The gold standard for public-sector AI evals"
- `docs/research/r3-propel-positioning-synthetic-data-voice.md` §"What we learned from Propel"
