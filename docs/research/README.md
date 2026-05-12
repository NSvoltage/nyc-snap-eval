# Research reports

The four upstream research syntheses that informed the project plan. These are reference material — Claude Code consults them when making design judgment calls, and they're cited from ADRs and the methodology PDF.

These are not meant to be re-litigated. The decisions made on the basis of this research are captured in `docs/decisions/`. If new information surfaces that contradicts a report, write an ADR — don't edit the report.

## What's here

- **`r1-nyc-poverty-and-benefits-infrastructure.md`** — the demographic and infrastructure context for why this work matters. NYC poverty numbers, the populations underserved by the current system, what an applicant's day-to-day looks like, the landscape of civic-tech organizations. Most useful as background and for the methodology PDF's introduction.
- **`r2-eval-methodology-and-mycity-postmortem.md`** — the substantive technical report. Three sections: (1) how Anthropic structures published research, with concrete patterns to mirror; (2) the gold standard for public-sector AI evals (Propel, GOV.UK Chat, Stanford RegLab, Nava Labs, Beeck Center); (3) the MyCity technical post-mortem with documented prompts and statute citations. This is the report cited most often.
- **`r3-propel-positioning-synthetic-data-voice.md`** — the design-tightening report. Four threads: deep reading of Propel's `snap-eval` as an artifact; the caseworker-versus-applicant positioning with v1/v2 framing; synthetic data methodology from Nemotron and Anthropic's model-written-evals work; and the Anthropic voice study with a twenty-item tone checklist.
- **`r4-corpus-access-verification.md`** — the verification audit of policy corpus access. Confirms which sources are publicly accessible (eCFR API, OTDA Source Book, NYC Benefits Screening API, public HRA pages) and which are not (HRA Policy Directives and Bulletins). ADR-005 is the decision derived from this report. Superseded in parts by r5 (see below).
- **`r5-freshness-audit-2026-05-11.md`** — point-in-time re-audit conducted during the Day-1 corpus pull. Records that the MyCity chatbot was discontinued by the Mamdani administration in February 2026, that the One Big Beautiful Bill Act of 2025-07-04 changed federal SNAP statute (but not yet the 7 CFR regulations), and two factual errors in ADR-005/r4 that the pull surfaced. ADR-008 is the decision derived from this report.

## How to use these

- When making a design decision, find the relevant report section and cite it in the ADR
- When writing the methodology PDF, paraphrase rather than copy-paste; the reports were exploratory and the PDF is final
- When in doubt about whether a deviation from the plan is justified, surface the deviation against the relevant report rather than against the plan itself — the report is the underlying reasoning
