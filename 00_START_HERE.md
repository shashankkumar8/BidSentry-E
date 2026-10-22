# BidSentry-E / Syntax Squad — Technical Release

**Kritical Hacks 2026 · AI/ML Track · Technical-only project bundle**

## What this archive is

This ZIP contains the BidSentry-E application source, tests, technical documentation, run instructions, submission text, and the original user-provided reference files. **It intentionally contains no pitch PPT, presentation PDF, deck-generation scripts, deck screenshots or unrelated project ideas.** Upload the separately prepared PPTX as the primary initial-round submission; attach this technical ZIP only where the application asks for a code/project archive or provide its public repository link after publishing it yourself.

The original source bundle and the long user-provided master-build paste are preserved unchanged in `references/`. The current working implementation lives in `app/`, `engine.py`, and `tests/`.

## Read and run in this exact sequence

1. `SOURCE_PROVENANCE.md` and `INPUT_HASHES.txt` — what was provided and how the original inputs are preserved.
2. `references/Exact_Copies_Bundle.zip` and `references/extracted/` — the four original source documents, byte-preserved and separately readable.
3. `references/Proposed_Master_Build_Original.txt` — the complete user-provided master-build proposal, unchanged.
4. `REFERENCE_SYNTHESIS.md` and `PROPOSED_MASTER_BUILD_AUDIT.md` — requirement mapping and a technical audit of the proposed implementation.
5. `SPEC.md` — current intended application behavior and boundaries.
6. `SSE_STREAM_CONTRACT.md` — provider-stream lifecycle, terminal-state gates, independent quote verification and cost/step reporting.
7. `BUILD_SEQUENCE.md` and `QUICK_START.txt` — follow install, offline tests and launch steps in order.
8. Run `pytest -q`, `python -m compileall -q app engine.py`, `node --check app/static/app.js`, and `python -m scripts.check_inline_js`.
9. Configure your own TinyFish key locally using `.env.example`, then perform a live Search → Fetch → Agent REST SSE → separate Fetch quote-check → source recheck.
10. Use `SUBMISSION_GUIDE.md`, `FINAL_SUBMISSION_COPY.txt`, and `SUBMISSION_CHECKLIST.md` to complete Unstop. Save the portal confirmation yourself.

## Verified locally in this release

- `pytest -q`: **68 passed** (provider interactions are mocked in local tests; comprehensive adversarial regression suite).
- Python compile check: pass (`python -m compileall -q app engine.py tests scripts`).
- JavaScript syntax checks: pass (`node --check app/static/app.js` and `python -m scripts.check_inline_js`).
- Synthetic smoke CLI: pass (`python engine.py`).
- This is not evidence of a successful live TinyFish run; no team-owned API key is included or used here.

## Live proof boundary

Do not report a live integration as demonstrated until a run with your own key returns actual provider responses. Do not claim legal eligibility, zero hallucinations, measured savings, guaranteed qualification, complete amendment coverage, or production readiness without supporting evidence. A text match confirms quote occurrence, not legal interpretation or completeness of every linked attachment.
