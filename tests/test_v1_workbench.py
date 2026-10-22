from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_versioned_health_exposes_configuration_not_key():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "BidSentry-E"
    assert "TINYFISH_API_KEY" not in str(body)


def test_versioned_presets_are_clearly_synthetic():
    response = client.get("/api/v1/presets")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "benchmark"
    assert "synthetic" in body["notice"].lower()
    assert all("synthetic" in p["subtitle"].lower() for p in body["presets"])


def test_versioned_verify_demo_is_explicitly_synthetic():
    response = client.post("/api/v1/verify", json={"mode": "demo"})
    assert response.status_code == 200
    assert response.json()["mode"] == "demo"


def test_versioned_verify_requires_profile_for_live_search():
    response = client.post("/api/v1/verify", json={"mode": "search"})
    assert response.status_code == 422


def test_quote_guard_lab_rejects_spoofed_quote():
    response = client.post("/api/v1/lab/quote-check", json={
        "quote": "Bidder must hold CMMI Level 5 and ISO 27001 certification.",
        "source_text": "The bidder shall submit the GST registration certificate.",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "synthetic_quote_guard_lab"
    assert body["badge"] == "UNVERIFIED_QUOTE"
    assert body["blocker_allowed"] is False


def test_api_response_has_real_timing_and_audit_headers():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.headers.get("X-Audit-ID", "").startswith("AUD-")
    assert float(response.headers["X-Execution-Time-Ms"]) >= 0


def test_recent_history_endpoint_returns_metadata_list():
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["audit_runs"], list)
    assert "request bodies" in body["storage"]


def test_workbench_uses_live_agent_stream_and_no_legacy_sync_path_for_ui():
    from pathlib import Path
    markup = Path("app/static/workbench.html").read_text(encoding="utf-8")
    assert "fetch('/api/v1/inspect/stream'" in markup
    assert "provider_sse_events_observed" in markup
    assert "SSE event count is not billable step count" in markup
    assert "No demo data is substituted on failure" in markup
