# 2:30-minute demo recording script — BidSentry

**Important:** record the live version only after putting your own TinyFish key in `.env` and successfully running a real Search + Fetch. If live search is not working, do not claim the demo data is live; record a clearly labeled concept walkthrough instead and fix the integration before submission if time permits.

## 0:00–0:15 — The problem
“Small suppliers can find procurement notices, but deciding whether a bid is worth pursuing means checking eligibility, turnover, experience, certificates, deadlines and amendments. BidSentry makes that screening traceable instead of turning it into a black-box chatbot.”

## 0:15–0:40 — Enter the supplier profile
Show the profile form. Use a real, non-sensitive fictional company profile. Do not enter PAN, bank details, or personal credentials.
“Here is a sample IT services supplier. We enter its sector, region, turnover, experience, bid-security capacity and certificates. These are declared profile inputs, not verified documents; the tool does not automatically apply an MSME exemption.”

## 0:40–1:10 — Prove TinyFish is functional
Click **Search live tenders**. Show the actual request completing. Keep the provider status and the result source visible.
“TinyFish Search discovers current public procurement pages. TinyFish Fetch then reads the selected source pages. This is the core live-web layer; if the provider returns no page text, we say so instead of inventing evidence.”

## 1:10–1:45 — The distinctive workflow
Open **Inspect evidence** for the initial deterministic screen. Then click **Deep inspect · Agent** on a fetched official-domain result. Point to the Agent run ID, reported step count, structured clauses, and the second Fetch verification status: `QUOTE VERIFIED` only when the text appears in the separately fetched source; otherwise `UNVERIFIED` and not used alone to trigger a blocker.
“The relevance score only prioritizes what to read. It is not an eligibility probability. The Agent extracts candidate clauses, and a separate Fetch pass checks the quote against source text before that quote can influence a potential-blocker result. Unverified requirements stay unknown. This is a reason for human review, not a legal judgment.”

## 1:45–2:10 — Change watch
Click **Recheck** on a source that has a saved baseline. Show a detected difference or explicitly show “no text difference detected.”
“Change watch fetches the same source again and compares the page text. A difference is a review signal; the vendor still opens the official notice and linked corrigenda.”

## 2:10–2:30 — Impact and close
“GeM reported over 11.75 lakh MSMEs registered by July 2026. BidSentry aims to reduce the time it takes a small supplier to move from a broad search to an evidence-backed shortlist. We will evaluate criterion extraction, deadline accuracy and shortlist time with a manually checked tender set. BidSentry never submits a bid automatically.”

## Recording checklist
- Hide terminal environment variables and never show `.env` contents.
- Ensure TinyFish key is not in the URL, browser devtools, console or shared screen.
- Show at least one actual official source URL.
- Keep a clear live indicator visible.
- If the source can't be fetched, state that limitation; don't substitute synthetic data and call it live.
- End on the public GitHub README or repository home page.
