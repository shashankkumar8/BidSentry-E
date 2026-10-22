# BidSentry-E — Product and Engineering Specification

**Team:** Syntax Squad  
**Challenge:** Kritical Hacks 2026 — AI/ML Track, Open Innovation  
**Version:** 1.0 candidate release, 22 October 2026  
**Status:** Locally validated prototype; live TinyFish behavior still requires a team-side API-key run.

## 1. Product promise

BidSentry-E helps Indian MSME suppliers and bid coordinators pre-screen a public tender by showing candidate requirements, their source evidence, what can be compared with declared supplier facts, what remains unknown, and what changed in a rechecked page snapshot.

It is a **review-support tool**, not a legal eligibility determination, procurement advisor, bid submission robot, or guarantee that a supplier will qualify.

## 2. Primary user and moment

- **Primary user:** MSME owner, bid coordinator or tender consultant.
- **Moment:** a tender appears relevant; the user needs to decide what to verify before spending more time preparing a bid.
- **Job to be done:** “Show the requirements that may matter, let me inspect the source, compare them with our declared facts, and surface the gaps I need to resolve.”
- **Out of scope:** automated bid submission, legal interpretation, complete monitoring of all linked attachments, universal statutory exemption logic, authenticated GeM workflow automation and paid production operations.

## 3. Architecture and workflow

1. **Search — TinyFish Search REST.** Discover candidate URLs. Search results/snippets are discovery metadata, not evidence for a blocker.
2. **Fetch — TinyFish Fetch REST.** Retrieve readable Markdown and available metadata from selected URLs; save a local snapshot for recheck.
3. **Rank / extract — local AI/ML + rules.** TF-IDF ranks text relevance. Deterministic patterns surface candidate clauses. TF-IDF is not a trained eligibility model and its score is not a qualification probability.
4. **Inspect — TinyFish Agent REST SSE.** The primary UI path calls the documented `run-sse` endpoint and streams provider events (e.g. start, streaming URL, progress and terminal completion when returned by the provider). A separate synchronous official Python SDK route remains available as a compatibility/fallback API. The two contracts are not mixed.
5. **Independent quote check.** Agent-proposed quotes are checked against a separate Fetch response for the listed source URL. Exact normalized substring match is accepted as *quote presence*, not proof that the quote includes every exception or that the full tender has been inspected. Mismatch/unavailable source stays unverified and cannot alone create a blocker.
6. **Compare.** Compare supported text with explicitly declared supplier information. Use “Potential blocker” only as a possible gap that requires human verification. Missing facts and ambiguous rules remain unknown/review-needed.
7. **Re-check / change history.** Re-fetch the exact URL with live-cache bypass and origin validators when supported; if `conditional_unsupported` is returned, retry without conditional validators. A text diff covers the checked page only. Linked PDFs and separate corrigenda need their own URL checks.
8. **Audit metadata.** SQLite stores request ID, timestamp, HTTP method, endpoint, status and measured end-to-end duration. It does not store API keys or full request/response bodies. The hash is a content/record fingerprint, not a digital signature or tamper-proof audit log.

## 4. Status semantics and Clause Ledger states

The system maintains a structured Clause Ledger with transparent deterministic comparison states:

- **MET / reviewable match:** the declared supplier value appears to meet a simple parsed threshold. Documentary proof, averaging period, dates, scope and tender exceptions still need review.
- **POTENTIAL_BLOCKER / Potential blocker:** a parsed and source-backed requirement appears inconsistent with the declared profile. This does not itself establish disqualification.
- **UNKNOWN_PROOF_MISSING:** the requirement threshold is extracted, but the supplier fact is undeclared or documentary proof is missing.
- **UNVERIFIED_QUOTE:** the candidate quote could not be found verbatim in a separate source fetch snapshot, or no source text was available. Barred from triggering a blocker.
- **NEEDS_HUMAN_REVIEW:** ambiguous applicability, non-standard unit/format, partial token overlap without verbatim match, or policy uncertainty.
- **No obvious blocker found:** never render as “eligible”, “ready to bid”, “guaranteed compliant” or “all clauses satisfied”. Prefer: "No potential blocker detected among the requirements checked; manual review required".

## 5. Rules for consequential extraction

- Never create a blocker from a search snippet, third-party mirror or synthetic fixture.
- Preserve source URL, quote, page/heading when provided, verification status and reviewer action.
- Do not accept token-overlap/fuzzy matching as quote proof; token sets can lose order, negation, amounts and exceptions.
- Exact substring matching proves only that a string occurs in captured text. It does not validate context completeness; require human review of the surrounding clause and linked schedule.
- Do not parse “exempt” as zero. Do not calculate percentage EMD without a tender-specific rule. Ambiguous currency values are `Unknown`.
- Do not universally apply EMD, Udyam, turnover relaxations or CPWD/PSU similar-work formulas. Evaluate only when the exact tender wording and policy applicability have been verified; otherwise review manually.
- Do not infer Goods/Services vs Works from absence of words. Unknown procurement category stays unknown.
- A hash is an integrity fingerprint only; it is not a signature, source authenticity proof, or immutable log.
- A live Search/Fetch/Agent/recheck failure must surface as an error. No demo data may be substituted on a live-error path.
- Demo/preset data must say synthetic or benchmark everywhere it could be confused with a real source.

## 6. Current API surface

The exact schemas and implementation live in `app/main.py`. The browser UI uses the streaming Agent route; the synchronous SDK route remains for compatibility. Core routes:

- `GET /api/health`, `GET /api/v1/health`
- `GET /api/demo`
- `GET /api/v1/presets`, `GET /api/v1/presets/{preset_id}`
- `GET /api/history`, `GET /api/v1/history`
- `POST /api/search`, alias `/api/v1/search`
- `POST /api/inspect`, alias `/api/v1/inspect` (synchronous SDK compatibility route)
- `POST /api/v1/inspect/stream` (provider SSE UI path)
- `POST /api/recheck`, alias `/api/v1/recheck`
- `POST /api/v1/verify` — explicit demo/search/inspect mode
- `POST /api/v1/lab/quote-check` — synthetic adversarial quote guard

Live Search/Inspect/Recheck require `TINYFISH_API_KEY`. Read-only inspection only: no tender submission, registration, upload, payment or state-changing portal actions.

## 7. Runtime and security

- Python 3.11+ is required by the pinned TinyFish SDK contract used in this build.
- Secrets belong in a local `.env`, never in screenshots, source, shared logs or GitHub.
- Only public HTTPS Government/NIC tender URLs are accepted for direct Agent inspection and recheck.
- SQLite databases and caches are local runtime state and excluded from source/release ZIPs.
- Request audit rows intentionally omit request body, query values and headers containing secrets.
- Frontend must escape dynamic strings inserted into HTML, and must not ask a user to type the API key into page JavaScript.

## 8. Acceptance criteria

1. All unit/API tests pass from a clean archive extraction.
2. `python engine.py` prints a clearly labelled synthetic smoke report and demonstrates rejection of a fake quote; it does not perform a network call.
3. `GET /` serves the workbench and the versioned health/preset/history routes work.
4. Live paths without a key show a clear setup error and no fake live data.
5. Exact-source quote guard rejects a fabricated clause and does not discard negation.
6. Missing supplier facts stay unknown/review-needed.
7. Recheck diffs are scoped to the checked URL and say so.
8. Request time displayed in UI is measured; the streamed route writes end-to-end duration to the audit ledger only after stream completion. Agent steps come only from provider terminal/run metadata; SSE event count is separate; any dollar cost is an estimate and billing account is authoritative.
9. Nine-slide pitch covers all eight published submission requirements. No unsupported impact, accuracy, customer, revenue or cost claims.
10. `RELEASE_VERIFICATION.md` lists exactly what was run and clearly identifies the unverified live-provider gate.

## 9. Known limitations

- The heuristic clause parser can miss clauses or extract incomplete context. No labelled tender benchmark has yet established precision/recall.
- Exact quote presence is not a semantic or legal validation and can still select only part of a clause; humans must inspect context and linked documents.
- OCR for scanned PDFs, authenticated portals, full document graphs, legal policy decisioning, scheduled monitoring, user accounts and deployment are out of scope.
- Search availability, source HTML/PDF access, Agent permissions, account billing and response latency must be tested with the team's own TinyFish account.
