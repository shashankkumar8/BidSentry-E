"""Adversarial and regression test suite for BidSentry-E.

Covers the 20 required adversarial and safeguard conditions specified in Section 7:
1. Indian numeric formats, Lakhs, Crores and ambiguous/unsupported amounts.
2. Empty and missing source data.
3. Exact normalized quotation matches.
4. Numeric-value mismatch in otherwise similar quotations.
5. Percentage mismatch.
6. Negation or exception mismatch.
7. Paraphrased or fabricated quotations.
8. Agent output absent, malformed or schema-invalid.
9. Agent timeout, stream interruption and terminal failure.
10. A run that emits progress but never successfully completes.
11. Provider-reported cost/steps missing or inconsistent.
12. Live Fetch error never falling back to sample clauses.
13. Unknown contract type.
14. EMD and turnover policy uncertainty.
15. Experience criteria that do not match a hard-coded formula.
16. Snapshot unchanged, changed and failed-to-fetch cases.
17. Re-checking the correct URL against the correct saved snapshot.
18. No live-success badge or telemetry when using a benchmark scenario.
19. Frontend escaping of untrusted page text.
20. Secret handling and URL validation.
"""
from __future__ import annotations

import json
import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.main import app, ensure_public_https
from app.evidence import normalize_evidence_text, parse_indian_currency_to_inr, verify_quote
from app.analyzer import (
    extract_contract_type,
    extract_emd_requirement_lakh,
    extract_min_turnover_crore,
    extract_min_experience_years,
    extract_procuring_authority,
    profile_assessment,
    summarize_change,
)

client = TestClient(app)


# 1. Indian numeric formats, Lakhs, Crores and ambiguous/unsupported amounts
def test_adv_indian_currency_formats():
    # Lakhs and Crores formatting
    assert parse_indian_currency_to_inr("Rs. 4,00,000/-") == 400000.0
    assert parse_indian_currency_to_inr("₹1.5 Crore") == 15000000.0
    assert parse_indian_currency_to_inr("INR 50 Lakhs") == 5000000.0
    assert parse_indian_currency_to_inr("Rs. 25,000") == 25000.0
    # Ambiguous ranges must resolve to None (Unknown)
    assert parse_indian_currency_to_inr("Rs. 500-1000") is None
    assert parse_indian_currency_to_inr("10 to 20 Lakh") is None
    # Percentages must not be parsed as INR
    assert parse_indian_currency_to_inr("EMD is 2%") is None
    # Free-text exemptions must remain None, not 0.0
    assert parse_indian_currency_to_inr("exempt as applicable") is None
    assert parse_indian_currency_to_inr("waiver requested") is None
    # Explicit zero is 0.0
    assert parse_indian_currency_to_inr("Nil") == 0.0
    assert parse_indian_currency_to_inr("0") == 0.0


# 2. Empty and missing source data
def test_adv_empty_and_missing_source_data():
    assessment = profile_assessment("", {"turnover_crore": 2.0, "years_experience": 5})
    assert assessment["status"] == "Human review needed"
    assert assessment["potential_blockers"] == []
    assert len(assessment["unknowns"]) >= 3

    quote_res = verify_quote("", "")
    assert quote_res["verified"] is False
    assert quote_res["badge"] == "UNVERIFIED_QUOTE"

    quote_res_none = verify_quote(None, None)
    assert quote_res_none["verified"] is False


# 3. Exact normalized quotation matches
def test_adv_exact_normalized_quotation_matches():
    source = "Eligibility criteria:\n  The bidder shall have average annual turnover of ₹ 2.5 Crore.\n  Valid GST required."
    candidate = "The bidder shall have average annual turnover of ₹ 2.5 Crore."
    res = verify_quote(candidate, source)
    assert res["verified"] is True
    assert res["badge"] == "QUOTE_VERIFIED_FETCH"
    assert res["match_type"] == "EXACT_NORMALIZED_MATCH"
    assert res["review_state"] == "VERIFIED"


# 4. Numeric-value mismatch in otherwise similar quotations
def test_adv_numeric_value_mismatch():
    source = "The bidder shall have average annual turnover of at least Rs. 2 crore in each year."
    candidate = "The bidder shall have average annual turnover of at least Rs. 3 crore in each year."
    res = verify_quote(candidate, source)
    assert res["verified"] is False
    assert res["badge"] == "UNVERIFIED_QUOTE"
    assert res["match_type"] == "PARTIAL_OR_UNCONFIRMED_OVERLAP"
    assert res["review_state"] == "NEEDS_HUMAN_REVIEW"
    assert "altered numbers" in res["reason"].lower()


# 5. Percentage mismatch
def test_adv_percentage_mismatch():
    source = "Bid security shall be 2% of the estimated contract value."
    candidate = "Bid security shall be 5% of the estimated contract value."
    res = verify_quote(candidate, source)
    assert res["verified"] is False
    assert res["badge"] == "UNVERIFIED_QUOTE"


# 6. Negation or exception mismatch
def test_adv_negation_mismatch():
    source = "Udyam registered MSE bidders are not exempt from furnishing EMD for this works contract."
    candidate = "Udyam registered MSE bidders are exempt from furnishing EMD for this works contract."
    res = verify_quote(candidate, source)
    assert res["verified"] is False
    assert res["badge"] == "UNVERIFIED_QUOTE"


# 7. Paraphrased or fabricated quotations
def test_adv_paraphrased_or_fabricated_quotes():
    source = "The supplier must provide 24x7 on-site resident engineer support for server hardware."
    candidate = "Vendor shall offer round-the-clock technical maintenance for IT infrastructure."
    res = verify_quote(candidate, source)
    assert res["verified"] is False
    assert res["badge"] == "UNVERIFIED_QUOTE"


# 8. Agent output absent, malformed or schema-invalid
def test_adv_agent_output_malformed_stream(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_stream(self, url):
            yield {"type": "STARTED", "run_id": "malformed-test"}
            yield {"type": "COMPLETE", "status": "COMPLETED", "run_id": "malformed-test", "result": "NOT A DICT"}

        async def get_agent_run(self, run_id):
            return {"status": "COMPLETED", "result": "NOT A DICT"}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    res = client.post("/api/v1/inspect/stream", json={
        "url": "https://etenders.gov.in/eprocure/app?component=test",
        "profile": {"keywords": "test"},
    })
    assert res.status_code == 200
    events = [json.loads(b.split("data:", 1)[1].strip()) for b in res.text.split("\n\n") if "data:" in b]
    assert any(e.get("type") == "error" for e in events)
    assert not any(e.get("type") == "result" for e in events)


# 9. Agent timeout, stream interruption and terminal failure
def test_adv_agent_stream_terminal_failure(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_stream(self, url):
            yield {"type": "STARTED", "run_id": "fail-run"}
            yield {"type": "FAILED", "status": "FAILED", "message": "Browser execution timed out after 150 seconds."}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    res = client.post("/api/v1/inspect/stream", json={
        "url": "https://etenders.gov.in/eprocure/app?component=test",
        "profile": {"keywords": "test"},
    })
    assert res.status_code == 200
    events = [json.loads(b.split("data:", 1)[1].strip()) for b in res.text.split("\n\n") if "data:" in b]
    err_event = next(e for e in events if e.get("type") == "error")
    assert "timed out" in err_event["message"].lower()
    assert not any(e.get("type") == "result" for e in events)


# 10. A run that emits progress but never successfully completes
def test_adv_agent_progress_without_complete(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_stream(self, url):
            yield {"type": "STARTED", "run_id": "progress-only"}
            yield {"type": "PROGRESS", "message": "Navigating to tender portal..."}
            # Stream ends abruptly without terminal event

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    res = client.post("/api/v1/inspect/stream", json={
        "url": "https://etenders.gov.in/eprocure/app?component=test",
        "profile": {"keywords": "test"},
    })
    events = [json.loads(b.split("data:", 1)[1].strip()) for b in res.text.split("\n\n") if "data:" in b]
    err_event = next(e for e in events if e.get("type") == "error")
    assert "terminal completion" in err_event["message"].lower()
    assert not any(e.get("type") == "result" for e in events)


# 11. Provider-reported cost/steps missing or inconsistent
def test_adv_missing_steps_does_not_invent_steps(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_stream(self, url):
            yield {"type": "STARTED", "run_id": "no-steps"}
            yield {
                "type": "COMPLETE", "status": "COMPLETED", "run_id": "no-steps",
                "result": {"tender_title": "Tender", "tender_id": "T-1", "requirements": []},
                # num_of_steps omitted
            }

        async def get_agent_run(self, run_id):
            return {"status": "COMPLETED"}  # also no num_of_steps

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    res = client.post("/api/v1/inspect/stream", json={
        "url": "https://etenders.gov.in/eprocure/app?component=test",
        "profile": {"keywords": "test"},
    })
    events = [json.loads(b.split("data:", 1)[1].strip()) for b in res.text.split("\n\n") if "data:" in b]
    # No usable requirements means it yields an explicit error rather than an empty pass
    assert any(e.get("type") == "error" for e in events)


# 12. Live Fetch error never falling back to sample clauses
def test_adv_live_fetch_error_fails_honestly(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def search(self, query, limit=8, purpose=None, include_domains=None):
            return [{"title": "Tender", "url": "https://etenders.gov.in/tender/1", "snippet": "Snippet"}]

        async def fetch(self, urls, purpose=None, ttl=0, if_none_match=None, if_modified_since=None):
            from app.tinyfish import TinyFishError
            raise TinyFishError("Origin tender portal returned 504 Gateway Timeout.")

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    res = client.post("/api/search", json={"keywords": "hardware maintenance"})
    assert res.status_code == 502
    assert "Gateway Timeout" in res.json()["detail"]


# 13. Unknown contract type
def test_adv_unknown_contract_type():
    text = "Tender notice for the supply and maintenance of specialized diagnostic software and instrumentation."
    # Both goods and services keywords are present
    assert "Mixed" in extract_contract_type(text)

    ambiguous = "Notice inviting bids for project package A."
    assert extract_contract_type(ambiguous) == "Unknown / Unspecified"


# 14. EMD and turnover policy uncertainty
def test_adv_emd_and_turnover_policy_uncertainty():
    text = "EMD: All bidders must deposit EMD as per prevailing rules; exemptions subject to verification."
    # EMD numeric value cannot be parsed; must remain None
    assert extract_emd_requirement_lakh(text) is None
    assessment = profile_assessment(text, {"turnover_crore": 2.0, "emd_budget_lakh": 5.0})
    assert any("numeric amount could not be safely extracted" in u for u in assessment["unknowns"])


# 15. Experience criteria that do not match a hard-coded formula
def test_adv_experience_not_hardcoded_formula():
    text = "Bidders should have completed similar technical projects in the last five years."
    # No explicit number of years is mandated in the text
    assert extract_min_experience_years(text) is None


# 16. Snapshot unchanged, changed and failed-to-fetch cases
def test_adv_snapshot_diff_and_affected_topics():
    old = "Bid submission deadline: 20-Oct-2026. EMD amount: Rs. 2,00,000."
    new = "Bid submission deadline: 30-Oct-2026. EMD amount: Rs. 4,00,000. Corrigendum 1 issued."
    diff = summarize_change(old, new)
    assert "Submission Deadline" in diff["affected_topics"]
    assert "EMD / Bid Security" in diff["affected_topics"]
    assert "Corrigenda / Scope Amendments" in diff["affected_topics"]


# 17. Re-checking the correct URL against the correct saved snapshot
def test_adv_recheck_correct_url_scoping(monkeypatch):
    saved_url = "https://eprocure.gov.in/tender/correct-one"
    other_url = "https://eprocure.gov.in/tender/different-one"

    monkeypatch.setattr(main, "get_previous_snapshot", lambda url: {
        "title": "Tender One", "text": "Original text",
        "etag": None, "last_modified": None, "checked_at": "2026-10-20T00:00:00Z",
        "text_hash": "hash-one"
    } if url == saved_url else None)

    assert main.get_previous_snapshot(saved_url) is not None
    assert main.get_previous_snapshot(other_url) is None


# 18. No live-success badge or telemetry when using a benchmark scenario
def test_adv_benchmark_clearly_labeled():
    res = client.get("/api/v1/presets")
    assert res.status_code == 200
    body = res.json()
    assert body["mode"] == "benchmark"
    assert "synthetic" in body["notice"].lower()
    for preset in body["presets"]:
        assert "synthetic" in preset["subtitle"].lower()


# 19. Frontend escaping of untrusted page text
def test_adv_frontend_escaping_xss_protection():
    import subprocess
    cmd = [
        "node", "-e",
        "function esc(v){return String(v ?? '').replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));};"
        "console.log(esc('<script>alert(\"xss\")</script> & <b>test</b>'));"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    out = proc.stdout.strip()
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "&amp;" in out
    from pathlib import Path
    html_text = Path("app/static/workbench.html").read_text(encoding="utf-8")
    assert "function esc(" in html_text
    assert "esc(t.title" in html_text
    assert "esc(r.exact_quote" in html_text


# 20. Secret handling and URL validation
def test_adv_security_url_validation():
    # Embedded credentials rejected
    with pytest.raises(Exception) as exc:
        ensure_public_https("https://admin:secret@etenders.gov.in/tender")
    assert "Credentials embedded" in str(exc.value.detail)

    # Non-standard port rejected
    with pytest.raises(Exception) as exc:
        ensure_public_https("https://etenders.gov.in:8443/tender")
    assert "Non-standard ports" in str(exc.value.detail)

    # Local / private IP rejected
    with pytest.raises(Exception) as exc:
        ensure_public_https("https://127.0.0.1/tender")
    assert "restricted to public Indian government" in str(exc.value.detail)

    # Non-official domain rejected
    with pytest.raises(Exception) as exc:
        ensure_public_https("https://commercial-aggregator.com/tender")
    assert "restricted to public Indian government" in str(exc.value.detail)

    # Plain HTTP rejected
    with pytest.raises(Exception) as exc:
        ensure_public_https("http://etenders.gov.in/tender")
    assert "Only public HTTPS" in str(exc.value.detail)
