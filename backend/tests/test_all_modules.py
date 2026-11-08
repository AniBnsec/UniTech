import pytest
from app.modules.url_analyzer import URLAnalyzer, calculate_shannon_entropy, is_safe_public_ip
from app.modules.tls_analyzer import TLSAnalyzer
from app.modules.ai_scam_analyzer import AIScamAnalyzer
from app.modules.web3_service import Web3Service
from app.core.risk_engine import RiskEngine
from app.schemas.threat import IndicatorSeverity, RiskClassification

def test_entropy_and_ssrf_guards():
    # Entropy
    assert calculate_shannon_entropy("aaaaaa") == 0.0
    assert calculate_shannon_entropy("89a3f!c2x_9zQ") > 3.0

    # SSRF IP Guards
    assert not is_safe_public_ip("127.0.0.1")
    assert not is_safe_public_ip("10.0.0.5")
    assert not is_safe_public_ip("192.168.1.1")
    assert not is_safe_public_ip("169.254.169.254")  # AWS metadata
    assert is_safe_public_ip("8.8.8.8")
    assert is_safe_public_ip("104.244.42.1")

def test_url_homoglyph_and_typosquatting():
    # Typosquatting test: paypaI-security-update.com
    host, domain, ip, indicators = URLAnalyzer.inspect_lexical_indicators("https://paypaI-security-update.com/login")
    assert any("Typosquatting" in ind.category or "Brand Impersonation" in ind.category for ind in indicators)

    # Clean domain test
    _, _, _, clean_indicators = URLAnalyzer.inspect_lexical_indicators("https://www.google.com")
    assert not any(ind.severity in [IndicatorSeverity.CRITICAL, IndicatorSeverity.HIGH] for ind in clean_indicators)

def test_tls_emudhra_compromised_ca_detection():
    # Check simulated eMudhra compromised CA domain
    details, indicators = TLSAnalyzer.inspect_tls_certificate("emudhra-test.unitech-demo.local")
    assert details is not None
    assert details.is_compromised_ca is True
    assert "eMudhra" in details.issuer_org
    assert any("eMudhra Intermediate CA Distrust Action Detected" in ind.title for ind in indicators)

def test_ai_scam_analyzer_urgency_and_entities():
    sample_scam = (
        "URGENT: SBI Account 4821 suspended due to missing KYC! "
        "Within 24 hours, click https://sbi-kyc-panupdate.top or deposit 0.05 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. "
        "Share your 6-digit OTP verification code with our agent to prevent immediate arrest."
    )
    result = AIScamAnalyzer.analyze_message(sample_scam)
    
    assert result.risk_score >= 70
    assert result.risk_classification in [RiskClassification.HIGH_RISK, RiskClassification.CONFIRMED_MALICIOUS]
    assert result.coercion_scores["urgency"] >= 50
    assert result.coercion_scores["credential_solicitation"] >= 35
    assert len(result.extracted_entities.crypto_addresses) > 0
    assert "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" in result.extracted_entities.crypto_addresses
    assert "https://sbi-kyc-panupdate.top" in result.extracted_entities.urls

def test_web3_cryptographic_commitments():
    web3_svc = Web3Service()
    test_report = {
        "domain": "phish-test.xyz",
        "risk_score": 85,
        "classification": "Confirmed Malicious"
    }

    canonical_str, report_hash = web3_svc.canonicalize_and_hash_report(test_report)
    assert report_hash.startswith("0x")
    assert len(report_hash) == 66  # 32 bytes in hex = 64 chars + '0x'

    # Register and verify
    proof = web3_svc.register_threat_report(
        report_data=test_report,
        indicator="phish-test.xyz",
        risk_score=85,
        risk_class=RiskClassification.CONFIRMED_MALICIOUS
    )
    assert proof.report_hash == report_hash

    # Independent check
    verified = web3_svc.verify_report(report_hash)
    assert verified is not None
    assert verified["exists"] is True
    assert verified["risk_score"] == 85

