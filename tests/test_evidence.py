from app.evidence import normalize_evidence_text, parse_indian_currency_to_inr, verify_quote


def test_quotecheck_verifies_whitespace_and_unicode_normalization_only():
    source = "The bidder shall have\n average annual turnover of ₹2 crore."
    quote = "The bidder shall have average annual turnover of ₹2 crore."
    result = verify_quote(quote, source)
    assert result["verified"] is True
    assert result["badge"] == "QUOTE_VERIFIED_FETCH"


def test_quotecheck_does_not_accept_distributed_token_overlap():
    source = "The bidder may submit documents. CMMI appears in another unrelated section. ISO 27001 may be mentioned as an example only."
    fake_quote = "Bidder must hold CMMI Level 5 and ISO 27001 certification."
    result = verify_quote(fake_quote, source)
    assert result["verified"] is False
    assert result["badge"] == "UNVERIFIED_QUOTE"


def test_quotecheck_does_not_ignore_negation():
    assert not verify_quote("Udyam exemption is not applicable to this works contract.",
                            "Udyam exemption is applicable to this works contract.")["verified"]


def test_short_quotes_remain_unverified():
    result = verify_quote("EMD 4L", "EMD 4L")
    assert result["verified"] is False


def test_currency_parser_handles_indian_units_without_auto_exemption():
    assert parse_indian_currency_to_inr("Rs. 4,00,000/-") == 400000.0
    assert parse_indian_currency_to_inr("Rs. 2.5 Crore") == 25000000.0
    assert parse_indian_currency_to_inr("INR 15 Lakhs") == 1500000.0
    assert parse_indian_currency_to_inr("exempt as applicable") is None
    assert parse_indian_currency_to_inr("Nil") == 0.0


def test_normalization_preserves_content_order_and_words():
    assert normalize_evidence_text("No EMD required") != normalize_evidence_text("EMD required")
