# BidSentry-E — Research notes and source register

Research checked 22 October 2026. These links substantiate event/API/context statements. Product pain and our differentiation remain hypotheses until validated with users.

## 1. Competition requirements

- **Unstop — Kritical Hacks 2026:** https://unstop.com/o/1760989
- **API-backed listing:** https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989

The current listing states team size 2–5, an initial PPT explaining the problem, solution, target user/use case, AI/ML technical approach, TinyFish integration, expected impact, feasibility and future scope. It says meaningful TinyFish integration is mandatory and must be demonstrable during evaluation. The current public listing shows 22 Oct 2026, 11:59 PM IST; due to different historical listing variants, the registered application is the final time reference.

## 2. TinyFish contracts

- **Official cookbook and Search/Fetch/Agent examples:** https://github.com/tinyfish-io/tinyfish-cookbook
- **Use TinyFish skill:** https://github.com/tinyfish-io/tinyfish-cookbook/blob/main/skills/use-tinyfish/SKILL.md
- **Python SDK v0.9.0:** https://pypi.org/project/tinyfish/0.9.0/
- **Current package landing page:** https://pypi.org/project/tinyfish/
- **Fetch integration guidance for conditional requests:** https://github.com/tinyfish-io/tinyfish-web-agent-integrations/blob/main/claude/skills/fetch/SKILL.md

Use Search for discovering URLs, Fetch for readable content at URLs and Agent for interactive pages. Don't mix fields supported by one REST endpoint with SDK method kwargs. The application pins `tinyfish==0.9.0` for reproducible compatibility with its adapter; changing SDK versions requires re-reading the versioned docs and rerunning adapter tests. The UI uses a direct Agent REST SSE stream for the primary inspection path; a separate synchronous SDK path remains for compatibility. Agent `num_of_steps` is read only from terminal/provider run metadata, never inferred from SSE event count. Any per-step cost calculation is a configured estimate, not an account invoice.

The fetch guidance describes conditional validators as single-URL behavior and notes that unsupported conditional requests may need a live fetch retry. BidSentry sends validators only when one URL is being fetched and retries `conditional_unsupported` with `ttl=0` without the validator.

## 3. Public procurement context

- **PIB / Ministry of Commerce & Industry — GeM strengthens participation of MSMEs, startups, women entrepreneurs and SHGs**, published 11 Aug 2026, Release ID 2297820: https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2297820&lang=2&reg=48

The release reports 1,175,001 MSMEs registered on GeM as of 30 July 2026 and ₹237,235 crore in MSME order value in FY 2025–26. These figures show ecosystem scale only. They do not establish the frequency of missed clauses, hours spent reviewing or BidSentry's potential benefit.

- **Department of Expenditure — General Financial Rules page:** https://doe.gov.in/en/orders-circulars/31

The page lists a biannual compilation/update of GFR 2017 through 31 January 2026. Rule interpretation must use the appropriate current source, procurement category, purchaser terms and exact tender. BidSentry deliberately does not make universal statutory exemption claims.

## 4. Competitive context / positioning

- **Tender247:** https://www.tender247.com/

Public product material describes tender search, AI-style summaries/eligibility support and corrigendum-like workflows. That is enough to establish that these broad feature classes are not unique; it does not prove exact performance. BidSentry's evidence-ledger workflow is a differentiation hypothesis to test with a real competitive comparison, not a proven moat.

## 5. Research gaps to close after submission

1. Interview MSME bid coordinators/advisers to determine current review process, costly failure modes and the actual decision point.
2. Run a competitive task study against two current products using the same tender documents and supplier profile.
3. Build a labelled benchmark of 25–50 tender notices plus linked schedules/corrigenda, dual-annotated for source/quote/threshold/exception.
4. Report exact-match quote precision/recall, source coverage, false blocker rate, missed clause rate, recheck change detection on the tested URL, and human review time. Label dataset and limitations.
5. Measure TinyFish API calls, provider-reported steps, observed latency and account costs. Do not extrapolate to margins until usage and willingness-to-pay are tested.

## 6. Citation and version notes

Web content can change; recheck live event dates, SDK versions, API contracts, pricing and procurement orders immediately before presenting. A URL in this note is not evidence that BidSentry was itself run against that URL.
