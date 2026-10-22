from app.analyzer import (
    build_tender_result,
    extract_clauses,
    extract_deadline,
    extract_emd_requirement_lakh,
    extract_min_experience_years,
    extract_min_turnover_crore,
    profile_assessment,
    relevance_score,
    source_type,
    summarize_change,
)


def test_extracts_turnover_in_crore():
    text = "The bidder shall have average annual turnover of at least Rs. 2.5 crore during the last three years."
    assert extract_min_turnover_crore(text) == 2.5


def test_extracts_turnover_in_lakh():
    text = "Minimum average annual turnover should be ₹50 lakh for the previous financial years."
    assert extract_min_turnover_crore(text) == 0.5


def test_extracts_experience_when_explicit():
    assert extract_min_experience_years("Bidder must have at least 3 years of relevant work experience.") == 3


def test_deadline_requires_closing_context():
    assert extract_deadline("Notice issued on 20 October 2026. Work commences 1 December 2026.") == "Not extracted"
    assert "27-Oct-2026" in extract_deadline("Bid closing date: 27-Oct-2026 03:00 PM")


def test_clause_quotes_are_verbatim_fragments():
    text = "Eligibility criteria\nThe bidder shall have ISO 9001 certification.\nBids must be submitted before the closing date."
    clauses = extract_clauses(text)
    assert any("ISO 9001" in c["quote"] for c in clauses)
    assert all(c["quote"] in text for c in clauses)


def test_profile_assessment_never_claims_final_eligibility():
    text = "The bidder shall have average annual turnover of at least Rs. 2 crore and must have at least 5 years of work experience."
    result = profile_assessment(text, {"turnover_crore": 1.0, "years_experience": 2, "certifications": [], "udyam_registered": None})
    assert result["status"] == "Potential blocker"
    assert result["potential_blockers"]
    assert "complete tender schedule" in result["disclaimer"].lower()
    assert result["status"] != "Eligible"


def test_profile_does_not_get_false_clearance_when_requirements_unknown():
    result = profile_assessment("Public tender: network support services.", {"turnover_crore": 10, "years_experience": 20, "certifications": ["ISO 9001"]})
    assert result["status"] == "Human review needed"
    assert result["unknowns"]


def test_tfidf_relevance_is_bounded():
    score = relevance_score({"keywords": "network maintenance", "sector": "IT"}, {"title": "Network maintenance tender", "snippet": "IT maintenance", "content": ""})
    assert 0 <= score <= 100


def test_official_domain_detection():
    assert source_type("https://www.etenders.gov.in/eprocure/app") == "Official domain"
    assert source_type("https://example.com/tender") == "Other public source"


def test_change_summary_marks_high_signal_added_lines():
    out = summarize_change("Bid closing date: 25-Oct-2026", "Bid closing date: 30-Oct-2026")
    assert out["added"]
    assert out["high_signal_lines"]


def test_search_snippet_not_used_as_assessment_evidence():
    result = build_tender_result(
        {"title": "Snippet-only", "url": "https://etenders.gov.in/tender/1", "snippet": "The bidder shall have average annual turnover of at least Rs. 99 crore."},
        {"url": "https://etenders.gov.in/tender/1", "text": ""},
        {"turnover_crore": 1.0, "years_experience": 3, "certifications": []},
    )
    assert result["assessment"]["potential_blockers"] == []
    assert result["assessment"]["status"] == "Human review needed"
    assert result["clauses"] == []
    assert result["assessment_basis"].startswith("No readable fetched text")


def test_missing_supplier_numbers_are_unknown_not_zero():
    result = profile_assessment(
        "The bidder shall have average annual turnover of at least Rs. 2 crore and must have at least 5 years of relevant work experience.",
        {"turnover_crore": None, "years_experience": None, "certifications": None, "udyam_registered": None},
    )
    assert result["status"] == "Human review needed"
    assert result["potential_blockers"] == []
    assert any("has not declared turnover" in item for item in result["unknowns"])
    assert any("has not declared relevant experience" in item for item in result["unknowns"])


def test_lookalike_host_is_not_official():
    assert source_type("https://etenders.gov.in.attacker.example/tender") == "Other public source"
    assert source_type("https://etenders.gov.in:443/tender") == "Official domain"


def test_emd_amount_parsing_is_scoped_to_emd_label():
    assert extract_emd_requirement_lakh("EMD: Rs. 50,000") == 0.5
    assert extract_emd_requirement_lakh("Earnest Money Deposit of ₹1.5 lakh") == 1.5
    assert extract_emd_requirement_lakh("EMD: Rs. 1,50,000/-") == 1.5
    # It does not treat the word 'exempt' as a zero amount or infer an exemption.
    assert extract_emd_requirement_lakh("EMD exemption not applicable; estimated cost Rs. 10 lakh") is None
    # A percentage-based EMD rule must not interpret the tender value as the EMD.
    assert extract_emd_requirement_lakh("EMD shall be 2% of estimated cost Rs. 2 crore") is None


def test_emd_shortfall_is_only_a_potential_gap_and_carries_evidence():
    result = profile_assessment(
        "Tender Security: EMD of Rs. 50,000 must accompany the bid.",
        {"turnover_crore": 1.0, "years_experience": 3, "emd_budget_lakh": 0.2, "certifications": [], "udyam_registered": True},
    )
    assert result["status"] == "Potential blocker"
    assert any("tender-specific exemptions" in item for item in result["potential_blockers"])
    assert result["emd_requirement_lakh"] == 0.5
    assert any(q["category"] == "EMD / bid security" for q in result["evidence_quotes"])


def test_non_official_fetched_page_cannot_trigger_blocker():
    result = build_tender_result(
        {"title": "Third-party mirror", "url": "https://example.com/tender/1", "snippet": ""},
        {"url": "https://example.com/tender/1", "text": "The bidder shall have average annual turnover of at least Rs. 99 crore."},
        {"turnover_crore": 1.0, "years_experience": 3, "certifications": []},
    )
    assert result["assessment"]["potential_blockers"] == []
    assert result["assessment"]["status"] == "Human review needed"
    assert "excluded from profile assessment" in result["assessment_basis"]
