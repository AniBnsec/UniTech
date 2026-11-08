import uuid
from urllib.parse import urlparse
from fastapi import APIRouter, HTTPException

from app.schemas.threat import (
    URLScanRequest,
    URLScanResult,
    MessageScanRequest,
    MessageScanResult
)
from app.modules.url_analyzer import URLAnalyzer, normalize_target_url
from app.modules.tls_analyzer import TLSAnalyzer
from app.modules.security_headers import SecurityHeadersAuditor
from app.modules.email_security import EmailSecurityAuditor
from app.modules.ai_scam_analyzer import AIScamAnalyzer
from app.modules.threat_correlator import correlator
from app.modules.web3_service import web3_service
from app.core.risk_engine import RiskEngine

router = APIRouter(prefix="", tags=["Investigation & Threat Analysis"])

@router.post("/analyze/url", response_model=URLScanResult)
async def analyze_url_endpoint(request: URLScanRequest):
    """
    Investigates a submitted URL across all cybersecurity dimensions:
    - Homoglyph & Typosquatting Detection
    - SSRF-Safe Redirect Tracing
    - TLS & eMudhra CA Trust Auditing
    - Passive Security Header Evaluation
    - Cryptographic On-Chain Commitment (Web3)
    """
    if not request.url or not request.url.strip():
        raise HTTPException(status_code=400, detail="A valid URL or domain is required.")

    norm_url = normalize_target_url(request.url)
    
    # 1. Lexical and Domain Analysis
    raw_host, domain, ip_address, lexical_indicators = URLAnalyzer.inspect_lexical_indicators(norm_url)

    # 2. Safe Redirect Tracing
    hops, redirect_indicators = [], []
    if request.allow_redirects:
        hops, redirect_indicators = await URLAnalyzer.trace_redirects_safely(norm_url)
        if hops and hops[-1].ip_address:
            ip_address = hops[-1].ip_address

    # 3. TLS Certificate and Digital Trust Chain Audit
    cert_details, tls_indicators = TLSAnalyzer.inspect_tls_certificate(raw_host)

    # 4. Passive Website Security Headers Audit
    security_headers = await SecurityHeadersAuditor.audit_url_headers(norm_url)

    # 5. Email Domain Authentication (SPF/DMARC) Audit
    email_audit, email_indicators = EmailSecurityAuditor.audit_domain_email_security(domain)

    # Combine all threat indicators
    all_indicators = lexical_indicators + redirect_indicators + tls_indicators + email_indicators

    # 5. Risk Assessment Engine
    risk_score, classification, confidence, verdict, explanation, precautions = RiskEngine.calculate_url_risk(
        indicators=all_indicators,
        header_findings=security_headers,
        has_reachable_host=bool(hops or cert_details)
    )

    scan_id = f"url-{uuid.uuid4().hex[:12]}"

    result = URLScanResult(
        scan_id=scan_id,
        target_url=request.url,
        normalized_url=norm_url,
        domain=domain,
        ip_address=ip_address,
        risk_score=risk_score,
        risk_classification=classification,
        confidence=confidence,
        summary_verdict=verdict,
        executive_explanation=explanation,
        indicators=all_indicators,
        redirect_chain=hops,
        certificate=cert_details,
        security_headers=security_headers,
        email_security=email_audit,
        recommended_precautions=precautions,
        limitations="Passive analysis reflects publicly observable signals and cryptographic assertions. The absence of flags does not guarantee total security."
    )

    # 6. Web3 On-Chain Anchoring (if requested or by default)
    try:
        proof = web3_service.register_threat_report(
            report_data=result.model_dump(),
            indicator=domain,
            risk_score=risk_score,
            risk_class=classification
        )
        result.on_chain_proof = proof
    except Exception:
        pass

    # 7. Threat Correlation Indexing
    correlator.register_url_scan(result)

    return result

@router.post("/analyze/message", response_model=MessageScanResult)
async def analyze_message_endpoint(request: MessageScanRequest):
    """
    Analyzes suspicious communication (email, SMS, job offers, WhatsApp lures)
    for psychological manipulation and digital threat artifacts.
    """
    if not request.message_text or not request.message_text.strip():
        raise HTTPException(status_code=400, detail="Message text is required.")

    result = AIScamAnalyzer.analyze_message(request.message_text, request.channel_type or "generic")

    # Web3 On-Chain Anchoring
    try:
        indicator_seed = result.extracted_entities.urls[0] if result.extracted_entities.urls else "message-scam-ioc"
        proof = web3_service.register_threat_report(
            report_data=result.model_dump(),
            indicator=indicator_seed,
            risk_score=result.risk_score,
            risk_class=result.risk_classification
        )
        result.on_chain_proof = proof
    except Exception:
        pass

    correlator.register_message_scan(result)
    return result
