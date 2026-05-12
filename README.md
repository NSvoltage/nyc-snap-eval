# nyc-snap-eval

A statute-grounded evaluation suite for caseworker-facing benefits-navigation AI in New York, scoped to the Supplemental Nutrition Assistance Program (SNAP). This project contributes a reusable set of test cases, a published grader, and a narrow reference implementation that the eval can be run against.

## What this is

The work focuses on a single deployment surface — tools that support trained SNAP caseworkers — and a single program in a single jurisdiction at a stated point in time. It is not a benchmark. It is an illustrative suite of approximately seventy test cases across seven failure surfaces, anchored where possible to specific federal and state policy citations. The reference implementation exists to make the eval concrete and to test that the eval itself is well-formed; it is not a product proposal.

The scaffolding here — a Google Sheet of SME-authored cases consumed directly by Promptfoo, a four-capability taxonomy spanning factual knowledge through communication style, and the discipline of releasing a small illustrative set rather than waiting on comprehensive coverage — is taken directly from Dave Guarino and Propel's [`snap-eval`](https://github.com/propelinc/snap-eval), which remains the clearest public worked example of a domain-specific benefits eval. Where this project evolves the design, the evolutions are in places Propel themselves implicitly flagged as open: pinning and publishing the judge model and meta-prompt, anchoring each case to a statutory citation, and reporting per-case rather than only aggregate results. Where it differs in kind — caseworker-facing rather than applicant-facing, a published baseline simulation tied to a documented incident — the differences are responses to a different deployment surface, not corrections to Propel's choices.

## Why caseworker-facing first

Two distinct deployment surfaces in benefits administration warrant different evaluation discipline: tools that support trained caseworkers, and tools that speak directly to applicants. This project ships caseworker-facing evaluations first, where the caseworker remains the principal basis for every determination of record, citations can be domain-specific, and integration sits inside existing case-management workflows. We sketch a forward-looking framework for applicant-facing evaluation as future work — a harder surface that requires trauma-informed design, native-language generation, plain-language guarantees, and structured handoff to human help. We do not ship applicant-facing evaluations in this release.

## What's in the repo

```
eval/
  promptfooconfig.yaml      — Promptfoo entry point, pins judge model and meta-prompt
  cases/                    — CSV exports of the authoring Google Sheet, one per category
  graders/                  — LLM-judge meta-prompts, citation validators, consistency checks
  validation/               — SME-labeled gold examples and inter-rater agreement notebooks
  results/                  — per-run results with confidence intervals

demo/                       — narrow reference implementation (Next.js + Claude Sonnet 4.5)
data/policy_corpus/         — pinned federal and state SNAP policy documents
docs/
  project-plan.md           — the v2 build plan
  conventions.md            — code style, file layout, naming, voice
  research/                 — upstream research reports
  decisions/                — architecture decision records
```

## Running the eval

[To be filled in once the eval runner is wired up. Will include: prerequisites, how to set API keys, how to run the full suite, how to run a single category, how to read the results.]

## Limitations

The suite is calibrated to SNAP policy structure (federal–state–county layering, expedited service rules, categorical eligibility) and to the caseworker-facing task. Several constraints are documented and intentional:

- **Single program, single jurisdiction.** SNAP in New York. We expect the structural elements — paired-prompt evaluation across policy interpretations, refusal calibration on under-specified facts, citation-grounding checks — to transfer to other means-tested programs, but we have not tested this transfer.
- **Single point in time.** Cases are pinned to specific revisions of 7 CFR Part 273 and the July 2025 NYS OTDA SNAP Source Book. Re-validation is required when regulations change.
- **NYC HRA Policy Directives and Policy Bulletins are out of scope.** These are not publicly published as a canonical corpus. Cases whose correct answer turns on city-specific HRA guidance are deferred to future work.
- **Small SME pool.** Cases requiring expert review are validated by one or two reviewers with state-SNAP-administration or benefits-navigation experience. Inter-rater disagreement is reported per case.
- **Simulated baseline.** Where we report a comparison against a "poorly-scaffolded baseline," we are simulating a configuration consistent with publicly documented failure patterns, not reproducing any specific deployed system.
- **Caseworker-facing only.** Applicant-facing rubrics are described as forward work but not authored.

## Citation

If you use this work, please cite via the `CITATION.cff` in the repo root.

## Acknowledgments

This project builds on substantial prior work. We name several contributions directly because they materially shaped the design:

- **Dave Guarino and Propel** for [`snap-eval`](https://github.com/propelinc/snap-eval) and the three-part [blog series](https://www.propel.app/insights/) that frames the methodology. The authoring affordances, the four-capability taxonomy, and the discipline of releasing a small illustrative set are all directly inherited.
- **Anthropic's research team** for the published [`political-neutrality-eval`](https://github.com/anthropics/political-neutrality-eval), which is the closest stylistic and methodological template for an open eval release, and for the body of public research on eval design that informs the validation methodology here.
- **The Markup**, particularly Colin Lecher and Julia Angwin, whose [March 2024 reporting](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law) on the MyCity chatbot documented the failure modes that anchor the regression set in this suite.
- **The UK Government Digital Service** for the published [GOV.UK Chat evaluation methodology](https://insidegovuk.blog.gov.uk/) and algorithmic transparency record, which model what disciplined public-sector eval reporting looks like.
- **Nava Labs** for the Imagine LA pilot methodology and **Code for America** for the SNAP Policy Navigator partnership announced in May 2026, both of which inform the caseworker-facing positioning.
- **Stanford RegLab** for hallucination work on legal-domain LLM systems that informs the citation-grounding category.

## Contributing

This repo is published as an artifact, not a maintained service. Issues and pull requests are welcome — particularly from practitioners working on adjacent benefits programs who want to adapt the suite to their contexts. Please open an issue before submitting a substantive PR so we can discuss scope. We are especially interested in:

- Translation of cases into the top NYC LEP languages beyond English and Spanish
- Adaptation to other means-tested programs (Medicaid, TANF, WIC, LIHEAP)
- Cases that surface failure modes the current suite does not cover

## License

Code: MIT. Data (eval cases, policy corpus excerpts, results): CC-BY-4.0. See `LICENSE`.
