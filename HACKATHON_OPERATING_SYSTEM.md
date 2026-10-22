# Syntax Squad — Repeatable Hackathon Operating System

This playbook synthesizes the four user-supplied Exact Copies notes with the practical lessons from BidSentry. It is a disciplined method, not a guarantee of selection.

## Phase 1 — Decode the rules before ideation

Create a one-page brief that lists: track/category eligibility, allowed team size, deadline/time zone, mandatory APIs, deliverables, judging weights, disallowed claims, demo requirements, public URL requirements and submission mechanism. Link every item to the official rule or mark it unverified. Resolve ambiguous dates with the registered portal/organizer.

**Output:** `BRIEF.md` + judge evidence matrix.

## Phase 2 — Define the real user moment

Name one primary user and a specific trigger moment. Write the present workaround, cost/risk, constraints and assumptions. Seek first-hand evidence: a short user walkthrough, prior workflow, public forum/product review or official data. Do not inflate market scale into proof of pain.

**Output:** one-sentence problem and 2–3 testable hypotheses.

## Phase 3 — Map competitors and reject clichés

Search products, papers, repositories, official portals and previous winners. Build a matrix of real capabilities and sources. Never assume “no competitor does X” based on a short search. Ask separate LLM critiques to enumerate generic solution patterns, failure cases, and reasons an experienced user might reject the proposed idea. The team—not the model—makes the final choice.

**Output:** competitor matrix, non-goals and clear differentiation hypothesis.

## Phase 4 — Score hypotheses with explicit weights

Use a provisional 100-point score, adjusted to the event rubric:

- Rubric fit: 25
- Evidence of user/problem: 20
- Differentiation: 20
- Feasibility within time: 15
- Demo clarity: 10
- Required API readiness: 10

Score at least three meaningfully different ideas, not three variations of the same dashboard. Record unknowns and how to falsify the top idea. Scores are team estimates, not predicted judge scores.

## Phase 5 — Lock `SPEC.md`

Freeze product promise, primary workflow, architecture, stack, API request/response contracts, data model, no-go claims, folder structure, acceptance tests and release gate. Let LLMs challenge the spec but do not let implementation improvise silently.

## Phase 6 — Test the riskiest dependency first

Build a small standalone script for the required external API, data source, model, hardware or auth flow before decorating the interface. Verify actual responses, permissions, rate limits, error shapes and version differences. If it fails, cut scope or change approach early.

## Phase 7 — Build vertical slices, one at a time

Each slice must include input → processing → stored/returned result → visible UI → failure handling → automated test. Avoid fake buttons and placeholder outputs. Maintain clean separation between test fixtures and live data. Make the hardest core path work before login/settings/analytics.

Suggested AI IDE prompt structure:

> Read `SPEC.md`, relevant source files and tests before modifying anything. Implement only [one slice]. Do not change unrelated interfaces. Use actual provider API shapes; do not invent fields, prices, credentials or successes. Add tests for success, empty, timeout, error and missing data. Run the tests and syntax checks, report exact commands/output, and list unresolved issues. Do not mark the work complete if a test is skipped or the provider call is mocked.

## Phase 8 — Instrument the demo honestly

Show real elapsed time, source URL, result count, status, error, steps and output provenance where available. Keep a visible distinction between real runs, mocks, fixtures and static illustrations. A nice screen without working controls is not a prototype.

## Phase 9 — Attack the product before judges do

Use a red-team checklist: bad input, missing value, source not found, empty extraction, contradiction, units, negation, stale page, unsupported API kwargs, permissions, network timeout, malicious/irrelevant page text, broken URL, secret leakage, fake success and screenshot overclaiming. Run on a fresh install. Capture test artifacts.

## Phase 10 — Pitch, submit, learn

Pitch in this order: human problem → immediate demo → technical evidence → measurable impact hypothesis → limitation and next test. Cut jargon unless it explains a real design decision. Submit required assets first; optional video/social polish comes after. Verify receipt. After results, log judges' questions, product failures, what the team assumed incorrectly and the next single improvement.

## Team coordination

Assign one named owner per file/workstream. Freeze cross-team JSON contracts early. Commit small changes; pull/test before merging. One release owner checks the clean build and final submission. If team size is 2–3, combine responsibilities but retain explicit ownership. Never invent team members, results or links.
