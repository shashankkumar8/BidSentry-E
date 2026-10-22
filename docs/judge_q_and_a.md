# Judge Q&A — BidSentry / Syntax Squad

Use concise answers grounded in the current code. If asked about live tests, distinguish local mocks from the live API run.

## 1. What problem are you solving?

A tender title can match a supplier's work while a requirement in a notice, tender page or amendment still needs careful review. BidSentry aims to help a small bid reviewer surface those requirements, see their source quote, compare them with declared supplier information, and identify what remains unknown before investing more effort.

## 2. What makes this different from tender aggregators?

We do not claim aggregators only search or that nobody offers AI eligibility checking—Tender247 publicly advertises eligibility and bid/no-bid functions, as well as corrigendum tracking. Our differentiation hypothesis is the evidence chain: fetched source URL → quote checked against a separate fetch → declared profile comparison → explicit Unknown/review state → page-text diff. We need a same-tender product trial to measure whether this is clearer or more trustworthy.

## 3. Why is TinyFish meaningful rather than decorative?

Search discovers current public tender pages; Fetch retrieves text and metadata used by the analyzer; the user-triggered Agent extracts structured criteria from a selected official page; a separate Fetch pass checks the Agent quote; and a live Fetch re-checks a saved source snapshot. These are separate, observable API responsibilities. The demo must show a real account-backed run to prove the mandatory integration.

## 4. Is the system actually AI/ML?

The prototype is hybrid. Scikit-learn TF-IDF ranks page relevance; transparent deterministic patterns extract selected clauses and numeric values; a schema-constrained TinyFish Agent can inspect a selected official page. We do not claim a trained Indian tender eligibility classifier or a learned probability of success.

## 5. How do you stop the LLM from inventing a requirement?

A search snippet cannot trigger a blocker. Agent outputs are structured but not automatically trusted; a second independent Fetch checks if the quote occurs in the retrieved text. The verification normalizer preserves numbers and negation and does not use fuzzy token overlap. A failed match stays unverified. This reduces one failure path, but does not guarantee that every source passage, cross-reference or attachment was included.

## 6. What does “verified” mean?

It means the displayed quote occurs in a separate fetched text response for the listed source URL under documented conservative normalization. It does not mean the whole tender is complete/current, the passage is legally interpreted correctly, or the supplier is eligible. The complete document and amendments still need review.

## 7. Does a blocker mean the supplier cannot bid?

No. The UI says “potential gap” when an explicitly extracted requirement appears to conflict with a supplier-declared value. Eligibility may depend on exceptions, definitions, registration scope, purchaser policy, other documents or clarifications. Missing fields are Unknown; absence of found blockers is not an eligibility certificate.

## 8. How do you handle EMD and Udyam exemptions?

We do not auto-apply an exemption just because `udyam_registered` is true. The policy scope depends on procurement category, purchaser, registration and tender language; official policy material also distinguishes goods/services from works contracts. The current model is conservative: it surfaces a stated EMD and compares it with declared liquidity where parsing is reliable, while percentage-based or ambiguous clauses should remain Review/Unknown.

## 9. What is the quality evidence?

The local test suite currently has 48 passing tests using fixtures and mocks. It checks behavior such as fail-honestly without a key, unknown when data are missing, no snippet-only blocker, conservative quote verification and conditional-fetch fallback. These tests do not prove live credentials or accuracy on the full range of Indian tenders. The next step is a 20–30-tender annotated test set and a live account-backed demo.

## 10. What are the main limitations?

The baseline may miss criteria in linked PDFs, BOQs, ATC tabs or attachments; parsers cover only selected text patterns; the current recheck compares the reached page's text and does not traverse all linked documents. Dynamic pages may need the Agent. A page diff can contain noise. Each limitation is disclosed rather than silently treated as a pass.

## 11. What is your revenue model?

A capped monthly plan for small suppliers or a seat/usage plan for bid consultants is a hypothesis. Price points in the deck are not validated. The next step is to interview users about tender volume, current tools, review costs and willingness to pay, then test a small paid pilot.

## 12. Why not submit bids automatically?

This is a high-consequence procurement decision. BidSentry's immediate job is to make pre-screening evidence easier to review. Automatic portal login/submission raises identity, compliance, security and irreversible-action risks and is out of scope.

## 13. Does the project use Agent-E?

No. Agent-E is a research paper that informs ideas such as separating high-level planning from browser execution and observing page changes. BidSentry borrows general design lessons; it neither implements Agent-E nor claims its benchmark results.

## 14. What would you build next?

Use an annotated tender corpus to measure extraction and quote-verification precision/recall; inventory linked attachments and show incomplete coverage; benchmark page-change signal quality; then run a time-to-shortlist study with bid reviewers. Scale only the workflow that improves measured outcomes.
