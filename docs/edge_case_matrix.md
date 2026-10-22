# BidSentry edge-case and acceptance matrix

This matrix is the test contract for the current prototype. **“Unit-tested” means locally tested with controlled fixtures/mocks, not live-verified against TinyFish or a production procurement portal.**

| # | Case | Expected safe behavior | Current status |
|---|---|---|---|
| 1 | Search snippet claims a huge turnover requirement, but Fetch returns no text | Show search result for discovery only; do not generate a blocker from snippet text | Unit-tested |
| 2 | Source host imitates an official host, e.g. `etenders.gov.in.attacker.example` | Classify as non-official; do not treat a substring lookalike as an official domain | Unit-tested |
| 3 | Official hostname includes a normal port such as `:443` | Normalize host and classify by hostname, not display string | Unit-tested |
| 4 | Supplier omits turnover/experience fields | Keep the assessment Unknown / Human review needed; do not convert null to zero | Unit-tested |
| 5 | EMD text says `Rs. 50,000`, `₹1.5 lakh`, or Indian comma group `1,50,000` | Parse only when the amount follows a nearby EMD/bid-security label; capacity gap is a potential blocker only | Unit-tested |
| 6 | EMD is exempt/waived or amount is stated before the EMD label | Do not infer an amount of zero or apply an exemption automatically | Unit-tested, conservative parser |
| 7 | Clause says “EMD shall be 2% of estimated cost Rs. 2 crore” | Do not treat ₹2 crore as the EMD; leave amount unknown pending tender-specific calculation | Unit-tested |
| 8 | Agent returns exact quote present in an independent Fetch response | Mark `verified_by_fetch`; evaluate only the verbatim verified span | Unit-tested with mock Fetch |
| 9 | Agent paraphrase says ₹99 crore but its returned quote merely says “submit supporting documents” | Never infer the ₹99 crore threshold from the paraphrase; show Human review needed | Unit-tested |
| 10 | Agent quote absent from Fetch text or a source URL is disallowed | Keep quote unverified; do not let it alone trigger a blocker | Unit-tested |
| 11 | Conditional recheck returns `conditional_unsupported` on a JS-rendered page | Retry once without conditional validators with `ttl: 0`; preserve a visible error if retry also fails | Unit-tested with mock API |
| 12 | Missing API key or network/API failure | Return a visible configuration/error state; never silently replace it with synthetic data | Unit-tested for key path; credential/HTTP failures need a live smoke test |
| 13 | TinyFish Agent returns 401/403 because a feature is not enabled | Baseline Agent call avoids documented account-gated capture/strict settings; remaining account/network errors must be shown honestly | Code guard reviewed; live account test required |
| 14 | Direct PDF NIT URL | Fetch without CSS selector filters; verify whether text comes back | REST doc reviewed; live PDF not tested; OCR is not implemented |
| 15 | Clause appears inside JavaScript-injected iframe/accordion absent from Fetch Markdown | Do not mark an Agent quote as verified unless separate Fetch returns the exact quote; prompt manual review | Design guard; this page class may remain unverified until browser-visible evidence is available |
| 16 | Recheck page returns unchanged ETag / 304-like `not_modified` | Do not claim that all tender attachments/corrigenda are unchanged—only the checked URL was unchanged | Single-URL conditional path; add live recheck demonstration |
| 17 | Corrigendum contradicts original NIT | Display changed-source evidence, do not silently choose a winner; require human resolution | Manual review required; automated conflict resolver is not implemented |
| 18 | Multilingual notice, scanned PDF/OCR, unusual date/currency formatting | Leave uncertain extraction as Unknown and point to the official source; no unsupported pass/fail | Known limitation; future work |
| 19 | A similar-work rule requires one or multiple completed works | Do not apply universal 1×80% / 2×50% / 3×40% rule across tenders; extract tender-specific wording for review | Explicitly not implemented as a universal rule |
| 20 | Page text changes because of layout/advertising rather than a legal amendment | Surface text diff and hot terms only as a review signal; do not call it a legal change | Implemented at page-text level; semantic amendment linkage is future work |
| 21 | Repeated background monitoring/alerts or auto-submitting a bid | Do not imply scheduled monitoring, enterprise workspaces, form submission or legal decisioning exists | Out of scope |
| 22 | Agent stream disconnects with a run ID already captured | Lookup `/v1/runs/{id}` to recover terminal metadata; reject non-terminal or failed runs | Unit-tested with mock SSE & run recovery |
| 23 | Altered numbers in candidate quotation (e.g. 3 crore vs 2 crore) | QuoteCheck rejects verbatim match and flags `PARTIAL_OR_UNCONFIRMED_OVERLAP` with `NEEDS_HUMAN_REVIEW` | Unit-tested in `test_adversarial_regressions.py` |
| 24 | Inverted negation / tampering (e.g. "is required" vs "is not required") | QuoteCheck strictly fails closed and prevents blocker generation | Unit-tested in `test_adversarial_regressions.py` |
| 25 | URL with embedded credentials or non-standard port | Hardened `ensure_public_https` rejects with 400 Bad Request to prevent SSRF and credential leaks | Unit-tested in `test_adversarial_regressions.py` |
| 26 | Free-text exemption or ambiguous range in currency parsing | Stays unresolved as `None` (Unknown) rather than inventing 0.0 or a false amount | Unit-tested in `test_adversarial_regressions.py` |

## Release acceptance gate

The local suite passes **68 automated tests** (including 20 focused adversarial regression tests); it does not replace this live release gate. If a live step fails, show the failure and fix it rather than recording fabricated output.
