# BidSentry-E — Judge Q&A

## What problem do you solve?
A supplier can discover a tender yet still need to inspect several sources and compare requirements with company evidence. BidSentry-E narrows that review by surfacing candidate clauses, their source text, supplier gaps and changes on a checked page.

## What exactly is innovative?
The individual ideas—search, tender summaries, qualification checks and change alerts—exist in the market. Our differentiation hypothesis is an inspectable evidence chain: the reviewer sees the URL, quote-check method, separate-source verification status, profile comparison, uncertainty state and recheck scope in one workbench. We plan to validate usefulness against current tools and real reviewers instead of claiming the features are unique by themselves.

## Where is the AI/ML?
TF-IDF with lexical overlap ranks the relevance of tender text to a supplier profile. It prioritizes research and is not a trained eligibility classifier or qualification probability. TinyFish Agent performs structured extraction when portal interaction is needed. Deterministic code handles conservative comparisons and explicit uncertainty.

## Why TinyFish Search, Fetch and Agent?
Search discovers candidates; Fetch gets content/metadata at known URLs; The primary workbench Agent path uses REST SSE to handle interactive pages and expose provider progress; the synchronous Python SDK path remains as compatibility. REST and SDK use their respective contracts. Search snippets do not count as source evidence, and Agent-generated quotes are checked against a separate Fetch response.

## Does QuoteCheck guarantee no hallucinations?
No. It rejects a quote when the required string cannot be found in the independently fetched text. Exact string presence doesn't establish full context, completeness, truth, or legal applicability. A human must inspect the full clause, linked documents and amendments.

## Why not use fuzzy token recall?
Token overlap can approve a sentence whose words occur in a different order or context and may weaken negation, amounts or exceptions. This build deliberately uses strict normalized substring presence. The tradeoff is that genuine quotes reformatted by HTML/table rendering can be marked unverified; we prefer manual review over overstating evidence.

## What happens when supplier information is missing?
The status remains Unknown / Human review needed. It is not silently treated as zero, failure or success.

## How do you handle EMD and Udyam exemptions?
We do not apply a universal exemption. Applicable conditions depend on tender wording, purchaser, procurement category and current rules. The user should validate the exact notice and governing policy. Percentage-based EMD stays unresolved unless supported by a tender-specific calculation rule.

## What does the change monitor actually cover?
It compares the content returned for the specified URL against the stored text snapshot and uses ETag/Last-Modified when available. It does not prove that external PDFs or separate corrigenda changed or remained unchanged unless those URLs are checked too.

## How is TinyFish cost computed?
The app uses the provider-reported `num_of_steps` for Agent runs. A displayed dollar figure, if configured, is only a rate-based estimate; actual account billing and current pricing control. We do not claim fixed COGS or percentage savings without real usage logs.

## Is the app production-ready?
No. The local prototype has automated tests and explicit error handling, but live TinyFish calls, tender extraction accuracy and measurable customer impact require further validation. We have not claimed deployment, customers or a production SLA.

## What would you validate next?
A live Search → Fetch → Agent → separate Fetch verification → recheck run; then a labelled benchmark of 25–50 real tender pages/linked documents reviewed by two annotators; then 5–8 MSME bid-reviewer interviews to measure review time, missed clauses and trust.
