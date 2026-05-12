# ADR-003: v1 targets caseworker-facing deployment

**Status:** Accepted
**Date:** 2026-05-11
**Decision-makers:** [project lead]

## Context

Benefits AI sits on two distinct deployment surfaces: tools that support trained caseworkers, and tools that speak directly to applicants. The risk profiles, the institutional pathways, the eval rubrics, and the failure modes are different enough that conflating them produces a worse artifact than picking one.

The field has converged on caseworker-facing as the entry point for institutionally credible benefits AI: Nava Labs' Imagine LA pilot (caseworker-facing, RCT-evaluated), Pennsylvania's ChatGPT Enterprise pilot (state employees), and the May 2026 Code for America–Anthropic SNAP Policy Navigator partnership (caseworker-facing, MCP-grounded). All three frame the human as the principal basis for any determination of record.

The MyCity failure was specifically an applicant-facing failure mode: lay users acting on confident, illegal-action-inducing model output with no human intermediation. The harder problems that applicant-facing benefits AI must solve — trauma-informed design, native-language generation at L1, plain-language guarantees, structured handoff to human help, escalation patterns on distress signals, disclaimer integrity — are real and they warrant their own evaluation discipline.

## Decision

v1 evaluates caseworker-facing deployment. The reference implementation is built for a trained user; the eval rubrics permit domain terminology, dense citations, and surfaced "depends on..." qualifications rather than smoothed answers. The seven categories and ~70 cases are scoped to this surface.

v2 is described as forward work in the methodology PDF and README. The framework for applicant-facing eval is sketched but not authored. We do not ship applicant-facing rubrics in this release.

## Consequences

**Positive:**
- Aligns with where the field has converged; the artifact is in conversation with Nava, PA, and the CfA–Anthropic partnership rather than competing with them
- Eval rubrics are tractable in two weeks; applicant-facing rubrics require trauma-informed design and accessibility expertise we don't have
- The principal-basis question is cleaner: the caseworker is the determination of record
- The methodology PDF can credit the harder problem honestly: "applicant-facing benefits AI deserves an eval suite built for it; we hope this one is a useful precursor"

**Negative:**
- The MyCity failure was applicant-facing, and we're explicitly not building the eval for the surface where that failure happened. We address this by framing the regression set (Category A) as a known-failure pattern that any benefits-AI deployment — caseworker or applicant — should be tested against, while acknowledging that applicant-facing deployment has additional requirements we're not covering.
- We are leaving the more important problem on the table for v2. The README and methodology PDF must be explicit that this is a sequencing choice, not a claim that caseworker-facing is sufficient.

## Alternatives considered

- **Applicant-facing v1.** Considered. Rejected because the harder problems (trauma-informed design, multilingual at L1, plain-language guarantees) require expertise and SME pools we don't have access to in a two-week build. Shipping applicant-facing without solving these would replicate MyCity's failure mode.
- **Both in v1, with different rubrics.** Considered. Rejected as scope creep. Each surface deserves its own eval discipline; producing a half-baked version of both is worse than a complete version of one.
- **Generic eval that doesn't commit to a surface.** Rejected. "Generic" benefits AI is the problem MyCity had — no defined user, no defined risk profile.

## References

- Code for America–Anthropic SNAP Policy Navigator announcement, May 8, 2026
- Nava Labs Imagine LA pilot
- Pennsylvania ChatGPT Enterprise pilot evaluation, March 2025
- OMB M-25-21 (April 2025) on the principal-basis test
- `docs/research/r3-propel-positioning-synthetic-data-voice.md` §"Caseworker-facing in v1, applicant-facing as v2 framework"
