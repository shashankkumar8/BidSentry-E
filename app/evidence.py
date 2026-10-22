"""Conservative evidence checks used by BidSentry-E.

Consequential tender checks use a direct normalized quote match. Fuzzy token overlap is
intentionally not accepted as proof because it can drop or reorder negation, amounts, and
exceptions. This module does not decide legal eligibility.
"""
from __future__ import annotations

import html
import re
import unicodedata
from typing import Any


def normalize_evidence_text(value: str | None) -> str:
    value = html.unescape(unicodedata.normalize("NFKC", value or ""))
    value = value.replace("\u00a0", " ")
    # Strip leading and trailing quotation marks and whitespace
    value = value.strip(" \t\r\n\"'“”‘’")
    return re.sub(r"\s+", " ", value).strip().casefold()


def verify_quote(quote: str | None, source_text: str | None, *, minimum_chars: int = 12) -> dict[str, Any]:
    """Verify a candidate quote by normalized direct substring matching only.

    Distinguishes exact normalized substring matches from partial/approximate token overlap.
    Ordinary token overlap is strictly rejected as proof, as it may drop or alter negations,
    currency amounts, percentages, or exceptions.
    """
    normalized_quote = normalize_evidence_text(quote)
    normalized_source = normalize_evidence_text(source_text)
    if len(normalized_quote) < minimum_chars:
        return {
            "verified": False,
            "badge": "UNVERIFIED_QUOTE",
            "match_type": "TOO_SHORT",
            "review_state": "NEEDS_HUMAN_REVIEW",
            "method": "normalized_exact_substring",
            "reason": f"Quote is shorter than {minimum_chars} normalized characters.",
        }
    if not normalized_source:
        return {
            "verified": False,
            "badge": "UNVERIFIED_QUOTE",
            "match_type": "NO_SOURCE_TEXT",
            "review_state": "NEEDS_HUMAN_REVIEW",
            "method": "normalized_exact_substring",
            "reason": "No independently fetched source text was available.",
        }

    verified = normalized_quote in normalized_source
    if verified:
        return {
            "verified": True,
            "badge": "QUOTE_VERIFIED_FETCH",
            "match_type": "EXACT_NORMALIZED_MATCH",
            "review_state": "VERIFIED",
            "method": "normalized_exact_substring",
            "reason": "Candidate quote appears as a normalized substring of the separate source snapshot.",
        }

    # Check for approximate / partial token overlap to provide specific diagnostic guidance
    quote_tokens = set(re.findall(r"\b[a-z0-9]+\b", normalized_quote))
    source_tokens = set(re.findall(r"\b[a-z0-9]+\b", normalized_source))
    overlap = len(quote_tokens & source_tokens) / max(1, len(quote_tokens))

    if overlap >= 0.60:
        return {
            "verified": False,
            "badge": "UNVERIFIED_QUOTE",
            "match_type": "PARTIAL_OR_UNCONFIRMED_OVERLAP",
            "review_state": "NEEDS_HUMAN_REVIEW",
            "method": "normalized_exact_substring",
            "reason": (
                "Partial text overlap detected, but verbatim quote was not found. "
                "High risk of altered numbers, omitted negation, or paraphrasing. Human review required."
            ),
        }

    return {
        "verified": False,
        "badge": "UNVERIFIED_QUOTE",
        "match_type": "NO_MATCH",
        "review_state": "NEEDS_HUMAN_REVIEW",
        "method": "normalized_exact_substring",
        "reason": "Candidate quote was not found verbatim in the separate source snapshot; manual review is required.",
    }


def parse_indian_currency_to_inr(raw_value: Any) -> float | None:
    """Parse a clearly formatted INR amount; ambiguous phrases or ranges remain None.

    This utility deliberately does not infer an exemption from the word 'exempt' and does
    not calculate percentage-based EMD. Those require tender-specific contextual review.
    """
    if raw_value is None or isinstance(raw_value, bool):
        return None
    if isinstance(raw_value, (int, float)):
        return float(raw_value) if raw_value >= 0 else None
    text = str(raw_value).strip().lower()
    if not text or text in {"unknown", "null", "n/a", "not specified", "none", "unresolved"}:
        return None
    if text in {"nil", "zero", "0", "rs. 0", "₹0", "inr 0", "no emd", "emd not required"}:
        return 0.0

    # Percentages are never parsed as absolute currency amounts
    if "%" in text:
        return None

    # Range check: e.g. "Rs. 500-1000" or "10 to 20 lakh" is ambiguous
    if re.search(r"\d+\s*(?:-|to)\s*\d+", text):
        return None

    # Do not treat free-text 'exempt' as zero; the exact amount might still be present,
    # and exemption applicability cannot be safely inferred from a single word.
    if "exempt" in text or "waiver" in text or "waived" in text:
        return None

    multiplier = 1.0
    if re.search(r"\b(crore|crores|cr)\b", text):
        multiplier = 10_000_000.0
    elif re.search(r"\b(lakh|lakhs|lac|lacs)\b", text):
        multiplier = 100_000.0
    elif re.search(r"\b(thousand|thousands|k)\b", text):
        multiplier = 1_000.0
    cleaned = text.replace(",", "").replace("₹", " ")
    match = re.search(r"(?<![a-z])(?:rs\.?\s*|inr\s*)?(\d+(?:\.\d+)?)", cleaned)
    if not match:
        return None
    # A percentage is a separate rule; never parse the percentage itself as INR.
    start = max(0, match.start() - 12)
    if re.search(r"\d\s*%", cleaned[start:match.start()]):
        return None
    return float(match.group(1)) * multiplier
