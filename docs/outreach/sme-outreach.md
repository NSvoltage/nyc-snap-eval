# SME reviewer outreach

A reusable template for recruiting one or two subject-matter experts to validate a sampled subset of cases (per ADR-007, target n ≥ 30 across the seven categories) so we can report Cohen's κ between expert labels and the LLM judge.

Send one cold email per target. Personalize the **"Why you specifically"** paragraph before sending — generic outreach to advocacy-org staff lands badly.

## Open variables (fill in before sending)

| Variable | Recommendation |
|---|---|
| **Honorarium** | $300–900 range for ~3 hours of structured review (rate consistent with public-benefits attorney consult time). If no budget exists, say so honestly and lower the ask. Unpaid review is awkward to request from advocacy-org staff; reasonable for academics, retired SMEs, or organizations where this kind of review fits the org's mission. |
| **Timeline** | Per `docs/project-plan.md` Days 4–7 means turnaround within ~7 calendar days of acceptance. State a specific deadline, not "ASAP." |
| **Attribution** | Default to anonymized (`SME-01`, per `eval/validation/README.md`). Offer named credit as an opt-in. Some reviewers prefer named visibility; others can't be named because of their org's media policy. |
| **Repo state at send time** | The repo is public at https://github.com/NSvoltage/nyc-snap-eval. Reference [`docs/research/r5-freshness-audit-2026-05-11.md`](../research/r5-freshness-audit-2026-05-11.md) and [ADR-008](../decisions/ADR-008-post-obbba-post-mycity-amendments.md) so the SME can pre-vet your framing. |

## Target organizations and roles

You know your network; this is a starting list, not a prescription. The strongest candidates have direct SNAP caseworking or benefits-attorney experience and have worked through the post-OBBBA ABAWD rollout in NYC.

| Organization | Group / role to target | Why this fits |
|---|---|---|
| Empire Justice Center | Public Benefits team; SNAP specialists | Authors the practice manual most NYC benefits attorneys cite; deep statutory fluency; staff have testified on OBBBA implementation. |
| Legal Aid Society — Civil Practice | Government Benefits Practice | Direct casework; current NYC HRA interactions; strong on procedural cases (Category D). |
| Legal Services NYC (LSNY) | Public Benefits Unit | Litigation-grade statutory grounding; comfortable evaluating refusal-calibration cases (Category C). |
| Community Service Society of New York (CSS-NY) | Benefits Plus Learning Center editors | Authors of the Benefits Plus reference manual; deeply versed in the federal-state-city policy chain. |
| Single Stop USA — NYC | Benefits navigators on the floor | Frontline navigator perspective; complements statutory experts who don't see weekly intake. |
| Hispanic Federation | Public benefits programs lead | Strong on multilingual consistency cases (Category F) and noncitizen eligibility post-OBBBA. |
| Food Bank for New York City | SNAP outreach team / policy staff | Direct ABAWD-rollout experience; high familiarity with the 2026-03-01 implementation HRA pages now reflect. |
| Academic candidates | NYU Furman Center, Columbia School of Social Work, Stony Brook Center for Survey Research | Useful when no advocacy-org SME can commit; trade currency for methodology rigor. |

## Subject line options

Pick one. Specificity beats cleverness — these are professionals who triage email by scanning sender + subject:

- `Eval-suite review for SNAP caseworker AI — ~3 hours, statute-grounded, paid` (when honorarium confirmed)
- `Brief review opportunity: SNAP eval-suite case validation, post-OBBBA`
- `Statute-grounded SNAP eval-suite: SME review (Day-2 ask)`

## Email body template

> [Name],
>
> I'm reaching out because of your work at [organization] on [specific issue area — e.g. "ABAWD implementation in NYC," "the Benefits Plus manual's SNAP chapters," "the public-benefits practice your office runs"]. Your judgment on a small set of test cases would materially improve the project I'm describing below.
>
> **What this is.** A statute-grounded evaluation suite for caseworker-facing SNAP benefits-navigation AI in New York. Approximately seventy test cases across seven failure surfaces, every case anchored to a 7 CFR or NYS OTDA citation, with a published grader and a narrow reference implementation. The methodology takes directly from Dave Guarino and Propel's [`snap-eval`](https://github.com/propelinc/snap-eval); the failure cases we anchor against include the documented MyCity errors that [The Markup](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law) reported in 2024 and that the Mamdani administration cited when discontinuing the chatbot in February 2026. The repo is public at https://github.com/NSvoltage/nyc-snap-eval; the freshness audit at [`docs/research/r5-freshness-audit-2026-05-11.md`](https://github.com/NSvoltage/nyc-snap-eval/blob/main/docs/research/r5-freshness-audit-2026-05-11.md) captures the post-OBBBA, post-MyCity-shutdown landscape that shapes the case set.
>
> This is an illustrative research artifact, not a production system. It is meant to demonstrate one shape of measurable bar that benefits-AI tools could be held to before deployment.
>
> **What I'd ask of you.** Review approximately 30 cases (sampled across all seven categories), label each as pass / fail / contested against the case's expected behavior, and note any disagreement with the citation or expected answer. Time budget: about 3 hours, on your own schedule, by [specific date]. I'd pair the labels with the LLM judge's verdicts and report inter-rater agreement (Cohen's κ) in the methodology writeup. Disagreements would be retained and surfaced as contested rather than scored.
>
> **Why you specifically.** [Two or three sentences personalized to the recipient — e.g. "Your testimony at the State Legislature's OBBBA-implementation hearing demonstrates exactly the kind of statutory fluency Category D needs," or "Your work on the Benefits Plus manual's expedited-issuance chapter is the closest public source to what Category B's expedited-service cases test against."]
>
> **What you'd get.** [If honorarium: "An honorarium of $[amount] for the time."] Named credit in the methodology PDF and repo acknowledgments, or anonymized as `SME-01` if you prefer — your call. The full case set and your labels are open-source (MIT for code, CC-BY-4.0 for data), so your contribution would be visible to the public-benefits AI community and reusable in subsequent work.
>
> **The lowest-friction first step.** A 20-minute video call to walk through one example case and the labeling rubric, so you can decide whether the ask is well-defined before committing further. I am flexible on timing.
>
> Limitations I want to be upfront about: the SME pool is small, my standard for "consensus" is per-case rather than category-aggregated, and any case where reviewers can't agree gets documented as contested instead of dropped. I am not asking you to validate the entire eval — just a sampled subset.
>
> If this isn't a fit, an introduction to a colleague who'd be better positioned would also help.
>
> Thank you for considering it.
>
> Best,
> Naman Sharma
> [phone / signal / scheduling link]
> https://github.com/NSvoltage/nyc-snap-eval

## Per-recipient adaptation notes

- **Empire Justice or CSS-NY (manual authors):** lean into the citation-grounding category (G) and the federal-state-city chain. They wrote the corpus we're testing against.
- **Legal Aid / LSNY (litigation practices):** lean into refusal-and-escalation (C) and adversarial inputs (E). They've seen what happens when systems give bad advice that gets acted on.
- **Single Stop / Food Bank (frontline navigators):** lean into MyCity replay (A) and eligibility edge cases (D). They've seen real applicant questions; their intuition for what a caseworker actually faces is the strongest.
- **Hispanic Federation:** lean into multilingual consistency (F) and noncitizen-eligibility cases. The April 9, 2026 humanitarian sunset is a live issue for their constituency.
- **Academic candidates:** lean into validation methodology (Cohen's κ, inter-rater agreement). Frame this as methodological collaboration rather than domain consultation.

## Follow-up cadence

- T+5 business days, if no response: one brief follow-up ("Wanted to check this didn't get buried. If now isn't a fit, no need to reply.")
- T+10 business days: move to the next target on the list.
- Track contacts and responses in `docs/outreach/contacts.md` (not committed; keep contact data out of the public repo).
