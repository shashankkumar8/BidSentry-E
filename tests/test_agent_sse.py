"""Tests for the provider-streaming Agent inspection path; providers are mocked locally."""
import json
from fastapi.testclient import TestClient
import app.main as main
from app.main import app

client = TestClient(app)
URL = "https://eprocure.gov.in/eprocure/app?component=stream-test"
PROFILE = {"keywords": "network support", "turnover_crore": 1.0}
RESULT = {
    "tender_title": "Illustrative test tender",
    "tender_id": "TEST-ONLY",
    "deadline": "",
    "requirements": [{
        "category": "Financial",
        "requirement_text": "Average annual turnover of at least Rs. 2 crore",
        "exact_quote": "The bidder shall have average annual turnover of at least Rs. 2 crore.",
        "source_url": URL,
        "source_heading_or_page": "Eligibility",
        "uncertainty_note": "",
    }],
}
SOURCE = "Eligibility\nThe bidder shall have average annual turnover of at least Rs. 2 crore."


class FakeStreamingTinyFish:
    configured = True

    def __init__(self, events, run_record=None):
        self.events = events
        self.run_record = run_record
        self.run_lookups = 0

    async def agent_stream(self, url):
        assert url == URL
        for item in self.events:
            yield item

    async def get_agent_run(self, run_id):
        self.run_lookups += 1
        return self.run_record or {"status": "COMPLETED", "num_of_steps": 9}

    async def fetch(self, urls, purpose="", ttl=0, if_none_match=None, if_modified_since=None):
        assert urls == [URL]
        assert "verify" in purpose.lower()
        return {"results": [{"url": URL, "final_url": URL, "text": SOURCE}], "errors": []}


def provider_events(*, steps=7, include_result=True):
    terminal = {
        "type": "COMPLETE", "status": "COMPLETED", "run_id": "real-shape-mocked-run",
        "num_of_steps": steps,
    }
    if include_result:
        terminal["result"] = RESULT
    return [
        {"type": "STARTED", "run_id": "real-shape-mocked-run", "message": "Started"},
        {"type": "STREAMING_URL", "streaming_url": "https://agent.tinyfish.ai/session/example"},
        {"type": "PROGRESS", "message": "Inspecting eligibility sections"},
        terminal,
    ]


def parse_sse(response_text):
    return [json.loads(block.split("data:", 1)[1].strip()) for block in response_text.replace("\r\n", "\n").split("\n\n") if "data:" in block]


def test_stream_route_emits_provider_events_then_independently_verified_result(monkeypatch):
    fake = FakeStreamingTinyFish(provider_events())
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    assert response.status_code == 200
    events = parse_sse(response.text)
    assert any(e.get("type") == "provider_event" and e["event"].get("type") == "STREAMING_URL" for e in events)
    result_event = next(e for e in events if e.get("type") == "result")
    result = result_event["data"]
    assert result["source_api"] == "TinyFish Web Agent REST SSE"
    assert result["run_id"] == "real-shape-mocked-run"
    assert result["num_of_steps"] == 7
    assert result["provider_sse_events_observed"] == 4
    assert result["estimated_cost_usd"] == 0.112
    assert result["streaming_url"] == "https://agent.tinyfish.ai/session/example"
    assert result["extraction"]["requirements"][0]["evidence_verification"] == "verified_by_fetch"
    assert result["assessment"]["potential_blockers"]
    assert events[-1]["type"] == "done"


def test_stream_route_looks_up_provider_steps_instead_of_counting_sse_events(monkeypatch):
    fake = FakeStreamingTinyFish(provider_events(steps=None), run_record={"status": "COMPLETED", "num_of_steps": 11})
    # Remove step count at terminal, so endpoint must consult the provider's run record.
    fake.events[-1].pop("num_of_steps", None)
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    events = parse_sse(response.text)
    result = next(e["data"] for e in events if e.get("type") == "result")
    assert fake.run_lookups == 1
    assert result["provider_sse_events_observed"] == 4
    assert result["num_of_steps"] == 11
    assert result["estimated_cost_usd"] == 0.176


def test_stream_route_does_not_create_assessment_without_terminal_completion(monkeypatch):
    fake = FakeStreamingTinyFish([
        {"type": "STARTED", "run_id": "incomplete-run"},
        {"type": "PROGRESS", "message": "Still working"},
    ])
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    assert response.status_code == 200
    events = parse_sse(response.text)
    assert any(e.get("type") == "error" and "without a terminal completion" in e.get("message", "") for e in events)
    assert not any(e.get("type") == "result" for e in events)


def test_stream_route_surfaces_provider_failure_without_fake_result(monkeypatch):
    fake = FakeStreamingTinyFish([
        {"type": "STARTED", "run_id": "failed-run"},
        {"type": "FAILED", "status": "FAILED", "message": "Access denied by target portal"},
    ])
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    events = parse_sse(response.text)
    assert any(e.get("type") == "error" and "Access denied" in e.get("message", "") for e in events)
    assert not any(e.get("type") == "result" for e in events)


def test_stream_route_rejects_failed_run_metadata_even_if_terminal_contains_output(monkeypatch):
    fake = FakeStreamingTinyFish(provider_events(steps=None), run_record={"status": "FAILED", "num_of_steps": 5})
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    events = parse_sse(response.text)
    assert any(e.get("type") == "error" and "metadata reports FAILED" in e.get("message", "") for e in events)
    assert not any(e.get("type") == "result" for e in events)


def test_stream_audit_duration_is_recorded_after_stream_finishes(monkeypatch):
    fake = FakeStreamingTinyFish(provider_events())
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    recorded = []
    monkeypatch.setattr(main, "record_api_call", lambda **kwargs: recorded.append(kwargs))
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    assert response.status_code == 200
    # TestClient consumes the StreamingResponse body before returning from post(),
    # which is when the middleware's wrapped iterator writes its final duration row.
    rows = [row for row in recorded if row["endpoint"] == "/api/v1/inspect/stream"]
    assert len(rows) == 1
    assert rows[0]["duration_ms"] >= 0
    assert response.headers["X-Execution-Time-Ms"] == "stream-completion-reported-in-SSE"


def test_tinyfish_rest_adapter_parses_named_sse_events(monkeypatch):
    import asyncio
    import app.tinyfish as tinyfish_module
    from app.tinyfish import TinyFishClient

    frames = [
        "event: STARTED", 'data: {"run_id":"unit-run","message":"Started"}', "",
        "event: STREAMING_URL", 'data: {"streaming_url":"https://agent.tinyfish.ai/session/unit"}', "",
        "event: COMPLETE", 'data: {"status":"COMPLETED","num_of_steps":4,"result":{"tender_title":"T","tender_id":"ID","deadline":"","requirements":[]}}', "",
    ]

    class FakeResponse:
        status_code = 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        def raise_for_status(self):
            return None

        async def aiter_lines(self):
            for line in frames:
                yield line

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        def stream(self, method, url, json, headers):
            assert method == "POST"
            assert url == tinyfish_module.AGENT_SSE_URL
            assert "output_schema" in json
            assert headers["Accept"] == "text/event-stream"
            return FakeResponse()

    monkeypatch.setattr(tinyfish_module.httpx, "AsyncClient", FakeAsyncClient)
    client_with_key = TinyFishClient(api_key="test-key-not-real")

    async def collect():
        return [event async for event in client_with_key.agent_stream(URL)]

    items = asyncio.run(collect())
    assert [item["type"] for item in items] == ["STARTED", "STREAMING_URL", "COMPLETE"]
    assert items[-1]["num_of_steps"] == 4
    assert items[-1]["result"]["tender_title"] == "T"


def test_stream_route_does_not_treat_empty_extraction_as_success(monkeypatch):
    empty = {"tender_title": "A title", "tender_id": "ID", "deadline": "", "requirements": []}
    fake = FakeStreamingTinyFish(provider_events(steps=2))
    fake.events[-1]["result"] = empty
    monkeypatch.setattr(main, "TinyFishClient", lambda: fake)
    response = client.post("/api/v1/inspect/stream", json={"url": URL, "profile": PROFILE})
    events = parse_sse(response.text)
    assert any(e.get("type") == "error" and "no usable tender requirements" in e.get("message", "") for e in events)
    assert not any(e.get("type") == "result" for e in events)
