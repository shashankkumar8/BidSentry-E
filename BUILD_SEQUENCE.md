# BidSentry-E — Build Sequence (follow in order)

## Sequence map

| Seq | Goal | Gate to pass before continuing |
|---|---|---|
| 00 | Decode the event/rubric and lock the product promise | This scope and all eight pitch sections are clear |
| 01 | Install runtime and dependencies | App starts, tests import |
| 02 | Verify deterministic evidence core | CLI output labels synthetic mode and rejects fabricated quote |
| 03 | Verify local web workbench | Root page, API health, presets and audit-history route work |
| 04 | Run the local test gates | pytest + compile + JS syntax pass |
| 05 | Configure live TinyFish | Key remains in local `.env`; health indicates configured |
| 06 | Run live Search → Fetch | Real URLs and readable text are returned; no synthetic substitution |
| 07 | Run live Agent REST SSE → terminal status/step check → independent Fetch QuoteCheck | Provider events are visible; only terminal/provider-run `num_of_steps` is used; at least one Agent quote is independently checked |
| 08 | Run live recheck | A source snapshot is saved; a second fetch reports a scope-limited diff or not-modified status |
| 09 | Capture proof | Record screenshots / screen recording that show actual provider responses and source URLs |
| 10 | Package and submit | Upload the separately delivered PPTX; use this technical ZIP only where source is requested; save actual confirmation |

## 1. Install (Windows PowerShell)

```powershell
cd path\to\BidSentry-E
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If Python 3.11 is not installed, install it before proceeding. The pinned TinyFish SDK used here targets Python 3.11+.

## 2. Local validation (offline — no API key needed)

```powershell
python engine.py
pytest -q
python -m compileall -q app engine.py
node --check app/static/app.js
python -m scripts.check_inline_js
```

The inline script in `app/static/workbench.html` is also checked with `python -m scripts.check_inline_js`. Local tests mock provider responses; they do not count as proof of live API behavior.

Expected CLI marker: `LOCAL_SYNTHETIC_SMOKE_TEST`. The fabricated quote should be rejected. The parser should treat vague `exempt as applicable` as unknown, not zero.

## 3. Launch the workbench

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Check the UI and API docs at `http://127.0.0.1:8000/docs`. Stop with Ctrl+C.

## 4. Configure TinyFish privately

```powershell
Copy-Item .env.example .env
notepad .env
```

Place your own `TINYFISH_API_KEY` value in `.env`. Never paste the key into chat, source code, UI screenshots, or a public repository. Restart the server after changing `.env`. `/api/v1/health` must show `tinyfish_configured: true` but must never return the key itself.

## 5. Live vertical slice

1. In the UI, use a narrowly scoped profile/keyword query.
2. Click live Search; confirm response mode says live and inspect source URL/domain and Fetch status.
3. Pick one official `.gov.in` / `.nic.in` tender page and click **Deep inspect · Agent**. The UI should use `POST /api/v1/inspect/stream` and visibly receive provider events; the old synchronous SDK route remains as a compatibility fallback API only.
4. Confirm the trace shows real provider event types such as STARTED / STREAMING_URL / PROGRESS / COMPLETE as the provider actually emits them. The UI’s observed SSE event count is not a billable step count.
5. Open each candidate clause. Confirm source URL and separate Fetch verification status. If a quote was not returned by independent Fetch, it must stay unverified.
6. Run Re-check on the exact same page URL twice. Inspect saved snapshot time, ETag when available, and text differences.
7. If any step fails, keep the real error, save the status and fix it. Do not narrate a mock preset as a live run.

## 6. Evidence capture

Capture one screenshot each of (a) live Search result and official source URL, (b) Agent extraction + independent Fetch quote status, (c) exact URL recheck diff, and (d) API execution/audit metadata. Redact credentials, personal supplier facts and any sensitive browser context.

## 7. Final package gate

```powershell
pytest -q
python -m compileall -q app engine.py
node --check app/static/app.js
python -m scripts.check_inline_js
```

Then verify the technical ZIP from a clean extraction; it contains no deck assets and must have no `.env`, API key, runtime database, cache or `.venv`. Upload the pitch PPTX separately.
