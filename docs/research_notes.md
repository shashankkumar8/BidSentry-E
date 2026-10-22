# Research notes informing BidSentry

This is a short design-oriented literature review, not a systematic review and not evidence that BidSentry itself has been evaluated in production.

## 1. Public procurement suitability-criteria extraction

**Endtner, Janik & Stürmer, Matthias (2019). _Extraction of Suitability Criteria from Tender Documents Using Machine Learning._** DOI: https://doi.org/10.13140/RG.2.2.35360.12808. Public full-text/preprint landing page: https://www.researchgate.net/publication/335567902_Extraction_of_Suitability_Criteria_from_Tender_Documents_Using_Machine_Learning

The case study describes a pipeline for unstructured tender documents that combines pattern matching, logical text segmentation, text features and Random Forest classification to identify suitability criteria. Its line-joining test reported 94.5% accuracy in that specific experiment; that number is **not** an overall tender-eligibility extraction accuracy and must not be represented as BidSentry's performance. The authors worked with Swiss procurement documents and noted document-structure limitations. This motivates a layered extractor, exact evidence spans and explicit unknown states rather than an unqualified eligibility label.

## 2. RAG and question-answering over tender files

**A Dual-Mode Retrieval-Augmented Generation System for Interactive Question Answering of Public Tender Documents (2026).** Procedia Computer Science, Volume 278, pp. 1478-1486. DOI: https://doi.org/10.1016/j.procs.2026.03.134

The paper describes lexical plus semantic retrieval and a response generator constrained to retrieved context for tender-document Q&A. Its study used synthetic tender documents and qualitative testing, so it is a useful architectural precedent, not strong field evidence. BidSentry therefore keeps the initial prototype conservative: retrieve live page content, preserve quotations, use transparent scoring and leave unclear requirements for human review.

## 3. Retrieval-grounded generation and citation reliability

**Brown, Andrew; Roman, Muhammad; Devereux, Barry (2025). _A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges._** arXiv:2508.06401. https://arxiv.org/abs/2508.06401

The review synthesizes 128 selected studies from 2020 through May 2025 and describes how retrieval can ground generation in up-to-date external information while also highlighting evaluation challenges. This supports measuring evidence coverage and extraction errors, not only interface quality.

**_Synthesizing scientific literature with retrieval-augmented language models_ (OpenScholar).** Nature, https://www.nature.com/articles/s41586-025-10072-4

The paper reports a specific experiment in which GPT-4o fabricated citations frequently when asked to cite recent literature across fields. That percentage applies to the paper's experimental setup; it is not a universal hallucination rate. The product lesson is to preserve source URLs and textual evidence, and to separate directly observed facts from model/rule inferences.


## 4. Browser-agent planning is a design input, not a result claim

**Abuelsaad et al. (2024), _Agent-E: From Autonomous Web Navigation to Foundational Design Principles in Agentic AI_.** arXiv:2407.13032. https://arxiv.org/abs/2407.13032

Agent-E (from Emergence AI, not TinyFish) studies separation of planning and browser execution, task-oriented DOM distillation and change observation for website interaction. BidSentry borrows the broad principle of separating cheap discovery/retrieval from a deeper, goal-constrained browser task. Its current prototype does **not** reproduce the complete Agent-E architecture, and a benchmark score reported by a paper must not be presented as BidSentry's own success rate. Browser agents can fail on dynamic pages; only the team's own test runs can establish performance on the selected tender sources.

## 5. Evidence-backed answers and citation verification

**Gao, Yen & Chen (2023), _Enabling Large Language Models to Generate Text with Citations_ (ALCE).** EMNLP 2023. https://aclanthology.org/2023.emnlp-main.398/

ALCE evaluates generated answers and citations, including whether cited evidence supports answer claims. The relevance to BidSentry is methodological: a citation existing is not enough; the quote and the assessment must be traceable to the same source. The prototype therefore checks a proposed Agent quote against separately fetched text and fails closed if it cannot find the quote. This exact-text check is intentionally conservative: it may miss clauses exposed only after browser interaction, and those should stay unverified instead of being automatically accepted through an undocumented DOM field.

## 6. Official procurement-policy caveat for MSE/EMD logic

**Government of India, Department of Expenditure (2024), _Manual for Procurement of Goods_.** https://www.doe.gov.in/manuals (official manuals page; select Manual for Procurement of Goods, Second Edition, 2024)

The manual describes central MSE procurement policy and bid-security provisions within a particular legal/purchaser context. It excludes works contracts from the relevant central MSE policy and explains that State governments may have their own procurement policies. This makes a universal “Udyam means EMD exempt” rule unsafe. BidSentry records declared EMD capacity and points users to a clause; it does not automatically grant a statutory exemption based only on Udyam registration. The purchaser, procurement category, current policy, registration scope and exact tender wording must be checked by a responsible human.

## 7. TinyFish integration contract reviewed for this build

Official references checked/rechecked on 22 October 2026:
- Search REST reference: https://docs.tinyfish.ai/api-reference/search-the-web
- Fetch REST reference: https://docs.tinyfish.ai/fetch-api/reference
- Agent REST reference: https://docs.tinyfish.ai/agent-api/reference
- Python SDK listing/API README: https://pypi.org/project/tinyfish/
- Search/Fetch pricing announcement: https://www.tinyfish.ai/blog/search-and-fetch-are-now-free-for-every-agent-everywhere

Implementation-relevant observations: Search and Fetch have REST parameter shapes distinct from the Python SDK; Fetch's conditional validators are single-URL only; conditional revalidation may be unsupported for pages requiring browser rendering; direct PDF URLs do not support CSS selector filters; `ttl: 0` is documented for fresh retrieval; SSE streams may need status polling after disconnect; and some Agent configurations/capture artifacts are gated by account entitlements. The current build uses a conservative baseline rather than assuming beta features are enabled. These integration details must still be verified by a live run using the team's account.

## 8. Generative AI risk guidance

**NIST AI 600-1 (2024), _Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile._** https://doi.org/10.6028/NIST.AI.600-1

NIST discusses confabulation—generated text that can be false or inconsistent—and proposes practices for trustworthy AI risk management. BidSentry applies the principle with provenance, a human review step, deterministic checks for explicit thresholds and a strict “unknown” state when evidence is not available.

## 9. Market/problem context from an official source

**Press Information Bureau, Ministry of Commerce & Industry, 11 August 2026, _GeM Strengthens Participation of MSMEs, Startups, Women Entrepreneurs and SHGs._** https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2297820&lang=2&reg=48

The release reports 1,175,001 MSMEs registered on GeM as of 30 July 2026 and MSME order value of ₹237,235 crore in FY 2025–26. These figures support the scale of the potential user ecosystem; they do **not** prove that suppliers are losing bids or quantify tender-search pain. That need must be validated with vendor interviews and a measured pilot.

## Design consequences

1. Use TinyFish Search to discover current public pages and TinyFish Fetch to retrieve page text; the external source is dynamic, so don't rely on model memory.
2. Store the exact source URL, final URL, check time and page fingerprint.
3. Keep relevance ranking distinct from eligibility. A high text similarity must never override a mandatory disqualifier.
4. Extract only evidence-backed clauses, show quoted source passages and mark unknowns visibly.
5. Compare page snapshots on re-check, but treat a detected text difference as a review signal—not a legal conclusion.
6. Evaluate a future labeled set manually: criterion extraction precision/recall, deadline exactness, source-traceability rate, and time to shortlist. Do not publish invented accuracy numbers.


## 10. Competitive products: category features are not a unique claim

Public product pages reviewed on 22 October 2026 show that Tender247/BidControl247 advertises tender discovery, AI summaries, eligibility/compliance checks, bid/no-bid decisions, corrigendum tracking and bid preparation (https://www.tender247.com/). BidAssist's public app listing advertises tender search/results, tender details, corrigenda and documents (https://play.google.com/store/apps/details?id=com.ofbusiness.cipher). These are vendor-described capabilities, not independently benchmarked outcomes. Therefore BidSentry cannot claim that eligibility checking or amendment tracking is novel by itself. Its differentiation hypothesis is the explicit evidence path (source → quote → independent fetched-text match → declared profile comparison → Unknown/review state → page diff), to be validated against real alternatives using a fixed set of public tenders.

## 11. Current hackathon deadline / requirement check

On 22 October 2026 the current Kritical Hacks Unstop listing shows team size 2–5 and 22 Oct 2026, 11:59 PM IST for registration/submission; it lists mentorship on 28 Oct and finale on 29 Oct. Another listing variant may display different dates, so participants should confirm inside their registered application and with the organizer. The listing requires a PPT covering problem, solution, users/use case, AI/ML approach, TinyFish integration, impact, feasibility and future scope. It explicitly states TinyFish integration must be meaningful and functional—mentioning the API in slides alone is not sufficient.

Source: https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989
