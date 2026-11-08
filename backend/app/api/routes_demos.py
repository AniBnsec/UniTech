from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/demo", tags=["Demo Test Suite"])

DEMO_CASES = [
    {
        "id": "malicious-1",
        "type": "URL",
        "title": "Phishing & Brand Typosquatting (PayPal)",
        "category": "MALICIOUS",
        "input": "https://paypaI-security-update.com/login?token=8923fd98234",
        "description": "Uses deceptive Latin/Greek lookalike characters and brand keyword stuffing to impersonate PayPal. Detected by the Levenshtein brand analyzer and threat feed.",
        "expected_classification": "Confirmed Malicious",
        "highlights": ["Homoglyph/Typosquatting match", "Keyword stuffing ('login', 'security')", "Threat feed match"]
    },
    {
        "id": "malicious-2",
        "type": "URL",
        "title": "eMudhra Compromised CA Incident Simulator",
        "category": "MALICIOUS",
        "input": "https://emudhra-test.unitech-demo.local/login",
        "description": "Simulates a site secured with an eMudhra intermediate CA certificate flagged under key-generation vulnerability notices, proving HTTPS ≠ Trust.",
        "expected_classification": "Confirmed Malicious",
        "highlights": ["Compromised CA Flag", "eMudhra Sub-CA Distrust match", "Expired / non-compliant lifetime"]
    },
    {
        "id": "malicious-3",
        "type": "MESSAGE",
        "title": "Urgent SMS Banking & Crypto Job Scam",
        "category": "MALICIOUS",
        "input": "URGENT: SBI Account 9021-XXXX suspended due to unverified KYC! To avoid immediate account termination and legal action within 24 hours, click https://sbi-kyc-update-pan.top or deposit 0.05 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. Share your 6-digit OTP verification code with our executive immediately. Do not disclose this message to anyone.",
        "description": "Multi-factor social engineering combining fake banking authority, manufactured 24-hr urgency, OTP harvesting, and an irreversible Bitcoin payment address.",
        "expected_classification": "Confirmed Malicious",
        "highlights": ["Urgency score 95/100", "Credential/OTP solicitation", "Extracted BTC wallet", "Extracted malicious URL"]
    },
    {
        "id": "benign-1",
        "type": "URL",
        "title": "Legitimate Banking Portal (State Bank of India)",
        "category": "BENIGN",
        "input": "https://www.onlinesbi.sbi",
        "description": "Authentic banking portal for State Bank of India with valid organization-validated TLS certificate and legitimate official TLD (.sbi).",
        "expected_classification": "Low Risk",
        "highlights": ["Valid TLS Trust Chain", "Clean domain reputation", "Authoritative banking infrastructure"]
    },
    {
        "id": "benign-2",
        "type": "URL",
        "title": "Enterprise Cloud & Identity (Microsoft)",
        "category": "BENIGN",
        "input": "https://www.microsoft.com",
        "description": "Production Microsoft portal featuring robust enterprise security headers, strict HSTS, and Microsoft Corporation EV/OV certificates.",
        "expected_classification": "Low Risk",
        "highlights": ["HSTS Preload active", "Valid DigiCert Trust Chain", "Clean lexical entropy"]
    },
    {
        "id": "benign-3",
        "type": "URL",
        "title": "Academic Institution (University of Oxford)",
        "category": "BENIGN",
        "input": "https://www.ox.ac.uk",
        "description": "Accredited higher-education institution with legitimate academic domain (.ac.uk) and verified cryptographic chain.",
        "expected_classification": "Low Risk",
        "highlights": ["Trusted Academic TLD", "Zero phishing flags", "Clean reputation"]
    }
]

@router.get("/cases")
async def get_demo_cases():
    """Returns the 6 mandatory demo test cases for 1-click live evaluation."""
    return DEMO_CASES
