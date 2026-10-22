# BidSentry — Master Solution Playbook

**Team:** Syntax Squad  
**Event:** Kritical Hacks 2026 · AI/ML Open Innovation  
**Product:** Evidence-first tender screening for Indian MSMEs  
**Document status:** Consolidated build, validation and pitch source of truth · updated 22 October 2026

> **One-sentence promise:** Before an MSME spends hours preparing a government bid, BidSentry helps a reviewer see which tender clauses might matter, what the fetched source actually says, how that evidence compares with the supplier's declared profile, what is still unknown, and whether the page text changed since the last check.

This is a decision-support prototype, not a legal eligibility certificate, tender interpretation service, or bid-submission robot.

---

## 1. The decision: what we are building—and what we are not

### Build

A narrow **evidence-backed tender pre-screening workbench**. It combines TinyFish-powered discovery/retrieval, visible source provenance, constrained extraction, deterministic checks for a small set of explicit criteria, an explicit Agent deep-inspection action, and a saved-page re-check. It prioritizes explaining uncertainty rather than forcing every tender into a simplistic green/red decision.

### Do not build in this sprint

- An all-in-one tender marketplace, complete bid-preparation suite, or replacement for GeM/CPPP/e-procurement portals.
- Automated submission, credential handling for user portal accounts, legal advice, or authoritative eligibility certification.
- Automatic blanket MSE/Udyam exemptions, a universal CPWD/PSU experience rule, or inferred percentage EMD calculations.
- Scheduled monitoring, WhatsApp notifications, OCR of arbitrary scanned attachments, full attachment graphs, or a claimed tamper-proof audit trail unless implemented and tested.
- A purportedly trained Indian-tender machine-learning model. The current relevance ranker is TF-IDF; clause extraction is rule-based; the Agent is a constrained optional extraction aid.

### Why this product direction

BidSentry-E is deliberately scoped to one repeated decision: help an MSME reviewer decide which tender requirements need attention before investing in bid preparation. Visible execution telemetry, deliberate Agent escalation and a source re-check signal make this workflow auditable without expanding it into a full procurement platform.

---

## 2. Hackathon brief decoded into build evidence

The current official Kritical Hacks listing asks the initial submission to cover:

1. Problem statement.
2. Proposed solution.
3. Target user / use case.
4. Role of AI/ML and proposed technical approach.
5. Proposed TinyFish integration.
6. Expected impact.
7. Feasibility.
8. Future scope.

It also says TinyFish integration must be meaningful and functional; naming TinyFish in a slide or README is insufficient. This means there are two distinct gates:

- **PPT shortlisting:** explain the problem, value, method, users, feasibility and roadmap clearly.
- **Build/finale proof:** demonstrate that real TinyFish Search/Fetch/Agent calls complete, show the actual source URLs and text, and show what the code does when evidence is missing or fails.

The current live Unstop listing surfaced on 22 October 2026 shows registration and submission closing at 11:59 PM IST on 22 October, team size 2–5, offline mentorship on 28 October and finale on 29 October. Some other listing variants can display different dates. Confirm the date/status inside the registered application and organizer channel; do not trust an old reminder or cached page.

Source: https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989

### Judge evidence matrix

| Requirement / scoring area | What to show | What not to substitute |
|---|---|---|
| Problem | Specific bidder's pre-bid review moment and a costly uncertainty | Unsupported claims about how many bids are lost |
| Solution | Source → quote → status → profile comparison → next action | A generic AI dashboard or a feature list alone |
| Target user | MSME tender owner, bid desk, or small bid consultancy reviewing a public tender | “Everyone in procurement” |
| AI/ML | TF-IDF relevance ranking + rule-based extraction + optional schema-constrained Agent with evidence checks | Calling the current prototype a trained eligibility model |
| TinyFish | A live Search, Fetch and one real Agent run with the returned URL/text and observable outcomes | A diagram, mocked fixture or API name without a real call |
| Impact | A test plan and measured pilot metrics | Claimed 10x/90%/hours saved without a baseline |
| Feasibility | Current implementation inventory, tests, failure paths, limitations | “100% working” or “production-ready” |
| Future scope | Prioritized roadmap based on missing evidence and observed user needs | A promise to solve every portal workflow |

### Rubric-weighted execution plan from the earlier chat

The scoring breakdown previously shared in this conversation was: GitHub 20, TinyFish integration 20, Social Media 10, Technical Implementation 10, Innovation 20, Impact 10 and Revenue Model 10 (100 total). Treat this as the working scorecard from the provided materials; verify the organizer's current official rules if they differ.

| Weight | Criterion | What would count as convincing evidence | Priority / current gap |
|---:|---|---|---|
| 20 | GitHub quality | Public, installable repo; coherent README/spec; reproducible tests; actual history; no secrets; screenshots/clip accurately labelled | High. Package is ready to publish, but public URL/push is not verified. |
| 20 | TinyFish integration | Live Search + Fetch + one structured Agent run; actual returned URL/text; independent quote check; observed re-check | Highest. Code path exists and mocks pass, but account-backed run is still required. |
| 10 | Social media | Real public post that explains the user problem and links to the real repo/demo; no fake engagement/results | Medium. Draft exists; posting is not performed. |
| 10 | Technical implementation | Readable API boundaries, conservative parsing, Unknown states, error paths and repeatable tests | Good local baseline; live API and arbitrary tender coverage remain unproven. |
| 20 | Innovation | The evidence ledger and conservative uncertainty experience are visible in the demo; differentiation tested rather than asserted | Focus on demonstrating the workflow and honestly acknowledging that competitors already market adjacent functions. |
| 10 | Impact | Pilot design measures extraction quality, traceability, missed criteria and time-to-shortlist against a human baseline | Plan is documented; no impact number is measured yet. |
| 10 | Revenue model | Plausible buyer/price hypothesis and interview/pilot plan; costs based on real provider usage before margin claims | Pricing is a hypothesis, not validated unit economics. |

**Operational implication:** Do not spend the last hours polishing social visuals while the TinyFish path has not been run live. First prove the required API, then publish a safe GitHub repository, then record the demo/post and verify all links. Evidence of implementation beats a broader feature list.

---

## 3. Problem framing: identify the moment, not just the market

### The user and moment

**Primary user:** a small Indian MSME supplier or contractor—or a bid consultant supporting one—who has found a potentially relevant public tender and needs to decide whether to spend additional effort reviewing it.

**Trigger:** the tender title looks relevant, but its requirements are spread across a notice, schedules, attachments, portal tabs and amendments. The reviewer has to compare them to supplier facts such as turnover, completed work, certificates, ability to fund a stated EMD, location and deadline.

**Job to be done:** “Help me identify what I need to verify before deciding whether to invest in this bid, and show me the evidence so I can check your work.”

**Current workarounds to validate:** manual PDF/page review; spreadsheets/checklists; messages between sales, technical and finance staff; tender alerts/aggregators; external bid consultants. This is a hypothesis from workflow analysis—not a completed interview result. No user interview or customer claim is included as fact in this package.

**Possible consequence:** unnecessary document preparation, missed requirements, or money/time committed before a critical condition is understood. The project must not state the size or frequency of these losses until real users or pilot data establish them.

### Market scale: use carefully

A Ministry of Commerce & Industry press release reported 1,175,001 MSMEs registered on GeM as of 30 July 2026 and MSME order value of ₹237,235 crore in FY 2025–26. This supports an observable ecosystem scale. It does **not** establish how many suppliers experience this pain, the amount lost, or how much time BidSentry saves.

Official source: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2297820&lang=1&reg=48

### The central hypothesis

> For a subset of MSME bid reviewers, a source-linked, uncertainty-aware evidence ledger will make it easier to decide what deserves attention than a summary or relevance score alone.

### Falsification plan

Interview 5–8 people who actually review public tenders if the event timeline permits. Ask for a recent example, their present steps, which requirement takes longest to confirm, how they handle amendments and what would make them trust an automated aid. Do not lead with “Would you use this?” Ask them to walk through an actual, non-confidential tender. If users primarily need discovery, annexure drafting or portal data coverage, refine the wedge rather than insist that evidence verification is the main problem.

---

## 4. Competitive landscape and what differentiation can honestly mean

A current desk research pass finds that existing options already cover much of the category:

| Alternative | Publicly described strengths | BidSentry should not claim |
|---|---|---|
| Official Government Services Portal / e-procurement sites | Official tender notices and search/filter access | That official portals are not authoritative sources |
| BidAssist | Tender search, results, document/corrigendum information and alerts | That aggregators only list titles or never track amendments |
| Tender247 / BidControl247 | Tender discovery, AI tender summaries, eligibility/compliance checks, bid/no-bid support, corrigendum tracking and bid preparation | That BidSentry is the first product to perform tender eligibility screening or change tracking |
| Spreadsheets / manual review / bid consultants | Flexible human review and existing expertise | That humans are always less accurate or slower |

Public product pages are marketing statements; feature-level comparisons require hands-on product trials and the same test tenders. Do not present vendor performance claims as independently verified fact.

Sources:
- Government Services Portal: https://services.india.gov.in/
- BidAssist listing: https://play.google.com/store/apps/details?id=com.ofbusiness.cipher
- Tender247: https://www.tender247.com/

### BidSentry's differentiation hypothesis

Not “we have AI eligibility checks” and not “nobody else tracks amendments.” The proposed distinction is **evidence legibility and fail-closed behavior**:

1. Search results are discovery signals, not proof of a clause.
2. A potentially consequential quote is linked to an actual fetched source URL and page snapshot.
3. Agent-extracted quotes are matched against a separate TinyFish Fetch response before receiving a verified status.
4. Missing supplier inputs and unparsed requirements remain Unknown / Review rather than passing or failing silently.
5. Profile comparison logic is explicit and inspectable; relevance score does not masquerade as eligibility probability.
6. Re-check produces a page-text diff and a review signal, not an automatic legal interpretation of a corrigendum.

This is a **product hypothesis to demonstrate and test**, not a proven competitive moat. The next research task is a structured trial against BidAssist and Tender247 using five public tenders, comparing quote traceability, unknown handling, amendment visibility, reviewer comprehension and time-to-shortlist.

---

## 5. Product workflow: one golden path, end to end

### Stage 1 — Describe the supplier

Capture only data needed for pre-screening: keywords/service, sector, location, turnover (if known), years of experience, EMD/bid-security budget, certifications and Udyam registration. Every profile field is user-declared; none is represented as independently verified.

### Stage 2 — Discover current sources with TinyFish Search

Use keywords and intent/purpose to discover public notices. Restrict the first pass to likely official domains. Label source/domain type. Search snippets are not evidence for a blocker. If broader public sources are used for discovery, make that distinction visible and guide the reviewer to the official notice.

### Stage 3 — Fetch the actual page content

Fetch selected sources as readable text/Markdown. Preserve the final URL, title, fetch time, returned status/error, ETag/Last-Modified when available, and text fingerprint. Handle errors explicitly. No hidden switch to a synthetic demo record after a live call fails.

### Stage 4 — Extract clauses and rank review priority

TF-IDF ranks textual similarity against the supplier's stated terms. Simple deterministic patterns attempt to identify explicit turnover, experience, EMD and mandatory certification mentions. The extraction is intentionally limited; unsupported formats, conflicting amounts, vague periods, percentage values and missing pages should remain review-needed/Unknown.

### Stage 5 — Optional deeper inspection with TinyFish Agent

The user explicitly clicks “Deep inspect · Agent” on an allowed official public government/NIC URL. Request schema-constrained requirements and source quote metadata. Use this for a hard-to-read or dynamically rendered page—not automatically for every result. Keep the Agent's proposed clause and its verification status distinct.

### Stage 6 — Independently verify quotes

Re-fetch the proposed source text. Mark a quote verified only if conservative normalized exact text occurs in the independent Fetch result. Do not verify by fuzzy token overlap. A missing/mismatched quote remains Unverified and cannot alone justify a potential blocker. Even an exact quote may be incomplete without context; the human must open the full clause and referenced attachment.

### Stage 7 — Compare facts with the supplier profile

For a small set of explicitly parsed values, compare the extracted requirement with supplier-declared values. Output categories:

- **Potential gap:** an evidence-backed threshold and declared profile value appear inconsistent.
- **Meets extracted threshold:** the declared value appears to meet the parsed numeric condition; this is not eligibility approval.
- **Unknown / missing input:** supplier data or a reliable requirement is absent.
- **Review required:** conflicting, conditional, percentage-based or unverified text needs human interpretation.

Never show “Ready to bid” because no blocker was detected. Preferred positive label: “No potential gap found in the criteria parsed so far — review the full tender and current amendments.”

### Stage 8 — Re-check a source

Keep the previous text snapshot and check time in local SQLite. Re-fetch a page; attempt ETag/Last-Modified validation where supported and fall back as documented when conditional validators are unsupported. Compare old/new page text and list changed lines. A text difference can be boilerplate/layout drift; it may not be a corrigendum. A lack of difference on the reached page does not establish that all attachments/amendments are unchanged.

---

## 6. Evidence model and trust policy

Every claim shown to the user should be classifiable into one of these buckets:

1. **Directly observed:** text from a fetched page, displayed with URL/time.
2. **Quote verified:** the proposed quote was found in an independent Fetch text result for the listed URL.
3. **Derived:** deterministic parsing/comparison was applied to verified or fetched text and a declared profile value.
4. **Unknown / Unverified:** source or requirement could not be confirmed, profile data are missing, or extraction did not fit supported patterns.
5. **Human decision needed:** interpretation depends on an attachment, qualification definition, exception, category, purchaser policy or legal context.

These labels are not formal legal statuses. “Verified” means the text matched a fetched snapshot, **not** that the official tender is authentic in every respect, complete, current across all documents, legally interpreted correctly, or applicable to a particular supplier.

### Non-negotiable safety rules

- No potential blocker from a search snippet alone.
- No numeric comparison if its requirement was not reliably extracted from source text.
- No verified badge merely because an Agent returned structured JSON.
- No treating a user's blank profile field as zero.
- No blanket EMD exemption based only on Udyam.
- No universal similar-work formula hard-coded as law.
- No “No blockers” → “eligible” conversion.
- No fake live records or fake current ETags in a live failure path.
- No hidden API key in frontend or repository.

---

## 7. Architecture as built

```text
Browser UI
   │ supplier profile / explicit actions
   ▼
FastAPI (app/main.py)
   ├── TinyFish Search REST ──► live result URLs
   ├── TinyFish Fetch REST  ──► Markdown/text + metadata
   ├── Analyzer             ──► TF-IDF rank + rules + unknown states
   ├── TinyFish Agent REST SSE ──► streamed structured extraction + provider trace
   │        └── synchronous SDK compatibility endpoint remains available
   │                           │
   │                           └─ independent Fetch quote verification
   └── SQLite snapshots/history ──► recheck + text diff
```

### Components and responsibilities

- `app/main.py`: HTTP endpoints, request models, allowed-domain checks, snapshots, independent Agent quote verification, response assembly.
- `app/tinyfish.py`: Search/Fetch REST wrappers, a direct Agent REST SSE adapter/run-lookup path, and a separate Python SDK compatibility wrapper with normalized errors.
- `app/analyzer.py`: domain/source labels, clause sentence splitting, rule-based extractions, profile assessment, TF-IDF relevance and text diff summary.
- `app/static/`: human-facing dashboard and client-side interaction.
- `tests/`: tests for fixtures/mocks, missing-key behavior, domain checks, evidence verification and conservative extraction.
- `.env.example`: names of configuration variables only; never commit a real `.env` file.
- `.bidsentry.db`: local runtime data; never include in release ZIP/GitHub.

### Current technical boundaries

- TF-IDF is the only explicit machine-learning ranking mechanism in the baseline; it is not a trained tender eligibility classifier.
- Clause matching is rule-based and coverage-limited.
- Agent inspection is user-triggered and the primary workbench path now streams provider SSE events. It does not claim raw Agent DOM corpus access or an automatic cost-aware escalation planner. SSE event count and billable step count remain separate.
- Re-check only covers the URL/page actually fetched; it does not recursively audit every PDF, BOQ, annexure or corrigendum.
- Local tests use mocks; they do not prove external credentials, live source availability or extraction quality on arbitrary tenders.

---

## 8. TinyFish integration design — what counts as meaningful

A strong live demo should produce an actual, inspectable trace for each action.

### Search

- Make one specific search from a tender category and supplier profile.
- Show that the backend returned actual result URLs and names from TinyFish Search.
- Make clear that results are candidates, not authoritative clause evidence.

### Fetch

- Fetch at least one official public tender page using the documented REST endpoint and show the returned final URL, title, readable text and any available validators/fingerprint.
- Preserve per-URL errors. Never call an empty result “success.”
- Use current official documentation because REST fields can differ from Python SDK method signatures.

### Agent

- User explicitly triggers an inspection on a public government/NIC URL.
- Show that the actual Agent SSE call ran and returned a successful terminal result; provider-reported steps come only from terminal/run metadata, not from event count.
- Immediately perform the independent Fetch verification pass. If exact quote matching fails, show Unverified; do not silently downgrade to approximate matching.
- Avoid optional capture/browser streaming configuration unless the account is confirmed to support it.

### Re-check

- Save one baseline snapshot and then re-fetch the same URL.
- Show the changed lines and available ETag/Last-Modified metadata.
- Test `conditional_unsupported` fallback; conditional validators are limited to a single URL and can fail for browser-rendered pages. `ttl: 0` requests a live fetch in the documented REST API.
- Explain that a page text diff is a signal for a human to inspect, not automatically a legally material amendment.

Official refs (reviewed 22 October 2026):
- Search: https://docs.tinyfish.ai/api-reference/search-the-web
- Fetch: https://docs.tinyfish.ai/fetch-api/reference
- Agent REST: https://docs.tinyfish.ai/agent-api/reference
- Python SDK: https://pypi.org/project/tinyfish/

No live account-backed run was performed while preparing this package. Complete and record it before claiming demonstrated live integration.

---

## 9. Procurement-policy boundary: especially EMD and experience

MSE benefits depend on policy scope, purchaser, type of procurement, registration and tender-specific wording. Official MSME public procurement policy material distinguishes goods/services from works contracts, and government procurement manuals describe bid-security treatment within their own contexts. Therefore:

- Udyam registration is not a universal bypass for every EMD, turnover or experience clause.
- Goods, services, works, consultancy and special procurement categories can follow different policy/manual provisions.
- Purchaser-specific and state policies may differ.
- A tender can state requirements or permitted relaxations that need contextual interpretation.
- Percentage-based EMD or values hidden in a linked document should not be guessed using a generic formula.
- The 1×80% / 2×50% / 3×40% similar-work pattern is not a universal rule. Extract a tender's actual statement and require manual validation.

BidSentry's proper role is to surface the clause, expose relevant declared facts, flag a possible mismatch, and ask for review of the governing clause/policy. It should not decide legal exemptions by itself.

References:
- Department of Expenditure procurement manuals: https://doe.gov.in/manuals
- MSME public procurement policy portal: https://my.msme.gov.in/MyMsme/Reg/PPP_Home.aspx

---

## 10. Validation plan: turn a demo into evidence

### Golden set

Build a small manually annotated set of 20–30 public tenders from multiple official portals and different procurement types. For each, record:

- Canonical official URL and date checked.
- Whether source page, PDF, BOQ, ATC/annexure or amendment contains the key condition.
- Exact quote and document/page location.
- Human-labeled criterion type, value, unit, modality, exceptions and whether interpretation is ambiguous.
- Whether BidSentry found it, quoted it accurately, categorized it correctly and produced the right `Unknown` when unsupported.

Do not tune against one public sample and call it a benchmark. Hold back a few documents from development tests.

### Core evaluation metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Source traceability rate | Share of displayed clause claims with a valid source link and inspection location | Can the reviewer audit the claim? |
| Quote exactness | Share of displayed “verified” quotes that match the independent fetched corpus under the documented normalization | Does “verified” mean what the UI says? |
| Criterion extraction precision / recall | Correct extracted clauses over extracted clauses / correct extracted clauses found over all gold clauses | Quantifies misses and false inclusions |
| Deadline exactness | Correct, context-labeled tender deadlines / all deadline outputs | Dates matter and must not be pulled from unrelated notices |
| Unknown correctness | Cases where system abstained when evidence/data were missing or conflicting | Measures healthy uncertainty instead of invented certainty |
| Amendment signal usefulness | Human-confirmed material changes surfaced / signals surfaced; plus missed known amendments | Separates noise from useful change detection |
| Time-to-shortlist | Median time for a user to reach a justified shortlist with/without tool | Tests the actual product outcome |
| Reviewer trust / correction rate | Task survey and number of claims users had to fix | Helps discover UX and reliability gaps |

Report sample size and uncertainty. Never report an accuracy percentage without the labeled set, denominator, sampling method and date.

### Pilot protocol

1. Recruit a handful of bid reviewers and use tenders they are allowed to share.
2. Ask each to complete a shortlist task manually and with BidSentry in counterbalanced order.
3. Compare times, missed criteria, incorrect blocker flags, quality of traceability and confidence calibration.
4. Review every disagreement with a knowledgeable procurement professional.
5. Decide whether to improve extraction, attachment coverage, amendment detection or interaction design based on the observed error distribution.

---

## 11. MVP priority and build order

### P0 — Release gate (must work)

- Clean Windows quick start.
- Server-side TinyFish key only.
- Search and Fetch with real URLs/returned text visible.
- A single official-source clause that is traceable.
- Explicit Agent inspection with independent Fetch verification.
- Unknown/unverified paths visible and safe.
- Snapshot save/recheck and human-readable diff.
- No hidden demo fallback or success state after external failure.
- Tests pass; no secrets or DB in ZIP.

### P1 — Demo polish

- Show a small event/telemetry trace: action, elapsed time, endpoint, result count, status, returned steps if provided, and whether a fetch/quote verification passed. Avoid invented cost or latency.
- Make synthetic examples visually obvious and separate from live mode.
- Add “What we could not inspect” messaging for linked files/page limitations.
- Show source URL, fetched-at timestamp and text fingerprint.
- Improve keyboard behavior, responsive layout and readable empty/error states.

### P2 — Only after observing users

- Attachment/PDF inventory and supported text extraction.
- Tender-family-specific extraction schemas with confidence/abstention thresholds.
- Scheduled re-check and alerts.
- More portals and document-version relationships.
- Evaluation dashboard against an annotated golden set.
- Multi-user accounts and secure profile management only if needed.

---

## 12. 90-second judge demo script

**0–10 seconds — the decision:** “A tender can match a supplier's keywords and still contain a requirement they need to inspect before spending more effort. BidSentry puts the requirement, source quote and missing facts in one evidence ledger.”

**10–25 seconds — live Search/Fetch:** Enter a real category and location. Point at actual returned URLs and the one fetched source. Say “Search finds a candidate; only fetched text can support a clause.”

**25–42 seconds — evidence ledger:** Open a clause. Show its quote, source URL, verification state and profile comparison. Explain what would become Unknown if a number were not declared. Do not claim the user is legally eligible/ineligible.

**42–57 seconds — Agent inspection:** Trigger Deep inspect on an official public page. Show that the API call ran and the quote is independently checked by Fetch. If the API is failing, do not imply a live Agent result; switch explicitly to the labelled synthetic demo and state the limitation.

**57–72 seconds — re-check:** Show a saved baseline and page text diff. Explain that a change triggers human review; it is not automatically classified as a corrigendum.

**72–85 seconds — differentiation:** “Other products already provide tender discovery, eligibility assistance and amendment tracking. Our hypothesis is that making the evidence-to-decision chain inspectable and unknowns explicit improves reviewer trust. We will compare that with existing tools and annotated tenders.”

**85–90 seconds — close:** “BidSentry doesn't replace procurement judgment. It helps make the first review more traceable and less blind.”

### Live failure plan

- If the API key is missing, the Search request should fail honestly; use only the clearly labelled sample path.
- If Search works but Fetch fails, show the error and do not assert evidence-backed analysis.
- If Agent fails, the rest of the product can be demonstrated, but say that Agent integration needs troubleshooting; do not show fabricated step counts as live telemetry.
- If the test tender is dynamic or blocked, choose a pre-smoke-tested public official source, not a fake URL.

---

## 13. Judge Q&A posture

**“Is this just another tender-search app?”**  
Search is only the start. The focus is tracing a possible requirement from fetched source text through independent quote verification and a comparison against declared supplier facts, while preserving unknowns. This difference is a hypothesis we must validate against existing bid-management products—not a claim that competitors lack eligibility features.

**“Where is the AI/ML?”**  
TF-IDF prioritizes textual relevance; deterministic rules extract a small set of explicit criteria; TinyFish Agent can inspect an official page on user request; a separate Fetch check verifies the Agent's quotes. It's a hybrid pipeline, not a trained tender-specific classifier.

**“Does it tell an MSME it qualifies?”**  
No. It says a parsed criterion appears met, may be a potential gap, or is unknown/review-needed. Full documents, exemptions, conditions and the current procurement policy need human review.

**“Why TinyFish?”**  
The core workflow requires current web discovery, readable fetched source content, and goal-driven inspection of difficult official pages. Search/Fetch/Agent are real integration points, and their returned evidence is visible. A live account-backed demo is required to prove it.

**“How do you prevent hallucinations?”**  
We don't claim to eliminate them. Search snippets are not blocker evidence; Agent quotes are independently matched against fetched text; unverified content remains unverified; missing fields become Unknown; rules and scores are separate from eligibility.

**“How do you compare with Tender247?”**  
Tender247 publicly advertises AI eligibility checks, bid/no-bid assistance and corrigendum tracking, so we don't claim those are unique. We propose testing the evidence provenance, conservative abstention and reviewer audit experience head-to-head.

**“What results do you have?”**  
The current candidate suite has 48 tests using unit tests and mocked provider responses. This proves selected local behavior and SSE-handling paths, not live integration accuracy. A live TinyFish smoke test and a manually labeled public-tender evaluation set remain release gates.

**“Can it read every PDF or attachment?”**  
Not yet. It analyzes fetched page text and uses bounded extraction. Linked PDFs, BOQs and annexures can contain critical criteria; unsupported or uninspected documents must remain a clearly disclosed coverage gap.

**“What is the business model?”**  
Small teams might pay for a capped monthly plan; bid consultants may prefer seat- or usage-based pricing. The listed prices are hypotheses to interview and test, not proven willingness to pay or validated unit economics.

**“Why not automate bid submission?”**  
The first product decision is whether to spend effort pursuing the tender. Automatic submissions would create high consequence and security/compliance burdens and are out of scope.

---

## 14. Risk register and mitigations

| Risk | Severity | MVP mitigation | Later work |
|---|---|---|---|
| Missed clause in a linked PDF or dynamic tab | High | Coverage disclaimer; explicit Agent on public page; Unknown when not found | Attachment inventory/extraction, corpus completeness indicators |
| False potential blocker | High | Require fetched source content; strict quote verification for Agent outputs; deterministic comparisons only on extracted values | Manual gold set, thresholds and review workflow |
| Wrong deadline due to unrelated date | High | Context-specific patterns; “Not extracted” on failure | Date parser benchmark with timezone and amendment cases |
| False EMD exemption | High | Do not auto-grant statutory exemption based on Udyam | Versioned policy rules reviewed by procurement experts |
| Stale/cached source page | High | `ttl: 0` on live Fetch paths; show checked time/validators | Source health and amendment coverage model |
| Conditional re-check not supported | Medium | Documented fallback without validators; display full fetch status | Retry/poll policy based on provider guidance |
| Search or Agent API outage | Medium | Honest errors; clearly synthetic demo separate | Retry with bounded backoff and user-visible status |
| API key exposure | High | Server-only environment variable; ignore `.env` and runtime DB | Secret scanning, deployment secret manager |
| Competitors replicate feature | Medium | Focus on evidence UX and measurable trust; validate user need | Build workflow integrations if users demand them |
| Market assumptions wrong | High | User interviews and pilot rather than top-down assumptions | Refine ICP and pricing based on evidence |

---

## 15. Team and execution system inspired by the reference bundle

The four supplied notes repeatedly recommend the same operating principle: **do not ask an LLM to generate a whole project at once**. Make the required evidence and interfaces explicit, build a single vertical slice, and insist on runnable proof.

If Syntax Squad has four people, a low-conflict split is:

- **Product/research/pitch owner:** verify brief/rubric, user assumptions, competitive claims, narrative and judge Q&A.
- **Integration owner:** TinyFish Search/Fetch/Agent, secrets, timeout/error behavior and live smoke test.
- **Analysis/data owner:** clause extraction, profile states, independent quote checks, snapshot diff and test fixtures.
- **UI/demo/release owner:** dashboard, telemetry, visual polish, README, packaging and demo recording.

For a 2–3 person team, combine roles, but one person must own each file/interface and one person owns release QA. The official listing says 2–5 participants; confirm actual registered roster and category. Do not invent people or eligibility.

### Workflow for future changes

1. Read `SPEC.md` before editing code.
2. State the exact file(s), API contract, acceptance test and allowed out-of-scope changes in every coding task.
3. Implement one vertical slice at a time, starting with the riskiest integration path.
4. Run the targeted test, full suite and app manually after every slice.
5. Inspect browser behavior and the HTTP response. A generated file or UI screenshot is not proof that the backend works.
6. Ask a separate critic pass to look for fake data, wrong units, broken error states, unsafe claims, dead buttons and secret leakage.
7. Rebuild the clean package from a fresh tree and verify every promised file exists.

---

## 16. Release checklist

### Product
- [ ] One real Search + Fetch sequence completes with the team's TinyFish key.
- [ ] One explicit Agent inspect succeeds on a public official URL.
- [ ] Agent quote verification is independently performed by Fetch.
- [ ] One mismatch/unknown path is visible and cannot auto-create a blocker.
- [ ] One page is re-fetched and its diff is inspected.
- [ ] UI visibly separates sample mode and live mode.

### Engineering
- [ ] `python -m pytest -q` passes.
- [ ] `python -m compileall -q app tests` passes.
- [ ] `node --check app/static/app.js` passes.
- [ ] A fresh environment installs requirements successfully.
- [ ] `.env`, `.bidsentry.db`, virtual environment, cache, private profile data and credentials are excluded from releases.

### Submission
- [ ] Team/category/track match the registered Unstop entry; roster satisfies the stated 2–5 requirement.
- [ ] Submit PPT before spending time on optional video or social assets.
- [ ] Confirm the live deadline in the registered portal/organizer channel due to listing variants.
- [ ] Public GitHub/demo/social links, when required for the next round, are real and accessible.
- [ ] Save proof of submission.

---

## 17. Research references

- Kritical Hacks 2026 official listing / required PPT and TinyFish integration: https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989
- GeM/PIB market context (11 Aug 2026): https://www.pib.gov.in/PressReleasePage.aspx?PRID=2297820&lang=1&reg=48
- Tender247 / BidControl247 product pages: https://www.tender247.com/ and https://bidcontrol.tender247.com/
- BidAssist Android listing: https://play.google.com/store/apps/details?id=com.ofbusiness.cipher
- TinyFish Search API: https://docs.tinyfish.ai/api-reference/search-the-web
- TinyFish Fetch API: https://docs.tinyfish.ai/fetch-api/reference
- TinyFish Agent API: https://docs.tinyfish.ai/agent-api/reference
- TinyFish Python SDK: https://pypi.org/project/tinyfish/
- Abuelsaad et al. (2024), Agent-E, arXiv:2407.13032: https://arxiv.org/abs/2407.13032
- Gao, Yen & Chen (2023), ALCE, EMNLP: https://aclanthology.org/2023.emnlp-main.398/
- NIST AI 600-1 GenAI Risk Profile: https://doi.org/10.6028/NIST.AI.600-1
- Department of Expenditure procurement manuals: https://doe.gov.in/manuals
- Public Procurement Policy for MSEs: https://my.msme.gov.in/MyMsme/Reg/PPP_Home.aspx

**Bottom line:** a trustworthy, narrowly scoped demo with genuine live retrieval, visible evidence and clear Unknown states is stronger than a more ambitious pitch whose claims cannot be demonstrated. No hackathon process can guarantee selection or winning; the goal is to make the problem, proof and limitations unusually easy to inspect.
