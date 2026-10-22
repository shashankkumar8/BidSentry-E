# Audit of the attached BidSentry-E “master build” proposal

## Verdict

The direction is strong and beyond a beginner concept: it combines a concrete procurement job, TinyFish Search/Fetch/Agent, evidence checks, explicit uncertainty, source recheck, audit telemetry and automated tests. **The pasted proposal should not be copied unchanged.** It contains several claims and code paths that would be easy for a technical judge to challenge. The final code keeps the useful constraints while rejecting the unsafe shortcuts.

## Rule-by-rule reconciliation

| Proposal rule / idea | Final treatment | Why |
|---|---|---|
| Unverified extracted clause cannot trigger a blocker | **Kept** | `/api/inspect` independently fetches listed source URLs; mismatched or missing quotes remain unverified and are excluded from the assessment input. |
| Missing supplier field remains unknown | **Kept** | Pydantic distinguishes `None` from a declared zero; assessment emits Unknown / Human review needed. |
| REST and SDK contracts remain separate | **Kept** | `app/tinyfish.py` uses direct REST for Search/Fetch and the pinned SDK for Agent; parameters are not copied across interfaces. |
| Count Agent steps only from provider `num_of_steps` | **Kept** | UI should display provider-reported step count; SSE events are not treated as billed steps. Unit costs are estimates only. |
| SHA-256 is a fingerprint, not “tamper-proof” | **Kept** | Hash/fingerprint language is restricted to captured content/record integrity, not signing/authenticity. |
| Recheck covers exact URL, not every attachment | **Kept** | API note says text-diff scope is checked page only; separate PDF/corrigendum URLs must be inspected separately. |
| Live failure must never mask as sample data | **Kept** | Live Search/Inspect/Recheck report errors; synthetic preset mode is separate and clearly labelled. |
| Build a three-column UI, single-click synthetic presets and an adversarial quote lab | **Kept** | `app/static/workbench.html` has profile/presets, results/evidence ledger and real response telemetry/history; `/api/v1/lab/quote-check` provides a synthetic negative test. |
| SQLite recent run ledger | **Kept with privacy limits** | Stores request ID, UTC timestamp, method, endpoint, HTTP status and measured duration. No request body, provider key or profile payload. |
| CLI can be called a full live smoke test | **Rejected** | `python engine.py` intentionally runs a local synthetic smoke test. Live tests require a key and real API responses. |
| Accept ≥85% token recall as verified evidence | **Rejected** | Token overlap can lose order, negation, value and exceptions. The final verifier uses strict normalized substring presence. It still does not guarantee quote-context completeness; human review remains required. |
| Any text containing “exempt” parses to zero | **Rejected** | Exemption is not numerically equivalent to zero; text must remain unresolved unless the exact applicable rule and tender clause establish the result. |
| Default missing contract category to goods/services and apply Udyam/EMD logic | **Rejected** | Absence of “works” does not prove “goods/services”. EMD and MSE conditions are purchaser/tender/policy specific. |
| Universal CPWD/PSU 1×80%, 2×50%, 3×40% logic | **Rejected as a universal rule** | Such criteria must come from the exact tender and applicable procurement documents. The product must not apply the formula to every procurement. |
| Mark “Eligible” when no blocker is detected or compute readiness as MET/total | **Rejected** | Missing clauses or unknown applicability make that score misleading. No legal eligibility badge/readiness percentage is emitted. |
| Claim 252 ms, $0.024 per tender, 82% saving, 83.5% margin or “zero hallucination” | **Rejected** | No evidence in the supplied content validates these operational or commercial claims. Measure from real runs and labelled pilot data first. |
| Pretend built-in scenarios are real public tender notices | **Rejected** | Presets are labelled synthetic benchmarks. Do not attach them to a false real-world URL or imply the data is current. |
| Display a designed workbench schematic as an actual runtime screenshot | **Rejected** | Slide 5 labels the visual as a schematic and synthetic example. Capture a real UI screenshot only after running the app. |

## Remaining nontrivial risks

1. Exact-substring match proves a candidate quote exists in captured text, but not that the excerpt includes all surrounding exception language. A future version should store the source line/paragraph context around each quote and require a reviewer to open that context before any high-impact classification.
2. The clause parser is heuristic, not a trained tender model. It may miss clauses, mishandle tables/PDFs or split context. Measure on a labelled corpus before claiming extraction accuracy.
3. A page-level recheck does not discover every separately hosted corrigendum or every attachment update. Document URL coverage and last checked time.
4. Local automated tests mock provider responses. The live service/SDK must be verified with the team's account, key permissions, billing and a real public tender.

## Decision

Use the final source plus `SPEC.md` as the contract. The long pasted proposal remains an input/specification source, not a tested codebase. Follow `BUILD_SEQUENCE.md`; do not swap in the pasted app/engine wholesale.
