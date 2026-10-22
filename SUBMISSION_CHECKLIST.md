# BidSentry-E — Final Checklist

## Submission
- [ ] Check deadline and application status inside the registered Unstop account; current public listing says 22 Oct 2026, 11:59 PM IST but variants have differed.
- [ ] Team size and category correctly represent the registered team (listing says 2–5 members).
- [ ] Upload `Syntax_Squad_BidSentry_E_Shortlist.pptx` as primary file.
- [ ] Open the preview; check title, Syntax Squad, track, all 6 slides and citations.
- [ ] Description is copied from `FINAL_SUBMISSION_COPY.txt` and within portal limit.
- [ ] Click final Submit and save confirmation.

## Code and demo
- [ ] Install under Python 3.11+.
- [ ] `python engine.py` prints `LOCAL_SYNTHETIC_SMOKE_TEST` and rejects the fabricated quote.
- [ ] `pytest -q` passes.
- [ ] `python -m compileall -q app engine.py` passes.
- [ ] `node --check app/static/app.js` passes.
- [ ] The inline JavaScript in `app/static/workbench.html` passes syntax check.
- [ ] `/api/v1/health` works; secrets never appear in its response.
- [ ] Live Search, Fetch, Agent and Recheck run with the team's own key and known official URL.
- [ ] Agent quote is checked against a separate Fetch snapshot; if not, it stays unverified.
- [ ] Source screenshots show real mode and actual returned source URLs; synthetic scenes are labelled.
- [ ] Public repository/video links are real and accessible before they are pasted into the form.

## Package hygiene
- [ ] No `.env`, key, SQLite database, cache, or `.venv` in ZIP.
- [ ] ZIP extracts into a clean directory and tests still pass.
- [ ] No claim of legal eligibility, zero hallucination, guaranteed accuracy, measured savings, deployed app, paid customers or submitted status without evidence.


## Streaming Agent release gate

- [ ] Workbench inspection calls `POST /api/v1/inspect/stream`.
- [ ] Terminal run status is successful; no assessment is generated from failed/incomplete streams.
- [ ] Provider `num_of_steps` comes from terminal event/run lookup; event count is shown separately.
- [ ] A returned quote is independently checked against a separate Fetch response.
- [ ] See `SSE_STREAM_CONTRACT.md`; local SSE tests use mocked provider responses and do not prove live service behavior.
