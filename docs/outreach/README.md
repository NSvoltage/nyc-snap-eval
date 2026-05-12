# `docs/outreach/`

Drafts for outreach the project lead needs to send before the build can continue. These are versioned in the repo so the team can iterate via PR before anything is actually sent.

## What's here

- [`sme-outreach.md`](sme-outreach.md) — Cold-email template for recruiting one or two subject-matter experts to validate a sampled subset of cases (per [ADR-007](../decisions/ADR-007-judge-model-and-meta-prompt.md), target n ≥ 30 for Cohen's κ). Includes target-organization list, per-recipient adaptation notes, and follow-up cadence.
- [`screening-api-account-request.md`](screening-api-account-request.md) — Account request for the NYC Benefits Screening API. Includes prose for the request form, a fallback email to `products@nycopportunity.nyc.gov`, and a first-use checklist for after the credential is issued.

## When to send

| Outreach | Send by | Why this date |
|---|---|---|
| Screening API account request | Day 2 | Lead time is unknown; the credential is needed by Day 8 (reference implementation build). |
| SME outreach (first batch of 3 targets) | Day 3 | Per project plan, SME engagement is Days 4–7. Cold-email response cadence is typically 2–5 business days; sending on Day 3 keeps you in the window. |
| SME outreach (second batch) | Day 5 if no responses by then | Move to the next 3 targets on the list. |

## Convention

Contact records, names, and any non-public correspondence stay **out** of the repo. If you need to track who you reached out to and when, keep that in a private note or spreadsheet — not in `docs/outreach/`.

The templates here are public on purpose: they are an artifact of the project's methodology. The actual emails sent and replies received are not.
