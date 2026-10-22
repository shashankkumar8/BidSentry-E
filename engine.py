"""Standalone smoke runner for BidSentry-E's deterministic evidence core.

This CLI intentionally runs synthetic examples only. It does not claim to perform a live
TinyFish request; configure the API key and use the web workbench for live Search/Fetch/Agent.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output on Windows consoles to prevent cp1252 charmap encoding errors
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from app.analyzer import extract_clauses, profile_assessment
from app.audit import new_audit_id, record_api_call
from app.evidence import parse_indian_currency_to_inr, verify_quote

ROOT = Path(__file__).resolve().parent


def run_local_smoke() -> dict:
    started = time.perf_counter()
    source = (
        "SYNTHETIC BENCHMARK NOTICE — not a real tender.\n"
        "The bidder shall have average annual turnover of at least Rs. 2 crore during the last three financial years.\n"
        "Bidders must furnish an Earnest Money Deposit (EMD) of Rs. 4,00,000/- through an accepted instrument.\n"
        "The bidder must hold a valid ISO 9001 certification.\n"
        "Bid closing date: 30-Oct-2026 15:00 IST."
    )
    profile = {
        "turnover_crore": 1.2,
        "years_experience": None,
        "emd_budget_lakh": 1.0,
        "certifications": ["GST"],
        "udyam_registered": None,
    }
    quote = "The bidder shall have average annual turnover of at least Rs. 2 crore during the last three financial years."
    hallucinated_quote = "Bidder must hold CMMI Level 5 and ISO 27001 certification."
    result = {
        "mode": "LOCAL_SYNTHETIC_SMOKE_TEST",
        "notice": "All source text below is synthetic. This CLI run is not a TinyFish live integration test.",
        "quotecheck": {
            "source_quote": verify_quote(quote, source),
            "hallucinated_quote": verify_quote(hallucinated_quote, source),
        },
        "parsed_currency_examples": {
            "rs_4_lakh": parse_indian_currency_to_inr("Rs. 4,00,000/-"),
            "two_crore": parse_indian_currency_to_inr("Rs. 2 crore"),
            "exemption_phrase_is_not_zero": parse_indian_currency_to_inr("exempt as applicable"),
        },
        "candidate_clauses": extract_clauses(source),
        "assessment": profile_assessment(source, profile),
    }
    result["duration_ms"] = round((time.perf_counter() - started) * 1000, 2)
    result["audit_id"] = new_audit_id()
    result["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    record_api_call(
        audit_id=result["audit_id"], method="CLI", endpoint="engine.py:synthetic-smoke",
        status_code=200, duration_ms=result["duration_ms"],
    )
    return result


if __name__ == "__main__":
    print(json.dumps(run_local_smoke(), indent=2, ensure_ascii=False))
