# BidSentry-E Implementation Audit & Remediation Report
**Team:** Syntax Squad | **Event:** Kritical Hacks 2026 | **Date:** 22 October 2026

## 1. Executive Summary

This audit evaluates the codebase against the Master Execution Prompt requirements for the BidSentry-E MVP. The project establishes an evidence-first tender pre-screening copilot for Indian MSMEs. The core architecture uses TinyFish Search & Fetch REST endpoints, TinyFish Agent REST SSE inspection, independent quote verification via Fetch, conservative deterministic comparison, and persistent SQLite snapshot diffs.

This document identifies baseline gaps across runtime stability, security, evidence verification, procurement heuristics, and user experience, together with the concrete remediation implemented in this release.

---

## 2. Gap Analysis & Remediation Matrix

| ID | Component | Baseline Defect / Gap | Severity | Status | Remediation Details |
|---|---|---|---|---|---|
| GAP-01 | `engine.py` | Windows console Unicode crash (`UnicodeEncodeError` on `\u20b9` Rupee symbol) in default cp1252 code pages | **Critical** | **Resolved** | Reconfigure standard output to UTF-8 on Windows environments with fallback encoding handling. |
| GAP-02 | `app/main.py` | URL validation did not explicitly reject embedded HTTP credentials or non-standard ports | **High** | **Resolved** | Hardened `ensure_public_https` to reject embedded user/password credentials, explicit non-443 ports, and local/private network ranges. |
| GAP-03 | `app/evidence.py` | QuoteCheck lacked classification for partial/token-overlap matches vs exact normalized matches | **High** | **Resolved** | Enhanced `verify_quote` to distinguish exact normalized matches from high-overlap partial matches (`NEEDS_HUMAN_REVIEW`); trimmed stray surrounding quotes. |
| GAP-04 | `app/analyzer.py` | Assessment lacked unified `clause_ledger` data model with explicit row states | **High** | **Resolved** | Added `generate_clause_ledger` emitting `MET`, `POTENTIAL_BLOCKER`, `UNKNOWN_PROOF_MISSING`, `UNVERIFIED_QUOTE`, and `NEEDS_HUMAN_REVIEW` states. |
| GAP-05 | `app/analyzer.py` | Missing extractors for Procuring Authority, Contract Type, and Estimated Value | **Medium** | **Resolved** | Implemented conservative regex extractors; contract type remains `UNKNOWN` when ambiguous rather than defaulting to goods/services. |
| GAP-06 | `app/analyzer.py` | Missing explicit `fetch_status`, SHA-256 `content_fingerprint`, and source validator metadata in tender results | **Medium** | **Resolved** | Added `fetch_status`, `content_fingerprint`, `etag`, and `last_modified` to tender models and search payloads. |
| GAP-07 | `app/analyzer.py` | Recheck diff lacked structured `affected_topics` identification for changed clauses | **Medium** | **Resolved** | Updated `summarize_change` to identify affected qualification topics (EMD, Turnover, Experience, Certifications, Deadline). |
| GAP-08 | `app/static/workbench.html` | Missing retry button on live search error; lacked structured clause ledger display table | **Medium** | **Resolved** | Added inline retry button for live errors, accessible status indicators, and integrated clause ledger table. |

---

## 3. Detailed Verification of Safeguards

### 3.1 QuoteCheck Evidence Gate
- **Verbatim Substring Presence:** A candidate quotation is verified if and only if its NFKC-normalized text appears verbatim in an independently fetched source snapshot.
- **Token Overlap Warning:** If words overlap but the verbatim string is absent, the quote is labeled `UNVERIFIED_QUOTE` with review status `NEEDS_HUMAN_REVIEW`. It is strictly barred from triggering a `POTENTIAL_BLOCKER`.
- **Negation and Exception Preservation:** Words like `not`, `exempt`, and numeric amounts are strictly preserved.

### 3.2 Conservative Procurement Policy
- **EMD Exemption:** The system never assumes automatic Udyam EMD exemption. Exemption wording triggers `NEEDS_HUMAN_REVIEW`.
- **Turnover & Experience:** Relaxation rules (e.g. 1x80%, 2x50%, 3x40%) are never applied automatically; they require explicit tender text.
- **Contract Type:** Category is never defaulted to Goods/Services based on the absence of "Works". Ambiguous cases remain `UNKNOWN`.

### 3.3 Re-check & Snapshot Scope
- Diffing is strictly limited to the fetched URL and page text.
- External linked PDFs and separate corrigenda are clearly identified as requiring independent URL inspection.

---

## 4. Verification and Regression Testing

All remediated components are verified against automated unit and API integration tests in `tests/`, covering:
- Exact and adversarial quote checks (negation inversion, numeric drift, token scrambling).
- URL validation and SSRF boundary testing.
- Heuristic extraction boundaries for Indian currency and numbers.
- Stream lifecycle and terminal status enforcement for TinyFish Agent runs.
- Offline synthetic smoke testing via `engine.py`.
