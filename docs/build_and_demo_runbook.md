# Build & Live Demo Runbook

**Windows PowerShell · Python 3.11+ · Team Syntax Squad**

## A. Start from a clean folder

1. Extract `Syntax_Squad_BidSentry_DeepDive_Final_Submission.zip` or the source-only ZIP to a new folder.
2. Open PowerShell in the project root, where `requirements.txt` lives.
3. Create an isolated environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Add a local key file; never give the key to an AI model or check it into source control:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set `TINYFISH_API_KEY=...` in `.env`. Use your own account and current provider terms. No `.env` file belongs in the public ZIP/repository.

## B. Verify the local baseline

```powershell
python -m pytest -q
python -m compileall -q app tests
node --check app/static/app.js
```

Expected prepared-environment result: **48 tests passed**. Tests include mocked API paths; a passing suite is not live TinyFish proof.

## C. Start the app

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

- Use **Explore sample** to demonstrate the UI only. Label it synthetic.
- Use **Search live tenders** to demonstrate real Search + Fetch.
- From a fetched official public government/NIC page, click **Deep inspect · Agent**.
- Run **Recheck** once a baseline snapshot exists.

## D. Live-smoke-test checklist

- [ ] `/api/health` shows `tinyfish_configured: true` without exposing the key.
- [ ] Search returns result URLs from the live API.
- [ ] Fetch returns actual text/metadata from at least one official source; preserve any error status.
- [ ] The interface shows the URL and fetched evidence; it does not silently substitute a sample after failure.
- [ ] Agent inspect runs from the explicit action and returns a structured result.
- [ ] The second Fetch response is the corpus used for quote verification.
- [ ] At least one quote is verified or visibly unverified; the badge is truthful.
- [ ] A missing profile field shows Unknown / not provided, not zero.
- [ ] Recheck compares against the saved page snapshot and returns a diff/status.
- [ ] No API key appears in terminal captures, screenshots, Git, or logs.

If a check fails, record the actual message and time. Do not silently switch to demo data and describe it as live.

## E. Suggested 90-second demo

1. **10 sec:** Tell the problem story; no unsupported time-loss stats.
2. **15 sec:** Run a specific live Search query and point to a returned URL.
3. **17 sec:** Show the fetched clause excerpt, source URL and profile comparison.
4. **15 sec:** Trigger Agent inspection and show separate Fetch quote verification.
5. **15 sec:** Show an Unknown/unverified path or missing profile field.
6. **15 sec:** Recheck a saved source, explain the page diff and what it does not cover.
7. **3 sec:** State the limitation: support, not eligibility certification.

## F. Live failure fallback

- Missing/invalid key: use clearly labelled demo mode and say live service could not be shown.
- Search returns no results: change query/sector, not the data source identity. Never invent a public tender.
- Fetch returns no readable text: show the error and keep criterion status Unknown.
- Agent fails: describe Agent as unverified for that run; do not display fake step counts.
- No snapshot exists: first create a baseline, then run Recheck.

## G. Release/security hygiene

Do not upload `.env`, `.bidsentry.db`, private supplier profiles, `.venv`, cache folders or temporary render assets. Use `.gitignore`; run a secret scan before making a repository public. Verify ZIP integrity after export and test from an extracted copy, not the development directory.
