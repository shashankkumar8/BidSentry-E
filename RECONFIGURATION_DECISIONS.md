# BidSentry-E — Implementation Decisions

This document records the technical decisions for this single project workstream. The original user-provided inputs are preserved unchanged under `references/`; active code in `app/` is the implementation to run and test.

## Product boundary

BidSentry-E helps a reviewer pre-screen an Indian public tender. It does not determine legal eligibility, submit bids, grant statutory exemptions, or claim complete monitoring of all linked tender documents.

## Accepted engineering rules

1. **Independent quote verification:** structured Agent quotes are matched against a separate TinyFish Fetch result using normalized exact substring matching. Fuzzy token recall is not used for the consequential verification path.
2. **Unknown is a first-class result:** missing supplier inputs, missing source content or missing quote verification do not become automatic failures or eligibility claims.
3. **REST and SDK contracts stay separate:** Search/Fetch/Agent SSE use documented REST adapters; the synchronous Python SDK path is explicitly separate and pinned in `requirements.txt`.
4. **Steps are not SSE events:** observed event count is telemetry only. Cost estimation uses provider-reported `num_of_steps` when present and labels the amount as an estimate.
5. **Fingerprint terminology:** SHA-256 is a content fingerprint/checksum, not a signature or proof that data was not modified by an attacker.
6. **Re-check scope is one URL:** the system compares the exact fetched page/snapshot. External or unlinked documents require independent checks.
7. **Live failures stay visible:** API errors, failed/incomplete Agent runs and empty extraction do not silently fall back to a synthetic success. Demo fixtures are clearly labelled synthetic.
8. **Read-only inspection:** the Agent goal explicitly prohibits submitting forms, uploading files, registering, paying, or changing site state.
9. **Official-source boundary:** third-party snippets/mirrors can assist discovery but do not establish a blocker. Inspection/recheck paths restrict sources to HTTPS Indian government/NIC domains.
10. **No hardcoded legal blanket rules:** tender-specific criteria, exemptions and similar-work requirements require manual review against the complete tender schedule and current rules.

## Deliberate limitations

- Heuristic extraction can miss table layouts, scanned PDFs, reverse-order monetary values, percentage-based EMD clauses, exceptions and cross-references.
- A quote match proves text occurrence, not that the Agent extracted every requirement or interpreted it correctly.
- An unchanged page does not prove all attachments/corrigenda are unchanged.
- Local provider tests are mocked. A team-owned API key and live provider run are required to verify integration.
