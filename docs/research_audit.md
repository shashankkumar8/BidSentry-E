# Research Audit — Source Bundle, Project History and External Evidence

**Reviewed:** 22 October 2026  
**Purpose:** separate source-derived workflow advice from independently verified facts and project-specific claims.

## 1. Themes across the four supplied exact-copy notes

The reference bundle repeats a consistent build discipline rather than a specific tender product design:

1. **Decode the actual rubric first.** Translate every stated criterion into evidence a judge can observe.
2. **Find a specific workflow bottleneck.** Avoid building the first common idea produced by an LLM; examine users, workarounds, constraints and competitors.
3. **Use LLMs as critics.** Ask them to list clichés, identify failure modes, challenge assumptions and compare distinct options rather than blindly choose the first suggestion.
4. **Lock a written specification.** Agree on architecture, data/API contracts, folder ownership, acceptance criteria and non-goals before asking an IDE to produce code.
5. **Build the riskiest part first.** Validate the technically uncertain integration before spending time on decorative screens.
6. **Build one vertical slice.** One end-to-end flow with source input, processing, result, error state and visible telemetry beats a wide collection of disconnected features.
7. **Show what actually ran.** Real API status, returned URLs, result count, durations and evidence are stronger than claimed capability; mocks must be labelled.
8. **Test adversarially.** Audit fake buttons, placeholder methods, hidden hard-coded outputs, unsupported claims, unit mistakes, missing edge cases and key leakage.
9. **Rehearse the demo and package the release.** A clean README, exact run commands, public links if required and proof of submission are part of execution.
10. **Review the result after the event.** Keep evidence, judge feedback and build failures as learning material for the next project.

These principles originate in the user-supplied notes. They are useful operational heuristics, not research proving that a given process wins competitions.

## 2. Claims in the notes that must not be repeated as facts

The notes include sweeping statements such as “90% of teams,” exact judge attention spans, exact AI code/token output ceilings, generic average winner traits or claims that a certain slide is the “#1” factor. These should be read as emphatic coaching, not independently supported statistics. This package does not reuse those numbers as research claims.

## 3. Project-history synthesis

The final product scope is tender-specific because it has a clear target user and a testable workflow. The architecture choices below are grounded in this workflow and the event’s TinyFish requirement:

- visible execution telemetry;
- controlled, explicit Agent escalation rather than running an agent on every result;
- source re-check/change observation;
- cost awareness without invented unit-economics claims.

Ideas intentionally excluded:

- broad cybersecurity/vendor-threat monitoring;
- claims of a raw Agent DOM/evidence corpus unless available and verified;
- an SSE live browser stream in the current SDK-based implementation;
- automatic legal exemptions or universal procurement formulas;
- “zero hallucination,” guaranteed qualification, zero false blockers or “ready to bid” claims;
- any claim that a demo, GitHub push, social post or Unstop submission was completed unless it actually was.

## 4. Official event requirements

The current official listing says initial submissions are a PPT and lists the following content: problem, solution, target user/use case, AI/ML or technical approach, TinyFish integration, expected impact, feasibility and future scope. It states meaningful and functional TinyFish use is mandatory and a mere mention is insufficient. The listing currently shows 22 Oct 2026 at 11:59 PM IST and a 2–5-member team; date variants have been observed, so check the registered application/organizer rather than relying on an earlier snapshot.

Source: https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989

## 5. Market context

A Ministry of Commerce & Industry/PIB release dated 11 August 2026 reports 1,175,001 MSMEs registered on GeM as of 30 July 2026 and ₹237,235 crore in MSME order value for FY 2025–26. This demonstrates ecosystem scale. It does not prove the size/frequency of pre-bid screening pain or the product's impact.

Source: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2297820&lang=1&reg=48

## 6. Competitor audit (public pages, not product benchmarking)

- **Official portals / government service portal:** authoritative sources and tender listings.
- **BidAssist:** publicly describes tender search/results, details, corrigenda and documents. Source: https://play.google.com/store/apps/details?id=com.ofbusiness.cipher
- **Tender247 / BidControl247:** publicly advertises discovery, AI summaries, eligibility/compliance checks, bid/no-bid support, amendment tracking, bid documents and workflows. Source: https://www.tender247.com/

Conclusion: tender eligibility and amendment tracking are already advertised by competitors. The project cannot claim these general features as unique. BidSentry's testable positioning is the evidence legibility and conservative abstention workflow: source URL and fetched quote, separate quote verification, declared profile comparison, Unknown state, and page text diff. Whether that is better for buyers is unproven until benchmarked through product trials.

## 7. Technical/research references and implications

### TinyFish official docs

- Search API: https://docs.tinyfish.ai/api-reference/search-the-web
- Fetch API: https://docs.tinyfish.ai/fetch-api/reference
- Agent REST API: https://docs.tinyfish.ai/agent-api/reference
- Python SDK: https://pypi.org/project/tinyfish/

Practical rules: REST and SDK payloads/signatures differ; Fetch conditional validators are limited to single-URL requests and can be unsupported for pages requiring browser rendering; `ttl: 0` is the documented live-fetch path; some optional Agent capture settings may depend on account entitlements. The actual integration needs a live smoke test with Syntax Squad's own key.

### Agent-E

Abuelsaad et al. (2024), “Agent-E: From Autonomous Web Navigation to Foundational Design Principles in Agentic Systems,” arXiv:2407.13032. https://arxiv.org/abs/2407.13032

It motivates hierarchical web-agent design, observation distillation and change observation. It is not a TinyFish paper, and BidSentry does not implement Agent-E or inherit its benchmark performance.

### Evidence and citation evaluation

Gao, Yen & Chen (2023), ALCE, EMNLP. https://aclanthology.org/2023.emnlp-main.398/

It formalizes evaluation of answer/citation correctness and support. Product implication: a cited URL existing is not sufficient; test whether a specific quote actually occurs in a retrieved corpus.

### GenAI risk

NIST AI 600-1 GenAI Risk Profile: https://doi.org/10.6028/NIST.AI.600-1

It identifies confabulation and other GenAI risks. Product implication: provenance, uncertainty, testing, human review and well-defined failure paths matter more than claiming that hallucinations are eliminated.

### Procurement policy

- Department of Expenditure procurement manuals: https://doe.gov.in/manuals
- MSME public procurement policy: https://my.msme.gov.in/MyMsme/Reg/PPP_Home.aspx

The policy context distinguishes categories and purchaser contexts. Never apply a universal EMD exemption, works-contract rule or experience formula without the current tender and applicable policy. This prototype is not a legal rule engine.

## 8. What remains unknown

- Whether real bid reviewers consider source-match verification the most valuable differentiator.
- Extraction precision/recall on a labeled corpus of Indian tenders.
- Coverage of dynamic tabs, attachment PDFs, BOQs and corrigenda.
- Live TinyFish account success, latency and actual cost in the competition network.
- User time saved, error reduction, willingness to pay and repeat usage.

These are validation tasks, not gaps to fill with invented data.
