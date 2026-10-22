# BidSentry-E — Technical Review

## Product claim

BidSentry-E pre-screens public tender notices for Indian MSMEs. It surfaces candidate requirements with a source URL, exact quote candidate, independent Fetch verification result, supplier-profile comparison and an explicit uncertainty state. The feature is decision support for human review, not a legal eligibility engine.

## Strengths

- Focuses on a specific high-stakes review moment rather than an all-purpose procurement platform.
- Meaningful TinyFish workflow uses Search, Fetch, user-triggered Agent REST SSE, separate Fetch quote checks and live page rechecks.
- Source verification and fail-closed Agent terminal-state handling are covered by mock-driven tests.
- Synthetic examples are explicitly labelled; live API failures must remain visible.
- The local app is runnable and the key is kept server-side in `.env`.

## Risks and open proof

- TinyFish authentication/permissions, target-portal access and live SSE behavior have not been proven with the team's account in this package.
- Rule-based extraction can miss complex tables, scanned documents, percentage-based rules, exceptions, cross-references and unlinked corrigenda.
- Exact text presence does not establish legal meaning or completeness.
- TF-IDF is a relevance ranking signal, not a trained eligibility probability.
- Competitor feature statements are sourced from public product pages and are not a controlled product benchmark.

## Local verification baseline

`pytest -q`: 48 passed in this prepared environment. Provider calls are mocked; this is not a live integration claim. Python compilation and JavaScript syntax checks also passed.

## Recommended live acceptance sequence

1. Search returns actual provider URLs.
2. Fetch returns readable text from an official source.
3. Agent SSE emits a terminal successful completion and usable structured requirements.
4. At least one Agent quote is independently matched against a separate Fetch result.
5. A failed/unverified quote cannot support a blocker.
6. Recheck saves and compares the exact same official page URL.
7. Screenshots/logs show real provider results, redacting the API key.
