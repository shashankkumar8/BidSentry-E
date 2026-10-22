"""Evidence-first tender analysis. Every extracted clause retains an exact source quote.

This is a decision-support prototype, not a procurement/legal eligibility determination.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CLAUSE_TERMS = {
    "Eligibility": ["eligibility", "eligible", "qualification", "qualify", "disqualif"],
    "Financial": ["turnover", "net worth", "financial capability", "solvency", "revenue", "crore", "lakh"],
    "Experience": ["experience", "similar work", "past performance", "work order", "completion certificate"],
    "Security": ["emd", "earnest money", "bid security", "performance security", "security deposit"],
    "Compliance": ["iso ", "gst", "udyam", "msme", "pan", "epf", "esi", "license", "registration", "certification"],
    "Deadline / process": ["closing date", "submission deadline", "last date", "bid opening", "delivery period", "corrigendum", "amendment"],
}
MANDATORY = re.compile(r"\b(must|shall|required|mandatory|minimum|at least|not less than|only bidders|eligible only)\b", re.I)


def normalize_domain(url: str) -> str:
    # hostname excludes a port and avoids display-only domain confusion.
    return (urlsplit(url).hostname or "").lower().removeprefix("www.")


def source_type(url: str) -> str:
    host = normalize_domain(url)
    official_suffixes = ("etenders.gov.in", "eprocure.gov.in", "gem.gov.in", "gov.in", "nic.in")
    return "Official domain" if any(host == d or host.endswith("." + d) for d in official_suffixes) else "Other public source"


def split_clauses(text: str) -> list[str]:
    if not text:
        return []
    lines = [re.sub(r"\s+", " ", x).strip(" \t-*#>•") for x in text.splitlines()]
    out: list[str] = []
    for line in lines:
        if len(line) < 24:
            continue
        # Avoid giant page blobs; sentence splitting keeps the evidence legible.
        pieces = re.split(r"(?<=[.;!?])\s+(?=[A-Z₹])", line)
        for part in pieces:
            part = part.strip()
            if len(part) >= 24 and part not in out:
                out.append(part[:520])
    return out


def classify_clause(sentence: str) -> str | None:
    low = sentence.lower()
    matches = []
    for category, terms in CLAUSE_TERMS.items():
        if any(term in low for term in terms):
            matches.append(category)
    if not matches:
        return None
    # Priority categories help the table stay readable and deterministic.
    priority = ["Eligibility", "Financial", "Experience", "Security", "Compliance", "Deadline / process"]
    return next(cat for cat in priority if cat in matches)


def extract_clauses(text: str, profile: dict[str, Any] | None = None, limit: int = 9) -> list[dict[str, Any]]:
    profile = profile or {}
    clauses: list[dict[str, Any]] = []
    seen: set[str] = set()
    for sentence in split_clauses(text):
        category = classify_clause(sentence)
        if not category:
            continue
        key = sentence.casefold()
        if key in seen:
            continue
        seen.add(key)
        status = "Review"
        reason = "Clause found; verify the requirement against the complete tender schedule."
        if MANDATORY.search(sentence):
            status = "Mandatory — check"
            reason = "Mandatory language detected. Do not infer eligibility without checking the full clause."
        clauses.append({"category": category, "quote": sentence, "status": status, "reason": reason})
        if len(clauses) >= limit:
            break
    return clauses


def extract_deadline(text: str) -> str:
    if not text:
        return "Not extracted"
    contextual = re.search(
        r"(?:bid\s+closing|closing\s+date|submission\s+deadline|last\s+date\s+(?:of\s+)?submission|bid\s+submission\s+end|tender\s+due\s+date)[^\n.]{0,100}",
        text,
        flags=re.I,
    )
    region = contextual.group(0) if contextual else ""
    if not region:
        # Don't treat any random date on a notice as the bid deadline.
        return "Not extracted"
    date_pat = re.search(
        r"\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-][A-Za-z]{3,9}[/-]\d{2,4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})\b(?:[^\n]{0,18})",
        region,
        re.I,
    )
    return date_pat.group(0).strip(" :,-") if date_pat else "Not extracted"


def extract_money_mentions(text: str) -> list[str]:
    pattern = re.compile(r"(?:₹|INR\s*|Rs\.?\s*)\s?[\d,]+(?:\.\d+)?\s*(?:crore|crores|cr|lakh|lakhs|lac|lacs|million)?", re.I)
    found = []
    for m in pattern.finditer(text or ""):
        phrase = re.sub(r"\s+", " ", m.group(0)).strip()
        if phrase and phrase not in found:
            found.append(phrase)
    return found[:8]


def extract_min_turnover_crore(text: str) -> float | None:
    if not text:
        return None
    patterns = [
        r"(?:annual|average|minimum|minimum average)[^\n.]{0,90}?(?:turnover|revenue)[^\n.]{0,90}?(?:₹|INR\s*|Rs\.?\s*)?([\d,]+(?:\.\d+)?)\s*(crore|crores|cr|lakh|lakhs|lac|lacs)",
        r"(?:turnover|revenue)[^\n.]{0,90}?(?:at least|minimum|shall be|not less than)[^\n.]{0,40}?(?:₹|INR\s*|Rs\.?\s*)?([\d,]+(?:\.\d+)?)\s*(crore|crores|cr|lakh|lakhs|lac|lacs)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            amount = float(m.group(1).replace(",", ""))
            unit = m.group(2).lower()
            return amount if unit in ("crore", "crores", "cr") else amount / 100
    return None


def extract_min_experience_years(text: str) -> int | None:
    if not text:
        return None
    candidates = re.findall(
        r"(?:minimum\s+of|at\s+least|not\s+less\s+than|minimum|required\s+of)?\s*(\d{1,2})\s*(?:\+\s*)?years?[^\n.]{0,60}(?:experience|similar work|work experience|relevant work)",
        text,
        re.I,
    )
    return max((int(x) for x in candidates), default=None)


def extract_emd_requirement_lakh(text: str) -> float | None:
    """Conservatively parse an EMD/bid-security amount into lakh INR.

    A currency amount must follow the EMD label in the same semicolon-delimited
    segment. Reverse-order amounts, percentage-based rules, exclusions and exemptions
    are not inferred; those cases stay unknown for manual review.
    """
    label = re.compile(r"(?:earnest\s+money(?:\s+deposit)?|\bEMD\b|bid\s+security)", re.I)
    amount = re.compile(r"(?:₹|INR\s*|Rs\.?\s*)\s*([\d,]+(?:\.\d+)?)\s*(crores?|cr|lakhs?|lacs?|thousand|k)?", re.I)
    for line in (text or "").splitlines():
        # Do not let a nearby estimated-contract value become the EMD value after an
        # exemption statement or semicolon. Parse only the segment that names the EMD.
        for segment in line.split(";"):
            label_match = label.search(segment)
            if not label_match:
                continue
            context = segment[max(0, label_match.start() - 30):min(len(segment), label_match.end() + 100)]
            if re.search(r"(?:EMD|earnest\s+money|bid\s+security).{0,55}\b(?:exempt(?:ion)?|waiv(?:ed|er)|not\s+required|nil|no\s+emd)\b", context, re.I):
                continue
            tail = segment[label_match.end():]
            match = amount.search(tail[:100])
            if not match:
                continue
            prefix = tail[:match.start()]
            # Do not mistake an estimated tender/project value for the EMD amount
            # in percentage-based bid-security clauses (e.g. "EMD shall be 2% of
            # estimated cost Rs. 2 crore"). A percentage calculation requires a
            # separate, tender-specific rule and stays Unknown until reviewed.
            if re.search(r"\d\s*%", prefix) and re.search(
                r"(?:estimated|tender|contract|project)\s+(?:cost|value)", prefix, re.I
            ):
                continue
            try:
                value = float(match.group(1).replace(",", ""))
            except ValueError:
                continue
            unit = (match.group(2) or "inr").lower()
            if unit in ("crore", "crores", "cr"):
                inr = value * 10_000_000
            elif unit in ("lakh", "lakhs", "lac", "lacs"):
                inr = value * 100_000
            elif unit in ("thousand", "k"):
                inr = value * 1_000
            else:
                inr = value
            return inr / 100_000
    return None


def extract_procuring_authority(text: str) -> str:
    """Extract procuring organization or authority when supported by source text."""
    if not text:
        return "Unknown / Not specified"
    patterns = [
        r"(?:procuring\s+entity|procuring\s+authority|organization|department|issued\s+by|buyer|client|nodal\s+agency)[:\s]+([A-Z0-9][^\n.,;]{2,70})",
        r"(?:invites?\s+bids\s+on\s+behalf\s+of|on\s+behalf\s+of)[:\s]+([A-Z0-9][^\n.,;]{2,70})",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            clean = m.group(1).strip(" -:\t")
            if len(clean) >= 3 and not re.search(r"^(the|an?|terms|conditions|schedule)\b", clean, re.I):
                return clean
    return "Unknown / Not specified"


def extract_contract_type(text: str) -> str:
    """Conservatively determine contract category only when supported by source text.

    Do not infer goods/services simply because 'works' was not detected.
    Ambiguous and unstated types remain 'Unknown / Unspecified'.
    """
    if not text:
        return "Unknown / Unspecified"
    has_works = bool(re.search(r"\b(?:works?\s+contract|civil\s+works?|construction\s+works?|electrical\s+works?|maintenance\s+works?)\b", text, re.I))
    has_goods = bool(re.search(r"\b(?:supply|procurement\s+of\s+goods|supply\s+contract|supply\s+and\s+delivery|equipment|hardware)\b", text, re.I))
    has_services = bool(re.search(r"\b(?:services?|consultancy|maintenance|facility\s+management|support\s+services?)\b", text, re.I))

    found = []
    if has_works:
        found.append("Works")
    if has_goods:
        found.append("Goods")
    if has_services:
        found.append("Services")

    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        return "Mixed / " + " + ".join(found)
    return "Unknown / Unspecified"


def extract_estimated_value_crore(text: str) -> float | None:
    """Conservatively extract estimated tender or contract value in ₹ Crore."""
    if not text:
        return None
    patterns = [
        r"(?:estimated\s+(?:tender\s+|contract\s+|project\s+)?(?:cost|value)|approximate\s+(?:cost|value)|tender\s+value)[^\n:]{0,30}[:\s]+(?:₹|INR\s*|Rs\.?\s*)?([\d,]+(?:\.\d+)?)\s*(crores?|cr|lakhs?|lacs?|thousand|k)?",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            try:
                val = float(m.group(1).replace(",", ""))
            except ValueError:
                continue
            unit = (m.group(2) or "inr").lower()
            if unit in ("crore", "crores", "cr"):
                return val
            elif unit in ("lakh", "lakhs", "lac", "lacs"):
                return val / 100.0
            elif unit in ("thousand", "k"):
                return val / 10000.0
            else:
                return val / 10_000_000.0 if val > 100_000 else val
    return None


def extract_required_certs(text: str) -> list[str]:
    supported = ["ISO 9001", "ISO 27001", "CMMI", "BIS", "CE", "FSSAI", "GST", "PAN", "Udyam"]
    found = []
    for cert in supported:
        # Use word boundaries to avoid false positives (e.g. 'ce' in 'accepted' or 'pan' in 'company')
        pattern = re.compile(rf"\b{re.escape(cert)}\b", re.I)
        for sentence in split_clauses(text):
            if pattern.search(sentence) and MANDATORY.search(sentence):
                if cert not in found:
                    found.append(cert)
    return found


def generate_clause_ledger(
    turnover_required: float | None,
    years_required: int | None,
    emd_required_lakh: float | None,
    emd_mentioned: bool,
    required_certs: list[str],
    msme_mentioned: bool,
    profile: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build a structured ledger of qualification clauses with explicit states.

    Preserves at least: MET, POTENTIAL_BLOCKER, UNKNOWN_PROOF_MISSING, UNVERIFIED_QUOTE, NEEDS_HUMAN_REVIEW.
    """
    ledger: list[dict[str, Any]] = []

    # 1. Turnover Requirement
    if turnover_required is not None:
        raw_to = profile.get("turnover_crore")
        if raw_to is None:
            ledger.append({
                "category": "Financial / Turnover",
                "requirement": f"Average annual turnover of at least ₹{turnover_required:g} Crore",
                "source_quote": f"Turnover requirement ₹{turnover_required:g} Crore extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Not declared",
                "state": "UNKNOWN_PROOF_MISSING",
                "comparison_logic": f"Tender requires ₹{turnover_required:g} Cr; supplier has not declared turnover figure.",
                "suggested_action": "Declare verified annual turnover from audited financials.",
            })
        elif float(raw_to) >= turnover_required:
            ledger.append({
                "category": "Financial / Turnover",
                "requirement": f"Average annual turnover of at least ₹{turnover_required:g} Crore",
                "source_quote": f"Turnover requirement ₹{turnover_required:g} Crore extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"₹{float(raw_to):g} Crore",
                "state": "MET",
                "comparison_logic": f"Declared turnover (₹{float(raw_to):g} Cr) meets or exceeds threshold (₹{turnover_required:g} Cr).",
                "suggested_action": "Verify CA turnover certificate and averaging financial years.",
            })
        else:
            ledger.append({
                "category": "Financial / Turnover",
                "requirement": f"Average annual turnover of at least ₹{turnover_required:g} Crore",
                "source_quote": f"Turnover requirement ₹{turnover_required:g} Crore extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"₹{float(raw_to):g} Crore",
                "state": "POTENTIAL_BLOCKER",
                "comparison_logic": f"Declared turnover (₹{float(raw_to):g} Cr) is below required threshold (₹{turnover_required:g} Cr).",
                "suggested_action": "Review whether consortium / JV or startup relaxation applies.",
            })
    else:
        ledger.append({
            "category": "Financial / Turnover",
            "requirement": "Annual turnover threshold",
            "source_quote": "No unambiguous turnover clause detected in fetched text.",
            "evidence_verification": "NEEDS_HUMAN_REVIEW",
            "supplier_declared": f"₹{profile.get('turnover_crore', 'Not declared')} Cr" if profile.get("turnover_crore") is not None else "Not declared",
            "state": "NEEDS_HUMAN_REVIEW",
            "comparison_logic": "Turnover threshold could not be safely extracted from fetched text.",
            "suggested_action": "Inspect full tender notice financial evaluation section manually.",
        })

    # 2. Similar Work / Experience Requirement
    if years_required is not None:
        raw_yr = profile.get("years_experience")
        if raw_yr is None:
            ledger.append({
                "category": "Experience / Similar Work",
                "requirement": f"Minimum {years_required} years of relevant experience",
                "source_quote": f"Experience requirement {years_required} years extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Not declared",
                "state": "UNKNOWN_PROOF_MISSING",
                "comparison_logic": f"Tender requires {years_required} years; supplier has not declared experience.",
                "suggested_action": "Declare completed similar work experience years.",
            })
        elif int(raw_yr) >= years_required:
            ledger.append({
                "category": "Experience / Similar Work",
                "requirement": f"Minimum {years_required} years of relevant experience",
                "source_quote": f"Experience requirement {years_required} years extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"{int(raw_yr)} years",
                "state": "MET",
                "comparison_logic": f"Declared experience ({int(raw_yr)} yrs) meets or exceeds threshold ({years_required} yrs).",
                "suggested_action": "Review work orders and completion certificates against similar-work definitions.",
            })
        else:
            ledger.append({
                "category": "Experience / Similar Work",
                "requirement": f"Minimum {years_required} years of relevant experience",
                "source_quote": f"Experience requirement {years_required} years extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"{int(raw_yr)} years",
                "state": "POTENTIAL_BLOCKER",
                "comparison_logic": f"Declared experience ({int(raw_yr)} yrs) is below required threshold ({years_required} yrs).",
                "suggested_action": "Check if past work contracts or joint venture credentials can be utilized.",
            })
    else:
        ledger.append({
            "category": "Experience / Similar Work",
            "requirement": "Similar work experience threshold",
            "source_quote": "No unambiguous experience clause detected in fetched text.",
            "evidence_verification": "NEEDS_HUMAN_REVIEW",
            "supplier_declared": f"{profile.get('years_experience', 'Not declared')} years" if profile.get("years_experience") is not None else "Not declared",
            "state": "NEEDS_HUMAN_REVIEW",
            "comparison_logic": "Experience threshold could not be safely extracted from fetched text.",
            "suggested_action": "Inspect technical specification and past experience schedule.",
        })

    # 3. EMD / Bid Security Requirement
    if emd_required_lakh is not None:
        raw_emd = profile.get("emd_budget_lakh")
        if raw_emd is None:
            ledger.append({
                "category": "EMD / Bid Security",
                "requirement": f"EMD / Bid Security of ₹{emd_required_lakh:g} Lakh",
                "source_quote": f"EMD amount ₹{emd_required_lakh:g} Lakh extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Not declared",
                "state": "UNKNOWN_PROOF_MISSING",
                "comparison_logic": f"Tender specifies ₹{emd_required_lakh:g} Lakh; supplier has not declared EMD capacity.",
                "suggested_action": "Check bank guarantee / FDR limits or verify tender-specific exemption rules.",
            })
        elif float(raw_emd) >= emd_required_lakh:
            ledger.append({
                "category": "EMD / Bid Security",
                "requirement": f"EMD / Bid Security of ₹{emd_required_lakh:g} Lakh",
                "source_quote": f"EMD amount ₹{emd_required_lakh:g} Lakh extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"₹{float(raw_emd):g} Lakh",
                "state": "MET",
                "comparison_logic": f"Declared capacity (₹{float(raw_emd):g} Lakh) covers EMD requirement (₹{emd_required_lakh:g} Lakh).",
                "suggested_action": "Verify acceptable payment instruments (BG, DD, online portal gateway).",
            })
        else:
            ledger.append({
                "category": "EMD / Bid Security",
                "requirement": f"EMD / Bid Security of ₹{emd_required_lakh:g} Lakh",
                "source_quote": f"EMD amount ₹{emd_required_lakh:g} Lakh extracted from source.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"₹{float(raw_emd):g} Lakh",
                "state": "POTENTIAL_BLOCKER",
                "comparison_logic": f"Declared capacity (₹{float(raw_emd):g} Lakh) is below EMD requirement (₹{emd_required_lakh:g} Lakh).",
                "suggested_action": "Review whether MSME / Udyam exemption applies specifically for this tender category.",
            })
    elif emd_mentioned:
        ledger.append({
            "category": "EMD / Bid Security",
            "requirement": "EMD clause mentioned without explicit single amount",
            "source_quote": "EMD or Bid Security mentioned in fetched text; numeric amount unresolved.",
            "evidence_verification": "NEEDS_HUMAN_REVIEW",
            "supplier_declared": f"₹{profile.get('emd_budget_lakh', 'Not declared')} Lakh" if profile.get("emd_budget_lakh") is not None else "Not declared",
            "state": "NEEDS_HUMAN_REVIEW",
            "comparison_logic": "EMD clause is present, but numeric amount or percentage formula requires manual reading.",
            "suggested_action": "Inspect EMD section of NIT for percentage calculation or exemption details.",
        })

    # 4. Mandatory Certifications
    raw_certs = profile.get("certifications")
    profile_certs = {str(x).strip().lower() for x in (raw_certs or []) if str(x).strip()} if raw_certs is not None else None
    for cert in required_certs:
        if profile_certs is None:
            ledger.append({
                "category": "Compliance / Certification",
                "requirement": f"Mandatory {cert} registration / certification",
                "source_quote": f"Mandatory certification requirement for {cert} detected.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Not declared",
                "state": "UNKNOWN_PROOF_MISSING",
                "comparison_logic": f"Tender requires {cert}; supplier certification profile is undeclared.",
                "suggested_action": f"Provide valid {cert} certificate copy or confirm validity.",
            })
        elif cert.lower() in profile_certs:
            ledger.append({
                "category": "Compliance / Certification",
                "requirement": f"Mandatory {cert} registration / certification",
                "source_quote": f"Mandatory certification requirement for {cert} detected.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": f"Holds {cert}",
                "state": "MET",
                "comparison_logic": f"Declared certifications include {cert}.",
                "suggested_action": f"Verify {cert} issuing body accreditation and expiry date.",
            })
        else:
            ledger.append({
                "category": "Compliance / Certification",
                "requirement": f"Mandatory {cert} registration / certification",
                "source_quote": f"Mandatory certification requirement for {cert} detected.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Not held",
                "state": "POTENTIAL_BLOCKER",
                "comparison_logic": f"Tender mandates {cert}, which is absent from supplier profile.",
                "suggested_action": f"Acquire {cert} or evaluate if equivalent standard is acceptable.",
            })

    # 5. MSME / Udyam Applicability
    if msme_mentioned:
        udyam_status = profile.get("udyam_registered")
        if udyam_status is True:
            ledger.append({
                "category": "Policy / MSME Preference",
                "requirement": "MSME / Udyam provisions noted in notice",
                "source_quote": "Tender mentions MSME/Udyam provisions.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Udyam registered",
                "state": "MET",
                "comparison_logic": "Supplier is Udyam-registered; review tender for applicable purchase preference or EMD waiver.",
                "suggested_action": "Attach valid Udyam Registration Certificate with appropriate NIC code.",
            })
        elif udyam_status is False:
            ledger.append({
                "category": "Policy / MSME Preference",
                "requirement": "MSME / Udyam provisions noted in notice",
                "source_quote": "Tender mentions MSME/Udyam provisions.",
                "evidence_verification": "QUOTE_VERIFIED_FETCH",
                "supplier_declared": "Not registered",
                "state": "NEEDS_HUMAN_REVIEW",
                "comparison_logic": "Supplier is not Udyam registered; verify whether MSME status is a mandatory criterion or an optional preference.",
                "suggested_action": "Check if non-MSME bids are accepted without penalty.",
            })
        else:
            ledger.append({
                "category": "Policy / MSME Preference",
                "requirement": "MSME / Udyam provisions noted in notice",
                "source_quote": "Tender mentions MSME/Udyam provisions.",
                "evidence_verification": "NEEDS_HUMAN_REVIEW",
                "supplier_declared": "Not declared",
                "state": "UNKNOWN_PROOF_MISSING",
                "comparison_logic": "MSME policy mentioned; supplier registration status is undeclared.",
                "suggested_action": "Declare Udyam registration status if registered.",
            })

    return ledger


def profile_assessment(text: str, profile: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    unknowns: list[str] = []
    matches: list[str] = []

    turnover_required = extract_min_turnover_crore(text)
    if turnover_required is not None:
        raw_turnover = profile.get("turnover_crore")
        if raw_turnover is None:
            unknowns.append("A turnover threshold appears in fetched text, but the supplier has not declared turnover.")
        else:
            have = float(raw_turnover)
            if have >= turnover_required:
                matches.append(f"Declared turnover meets the extracted threshold of ₹{turnover_required:g} crore; financial proof and averaging period still need review.")
            else:
                blockers.append(f"Potential turnover gap: fetched text appears to require ₹{turnover_required:g} crore; the declared profile reports ₹{have:g} crore.")
    else:
        unknowns.append("Minimum turnover threshold was not reliably extracted from the fetched text.")

    years_required = extract_min_experience_years(text)
    if years_required is not None:
        raw_years = profile.get("years_experience")
        if raw_years is None:
            unknowns.append("An experience threshold appears in fetched text, but the supplier has not declared relevant experience.")
        else:
            have_years = int(raw_years)
            if have_years >= years_required:
                matches.append(f"Declared experience meets the extracted threshold of {years_required} years; similar-work scope, recency, and work orders still need review.")
            else:
                blockers.append(f"Potential experience gap: fetched text appears to require {years_required} years; the declared profile reports {have_years} years.")
    else:
        unknowns.append("Minimum relevant-experience threshold was not reliably extracted.")

    emd_required_lakh = extract_emd_requirement_lakh(text)
    emd_mentioned = bool(re.search(r"earnest\s+money|\bEMD\b|bid\s+security", text or "", re.I))
    if emd_required_lakh is not None:
        raw_emd_budget = profile.get("emd_budget_lakh")
        if raw_emd_budget is None:
            unknowns.append("The fetched text states an EMD/bid-security amount, but the supplier has not declared available bid-security capacity.")
        else:
            emd_budget_lakh = float(raw_emd_budget)
            if emd_budget_lakh >= emd_required_lakh:
                matches.append(f"Declared bid-security capacity of ₹{emd_budget_lakh:g} lakh covers the parsed ₹{emd_required_lakh:g} lakh amount; payment instrument, validity period and tender terms still need review.")
            else:
                blockers.append(f"Potential bid-security capacity gap: fetched text appears to state ₹{emd_required_lakh:g} lakh, while the declared capacity is ₹{emd_budget_lakh:g} lakh. Check tender-specific exemptions, accepted instruments and purchaser rules before deciding.")
    elif emd_mentioned:
        unknowns.append("An EMD/bid-security clause appears in the fetched text, but a numeric amount could not be safely extracted.")
    else:
        unknowns.append("No numeric EMD/bid-security amount was reliably extracted from the fetched page text.")

    certs = extract_required_certs(text)
    raw_certifications = profile.get("certifications")
    profile_certs = {str(x).strip().lower() for x in (raw_certifications or []) if str(x).strip()}
    for cert in certs:
        if raw_certifications is None:
            unknowns.append(f"{cert} appears in a possible mandatory clause, but the supplier's certification profile was not declared.")
        elif cert.lower() in profile_certs:
            matches.append(f"Profile lists {cert}; verify validity, issuing authority, and the tender's precise scope.")
        else:
            blockers.append(f"Potential certification/registration gap: fetched text appears to make {cert} mandatory, but it is not listed in the declared profile.")
    if not certs:
        unknowns.append("No supported mandatory certificate could be confidently extracted.")

    if re.search(r"\b(msme|micro\s+and\s+small|udyam)\b", text or "", re.I):
        if profile.get("udyam_registered") is True:
            matches.append("Profile indicates Udyam registration; confirm the tender-specific MSE conditions.")
        elif profile.get("udyam_registered") is False:
            unknowns.append("The notice mentions MSME/Udyam; profile indicates no Udyam registration. Check whether this is a preference or a requirement.")
        else:
            unknowns.append("MSME/Udyam is mentioned; vendor registration status is unknown.")

    if blockers:
        status = "Potential blocker"
    elif unknowns:
        status = "Human review needed"
    else:
        status = "No obvious blocker found"

    # Compact source excerpts help a reviewer inspect the basis of the extracted checks.
    # Excerpts are direct trimmed lines from the fetched source, not model-generated summaries.
    evidence_quotes: list[dict[str, str]] = []
    evidence_patterns = [
        ("Financial / turnover", re.compile(r"turnover|revenue|net worth|solvency|crore|lakh", re.I)),
        ("Experience", re.compile(r"experience|similar work|past performance|work order|completion certificate", re.I)),
        ("EMD / bid security", re.compile(r"earnest\s+money|\bEMD\b|bid\s+security", re.I)),
        ("Certificates / registrations", re.compile(r"\b(?:ISO\s*9001|ISO\s*27001|CMMI|BIS|CE|FSSAI|GST|PAN|Udyam)\b", re.I)),
        ("Deadline / corrigendum", re.compile(r"closing date|submission deadline|last date|bid opening|corrigendum|amendment", re.I)),
    ]
    seen_evidence: set[str] = set()
    for source_line in (text or "").splitlines():
        quote = source_line.strip()
        if len(quote) < 16 or len(quote) > 900 or quote in seen_evidence:
            continue
        for category, pattern in evidence_patterns:
            if pattern.search(quote):
                evidence_quotes.append({"category": category, "quote": quote})
                seen_evidence.add(quote)
                break
        if len(evidence_quotes) >= 12:
            break

    msme_mentioned = bool(re.search(r"\b(msme|micro\s+and\s+small|udyam)\b", text or "", re.I))
    ledger = generate_clause_ledger(
        turnover_required=turnover_required,
        years_required=years_required,
        emd_required_lakh=emd_required_lakh,
        emd_mentioned=emd_mentioned,
        required_certs=certs,
        msme_mentioned=msme_mentioned,
        profile=profile,
    )

    return {
        "status": status,
        "potential_blockers": blockers,
        "matches": matches,
        "unknowns": unknowns,
        "turnover_threshold_crore": turnover_required,
        "experience_threshold_years": years_required,
        "emd_requirement_lakh": emd_required_lakh,
        "required_certifications": certs,
        "evidence_quotes": evidence_quotes,
        "clause_ledger": ledger,
        "disclaimer": "Pre-screen only. The complete tender schedule, corrigenda, supporting records and official procurement rules govern the final decision. Udyam/EMD/turnover relaxations are not automatically applied; verify the purchaser, procurement category, current policy and tender wording.",
    }


def relevance_score(profile: dict[str, Any], tender: dict[str, Any]) -> float:
    profile_text = " ".join([
        str(profile.get("keywords", "")),
        str(profile.get("sector", "")),
        str(profile.get("location", "")),
        " ".join(str(x) for x in (profile.get("certifications") or [])),
    ]).strip()
    document = " ".join([str(tender.get("title", "")), str(tender.get("snippet", "")), str(tender.get("content", "")[:3000])]).strip()
    if not profile_text or not document:
        return 0.0
    try:
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=2500).fit_transform([profile_text, document])
        semantic = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        semantic = 0.0
    profile_tokens = {t for t in re.findall(r"[a-z0-9]+", profile_text.lower()) if len(t) > 2}
    doc_tokens = {t for t in re.findall(r"[a-z0-9]+", document.lower()) if len(t) > 2}
    overlap = len(profile_tokens & doc_tokens) / max(1, len(profile_tokens))
    return round(max(0.0, min(100.0, (semantic * 0.70 + overlap * 0.30) * 100)), 1)


def build_tender_result(search_row: dict[str, Any], page: dict[str, Any] | None, profile: dict[str, Any]) -> dict[str, Any]:
    page = page or {}
    text = str(page.get("text") or "")
    title = str(page.get("title") or search_row.get("title") or "Untitled tender notice")
    url = str(page.get("final_url") or search_row.get("url") or "")
    source_status = source_type(url)
    # Search snippets help discovery and relevance only. They are truncated, may omit
    # exceptions/context, and are not accepted as evidence for a blocker. Retrieved
    # third-party mirrors can help locate a notice, but cannot trigger an assessment
    # until the corresponding official-domain source has been fetched.
    assessment_text = text[:12000] if text else ""
    if source_status == "Official domain" and assessment_text:
        assessment = profile_assessment(assessment_text, profile)
    else:
        assessment = {
            "status": "Human review needed",
            "potential_blockers": [],
            "matches": [],
            "unknowns": [
                "No readable official-domain source text is available for a profile assessment. Open the official notice and its complete schedule manually."
            ],
            "clause_ledger": [],
            "disclaimer": "Pre-screen only. Third-party search snippets/mirrors and incomplete pages cannot establish eligibility. Verify the purchaser's official notice and linked documents."
        }
    clauses = extract_clauses(assessment_text, profile) if text else []
    deadline = extract_deadline(assessment_text)
    procuring_authority = extract_procuring_authority(assessment_text)
    contract_type = extract_contract_type(assessment_text)
    estimated_value_crore = extract_estimated_value_crore(assessment_text)
    fetch_status = "FETCHED" if text else ("UNRESOLVED_FETCH_ERROR" if (page.get("error") or not page) else "METADATA_ONLY")
    content_fingerprint = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest() if text else None

    status_text = (title + " " + text[:1800]).lower()
    if any(term in status_text for term in ("corrigendum", "addendum", "amendment", "extension of last date")):
        flags = ["Possible amendment/corrigendum: open the official notice and verify the latest version."]
    else:
        flags = []
    if deadline == "Not extracted":
        flags.append("Closing date not reliably extracted; verify the official tender page.")
    if source_status != "Official domain":
        flags.append("Non-official result domain: locate and verify the corresponding official notice before acting.")
    if not text:
        flags.append("TinyFish did not return readable page text; search metadata is shown for discovery only and cannot trigger a blocker.")
    return {
        "id": str(abs(hash(url)) % 10_000_000),
        "title": title,
        "url": url,
        "domain": normalize_domain(url),
        "source_status": source_status,
        "procuring_authority": procuring_authority,
        "contract_type": contract_type,
        "estimated_value_crore": estimated_value_crore,
        "fetch_status": fetch_status,
        "content_fingerprint": content_fingerprint,
        "fingerprint_note": "SHA-256 checksum of retrieved page text; not a digital signature or legal proof of authenticity.",
        "etag": page.get("etag"),
        "last_modified": page.get("last_modified"),
        "snippet": str(search_row.get("snippet") or ""),
        "content": text[:16000],
        "deadline": deadline,
        "money_mentions": extract_money_mentions(assessment_text),
        "relevance_score": relevance_score(profile, {"title": title, "snippet": search_row.get("snippet", ""), "content": text}),
        "assessment": assessment,
        "assessment_basis": ("Fetched official-domain page text" if source_status == "Official domain" else "Non-official fetched text — discovery only; excluded from profile assessment") if text else "No readable fetched text; search snippet is discovery metadata only",
        "clauses": clauses,
        "risk_flags": flags,
        "fetched": bool(text),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def summarize_change(old_text: str, new_text: str) -> dict[str, Any]:
    old_lines = [x.strip() for x in (old_text or "").splitlines() if x.strip()]
    new_lines = [x.strip() for x in (new_text or "").splitlines() if x.strip()]
    old_set, new_set = set(old_lines), set(new_lines)
    added = list(new_set - old_set)[:8]
    removed = list(old_set - new_set)[:8]
    # Identify high-signal changed clauses without claiming the diff itself means a legal change.
    hot_terms = ("deadline", "closing", "submission", "emd", "earnest money", "turnover", "experience", "corrigendum", "mandatory", "shall", "must")
    hot = [line for line in added + removed if any(term in line.lower() for term in hot_terms)][:6]

    # Map changed lines to affected procurement topics
    affected_topics = []
    combined_changed = " ".join(added + removed).lower()
    topic_keywords = [
        ("EMD / Bid Security", ["emd", "earnest money", "bid security"]),
        ("Turnover / Financial Threshold", ["turnover", "crore", "lakh", "net worth", "solvency"]),
        ("Experience / Completed Work", ["experience", "similar work", "completion certificate", "work order"]),
        ("Mandatory Certifications", ["iso", "cmmi", "bis", "ce", "fssai", "gst", "pan", "udyam"]),
        ("Submission Deadline", ["closing date", "submission deadline", "last date", "due date", "bid opening"]),
        ("Corrigenda / Scope Amendments", ["corrigendum", "addendum", "amendment", "extension", "rectification"]),
    ]
    for topic, kw_list in topic_keywords:
        if any(kw in combined_changed for kw in kw_list):
            affected_topics.append(topic)

    return {
        "added": added,
        "removed": removed,
        "high_signal_lines": hot,
        "affected_topics": affected_topics,
        "summary": "Text changed; manually compare the official notice and all linked corrigenda." if (added or removed) else "No text difference detected in the returned page content."
    }
