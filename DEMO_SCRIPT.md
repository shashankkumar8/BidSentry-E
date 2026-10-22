# BidSentry-E — 90-second demo script (no fake-live narrative)

## Before recording

- Start the app with `.env` configured and confirm `/api/v1/health` reports TinyFish configured.
- Use a public official tender URL that has already succeeded in a live smoke test. Don't use a fabricated URL or a tender whose document you haven't checked.
- Close terminals or tabs showing API keys. Verify browser console and server output contain no secrets.
- If the live run fails, do not record a synthetic preset as a live result. Use the labelled synthetic UI to demonstrate the UI flow, and state that the provider step remains unverified.

## Timing

**0:00–0:12 — the problem**  
“BidSentry-E is a pre-screening workbench for Indian MSME suppliers. A tender search result doesn't tell a supplier which requirements need proof, whether their own facts are missing, or which page changed.”

**0:12–0:28 — source discovery**  
Run a live search. Point to the source URL and domain. Explain that snippets are discovery metadata only; assessment requires readable fetched official source text.

**0:28–0:47 — inspect & verify**  
Open an official source and launch Agent inspection. Show the returned requirement and the separate Fetch quote-check state. Explain that exact quote presence is not legal interpretation and the clause context still needs human review.

**0:47–1:02 — uncertainty and comparison**  
Open one status. Show a declared supplier field versus a missing field. Explain why missing facts remain Unknown and why a potential blocker is a review signal, not a disqualification verdict.

**1:02–1:15 — re-check**  
Recheck the exact same official source URL. Show the saved snapshot timestamp/ETag where available and the returned page-text diff. State that unlinked PDFs/corrigenda require separate URL checks.

**1:15–1:30 — proof boundary**  
“The local test suite covers negative quote checks, unknown fields, route behavior and recheck failures. The live calls shown here are from this run; our next research step is a labelled tender benchmark and reviewer pilot. BidSentry supports the decision—it doesn't certify eligibility.”
