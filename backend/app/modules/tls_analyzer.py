import ssl
import socket
import datetime
from typing import Optional, Tuple, List, Dict
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID, ExtensionOID

from app.schemas.threat import CertificateDetails, ThreatIndicator, IndicatorSeverity
from app.core.ca_blacklist import evaluate_certificate_trust, DISTRUSTED_CAS
from app.core.config import settings

# Pre-configured simulated mock certificates for test cases and offline demo scenarios
MOCK_TLS_SCENARIOS = {
    "emudhra-test.unitech-demo.local": {
        "subject_cn": "onlinesbi.sbi-secure.in",
        "subject_alt_names": ["onlinesbi.sbi-secure.in", "sbi-secure.in"],
        "issuer_org": "eMudhra Technologies Limited",
        "issuer_cn": "eMudhra Sub-CA 2024",
        "valid_from": datetime.datetime(2024, 1, 1),
        "valid_to": datetime.datetime(2025, 1, 1),
        "days_until_expiration": -300,
        "signature_algorithm": "sha256WithRSAEncryption",
        "public_key_bits": 2048,
        "public_key_type": "RSA",
        "is_expired": True,
        "is_self_signed": False,
        "is_hostname_mismatch": False,
        "is_compromised_ca": True,
        "ca_incident_notes": "Certificate issued by eMudhra Sub-CA subject to distrust actions following key generation vulnerability disclosures.",
        "raw_trust_chain": [
            {"subject": "CN=onlinesbi.sbi-secure.in", "issuer": "CN=eMudhra Sub-CA 2024, O=eMudhra Technologies Limited"},
            {"subject": "CN=eMudhra Sub-CA 2024, O=eMudhra Technologies Limited", "issuer": "CN=eMudhra Root CA"}
        ],
        "certificate_transparency_present": False
    },
    "selfsigned-phish.local": {
        "subject_cn": "paypal-login.suspicious.net",
        "subject_alt_names": ["paypal-login.suspicious.net"],
        "issuer_org": "Untrusted Self-Signed Issuer",
        "issuer_cn": "Untrusted Self-Signed Issuer",
        "valid_from": datetime.datetime(2025, 1, 1),
        "valid_to": datetime.datetime(2027, 1, 1),
        "days_until_expiration": 600,
        "signature_algorithm": "sha1WithRSAEncryption",
        "public_key_bits": 1024,
        "public_key_type": "RSA",
        "is_expired": False,
        "is_self_signed": True,
        "is_hostname_mismatch": False,
        "is_compromised_ca": False,
        "ca_incident_notes": "Self-signed certificate with obsolete 1024-bit RSA key and deprecated SHA-1 signature.",
        "raw_trust_chain": [
            {"subject": "CN=paypal-login.suspicious.net", "issuer": "CN=Untrusted Self-Signed Issuer"}
        ],
        "certificate_transparency_present": False
    }
}

class TLSAnalyzer:
    @staticmethod
    def inspect_tls_certificate(hostname: str, port: int = 443) -> Tuple[Optional[CertificateDetails], List[ThreatIndicator]]:
        """
        Extracts and rigorously audits TLS/HTTPS certificate details and trust chain for a hostname.
        """
        indicators: List[ThreatIndicator] = []

        # Check for simulated test-case scenario
        if hostname in MOCK_TLS_SCENARIOS:
            mock = MOCK_TLS_SCENARIOS[hostname]
            cert_details = CertificateDetails(**mock)
            
            # Generate threat indicators from mock
            if cert_details.is_compromised_ca:
                indicators.append(ThreatIndicator(
                    category="Compromised / Distrusted Certificate Authority",
                    severity=IndicatorSeverity.CRITICAL,
                    title="eMudhra Intermediate CA Distrust Action Detected",
                    evidence=f"Issuing CA '{cert_details.issuer_org}' matches active revocation/distrust policy notices.",
                    description="The certificate authority has been flagged for key generation vulnerabilities. Certificates from this hierarchy cannot guarantee identity authenticity.",
                    mitigation="Treat website as untrusted. Never provide banking credentials."
                ))
            if cert_details.is_self_signed:
                indicators.append(ThreatIndicator(
                    category="Untrusted TLS Certificate",
                    severity=IndicatorSeverity.HIGH,
                    title="Self-Signed Digital Certificate",
                    evidence=f"Issuer CN '{cert_details.issuer_cn}' equals Subject CN.",
                    description="Self-signed certificates are not validated by any trusted Certificate Authority and are vulnerable to Man-in-the-Middle attacks.",
                    mitigation="Reject connection unless testing in an isolated staging environment."
                ))
            if cert_details.public_key_bits and cert_details.public_key_bits < 2048:
                indicators.append(ThreatIndicator(
                    category="Cryptographic Weakness",
                    severity=IndicatorSeverity.HIGH,
                    title=f"Weak Public Key Length ({cert_details.public_key_bits}-bit)",
                    evidence=f"RSA public key size is {cert_details.public_key_bits} bits.",
                    description="Keys under 2048 bits fail modern cryptographic baseline requirements.",
                    mitigation="Upgrade to RSA 2048-bit or 4096-bit."
                ))
            return cert_details, indicators

        # Live TLS Probe
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE  # Allow reading invalid/expired certs for forensic analysis

        sock = None
        ssock = None
        try:
            sock = socket.create_connection((hostname, port), timeout=settings.SSL_TIMEOUT_SECONDS)
            ssock = context.wrap_socket(sock, server_hostname=hostname)
            der_cert = ssock.getpeercert(binary_form=True)

            if not der_cert:
                return None, indicators

            cert = x509.load_der_x509_certificate(der_cert, default_backend())

            # Extract Subject CN
            subject_cn = None
            try:
                cns = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
                if cns:
                    subject_cn = cns[0].value
            except Exception:
                pass

            # Extract Issuer Org & CN
            issuer_org = None
            issuer_cn = None
            try:
                orgs = cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
                if orgs:
                    issuer_org = orgs[0].value
                icns = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
                if icns:
                    issuer_cn = icns[0].value
            except Exception:
                pass

            # Extract SANs
            sans = []
            try:
                san_ext = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                sans = san_ext.value.get_values_for_type(x509.DNSName)
            except Exception:
                pass

            # Validity Dates (support datetime with timezone compatibility)
            valid_from = cert.not_valid_before_utc.replace(tzinfo=None) if hasattr(cert, 'not_valid_before_utc') else cert.not_valid_before
            valid_to = cert.not_valid_after_utc.replace(tzinfo=None) if hasattr(cert, 'not_valid_after_utc') else cert.not_valid_after
            now = datetime.datetime.utcnow()

            is_expired = now > valid_to or now < valid_from
            days_until_exp = (valid_to - now).days
            total_days_valid = (valid_to - valid_from).days

            # Public Key and Signature Info
            sig_algo = cert.signature_algorithm_oid._name
            pub_key = cert.public_key()
            pub_key_type = type(pub_key).__name__
            pub_key_bits = getattr(pub_key, "key_size", None)

            # Self-signed test
            is_self_signed = (cert.subject == cert.issuer)

            # Hostname mismatch check
            is_hostname_mismatch = False
            clean_host = hostname.lower()
            matching_names = sans if sans else ([subject_cn] if subject_cn else [])
            matched = False
            for name in matching_names:
                if name:
                    pattern = name.lower()
                    if pattern == clean_host or (pattern.startswith("*.") and clean_host.endswith(pattern[1:])):
                        matched = True
                        break
            if matching_names and not matched:
                is_hostname_mismatch = True

            # Evaluate against CA Blacklist & eMudhra database
            trust_findings = evaluate_certificate_trust(
                issuer_org=issuer_org,
                issuer_cn=issuer_cn,
                signature_algo=sig_algo,
                public_key_type=pub_key_type,
                public_key_bits=pub_key_bits,
                days_valid=total_days_valid
            )

            is_compromised = any(f["severity"] == "CRITICAL" and "Compromised" in f["category"] for f in trust_findings)
            ca_notes = trust_findings[0]["description"] if trust_findings else None

            for finding in trust_findings:
                indicators.append(ThreatIndicator(
                    category=finding["category"],
                    severity=IndicatorSeverity(finding["severity"]),
                    title=finding["title"],
                    evidence=finding["evidence"],
                    description=finding["description"],
                    mitigation=finding.get("mitigation")
                ))

            if is_expired:
                indicators.append(ThreatIndicator(
                    category="Expired Certificate",
                    severity=IndicatorSeverity.HIGH,
                    title="TLS Certificate Has Expired",
                    evidence=f"Certificate expired on {valid_to.strftime('%Y-%m-%d')} ({abs(days_until_exp)} days ago).",
                    description="Expired certificates break cryptographic trust and expose traffic to eavesdropping.",
                    mitigation="Renew certificate with a trusted Certificate Authority."
                ))

            if is_hostname_mismatch:
                indicators.append(ThreatIndicator(
                    category="Identity Mismatch",
                    severity=IndicatorSeverity.HIGH,
                    title="Certificate Name Mismatch",
                    evidence=f"Requested hostname '{hostname}' does not match certificate SANs ({', '.join(sans[:3])}).",
                    description="The server returned a certificate designated for a different domain, characteristic of domain impersonation or misrouted traffic.",
                    mitigation="Do not proceed. Validate the URL identity."
                ))

            if is_self_signed:
                indicators.append(ThreatIndicator(
                    category="Untrusted TLS Certificate",
                    severity=IndicatorSeverity.HIGH,
                    title="Self-Signed Certificate in Production",
                    evidence="Issuer name matches Subject name with no recognized Root CA.",
                    description="Self-signed certificates cannot be verified by standard operating system trust stores.",
                    mitigation="Obtain an authenticated certificate from a recognized CA."
                ))

            # CT presence
            has_sct = False
            try:
                cert.extensions.get_extension_for_oid(ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS)
                has_sct = True
            except Exception:
                has_sct = False

            details = CertificateDetails(
                subject_cn=subject_cn,
                subject_alt_names=sans,
                issuer_org=issuer_org,
                issuer_cn=issuer_cn,
                valid_from=valid_from,
                valid_to=valid_to,
                days_until_expiration=days_until_exp,
                signature_algorithm=sig_algo,
                public_key_bits=pub_key_bits,
                public_key_type=pub_key_type,
                is_expired=is_expired,
                is_self_signed=is_self_signed,
                is_hostname_mismatch=is_hostname_mismatch,
                is_compromised_ca=is_compromised,
                ca_incident_notes=ca_notes,
                raw_trust_chain=[
                    {"subject": f"CN={subject_cn}", "issuer": f"CN={issuer_cn}, O={issuer_org}"}
                ],
                certificate_transparency_present=has_sct
            )

            return details, indicators

        except (socket.timeout, socket.gaierror, ConnectionRefusedError, ssl.SSLError) as err:
            indicators.append(ThreatIndicator(
                category="TLS Handshake Failure",
                severity=IndicatorSeverity.LOW,
                title="Could Not Complete TLS Handshake",
                evidence=str(err),
                description="The server did not respond to standard HTTPS port 443 negotiation within timeout bounds.",
                mitigation="Verify server network availability."
            ))
            return None, indicators
        finally:
            if ssock:
                try:
                    ssock.close()
                except Exception:
                    pass
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass

