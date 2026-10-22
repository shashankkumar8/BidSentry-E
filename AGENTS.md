# Working instructions for coding agents — BidSentry-E

1. Treat `SPEC.md` as the contract. Do not broaden the product without updating the spec and tests first.
2. Keep the product name `BidSentry-E`, team `Syntax Squad`, and event `Kritical Hacks 2026` consistent.
3. Preserve source provenance: official-source URL, excerpt, source-check method, status and timestamp. Never invent a source or fabricate a live result.
4. Use TinyFish Search / Fetch REST contracts only in the REST adapter and the documented TinyFish Python SDK contract only in `app/tinyfish.py`. Don't mix parameter names across interfaces.
5. Never count SSE events as Agent steps. Use the provider's reported `num_of_steps`; label any unit cost as an estimate and keep rate configurable.
6. Do not claim “eligible”, “ready to bid”, “zero hallucinations”, “100% accurate”, “tamper-proof”, measured savings, production readiness, paid customers or validated margins without proof.
7. An unverified quote cannot trigger a blocker. Missing supplier facts and ambiguous clauses remain Unknown / Human review needed.
8. Do not infer exemptions from a keyword. Do not universally apply GFR, Udyam/EMD, turnover relaxations or experience formulas. Require tender-specific source/context and human review.
9. Live operation failures must be returned clearly. Never switch to benchmark data as a silent fallback. Benchmark presets must remain labelled synthetic.
10. Audit logs may store only request metadata and actual measured wall time; never keys, full request bodies, or supplier profile payloads.
11. No writes or actions on external tender sites. Inspection is read-only.
12. Make one small vertical-slice change at a time, add negative/edge-case tests, run tests/compile/JS syntax, and report actual outcomes.
13. Before editing an archive or source tree, inspect the existing files. Do not replace working code with a proposal snippet merely because it is longer.
14. Before a release: remove databases, `.env`, keys, caches and virtualenvs from deliverables; validate archives by fresh extraction and rerun tests.
