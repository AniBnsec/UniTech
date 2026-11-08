from typing import Dict, Optional, Tuple, List

# Catalog of known compromised, distrusted, or sanction-impacted Certificate Authorities
# and intermediate certificates based on public root store policy decisions (Mozilla, Google Chrome, Apple, Microsoft)
DISTRUSTED_CAS: Dict[str, Dict[str, str]] = {
    "emudhra": {
        "name": "eMudhra Trust Services (Compromised/Distrusted Intermediate)",
        "incident": "eMudhra Sub-CA Key Generation Weakness / Distrust Action",
        "description": "Certificates issued by eMudhra intermediates affected by key generation anomalies and revocation actions. Compromised key generation can allow fraudulent certificates to be minted for domain impersonation.",
        "reference": "Mozilla Bugzilla #1842841 / Chrome Root Program Policy Action",
        "severity": "CRITICAL"
    },
    "diginotar": {
        "name": "DigiNotar Root CA",
        "incident": "Catastrophic CA Infrastructure Breach",
        "description": "DigiNotar was compromised in 2011, allowing attackers to issue hundreds of rogue certificates including *.google.com. Distrusted across all major operating systems and browsers.",
        "reference": "RFC 6462 / Mozilla Revocation List",
        "severity": "CRITICAL"
    },
    "wosign": {
        "name": "WoSign / StartCom CA",
        "incident": "Backdating & Unauthorized Certificate Issuance",
        "description": "WoSign intentionally backdated SHA-1 certificates to evade browser restrictions and issued certificates without domain control validation.",
        "reference": "Google Security Blog: Distrusting WoSign and StartCom Certificates",
        "severity": "CRITICAL"
    },
    "symantec": {
        "name": "Symantec / GeoTrust / Thawte / RapidSSL (Legacy Hierarchy)",
        "incident": "Mass Unauthorized Certificate Issuances",
        "description": "Symantec's legacy PKI infrastructure was distrusted globally by Google and Mozilla following repeated unauthorized issuances of test and third-party certificates.",
        "reference": "Google Chrome Root Program: Distrust of Symantec PKI",
        "severity": "HIGH"
    },
    "trustcor": {
        "name": "TrustCor Systems",
        "incident": "Operational Integrity and Surveillance Concerns",
        "description": "Removed from Mozilla, Apple, and Google root stores following revelations of ties to spyware operations and lack of verifiable organizational controls.",
        "reference": "Mozilla Security Advisory / Washington Post Investigation 2022",
        "severity": "CRITICAL"
    },
    "camerfirma": {
        "name": "AC Camerfirma",
        "incident": "Systemic Inadequate Verification and Incident Response",
        "description": "Distrusted by Mozilla and Google due to systemic failure to address critical compliance and verification incidents over a multi-year period.",
        "reference": "Mozilla Bugzilla #1693006",
        "severity": "HIGH"
    },
    "darkcaracal": {
        "name": "Dark Caracal Malicious Testing / Rogue Intermediates",
        "incident": "Rogue Intermediate for APT Interception",
        "description": "Intermediate certificate authorities generated to perform Man-in-the-Middle (MitM) wiretapping on government and dissident targets.",
        "reference": "EFF & Lookout Cyber Threat Report",
        "severity": "CRITICAL"
    }
}

WEAK_SIGNATURE_ALGORITHMS = {
    "md5WithRSAEncryption": "MD5 hash is cryptographically broken and vulnerable to practical collision attacks.",
    "sha1WithRSAEncryption": "SHA-1 is deprecated across all modern browsers due to collision vulnerabilities (SHAttered).",
    "md2WithRSAEncryption": "MD2 is obsolete and thoroughly insecure."
}

def evaluate_certificate_trust(
    issuer_org: Optional[str],
    issuer_cn: Optional[str],
    signature_algo: Optional[str],
    public_key_type: Optional[str],
    public_key_bits: Optional[int],
    days_valid: Optional[int]
) -> List[Dict[str, any]]:
    """
    Evaluates certificate authority trust, cryptographic strength, and compliance.
    Returns a list of identified trust findings/threat indicators.
    """
    findings = []
    
    issuer_str = f"{issuer_org or ''} {issuer_cn or ''}".lower()
    
    # 1. Check against known distrusted / compromised CA catalog
    for ca_key, ca_meta in DISTRUSTED_CAS.items():
        if ca_key in issuer_str:
            findings.append({
                "category": "Compromised / Distrusted Certificate Authority",
                "severity": ca_meta["severity"],
                "title": f"Flagged CA: {ca_meta['name']}",
                "evidence": f"Issuer '{issuer_org or issuer_cn}' matches known distrusted authority: {ca_meta['incident']}.",
                "description": ca_meta["description"],
                "reference": ca_meta["reference"],
                "mitigation": "Do not enter passwords or credentials. The certificate authority cannot guarantee domain authenticity."
            })

    # 2. Check for weak or deprecated signature algorithm
    if signature_algo and signature_algo in WEAK_SIGNATURE_ALGORITHMS:
        findings.append({
            "category": "Weak Cryptographic Signature",
            "severity": "CRITICAL",
            "title": f"Deprecated Signature Algorithm: {signature_algo}",
            "evidence": f"Certificate signature uses '{signature_algo}'.",
            "description": WEAK_SIGNATURE_ALGORITHMS[signature_algo],
            "mitigation": "Re-issue certificate using modern SHA-256 or SHA-384 algorithm."
        })

    # 3. Check public key bit strength
    if public_key_type and "rsa" in public_key_type.lower():
        if public_key_bits and public_key_bits < 2048:
            findings.append({
                "category": "Inadequate Public Key Length",
                "severity": "HIGH",
                "title": f"Weak RSA Key Size ({public_key_bits}-bit)",
                "evidence": f"Public key size is {public_key_bits} bits (minimum standard is 2048-bit).",
                "description": "Keys under 2048 bits are vulnerable to modern factorization techniques and fail baseline requirements.",
                "mitigation": "Generate an RSA 2048-bit or 4096-bit key pair, or switch to ECDSA P-256."
            })
    elif public_key_type and "ec" in public_key_type.lower():
        if public_key_bits and public_key_bits < 256:
            findings.append({
                "category": "Inadequate Elliptic Curve Key Length",
                "severity": "HIGH",
                "title": f"Weak ECC Key Size ({public_key_bits}-bit)",
                "evidence": f"Elliptic curve key size is {public_key_bits} bits (minimum standard is 256-bit).",
                "description": "Elliptic curve keys below 256 bits fail modern cryptographic standards.",
                "mitigation": "Use NIST P-256 (secp256r1) or Edwards Curve Ed25519."
            })

    # 4. Check for abnormal validity span (modern TLS certs must not exceed 398 days)
    if days_valid and days_valid > 400:
        findings.append({
            "category": "Excessive Certificate Lifetime",
            "severity": "MEDIUM",
            "title": f"Non-Compliant Certificate Lifespan ({days_valid} days)",
            "evidence": f"Certificate validity span of {days_valid} days exceeds browser 398-day maximum standard.",
            "description": "Industry CA/Browser Forum baseline requirements limit TLS certificate validity to 398 days to minimize key compromise window.",
            "mitigation": "Shorten re-issuance lifecycle to 90–365 days."
        })

    return findings
