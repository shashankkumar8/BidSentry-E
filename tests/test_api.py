from fastapi.testclient import TestClient
import app.main as main
from app.main import app

client = TestClient(app)


def test_health_works_without_api_key():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_demo_is_clearly_marked_synthetic():
    response = client.get("/api/demo")
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "demo"
    assert "synthetic" in payload["notice"].lower()
    assert len(payload["tenders"]) >= 1


def test_live_search_fails_honestly_without_key(monkeypatch):
    monkeypatch.delenv("TINYFISH_API_KEY", raising=False)
    response = client.post("/api/search", json={"keywords": "network maintenance"})
    assert response.status_code == 503
    assert "TINYFISH_API_KEY" in response.json()["detail"]


def test_live_search_uses_search_and_fetch_and_returns_evidence(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def search(self, query, limit=8, purpose=None, include_domains=None):
            assert "network support" in query.lower()
            assert purpose and "official tender portals" in purpose.lower()
            assert include_domains == "etenders.gov.in,eprocure.gov.in,gem.gov.in"
            return [{
                "title": "Network Support Tender Notice",
                "url": "https://etenders.gov.in/eprocure/app?component=demo",
                "snippet": "Bidders must meet the published eligibility criteria.",
                "site_name": "etenders.gov.in",
            }]

        async def fetch(self, urls, purpose=None, ttl=0, if_none_match=None, if_modified_since=None):
            assert len(urls) == 1
            assert purpose and "tender requirements" in purpose.lower()
            assert ttl == 0
            return {"results": [{
                "url": urls[0],
                "final_url": urls[0],
                "title": "Network Support Tender Notice",
                "text": "Tender eligibility criteria\nThe bidder shall have average annual turnover of at least Rs. 2 crore.\nBid closing date: 27-Oct-2026 03:00 PM.",
                "etag": None,
                "last_modified": None,
            }], "errors": []}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    response = client.post("/api/search", json={"keywords": "network support", "turnover_crore": 1.0})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["mode"] == "live"
    assert payload["source_apis"] == ["TinyFish Search API", "TinyFish Fetch API"]
    assert len(payload["tenders"]) == 1
    tender = payload["tenders"][0]
    assert tender["fetched"] is True
    assert tender["source_status"] == "Official domain"
    assert tender["assessment"]["status"] == "Potential blocker"
    assert "2 crore" in tender["assessment"]["potential_blockers"][0]
    assert "27-Oct-2026" in tender["deadline"]


def test_agent_inspection_returns_evidence_and_fingerprint(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_extract(self, url):
            assert url.startswith("https://")
            return {
                "result": {
                    "tender_title": "Illustrative official tender",
                    "tender_id": "TEST-ONLY",
                    "deadline": "",
                    "requirements": [{
                        "category": "Financial",
                        "requirement_text": "Annual turnover at least Rs. 2 crore",
                        "exact_quote": "The bidder shall have average annual turnover of at least Rs. 2 crore.",
                        "source_url": url,
                        "source_heading_or_page": "Eligibility",
                        "uncertainty_note": "",
                    }],
                },
                "run_id": "test-run-not-live",
                "num_of_steps": 3,
                "cost_note": "Test fixture only",
            }

        async def fetch(self, urls, purpose="", ttl=0, if_none_match=None, if_modified_since=None):
            assert purpose and "verify" in purpose.lower()
            return {"results": [{"url": urls[0], "final_url": urls[0], "text": "Eligibility The bidder shall have average annual turnover of at least Rs. 2 crore."}], "errors": []}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    response = client.post("/api/inspect", json={
        "url": "https://eprocure.gov.in/eprocure/app?component=demo",
        "profile": {"keywords": "network support", "turnover_crore": 1.0},
    })
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["mode"] == "live"
    assert body["source_api"] == "TinyFish Web Agent via official Python SDK (synchronous)"
    assert len(body["evidence_sha256"]) == 64
    assert body["assessment"]["status"] == "Potential blocker"
    assert "2 crore" in body["assessment"]["potential_blockers"][0]
    assert body["extraction"]["requirements"][0]["evidence_verification"] == "verified_by_fetch"


def test_agent_quote_not_verified_does_not_trigger_blocker(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_extract(self, url):
            return {
                "result": {"tender_title": "Illustrative source", "tender_id": "TEST", "deadline": "", "requirements": [{
                    "category": "Financial", "requirement_text": "Annual turnover at least Rs. 2 crore",
                    "exact_quote": "The bidder shall have average annual turnover of at least Rs. 2 crore.",
                    "source_url": url, "source_heading_or_page": "Eligibility", "uncertainty_note": ""
                }]},
                "run_id": "mismatch-test", "num_of_steps": 2, "cost_note": "Test fixture only"
            }

        async def fetch(self, urls, purpose="", ttl=0, if_none_match=None, if_modified_since=None):
            return {"results": [{"url": urls[0], "final_url": urls[0], "text": "This text contains no such financial condition."}], "errors": []}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    response = client.post("/api/inspect", json={
        "url": "https://eprocure.gov.in/eprocure/app?component=demo",
        "profile": {"keywords": "network support", "turnover_crore": 1.0},
    })
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["extraction"]["requirements"][0]["evidence_verification"] == "unverified"
    assert body["assessment"]["status"] == "Human review needed"
    assert body["assessment"]["potential_blockers"] == []
    assert any("Unverified Agent quote" in item for item in body["assessment"]["unknowns"])


def test_verified_quote_not_expanded_by_agent_paraphrase(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def agent_extract(self, url):
            return {
                "result": {"tender_title": "Illustrative source", "tender_id": "TEST", "deadline": "", "requirements": [{
                    "category": "Financial",
                    "requirement_text": "Annual turnover at least Rs. 99 crore",
                    "exact_quote": "The bidder shall submit all relevant supporting documents.",
                    "source_url": url,
                    "source_heading_or_page": "Instructions",
                    "uncertainty_note": ""
                }]},
                "run_id": "paraphrase-mismatch-test", "num_of_steps": 2, "cost_note": "Test fixture only"
            }

        async def fetch(self, urls, purpose="", ttl=0, if_none_match=None, if_modified_since=None):
            return {"results": [{"url": urls[0], "final_url": urls[0], "text": "The bidder shall submit all relevant supporting documents."}], "errors": []}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    response = client.post("/api/inspect", json={
        "url": "https://eprocure.gov.in/eprocure/app?component=demo",
        "profile": {"keywords": "network support", "turnover_crore": 1.0},
    })
    assert response.status_code == 200, response.text
    body = response.json()
    req = body["extraction"]["requirements"][0]
    assert req["evidence_verification"] == "verified_by_fetch"
    # The parser evaluates only the verified verbatim quote, not the Agent's unverified paraphrase.
    assert body["assessment"]["potential_blockers"] == []
    assert body["assessment"]["status"] == "Human review needed"


def test_search_snippet_cannot_trigger_blocker_without_fetched_text(monkeypatch):
    class FakeTinyFish:
        configured = True

        async def search(self, query, limit=8, purpose=None, include_domains=None):
            return [{
                "title": "Snippet-only item",
                "url": "https://etenders.gov.in/eprocure/item",
                "snippet": "The bidder shall have average annual turnover of at least Rs. 99 crore.",
                "site_name": "etenders.gov.in",
            }]

        async def fetch(self, urls, purpose=None, ttl=0, if_none_match=None, if_modified_since=None):
            return {"results": [{"url": urls[0], "final_url": urls[0], "title": "Snippet-only item", "text": ""}], "errors": [{"url": urls[0], "error": "empty_content"}]}

    monkeypatch.setattr(main, "TinyFishClient", FakeTinyFish)
    response = client.post("/api/search", json={"keywords": "network support", "turnover_crore": 1.0})
    assert response.status_code == 200, response.text
    tender = response.json()["tenders"][0]
    assert tender["fetched"] is False
    assert tender["assessment"]["potential_blockers"] == []
    assert tender["assessment"]["status"] == "Human review needed"
    assert tender["clauses"] == []
    assert "discovery metadata only" in tender["assessment_basis"].lower()


def test_recheck_retries_conditional_unsupported(monkeypatch):
    class FakeTinyFish:
        configured = True
        calls = []

        async def fetch(self, urls, purpose="", ttl=0, if_none_match=None, if_modified_since=None):
            self.calls.append({"urls": urls, "if_none_match": if_none_match, "if_modified_since": if_modified_since, "ttl": ttl})
            if len(self.calls) == 1:
                return {"results": [], "errors": [{"url": urls[0], "error": "conditional_unsupported"}]}
            return {"results": [{"url": urls[0], "final_url": urls[0], "title": "Tender", "text": "Updated tender page\nBid closing date: 30-Oct-2026", "etag": None, "last_modified": None}], "errors": []}

    fake = FakeTinyFish()
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    monkeypatch.setattr(main, "get_previous_snapshot", lambda url: {
        "title": "Tender", "text": "Old tender page\nBid closing date: 27-Oct-2026",
        "etag": '"old"', "last_modified": "Mon, 19 Oct 2026 10:00:00 GMT",
        "checked_at": "2026-10-19T10:00:00+00:00", "text_hash": "old-hash"
    })
    monkeypatch.setattr(main, "save_snapshot", lambda url, title, text, etag=None, last_modified=None: {
        "hash": "new-hash", "changed_since_last_check": True, "checked_at": "2026-10-20T12:00:00+00:00"
    })
    response = client.post("/api/recheck", json={"url": "https://eprocure.gov.in/tender/123"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert len(fake.calls) == 2
    assert fake.calls[0]["if_none_match"] == '"old"'
    assert fake.calls[1]["if_none_match"] is None
    assert body["change_detected"] is True
    assert "live Fetch retry" in body["note"]


def test_agent_sdk_timeout_exceeds_agent_max_duration(monkeypatch):
    """Protect against an HTTP timeout shorter than the Agent's 150-second run cap."""
    import sys
    import types
    from types import SimpleNamespace
    import asyncio
    from app.tinyfish import TinyFishClient

    observed = {}

    class FakeRunStatus:
        COMPLETED = "COMPLETED"

    class FakeAgentConfig:
        def __init__(self, **kwargs):
            observed["agent_config"] = kwargs

    class FakeSDKClient:
        def __init__(self, api_key=None, timeout=None, max_retries=None):
            observed["timeout"] = timeout
            self.agent = self

        def run(self, **kwargs):
            observed["run_kwargs"] = kwargs
            return SimpleNamespace(
                status=FakeRunStatus.COMPLETED,
                result={"tender_title": "Test", "tender_id": "TEST", "deadline": "", "requirements": []},
                run_id="test-run", num_of_steps=1, error=None,
            )

    fake_module = types.SimpleNamespace(
        TinyFish=FakeSDKClient, AgentConfig=FakeAgentConfig, RunStatus=FakeRunStatus
    )
    monkeypatch.setitem(sys.modules, "tinyfish", fake_module)

    result = asyncio.run(TinyFishClient(api_key="test-key", timeout=10).agent_extract(
        "https://eprocure.gov.in/tender/test"
    ))
    assert result["status"] == "COMPLETED"
    assert observed["timeout"] >= 180
    assert observed["agent_config"]["max_duration_seconds"] == 150
