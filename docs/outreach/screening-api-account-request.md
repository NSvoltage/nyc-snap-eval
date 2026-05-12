# NYC Benefits Screening API account request

A request for credentials to call `POST /eligibilityPrograms` on the NYC Benefits Screening API. The API is administered by NYC Opportunity (the Mayor's Office for Economic Opportunity) and underlies the ACCESS NYC Eligibility Screener.

Per [ADR-008 §2](../decisions/ADR-008-post-obbba-post-mycity-amendments.md), an authenticated account is a prerequisite for the reference implementation (project plan Days 8–10). Submit the account request **on Day 2** so the credential is in hand by Day 8 — lead time for provisioning is unknown but the request is otherwise non-blocking.

## Submission channels

There are two channels; submit the form first, follow up by email only if there's no response within a week.

### Primary: the account-request form

URL: `http://eepurl.com/gfLTuH`

Discovered via "02 Request an Account" on https://screeningapidocs.cityofnewyork.us/getting-started. It is a short Mailchimp-hosted form that collects basic contact info and one free-text field. The fields are:

- **First name** (required)
- **Last name** (required)
- **Email** (required) — use the address you check daily; this is what credentials and follow-ups go to
- **Organization** (required)
- **Organization website** (optional but include — it's a free credibility signal)
- **How will you use the API?** (optional, ~free-text) — use the prose below
- **Agreement confirmation** (required) — type `YES` to confirm you've reviewed the Terms of Service, NYC.gov Terms of Use, and NYC.gov Privacy Policy. Read them first if you haven't.
- **Newsletter opt-in** (optional checkbox) — your call

### Secondary: direct email to NYC Opportunity

`products@nycopportunity.nyc.gov`

Send this only if the form has produced no response in approximately one week. Use the longer email below.

## Form prose — "How will you use the API?"

Paste this verbatim. It is tuned to the form field length and to NYC Opportunity's likely review criteria (small request volume, research framing, open-source posture, respect for rate limits).

> I'm building an illustrative evaluation suite for caseworker-facing SNAP benefits-navigation AI in New York. The reference implementation calls `/eligibilityPrograms` as a deterministic eligibility tool, with the LLM narrating the API's response rather than computing eligibility itself. Expected volume is low — a few hundred requests across a one-time evaluation run plus development testing, with rate-limit respect built into the client. The project is open-source at https://github.com/NSvoltage/nyc-snap-eval (MIT code, CC-BY-4.0 data), draws on the public ACCESS-NYC-Rules engine, and credits NYC Opportunity as the data source in all materials. Not a production deployment, not a commercial product. I'd be glad to share more detail on request.

If the field has a character limit, the shorter version is:

> Open-source research artifact — an evaluation suite for caseworker-facing SNAP AI in New York. The reference implementation uses `/eligibilityPrograms` as a deterministic tool so the LLM narrates eligibility rather than computing it. Expected volume: a few hundred requests across one evaluation run plus development testing. Repo: https://github.com/NSvoltage/nyc-snap-eval. Credits NYC Opportunity throughout. Not a product.

## Follow-up email (only if form gets no response in ~5 business days)

**To:** `products@nycopportunity.nyc.gov`
**Subject:** `NYC Benefits Screening API account request — open-source SNAP eval suite`

> Hello,
>
> I submitted an account request for the NYC Benefits Screening API on [date] via the form linked from `screeningapidocs.cityofnewyork.us/getting-started` (eepurl.com/gfLTuH). I'm following up here in case the form submission didn't reach the right inbox.
>
> What I'm building: an illustrative evaluation suite for caseworker-facing SNAP benefits-navigation AI in New York. The project anchors test cases to specific 7 CFR and NYS OTDA SNAP Source Book citations, publishes the LLM-judge meta-prompt for transparency, and includes a narrow reference implementation that calls `/eligibilityPrograms` as a deterministic eligibility tool. Per ADR-002 in the repo, the LLM narrates the API's response rather than computing eligibility itself — a discipline informed in part by the open-source ACCESS-NYC-Rules engine you maintain at github.com/NYCOpportunity/ACCESS-NYC-Rules.
>
> What I'd be using the API for:
>
> - Development testing during the Days-8–10 reference-implementation build (under 100 requests).
> - One full evaluation run against ~70 test cases that include eligibility-edge-case scenarios (~200–300 requests, single batch, rate-limited).
> - Optionally, comparison runs against the simulated baseline configuration (similar volume, same time window).
>
> The repo is public at https://github.com/NSvoltage/nyc-snap-eval. The methodology PDF and README credit NYC Opportunity by name in the first 1,000 words, alongside Propel, The Markup, GOV.UK Government Digital Service, Nava Labs, Code for America, and Stanford RegLab. License is MIT for code and CC-BY-4.0 for data and eval results.
>
> Constraints I've already designed around:
>
> - Composite synthetic households only — no PII-realistic inputs (per a hard rule in the project's CLAUDE.md).
> - Polite rate-limit handling, with exponential backoff, in the client.
> - Saved request and response samples in the repo at `data/policy_corpus/nyc/benefits-screening-api/sample-requests/`.
> - All credentials kept out of version control; `.env.example` documents the variables.
>
> If sandbox access (`sandbox.screeningapi.cityofnewyork.us`) is sufficient for the eval-run volume described above, I'd be glad to use only the sandbox. Production access is only required if the sandbox imposes lower throughput limits than the development testing needs.
>
> I'd welcome any guidance on the right scope of access for the use case described and on any constraints in the Terms of Service I should reread before integrating. If a brief call is easier than email, I'm flexible.
>
> Thank you for considering the request.
>
> Best,
> Naman Sharma
> https://github.com/NSvoltage/nyc-snap-eval
> [phone / scheduling link]

## After approval — first-use checklist

Once credentials are issued, complete these steps in order. They are sequenced to surface authentication issues before any real eval run.

1. Store the initial username and temporary password in a password manager. Do **not** put them in `.env` or anywhere in the repo.
2. Call `POST /authToken` with `username`, `password`, and `newPassword` to set the real password. (The OpenAPI spec at `data/policy_corpus/nyc/benefits-screening-api/openapi.yaml` defines the exact body shape.)
3. Save the returned Bearer token to a session-local secret store. The token expiration is undocumented in the spec; treat it as short-lived and re-issue per session.
4. Send the composite synthetic household at `data/policy_corpus/nyc/benefits-screening-api/sample-requests/composite-household-01.json` to `POST /eligibilityPrograms` with `Authorization: Bearer <token>` and confirm a 200 response with a non-empty program list that includes SNAP.
5. Save the first successful authenticated response to `data/policy_corpus/nyc/benefits-screening-api/sample-requests/responses/sandbox-200-snap-eligible.json` (or similar) and update the `meta.yaml` `auth_finding` block to note that authenticated access is operational.

## Constraints to know

- **The API is administered by NYC Opportunity, not HRA.** Routing questions to HRA will not reach the right team.
- **Terms of Service apply to every request.** Review at https://screeningapidocs.cityofnewyork.us/terms-of-service before integrating.
- **Bulk submission has a separate flow** (`/bulkSubmission/import` per the spec). The eval suite uses the single-request endpoint only; mention bulk only if scope changes.
- **The Mamdani administration retained NYC Opportunity** as far as I have been able to verify (May 2026); the office name and contact are unchanged. Re-verify if the request stalls.
