# BidSentry-E Automated Test Execution Report
**Team:** Syntax Squad | **Event:** Kritical Hacks 2026 | **Date:** 22 October 2026
**Environment:** Windows 11, Python 3.13.2, pytest 9.1.1, Node.js v25.5.0

---

## 1. Test Summary Overview

| Test Suite | File Path | Total Tests | Passed | Failed | Skipped | Duration |
|---|---|---|---|---|---|---|
| Provider SSE Contract | `tests/test_agent_sse.py` | 13 | 13 | 0 | 0 | 1.84s |
| Heuristic Parser & Analysis | `tests/test_analyzer.py` | 13 | 13 | 0 | 0 | 1.15s |
| API Endpoints & Lifecycle | `tests/test_api.py` | 10 | 10 | 0 | 0 | 2.10s |
| Evidence & QuoteCheck | `tests/test_evidence.py` | 6 | 6 | 0 | 0 | 0.05s |
| V1 Workbench & Telemetry | `tests/test_v1_workbench.py` | 8 | 8 | 0 | 0 | 0.85s |
| Adversarial Regressions | `tests/test_adversarial_regressions.py` | 18 | 18 | 0 | 0 | 3.22s |
| **Total Automated Suite** | **`tests/`** | **68** | **68** | **0** | **0** | **9.36s** |

**Result:** **100% PASS (68/68 tests passed).**

---

## 2. Command Execution Log

### 2.1 Pytest Execution
```powershell
python -m pytest -q
```
**Output:**
```
....................................................................     [100%]
68 passed in 9.36s
```

### 2.2 Python Compilation Check
```powershell
python -m compileall -q app engine.py tests scripts
```
**Exit Code:** `0` (Clean compilation, zero syntax or byte-compilation errors).

### 2.3 JavaScript Syntax Verification
```powershell
node --check app/static/app.js
python -m scripts.check_inline_js
```
**Output:**
```
PASS: 1 inline JavaScript block(s) parsed by node --check
```

### 2.4 Offline Synthetic Smoke Runner
```powershell
python engine.py
```
**Exit Code:** `0`
**Key Output Markers:**
- `mode`: `"LOCAL_SYNTHETIC_SMOKE_TEST"`
- `quotecheck.source_quote.badge`: `"QUOTE_VERIFIED_FETCH"` (`match_type: "EXACT_NORMALIZED_MATCH"`)
- `quotecheck.hallucinated_quote.badge`: `"UNVERIFIED_QUOTE"` (`match_type: "NO_MATCH"`, `review_state: "NEEDS_HUMAN_REVIEW"`)
- `assessment.clause_ledger`: 4 structured clauses evaluated against supplier profile
- `duration_ms`: ~9 ms
- `audit_id`: Logged to local SQLite audit table

### 2.5 API Endpoint Integration Smoke Check
```powershell
python -c "from fastapi.testclient import TestClient; from app.main import app; c = TestClient(app); print('Root:', c.get('/').status_code); print('Health:', c.get('/api/v1/health').json()); print('Presets:', len(c.get('/api/v1/presets').json()['presets'])); print('Lab:', c.post('/api/v1/lab/quote-check', json={'quote':'test quote for check', 'source_text':'sample'}).json()['badge']); print('Demo verify:', c.post('/api/v1/verify', json={'mode':'demo'}).json()['mode'])"
```
**Output:**
```
Root: 200
Health: {'ok': True, 'name': 'BidSentry-E', 'version': '0.1.0', 'tinyfish_configured': False, 'mode': 'demo-ready'}
Presets: 2
Lab: UNVERIFIED_QUOTE
Demo verify: demo
```

---

## 3. Adversarial Edge Case Coverage (20 Required Safeguards)

1. **Indian Currency Units:** Validated Lakhs (`4,00,000`), Crores (`1.5 Crore`), Thousands, Ambiguous ranges (`500-1000` -> `None`), Percentages (`2%` -> `None`), Exemption phrases (`exempt` -> `None`), and Explicit Zero (`Nil` -> `0.0`).
2. **Missing Source Data:** Empty text safely defaults to `Human review needed` with `UNKNOWN_PROOF_MISSING` states; no unhandled crashes.
3. **Exact Substring Verification:** Whitespace and unicode NFKC normalization accepted; non-verbatim text rejected.
4. **Numeric-Value Alteration:** Rejects quote with altered numeric values (`3 crore` vs `2 crore`) and flags `PARTIAL_OR_UNCONFIRMED_OVERLAP`.
5. **Percentage Drift:** Rejects quotes with modified percentages (`5%` vs `2%`).
6. **Negation & Exception Tampering:** Verifies that inverted negations (`is required` vs `is not required`) fail quote verification.
7. **Paraphrase Rejection:** Semantic paraphrases that lack verbatim source presence are marked `UNVERIFIED_QUOTE`.
8. **Malformed Agent Output:** Stream handles invalid JSON or missing `requirements` gracefully, emitting explicit error frame.
9. **Stream Interruption & Timeout:** Handles `FAILED` and `ERROR` stream events without creating unearned assessments.
10. **Incomplete Runs (Progress without Terminal):** Runs that emit `PROGRESS` but close without `COMPLETE` event fail closed.
11. **Provider Step Metadata:** Missing `num_of_steps` remains `None`; SSE event counts are never conflated with billable steps.
12. **Live Fetch Failure Isolation:** Live fetch errors return HTTP 502 and never silently substitute synthetic benchmarks.
13. **Unknown Contract Type:** Ambiguous tenders remain `Unknown / Unspecified`; never defaulted to `Goods` or `Services`.
14. **EMD & Policy Ambiguity:** Free-text exemptions and non-numeric EMD remain unresolved for human review.
15. **Experience Formula Restraint:** Non-standard formulas are not forced into rigid heuristics.
16. **Snapshot Differences:** Identifies changed lines and maps them to affected topics (`EMD`, `Turnover`, `Experience`, `Certificates`, `Deadline`).
17. **URL Scoping for Snapshots:** Re-check queries only the exact matched URL from the database.
18. **Benchmark Mode Separation:** Synthetic presets explicitly marked `mode: "benchmark"` / `mode: "demo"`.
19. **XSS Protection:** Untrusted HTML and Javascript in source text escaped via `esc()`.
20. **Security & URL Validation:** Reject URLs with embedded credentials (`user:pass@`), non-443 ports, private IPs (`127.0.0.1`), and non-gov domains.
