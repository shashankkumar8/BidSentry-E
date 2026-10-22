# BidSentry-E Live TinyFish Verification Status
**Team:** Syntax Squad | **Event:** Kritical Hacks 2026 | **Date:** 22 October 2026

---

## 1. Current Live Integration Status: **PENDING LOCAL USER API KEY**

In compliance with Non-Negotiable Project Boundary #9 and #10:
- **No live API key was embedded, committed, or transmitted in this workspace.**
- **No live run was fabricated or simulated as real.**
- All 68 offline unit, API, stream lifecycle, and adversarial regression tests **PASS** using rigorous mocked provider contracts.
- The live integration path is fully implemented in `app/tinyfish.py` and `app/main.py` according to the official TinyFish REST API and SDK contracts.

---

## 2. Verification Checklist for the Evaluator / User

To perform live end-to-end verification with your own valid TinyFish API key:

### Step 1: Configure Your Key Locally
```powershell
# Copy the template and add your real key
Copy-Item .env.example .env

# Edit .env and set:
# TINYFISH_API_KEY=your_actual_key_here
```

### Step 2: Launch the BidSentry-E Workbench
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open `http://127.0.0.1:8000` in your browser. Verify the status pill in the sidebar turns green: **"TinyFish key configured · live"**.

### Step 3: Run Live Search (Stage 1)
- Enter your query (e.g. `"IT infrastructure support and maintenance"`).
- Click **Search live tenders ↗**.
- Observe real HTTP responses from `https://api.search.tinyfish.ai` discovering public tender notices on `.gov.in` / `.nic.in`.

### Step 4: Run Live Deep Inspection via TinyFish Agent REST SSE (Stages 3 & 4)
- On an official fetched tender result, click **Deep inspect · Agent**.
- Watch the **Execution Observability** panel stream real provider lifecycle events:
  - `STARTED` (with Provider Run ID)
  - `STREAMING_URL` (direct link to TinyFish cloud browser session)
  - `PROGRESS` (real-time browsing progress updates)
  - `COMPLETE` (terminal completion)
- Notice that observed SSE event count is separated from provider-reported billable steps.

### Step 5: Verify QuoteCheck Independent Fetch Gate (Stage 5)
- After the Agent finishes, the backend independently executes `Fetch` against the cited official source URL.
- The UI displays `QUOTE VERIFIED BY FETCH` only when the verbatim normalized text occurs in the separate Fetch result.
- Unverified quotes remain explicitly flagged and cannot trigger a blocker.

### Step 6: Test Persistent Snapshot Recheck (Stage 7)
- Click **Re-check page** on the selected tender.
- On the first call: baseline snapshot is created.
- On the second call: verifies against the stored hash and reports `not_modified` or diff of modified lines and affected topics.

---

## 3. Redacted Provider Error Behavior

When `TINYFISH_API_KEY` is omitted or invalid:
- **Search:** Returns HTTP 503 (`"TinyFish API key is not configured. Add TINYFISH_API_KEY to .env."`).
- **Inspect Stream:** Yields error event `{"type": "error", "message": "TinyFish API key is not configured."}`.
- **Fail-Closed Guarantee:** The application **NEVER** silently falls back to synthetic benchmark data when a live operation fails. Live errors remain visible and actionable.
