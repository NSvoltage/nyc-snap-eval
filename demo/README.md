# `demo/`

The narrow reference implementation. Next.js 15 + Vercel AI SDK + Claude Sonnet 4.5.

This exists to make the eval suite concrete and to test that the eval itself is well-formed. It is **not a product proposal.** Per `docs/conventions.md` §"Voice," the methodology PDF and README frame this implementation as a probe for the eval, not as a recommendation for production deployment.

## Architecture

Per ADR-002 and ADR-005:

- **Model:** Claude Sonnet 4.5 via Anthropic API, with extended thinking enabled for complex eligibility narration
- **RAG:** pgvector on Supabase, indexed over the policy corpus in `data/policy_corpus/`. Embeddings: voyage-3. Hybrid retrieval (BM25 + vector)
- **Tools the model has access to:**
  - `retrieve_policy(query, jurisdictions)` — returns top-K chunks with provenance
  - `check_eligibility(household_json)` — calls the NYC Benefits Screening API (deterministic; per ADR-002 the model never computes eligibility)
  - `escalate(reason, language)` — returns the appropriate referral for the specific reason
- **System prompt:** mandates inline citations on every factual claim; refuses legal advice; surfaces ambiguity rather than smoothing
- **Two API endpoints:**
  - `/api/eval` — the reference implementation (full scaffolding)
  - `/api/eval/baseline` — the simulated baseline per ADR-004 (weak prompt, no tools, naive retrieval)

## Running locally

[To be filled in once the demo is built.]

## Deployment

Vercel, free tier. The deployed URL is recorded in the project's `CITATION.cff` and the README.

## What the demo does not do

This is a probe, not a product. It does not:

- Integrate with HRA case-management systems
- Provide authentication or session management for real users
- Handle PII (the eval uses composite synthetic personas per `docs/research/r3-...md`)
- Make any determination of record — the caseworker remains the principal basis
- Cover programs other than SNAP
- Cover jurisdictions other than New York

Per `CLAUDE.md` and `docs/conventions.md`, these constraints are documented as limitations in the methodology PDF.
