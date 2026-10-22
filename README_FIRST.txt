BIDSENTRY-E / SYNTAX SQUAD — TECHNICAL RELEASE

This ZIP is code + tests + technical/submission docs + original user-provided references. It intentionally excludes PPT/PDF presentation decks, deck source scripts and slide montages. Upload the separately delivered PPTX to Unstop as the initial submission.

Start: read 00_START_HERE.md, then SOURCE_PROVENANCE.md, SPEC.md, SSE_STREAM_CONTRACT.md and BUILD_SEQUENCE.md.

Run local checks: pytest -q; python -m compileall -q app engine.py; node --check app/static/app.js; python -m scripts.check_inline_js.

Local test baseline: 48 passed with provider calls mocked. This is not proof of live TinyFish operation. To run live mode, copy .env.example to .env and set your own TINYFISH_API_KEY privately. Never share or commit that key.

Demo fixtures are synthetic. BidSentry-E does not certify eligibility or submit bids automatically.
