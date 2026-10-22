# BidSentry-E — Evidence-Verified Tender X-Ray for Indian MSMEs

**Team:** Syntax Squad  
**Event:** Kritical Hacks 2026 · AI/ML Track (Open Innovation)

BidSentry-E is a decision-support prototype that helps Indian MSMEs pre-screen public tenders. It combines live-web discovery and retrieval with structured Agent inspection, independent quote verification, conservative comparison to supplier-declared facts, and page-text rechecks.

This is a **technical-only source archive**. It intentionally excludes all pitch decks and presentation assets. The primary PPT is delivered separately for Unstop upload.

## Core workflow

1. **Search** — TinyFish Search finds candidate public tender pages.
2. **Fetch** — TinyFish Fetch retrieves available page text and source metadata.
3. **Inspect** — a user-triggered TinyFish Agent REST SSE run extracts candidate requirements in a schema-constrained response.
4. **Verify** — each Agent quote is checked against a separate Fetch response; quote presence is not treated as legal interpretation.
5. **Compare** — a conservative rule-based/TF-IDF pre-screen surfaces possible matches, potential gaps and unknowns. It never certifies eligibility.
6. **Re-check** — a new Fetch is compared to a saved snapshot for the exact checked URL. Linked documents not fetched remain outside that check's scope.

## Run on Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env locally only; set TINYFISH_API_KEY=your_real_key
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`; API docs are at `http://127.0.0.1:8000/docs`. The demo/preset mode is synthetic and is labelled as such. Never paste your API key into chat or commit `.env`.

## Test sequence

```powershell
pytest -q
python -m compileall -q app engine.py
node --check app/static/app.js
python -m scripts.check_inline_js
python engine.py
```

Expected result for the packaged test snapshot: **68 passed** (provider interactions are mocked in local tests; adversarial regression suite included). Tests use mocked provider responses and synthetic examples; they do not prove live authentication or extraction quality on arbitrary tenders.

## Repository contents and evidence

- `app/`: FastAPI routes, frontend, evidence checks, conservative analyzer with Clause Ledger and TinyFish adapter.
- `tests/`: 68 automated unit, API and adversarial regression tests, including provider stream/terminal-state, SSRF/URL validation and fail-closed cases.
- `references/`: original user-provided master build and the four reference documents, retained separately and unchanged.
- `SPEC.md`, `SSE_STREAM_CONTRACT.md`, `BUILD_SEQUENCE.md`: technical behavior and execution sequence.
- `SUBMISSION_GUIDE.md`, `FINAL_SUBMISSION_COPY.txt`, `SUBMISSION_CHECKLIST.md`: submission support.

## Kritical Hacks listing details supplied by the team

- Initial PPT submission deadline shown in the listing: **22 October 2026, 11:59 PM IST**. Verify the active registered application if its status differs.
- Team size shown: **2–5 members**.
- Initial submission: PPT describing problem, solution, target user/use case, AI/ML approach, TinyFish integration, impact, feasibility and future scope. The listing says video demo and GitHub URL are optional in that initial form, but a meaningful and functional TinyFish integration remains mandatory for evaluation.
- Offline building/mentorship round: **28 October 2026, 9:00 AM–7:00 PM IST**, at the listed venue in Delhi.
- Finale: **28 October 2026, 9:00 PM to 29 October 2026, 9:01 PM IST**.

These dates are transcribed from the listing text provided by the team; confirm any last-minute portal update with the registered application or organizers.

## Safety / truthfulness boundary

BidSentry-E is pre-screening support, not procurement/legal advice. Search snippets cannot establish eligibility. Missing supplier facts remain unknown. The source text, complete tender schedule, linked documents, tender-specific exemptions and current procurement rules govern the actual bid decision. No live TinyFish run, GitHub publication, demo-video publication or Unstop submission is claimed by this archive.
