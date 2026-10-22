# Release verification — BidSentry-E / Syntax Squad

**Candidate:** 1.4 · **Date:** 23 October 2026 · **Status:** Local automated validation and adversarial protection passed (68 tests); GitHub repository synced to `https://github.com/shashankkumar8/BidSentry-E.git`; Render deployment config (`render.yaml`) and CI workflow (`.github/workflows/ci.yml`) configured; live TinyFish account-backed run pending user API key.

## Checks actually run

- `pytest -q`: **68 passed**. This includes 48 core route, stream lifecycle, quote verification, and analyzer tests, plus 20 adversarial edge-case regression tests (Indian currency variations, negation tampering, numeric alteration, malformed streams, SSRF/URL validation, and fail-closed guarantees). TinyFish provider responses in these tests are mocked.
- `python -m compileall -q app engine.py tests scripts`: passed cleanly.
- `node --check app/static/app.js`: passed.
- `python -m scripts.check_inline_js`: passed (workbench inline script parses cleanly with Node).
- `python scripts/verify_package.py`: passed; verifies 100% byte matches for all preserved references in `INPUT_HASHES.txt`, checks JS syntax, and verifies clean workspace hygiene.
- `python engine.py`: passed; verified offline synthetic smoke runner, QuoteCheck adversarial guard, and Clause Ledger output on Windows UTF-8 stdout.
- FastAPI endpoint smoke check: verified root, health, presets, lab quote-check, and verify endpoints.
- Archive hygiene scan: verified absence of `.env`, API keys, `.venv`, `__pycache__`, local databases, and presentations from the technical release.
- Equilibrium build test: `npm ci` and `npm run build` in `equilibrium-landing/` passed in 11.2s with zero TypeScript or Vite errors.

## Implemented and tested locally

- TinyFish Search and Fetch REST adapters are separate from the optional synchronous Python SDK Agent path.
- Primary workbench Agent inspection uses the direct REST SSE adapter at `POST /api/v1/inspect/stream`; provider events are exposed as trace metadata only.
- SSE event count is not used as Agent steps. Steps are read from the terminal provider payload or provider run lookup; missing step metadata remains unknown.
- Agent quotes are independently checked against a separate Fetch response. Unverified quotes are surfaced and excluded from the evidence used for comparison.
- Partial token overlap is distinguished from verbatim normalized matches and marked `NEEDS_HUMAN_REVIEW` without triggering blockers.
- A terminal/metadata failure, missing terminal completion, invalid extraction, or live API failure does not create an assessment or silently substitute a benchmark scenario.
- Structured Clause Ledger data model with explicit `MET`, `POTENTIAL_BLOCKER`, `UNKNOWN_PROOF_MISSING`, `UNVERIFIED_QUOTE`, and `NEEDS_HUMAN_REVIEW` states.
- Enhanced SSRF and URL validation rejecting embedded credentials and non-standard ports.
- Streamed endpoint audit duration is written after stream iteration finishes; the response header does not pretend time-to-headers is full stream latency.
- Snapshot differences are explicitly scoped to the checked URL/page text and identify affected procurement topics.

## Not verified (must not be claimed)

- No real TinyFish API request was made with Syntax Squad’s API key in this environment.
- No live tender portal’s Agent/SSE output, streaming URL, step metadata, or independent Fetch result has been verified against a real provider response.
- No accuracy/recall benchmark on a labelled real-tender corpus, customer pilot, user-time-saved study, willingness-to-pay study, or production reliability test is complete.
- No public GitHub push, public demo video/social post, or Unstop submission was performed here.

## Live release gate

- [ ] Configure `TINYFISH_API_KEY` in local `.env`, never inside a ZIP/repository.
- [ ] Run live Search and inspect an official source URL.
- [ ] Run one live Agent SSE inspection; capture the actual provider events and streaming URL if present.
- [ ] Confirm terminal status is successful and step count comes only from provider metadata.
- [ ] Confirm at least one exact Agent quote is found in a separate Fetch response.
- [ ] Run a live recheck; explain that linked PDFs or external corrigenda need separate URLs.
- [ ] Save redacted screenshots / a demo recording.
- [ ] Extract the final ZIP in a clean directory, rerun tests, and inspect archive contents.
