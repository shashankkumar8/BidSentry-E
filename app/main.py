from __future__ import annotations

import hashlib
import html
import json
import os
import re
import unicodedata
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .analyzer import build_tender_result, summarize_change, normalize_domain, source_type, profile_assessment
from .audit import new_audit_id, record_api_call, recent_api_calls
from .evidence import verify_quote
from .tinyfish import TinyFishClient, TinyFishError

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
load_dotenv(ROOT.parent / ".env")
DB_PATH = Path(os.getenv("BIDSENTRY_DB_PATH", str(ROOT.parent / ".bidsentry.db")))

app = FastAPI(title="BidSentry API", version="0.1.0", description="Evidence-first tender readiness for Indian MSMEs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


@app.middleware("http")
async def execution_audit_middleware(request, call_next):
    """Measure API duration and record a privacy-minimal audit row.

    Regular JSON requests are measured to response creation. For the Agent SSE route,
    response headers are sent before the stream finishes, so the audit row is written
    only after body iteration ends and uses the full observed stream duration. The SSE
    response header explicitly avoids pretending that time-to-headers is full latency.
    Request bodies, query strings, cookies and API keys are never logged.
    """
    if not request.url.path.startswith("/api/"):
        return await call_next(request)
    audit_id = new_audit_id()
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = (time.perf_counter() - started) * 1000
        try:
            record_api_call(audit_id=audit_id, method=request.method, endpoint=request.url.path,
                            status_code=500, duration_ms=elapsed_ms)
        except Exception:
            pass
        raise

    response.headers["X-Audit-ID"] = audit_id
    stream_endpoint = request.url.path == "/api/v1/inspect/stream"
    if stream_endpoint and hasattr(response, "body_iterator"):
        response.headers["X-Execution-Time-Ms"] = "stream-completion-reported-in-SSE"
        original_iterator = response.body_iterator

        async def measured_stream():
            try:
                async for chunk in original_iterator:
                    yield chunk
            finally:
                elapsed_ms = (time.perf_counter() - started) * 1000
                if request.url.path not in {"/api/history", "/api/v1/history"}:
                    try:
                        record_api_call(audit_id=audit_id, method=request.method, endpoint=request.url.path,
                                        status_code=response.status_code, duration_ms=elapsed_ms)
                    except Exception:
                        pass
        response.body_iterator = measured_stream()
        return response

    elapsed_ms = (time.perf_counter() - started) * 1000
    response.headers["X-Execution-Time-Ms"] = f"{elapsed_ms:.2f}"
    if request.url.path not in {"/api/history", "/api/v1/history"}:
        try:
            record_api_call(audit_id=audit_id, method=request.method, endpoint=request.url.path,
                            status_code=response.status_code, duration_ms=elapsed_ms)
        except Exception:
            pass
    return response


def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS snapshots (
        url TEXT PRIMARY KEY, title TEXT, text_hash TEXT NOT NULL, text TEXT NOT NULL,
        etag TEXT, last_modified TEXT, checked_at TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS snapshot_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL, text_hash TEXT NOT NULL,
        text TEXT NOT NULL, checked_at TEXT NOT NULL, changed INTEGER NOT NULL
    )""")
    conn.commit()
    return conn


def save_snapshot(url: str, title: str, text: str, etag: str | None = None, last_modified: str | None = None) -> dict[str, Any]:
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    now = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        prior = conn.execute("SELECT text, text_hash FROM snapshots WHERE url = ?", (url,)).fetchone()
        changed = bool(prior and prior["text_hash"] != digest)
        conn.execute(
            "INSERT INTO snapshots(url,title,text_hash,text,etag,last_modified,checked_at) VALUES(?,?,?,?,?,?,?) "
            "ON CONFLICT(url) DO UPDATE SET title=excluded.title,text_hash=excluded.text_hash,text=excluded.text,etag=excluded.etag,last_modified=excluded.last_modified,checked_at=excluded.checked_at",
            (url, title, digest, text, etag, last_modified, now),
        )
        conn.execute("INSERT INTO snapshot_history(url,text_hash,text,checked_at,changed) VALUES(?,?,?,?,?)", (url, digest, text, now, int(changed)))
        conn.commit()
    return {"hash": digest, "changed_since_last_check": changed, "checked_at": now}


def get_previous_snapshot(url: str) -> sqlite3.Row | None:
    with db() as conn:
        row = conn.execute("SELECT * FROM snapshots WHERE url = ?", (url,)).fetchone()
        return row


class SupplierProfile(BaseModel):
    keywords: str = Field(min_length=2, max_length=240)
    sector: str = Field(default="", max_length=100)
    location: str = Field(default="India", max_length=100)
    # None means not declared. Zero is a user-declared value and is assessed differently.
    turnover_crore: float | None = Field(default=None, ge=0, le=100000)
    years_experience: int | None = Field(default=None, ge=0, le=100)
    emd_budget_lakh: float | None = Field(default=None, ge=0, le=1000000)
    certifications: list[str] | None = Field(default=None, max_length=30)
    udyam_registered: bool | None = None
    max_results: int = Field(default=6, ge=1, le=8)


class RecheckRequest(BaseModel):
    url: str = Field(min_length=10, max_length=2048)


class InspectRequest(BaseModel):
    url: str = Field(min_length=10, max_length=2048)
    profile: SupplierProfile


class VerifyRequest(BaseModel):
    """Stable v1 entry point; each mode is explicit and failures are never replaced with demo data."""
    mode: Literal["demo", "search", "inspect"] = "demo"
    profile: SupplierProfile | None = None
    url: str | None = Field(default=None, min_length=10, max_length=2048)


class QuoteGuardRequest(BaseModel):
    quote: str = Field(min_length=1, max_length=600)
    source_text: str = Field(max_length=10000)


def ensure_public_https(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise HTTPException(status_code=400, detail="Only public HTTPS source URLs on Indian government/NIC domains can be inspected or rechecked.")
    if parsed.username or parsed.password:
        raise HTTPException(status_code=400, detail="Credentials embedded in URLs are not permitted.")
    if parsed.port and parsed.port != 443:
        raise HTTPException(status_code=400, detail="Non-standard ports are not permitted for public tender URLs.")
    host = parsed.hostname.lower().removeprefix("www.")
    blocked = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "169.254.169.254"}
    is_official = host.endswith(".gov.in") or host == "gov.in" or host.endswith(".nic.in") or host == "nic.in"
    if host in blocked or host.endswith(".local") or not is_official:
        raise HTTPException(status_code=400, detail="Change watch is restricted to public Indian government/NIC domains. Open third-party links manually and locate the official notice.")
    return url


@app.get("/")
def index() -> FileResponse:
    workbench = STATIC / "workbench.html"
    return FileResponse(workbench if workbench.exists() else STATIC / "index.html")


@app.get("/legacy")
def legacy_index() -> FileResponse:
    """Retain the original prototype UI as a fallback reference."""
    return FileResponse(STATIC / "index.html")


@app.get("/api/v1/health", include_in_schema=False)
@app.get("/api/health")
def health() -> dict[str, Any]:
    client = TinyFishClient()
    return {"ok": True, "name": "BidSentry-E", "version": app.version, "tinyfish_configured": client.configured, "mode": "live" if client.configured else "demo-ready"}


@app.get("/api/demo")
def demo() -> dict[str, Any]:
    path = ROOT / "data" / "demo_tenders.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {"mode": "demo", "notice": "Illustrative synthetic example only. Not a live tender, not a real government notice, and not evidence of eligibility.", **payload}


@app.get("/api/v1/presets")
def list_presets() -> dict[str, Any]:
    """Return only clearly labelled synthetic benchmark presets for deterministic demos."""
    data = demo()
    presets = []
    for tender in data.get("tenders", []):
        presets.append({
            "id": tender.get("id", "synthetic-demo"),
            "label": tender.get("title", "Synthetic benchmark scenario"),
            "subtitle": str(tender.get("reference", "SYNTHETIC")) + " · synthetic benchmark",
            "source_status": "Synthetic demo data",
        })
    return {"mode": "benchmark", "notice": data["notice"], "presets": presets}


@app.get("/api/v1/presets/{preset_id}")
def get_preset(preset_id: str) -> dict[str, Any]:
    data = demo()
    selected = next((t for t in data.get("tenders", []) if t.get("id") == preset_id), None)
    if not selected:
        raise HTTPException(status_code=404, detail="Unknown synthetic preset. Use /api/v1/presets to list available presets.")
    return {"mode": "demo", "notice": data["notice"], "tender": selected}


@app.get("/api/history")
@app.get("/api/v1/history", include_in_schema=False)
def api_history() -> dict[str, Any]:
    return {"audit_runs": recent_api_calls(20), "storage": "SQLite metadata only; request bodies and API keys are not stored."}


@app.post("/api/v1/verify")
async def verify_entry(payload: VerifyRequest) -> dict[str, Any]:
    """Single versioned entry point. Mode choice is explicit; live errors are not swapped for samples."""
    if payload.mode == "demo":
        result = demo()
        result["entry_mode"] = "synthetic_demo"
        return result
    if payload.profile is None:
        raise HTTPException(status_code=422, detail="A supplier profile is required for search or inspect mode.")
    if payload.mode == "search":
        return await search(payload.profile)
    if payload.mode == "inspect":
        if not payload.url:
            raise HTTPException(status_code=422, detail="A public official tender URL is required for inspect mode.")
        return await inspect_with_agent(InspectRequest(url=payload.url, profile=payload.profile))
    raise HTTPException(status_code=422, detail="Unsupported verification mode.")


@app.post("/api/v1/lab/quote-check")
def quote_guard_lab(payload: QuoteGuardRequest) -> dict[str, Any]:
    """Local synthetic adversarial test of the strict quote gate; never writes inputs to audit logs."""
    check = verify_quote(payload.quote, payload.source_text, minimum_chars=12)
    return {
        "mode": "synthetic_quote_guard_lab",
        "label": "Synthetic test only — not a tender analysis or live-source verification",
        **check,
        "blocker_allowed": bool(check["verified"]),
    }


@app.post("/api/v1/search", include_in_schema=False)
@app.post("/api/search")
async def search(profile: SupplierProfile) -> dict[str, Any]:
    tf = TinyFishClient()
    if not tf.configured:
        raise HTTPException(status_code=503, detail="TinyFish API key is not configured. Add TINYFISH_API_KEY to .env. Demo mode is available from the Explore Demo button.")
    query_parts = ["India government e-procurement tender notice bid qualification", profile.keywords]
    if profile.sector.strip():
        query_parts.append(profile.sector.strip())
    if profile.location.strip() and profile.location.lower() != "india":
        query_parts.append(profile.location.strip())
    query_parts.append("submission deadline eligibility corrigendum amendment")
    query = " ".join(query_parts)
    purpose = (
        "Find current public Indian government procurement notices relevant to this supplier profile. "
        "Prioritize official tender portals and include eligibility, financial, experience, bid-security, "
        "deadline, and corrigendum information when available. Do not infer eligibility from the search result."
    )
    try:
        search_rows = await tf.search(
            query=query, limit=profile.max_results, purpose=purpose,
            include_domains="etenders.gov.in,eprocure.gov.in,gem.gov.in",
        )
        if not search_rows:
            # This is an explicit broader-web fallback. Results stay visibly classified by source domain.
            search_rows = await tf.search(query=query, limit=profile.max_results, purpose=purpose)
        if not search_rows:
            return {"mode": "live", "query": query, "message": "TinyFish Search returned no usable HTTPS results. Try broader keywords.", "tenders": [], "source_apis": ["TinyFish Search API"]}
        # Prefer Indian government/official domains, but retain other results with clear labels.
        # Use suffix-boundary domain validation rather than substring matching; the
        # latter can misclassify lookalike hosts such as etenders.gov.in.attacker.example.
        official = [r for r in search_rows if source_type(r["url"]) == "Official domain"]
        ordered = official + [r for r in search_rows if r not in official]
        selected = ordered[:min(profile.max_results, 5)]
        fetch_payload = await tf.fetch(
            [r["url"] for r in selected],
            purpose=(
                "Extract public tender requirements for an evidence-first supplier readiness review: "
                "eligibility, turnover, experience, certificates, bid security, deadlines and corrigenda. "
                "Preserve source wording and do not infer missing requirements."
            ),
            ttl=0,
        )
    except TinyFishError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    fetched_map: dict[str, dict[str, Any]] = {}
    for page in fetch_payload.get("results", []):
        if isinstance(page, dict):
            key = str(page.get("url") or page.get("final_url") or "")
            fetched_map[key] = page
            if page.get("final_url"):
                fetched_map[str(page["final_url"])] = page
    tenders = []
    for row in selected:
        page = fetched_map.get(row["url"])
        if not page:
            page = next((p for p in fetch_payload.get("results", []) if isinstance(p, dict) and (p.get("url") == row["url"] or p.get("final_url") == row["url"])), None)
        result = build_tender_result(row, page, profile.model_dump())
        if result.get("content"):
            snap = save_snapshot(result["url"], result["title"], result["content"], (page or {}).get("etag"), (page or {}).get("last_modified"))
            result["changed_since_last_check"] = snap["changed_since_last_check"]
        else:
            result["changed_since_last_check"] = False
        tenders.append(result)
    tenders.sort(key=lambda x: (x["assessment"]["status"] != "Potential blocker", -x["relevance_score"]))
    return {
        "mode": "live",
        "query": query,
        "searched_at": datetime.now(timezone.utc).isoformat(),
        "source_apis": ["TinyFish Search API", "TinyFish Fetch API"],
        "result_count": len(tenders),
        "fetch_errors": fetch_payload.get("errors", []),
        "tenders": tenders,
        "method_note": "TF-IDF relevance ranks research priority; it is not an eligibility probability. Every clause must be checked against the complete official tender schedule and amendments.",
    }


async def build_inspection_result(
    url: str, profile: SupplierProfile, agent_payload: dict[str, Any], tf: TinyFishClient
) -> dict[str, Any]:
    """Common validation and assessment for SDK-synchronous and REST-SSE Agent runs."""
    extracted = agent_payload.get("result", {})
    requirements = extracted.get("requirements", []) if isinstance(extracted, dict) else []
    requirements = [item for item in requirements if isinstance(item, dict)]

    # Defense-in-depth: a Web Agent quote is not treated as verified just because it
    # was returned in structured JSON. Re-fetch up to 10 reported official source URLs
    # and check whether each quote occurs in the retrieved text (whitespace-insensitive).
    # Anything not independently matched remains unverified and cannot alone trigger a blocker.
    source_urls: list[str] = []
    safe_url_by_requirement: dict[int, str] = {}
    for idx, item in enumerate(requirements):
        source_url = str(item.get("source_url") or url).strip()
        try:
            safe_url = ensure_public_https(source_url)
        except HTTPException:
            safe_url = ""
        if safe_url:
            safe_url_by_requirement[idx] = safe_url
            if safe_url not in source_urls and len(source_urls) < 10:
                source_urls.append(safe_url)
        item["evidence_verification"] = "unverified"
        item["verification_note"] = "The source quote has not yet been independently matched."

    source_text_by_url: dict[str, str] = {}
    verification_error = ""
    if source_urls:
        try:
            verify_payload = await tf.fetch(
                source_urls,
                purpose=(
                    "Independently retrieve the text of these official public tender source pages to verify "
                    "whether the quoted excerpts appear verbatim. Return source text and metadata only; "
                    "do not infer or summarize eligibility."
                ),
                ttl=0,
            )
            for page in verify_payload.get("results", []):
                if not isinstance(page, dict):
                    continue
                page_text = str(page.get("text") or "")
                if not page_text:
                    continue
                for page_url in (page.get("url"), page.get("final_url")):
                    if page_url:
                        source_text_by_url[str(page_url)] = page_text
        except TinyFishError as exc:
            verification_error = str(exc)

    verified_lines: list[str] = []
    verification_unknowns: list[str] = []
    for idx, item in enumerate(requirements):
        quote = str(item.get("exact_quote") or "").strip()
        source_url = safe_url_by_requirement.get(idx, "")
        page_text = source_text_by_url.get(source_url, "")
        # Also permit TinyFish to return a canonical URL variant for the same source.
        if not page_text:
            page_text = next((txt for candidate_url, txt in source_text_by_url.items()
                              if source_url and (candidate_url.rstrip("/") == source_url.rstrip("/") or
                                                 candidate_url.rstrip("/").startswith(source_url.rstrip("/") + "?"))), "")
        quote_check = verify_quote(quote, page_text, minimum_chars=12)
        item["match_type"] = quote_check.get("match_type", "UNKNOWN")
        item["review_state"] = quote_check.get("review_state", "NEEDS_HUMAN_REVIEW")
        if quote_check["verified"]:
            item["evidence_verification"] = "verified_by_fetch"
            item["verification_note"] = quote_check["reason"]
            item["verification_method"] = quote_check["method"]
            verified_lines.append(quote)
        else:
            if not source_url:
                note = "The Agent returned a source URL outside the allowed official government/NIC domain set or no usable source URL."
            elif not page_text:
                note = "A separate Fetch response did not return text for this source; verify manually."
            elif len(quote.strip()) < 12:
                note = "The returned quote is too short to verify reliably; open the official source manually."
            elif quote_check.get("match_type") == "PARTIAL_OR_UNCONFIRMED_OVERLAP":
                note = quote_check["reason"]
            else:
                note = "The quote was not found in the separate Fetch text; it may be paraphrased, truncated, or from another linked document."
            if verification_error:
                note = f"Independent Fetch verification failed: {verification_error}"
            item["verification_note"] = note
            verification_unknowns.append(f"Unverified Agent quote: {str(item.get('requirement_text') or item.get('category') or 'requirement')} — {note}")

    # Assessment uses only independently verified text. Everything else stays unknown.
    evidenced_text = "\n".join(verified_lines).strip()
    assessment = profile_assessment(evidenced_text, profile.model_dump()) if evidenced_text else {
        "status": "Human review needed",
        "potential_blockers": [],
        "matches": [],
        "unknowns": ["No Agent quote was independently verified against a separate Fetch response. Review the official tender documents manually."],
        "clause_ledger": [],
        "disclaimer": "Pre-screen only. This is not a legal eligibility determination."
    }
    assessment.setdefault("unknowns", [])
    assessment["unknowns"].extend(verification_unknowns)
    assessment.setdefault("clause_ledger", [])

    # Append unverified Agent requirements to the clause ledger with explicit UNVERIFIED_QUOTE state
    for item in requirements:
        if item.get("evidence_verification") != "verified_by_fetch":
            assessment["clause_ledger"].append({
                "category": str(item.get("category") or "Agent Extracted"),
                "requirement": str(item.get("requirement_text") or "Requirement text unresolved"),
                "source_quote": str(item.get("exact_quote") or "No verbatim quote"),
                "source_url": str(item.get("source_url") or url),
                "evidence_verification": "UNVERIFIED_QUOTE",
                "supplier_declared": "Unverified clause excluded from profile matching",
                "state": "UNVERIFIED_QUOTE",
                "comparison_logic": item.get("verification_note", "Quote not matched in independent fetch."),
                "suggested_action": "Open primary tender notice and verify clause manually.",
            })
    if verification_unknowns and assessment.get("status") == "Evidence supports a match":
        # Do not present a clean result when some extracted clauses remain unchecked.
        assessment["status"] = "Human review needed"
    checked_at = datetime.now(timezone.utc).isoformat()
    canonical = json.dumps({"url": url, "checked_at": checked_at, "result": extracted}, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    evidence_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    raw_steps = agent_payload.get("num_of_steps")
    try:
        steps = int(raw_steps) if raw_steps is not None and int(raw_steps) >= 0 else None
    except (TypeError, ValueError):
        steps = None
    try:
        # Published reference rate only; set this to the account's applicable rate if it differs.
        step_rate = float(os.getenv("TINYFISH_AGENT_STEP_USD", "0.016"))
    except ValueError:
        step_rate = 0.016
    return {
        "mode": "live",
        "source_api": agent_payload.get("source_api") or "TinyFish Web Agent via official Python SDK",
        "url": url,
        "checked_at": checked_at,
        "run_id": agent_payload.get("run_id"),
        "num_of_steps": steps,
        "estimated_cost_usd": round(steps * step_rate, 6) if steps is not None else None,
        "cost_note": agent_payload.get("cost_note"),
        "extraction": extracted,
        "assessment": assessment,
        "evidence_sha256": evidence_hash,
        "integrity_note": "Fingerprint of this captured record; it is not a digital signature or proof that the source itself is authentic.",
        "limitations": [
            "Only accessible pages/documents reached during this run were inspected.",
            "Threshold comparisons use transparent rules and the supplier profile supplied by the user.",
            "Unknowns and source conflicts must be reviewed by a human before bidding."
        ]
    }




def _event_type(event: dict[str, Any]) -> str:
    return str(event.get("type") or event.get("event") or event.get("status") or "MESSAGE").strip().upper()


def _event_result(event: dict[str, Any]) -> dict[str, Any] | None:
    """Normalize documented/nested terminal-event result shapes without treating progress as output."""
    def decode(value: Any, depth: int = 0) -> dict[str, Any] | None:
        if depth > 4:
            return None
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return None
        if not isinstance(value, dict):
            return None
        # Only accept a structured extraction-like object as a final result.
        if isinstance(value.get("requirements"), list) and (
            isinstance(value.get("tender_title"), str) or isinstance(value.get("tender_id"), str)
        ):
            return value
        for key in ("result", "data", "output", "result_json", "resultJson", "response", "run"):
            if key in value:
                found = decode(value[key], depth + 1)
                if found is not None:
                    return found
        return None
    return decode(event)


def _provider_event_for_ui(event: dict[str, Any]) -> dict[str, Any]:
    """Forward only trace fields needed by the UI; avoid dumping arbitrary provider payloads."""
    allowed = ("type", "event", "status", "run_id", "runId", "streaming_url", "streamingUrl",
               "purpose", "message", "step", "progress", "num_of_steps", "numOfSteps")
    out = {key: event[key] for key in allowed if key in event and isinstance(event[key], (str, int, float, bool, type(None)))}
    out.setdefault("type", _event_type(event))
    return out


def _sse(payload: dict[str, Any]) -> str:
    return "data: " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n\n"


@app.post("/api/v1/inspect", include_in_schema=False)
@app.post("/api/inspect")
async def inspect_with_agent(payload: InspectRequest) -> dict[str, Any]:
    """Synchronous Python SDK route retained as a compatibility/fallback interface."""
    url = ensure_public_https(payload.url)
    tf = TinyFishClient()
    if not tf.configured:
        raise HTTPException(status_code=503, detail="TinyFish API key is not configured. Add TINYFISH_API_KEY to .env.")
    try:
        agent_payload = await tf.agent_extract(url)
    except TinyFishError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    agent_payload.setdefault("source_api", "TinyFish Web Agent via official Python SDK (synchronous)")
    return await build_inspection_result(url, payload.profile, agent_payload, tf)


@app.post("/api/v1/inspect/stream")
async def inspect_with_agent_stream(payload: InspectRequest):
    """Stream real provider SSE events, then independently Fetch-check Agent quotes."""
    from fastapi.responses import StreamingResponse

    url = ensure_public_https(payload.url)
    tf = TinyFishClient()
    if not tf.configured:
        raise HTTPException(status_code=503, detail="TinyFish API key is not configured. Add TINYFISH_API_KEY to .env.")

    async def event_stream():
        started = time.perf_counter()
        terminal: dict[str, Any] | None = None
        streaming_url: str | None = None
        observed_run_id: str | None = None
        event_count = 0
        yield _sse({"type": "phase", "phase": "agent", "status": "started",
                    "message": "Starting TinyFish Agent SSE inspection. Provider events are shown as received."})
        try:
            async for event in tf.agent_stream(url):
                event_count += 1
                etype = _event_type(event)
                run_id = event.get("run_id") or event.get("runId")
                if isinstance(run_id, str) and run_id:
                    observed_run_id = run_id
                stream_candidate = event.get("streaming_url") or event.get("streamingUrl")
                if isinstance(stream_candidate, str) and stream_candidate.startswith("https://"):
                    streaming_url = stream_candidate
                yield _sse({"type": "provider_event", "event": _provider_event_for_ui(event)})
                if etype in {"ERROR", "FAILED", "STREAM_ERROR", "RUN_FAILED"} or str(event.get("status", "")).upper() in {"FAILED", "ERROR"}:
                    message = str(event.get("message") or event.get("error") or "TinyFish Agent reported a failed run.")
                    yield _sse({"type": "error", "message": message, "run_id": observed_run_id})
                    return
                is_terminal = etype in {"COMPLETE", "COMPLETED", "RUN_COMPLETE", "RUN_COMPLETED"} or str(event.get("status", "")).upper() in {"COMPLETE", "COMPLETED"}
                if is_terminal:
                    terminal = event
                    # A terminal event should be terminal. Do not count progress events as steps.
                    break

            if terminal is None:
                yield _sse({"type": "error", "message": "TinyFish Agent SSE ended without a terminal completion payload. No assessment was created.", "run_id": observed_run_id})
                return

            terminal_result = _event_result(terminal)
            terminal_run_id = terminal.get("run_id") or terminal.get("runId") or observed_run_id
            steps = terminal.get("num_of_steps", terminal.get("numOfSteps"))
            provider_status = str(terminal.get("status") or _event_type(terminal)).upper()
            run_meta: dict[str, Any] = {}
            if (steps is None or terminal_result is None) and terminal_run_id:
                try:
                    run_meta = await tf.get_agent_run(str(terminal_run_id))
                except TinyFishError as exc:
                    # Result extraction can still proceed if the terminal event has usable output.
                    if terminal_result is None:
                        yield _sse({"type": "error", "message": f"Terminal payload lacked structured output and run lookup failed: {exc}", "run_id": terminal_run_id})
                        return
            nested_meta = run_meta.get("run") if isinstance(run_meta.get("run"), dict) else run_meta
            # A COMPLETE SSE frame and a successful extraction are separate facts. If
            # a metadata lookup is available, reject terminal failures/inconsistent
            # statuses before constructing any assessment.
            if isinstance(nested_meta, dict):
                meta_status = str(nested_meta.get("status") or nested_meta.get("run_status") or "").upper()
                if meta_status in {"FAILED", "ERROR", "CANCELLED", "CANCELED", "ABORTED", "TIMED_OUT", "TIMEOUT"}:
                    yield _sse({"type": "error", "message": f"TinyFish run metadata reports {meta_status}; no assessment was created.", "run_id": terminal_run_id})
                    return
                if meta_status and meta_status not in {"COMPLETE", "COMPLETED", "SUCCEEDED", "SUCCESS"}:
                    yield _sse({"type": "error", "message": f"TinyFish run metadata status is {meta_status}; no assessment was created.", "run_id": terminal_run_id})
                    return
            if steps is None:
                steps = nested_meta.get("num_of_steps", nested_meta.get("numOfSteps")) if isinstance(nested_meta, dict) else None
            if terminal_result is None:
                nested = run_meta.get("run") if isinstance(run_meta.get("run"), dict) else run_meta
                if isinstance(nested, dict):
                    terminal_result = _event_result(nested)
            if terminal_result is None:
                yield _sse({"type": "error", "message": "TinyFish completed the browser run but did not return a usable structured result. No assessment was created.", "run_id": terminal_run_id})
                return
            usable_requirements = [
                item for item in terminal_result.get("requirements", [])
                if isinstance(item, dict) and str(item.get("requirement_text") or "").strip()
            ]
            if not usable_requirements:
                yield _sse({"type": "error", "message": "TinyFish completed the browser run but extracted no usable tender requirements. No assessment was created; review the official notice manually.", "run_id": terminal_run_id})
                return
            if provider_status not in {"COMPLETE", "COMPLETED", "RUN_COMPLETE", "RUN_COMPLETED"}:
                # The event name can be COMPLETE while the actual run status says something else.
                if str(terminal.get("status", "")).upper() not in {"COMPLETE", "COMPLETED"}:
                    yield _sse({"type": "error", "message": f"Agent terminal status was {provider_status}; no assessment was created.", "run_id": terminal_run_id})
                    return

            try:
                steps_int = int(steps) if steps is not None and int(steps) >= 0 else None
            except (TypeError, ValueError):
                steps_int = None
            yield _sse({"type": "phase", "phase": "quote_verification", "status": "started",
                        "message": "Agent finished; independently Fetch-checking each cited source before comparison.",
                        "run_id": terminal_run_id, "provider_reported_steps": steps_int})
            agent_payload = {
                "result": terminal_result, "run_id": terminal_run_id, "num_of_steps": steps_int,
                "status": "COMPLETED", "source_api": "TinyFish Web Agent REST SSE",
                "streaming_url": streaming_url,
                "cost_note": "Steps are read only from the terminal provider run payload or run lookup; SSE event count is not billing. USD amount is an estimate and provider billing is authoritative.",
            }
            result = await build_inspection_result(url, payload.profile, agent_payload, tf)
            result["streaming_url"] = streaming_url
            result["provider_sse_events_observed"] = event_count
            result["inspection_elapsed_ms"] = round((time.perf_counter() - started) * 1000, 1)
            result["cost_note"] = agent_payload["cost_note"]
            yield _sse({"type": "result", "data": result})
            yield _sse({"type": "done", "message": "Inspection and independent quote verification completed."})
        except TinyFishError as exc:
            yield _sse({"type": "error", "message": str(exc), "run_id": observed_run_id})
        except Exception as exc:
            yield _sse({"type": "error", "message": f"Inspection stream failed: {type(exc).__name__}: {exc}", "run_id": observed_run_id})

    return StreamingResponse(
        event_stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"},
    )


@app.post("/api/v1/recheck", include_in_schema=False)
@app.post("/api/recheck")
async def recheck(payload: RecheckRequest) -> dict[str, Any]:
    url = ensure_public_https(payload.url)
    tf = TinyFishClient()
    if not tf.configured:
        raise HTTPException(status_code=503, detail="TinyFish API key is not configured. Add TINYFISH_API_KEY to .env.")
    prior = get_previous_snapshot(url)
    try:
        fetched = await tf.fetch(
            [url],
            purpose="Recheck this official tender source for textual changes that may affect eligibility, EMD, deadline or corrigenda.",
            ttl=0,
            if_none_match=str(prior["etag"]) if prior and prior["etag"] else None,
            if_modified_since=str(prior["last_modified"]) if prior and prior["last_modified"] else None,
        )
    except TinyFishError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    fallback_used = False
    fetch_errors = fetched.get("errors", [])
    # Some browser-rendered targets cannot honor origin conditional validators. Retry
    # once as an explicit live fetch without validators; do not suppress unrelated 401/403s.
    if any(isinstance(err, dict) and err.get("error") == "conditional_unsupported" for err in fetch_errors):
        try:
            fetched = await tf.fetch(
                [url],
                purpose="Live recheck of this official tender source because the origin does not support conditional validation.",
                ttl=0,
            )
            fallback_used = True
        except TinyFishError as exc:
            raise HTTPException(status_code=502, detail=f"Conditional recheck was unsupported and live retry failed: {exc}") from exc
    results = fetched.get("results", [])
    page = next((p for p in results if isinstance(p, dict) and (p.get("url") == url or p.get("final_url") == url)), None)
    if page and page.get("not_modified") is True and prior:
        # Origin returned 304 to a validator; keep the saved body and record a successful recheck.
        snap = save_snapshot(url, str(prior["title"] or "Tender source"), str(prior["text"]), str(prior["etag"] or "") or None, str(prior["last_modified"] or "") or None)
        return {
            "url": url, "title": prior["title"] or "Tender source", "checked_at": snap["checked_at"],
            "first_check": False, "change_detected": False, "not_modified": True,
            "previous_checked_at": prior["checked_at"],
            "diff": {"summary": "The origin returned 304 Not Modified for a saved validator; the stored page body remains unchanged."},
            "etag_available": bool(prior["etag"]), "last_modified": prior["last_modified"],
            "note": "Conditional recheck confirms no origin change for this URL. It does not prove that every linked tender document or corrigendum is unchanged.",
        }
    if not page or not page.get("text"):
        errors = fetched.get("errors", [])
        raise HTTPException(status_code=502, detail=f"TinyFish did not return page text. Details: {errors[:2]}")
    new_text = str(page.get("text") or "")
    old_text = str(prior["text"]) if prior else ""
    snap = save_snapshot(url, str(page.get("title") or (prior["title"] if prior else "Tender source")), new_text, page.get("etag"), page.get("last_modified"))
    return {
        "url": url,
        "title": page.get("title") or "Tender source",
        "checked_at": snap["checked_at"],
        "content_fingerprint": snap["hash"],
        "previous_fingerprint": prior["text_hash"] if prior else None,
        "fingerprint_note": "SHA-256 checksum of captured page text; not a digital signature.",
        "first_check": prior is None,
        "change_detected": bool(prior and prior["text_hash"] != snap["hash"]),
        "previous_checked_at": prior["checked_at"] if prior else None,
        "diff": summarize_change(old_text, new_text) if prior else {"summary": "Baseline created. Recheck this page later to compare future content."},
        "etag_available": bool(page.get("etag")),
        "last_modified": page.get("last_modified"),
        "scope_boundary": "Checked page text only. External linked PDFs and separate corrigenda must be inspected separately.",
        "note": ("Conditional validation was unsupported; a live Fetch retry was used. " if fallback_used else "") + "A textual change is a review signal, not a legal conclusion. Open the official notice and linked corrigenda before bidding.",
    }
