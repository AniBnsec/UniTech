import dns.resolver
from typing import Dict, List, Optional, Tuple
from app.schemas.threat import ThreatIndicator, IndicatorSeverity

class EmailSecurityAuditor:
    """
    Audits email domain trust infrastructure: SPF, DMARC, and MX records via DNS.
    Identifies domains vulnerable to spoofing, CEO fraud, and business email compromise (BEC).
    """
    @staticmethod
    def audit_domain_email_security(domain: str) -> Tuple[Dict[str, any], List[ThreatIndicator]]:
        """
        Queries DNS for SPF, DMARC, and MX records to evaluate spoofing vulnerability.
        """
        indicators: List[ThreatIndicator] = []
        clean_domain = domain.lower().strip()
        
        results = {
            "has_mx": False,
            "mx_records": [],
            "has_spf": False,
            "spf_record": None,
            "has_dmarc": False,
            "dmarc_record": None,
            "dmarc_policy": None,
            "spoofing_vulnerable": False
        }

        # 1. Query MX Records
        try:
            answers = dns.resolver.resolve(clean_domain, 'MX', lifetime=2.0)
            results["has_mx"] = True
            results["mx_records"] = [str(r.exchange).rstrip('.') for r in answers]
        except Exception:
            results["has_mx"] = False

        # 2. Query SPF (TXT record on domain)
        try:
            txt_answers = dns.resolver.resolve(clean_domain, 'TXT', lifetime=2.0)
            for rdata in txt_answers:
                txt_str = "".join([s.decode('utf-8', errors='ignore') if isinstance(s, bytes) else s for s in rdata.strings])
                if txt_str.startswith("v=spf1"):
                    results["has_spf"] = True
                    results["spf_record"] = txt_str
                    break
        except Exception:
            results["has_spf"] = False

        # 3. Query DMARC (TXT record on _dmarc.domain)
        try:
            dmarc_domain = f"_dmarc.{clean_domain}"
            dmarc_answers = dns.resolver.resolve(dmarc_domain, 'TXT', lifetime=2.0)
            for rdata in dmarc_answers:
                txt_str = "".join([s.decode('utf-8', errors='ignore') if isinstance(s, bytes) else s for s in rdata.strings])
                if txt_str.startswith("v=DMARC1"):
                    results["has_dmarc"] = True
                    results["dmarc_record"] = txt_str
                    # Extract policy: p=none, p=quarantine, p=reject
                    for tag in txt_str.split(';'):
                        tag_clean = tag.strip().lower()
                        if tag_clean.startswith("p="):
                            results["dmarc_policy"] = tag_clean.split('=')[1]
                    break
        except Exception:
            results["has_dmarc"] = False

        # Evaluate Vulnerabilities
        if results["has_mx"]:
            if not results["has_dmarc"]:
                results["spoofing_vulnerable"] = True
                indicators.append(ThreatIndicator(
                    category="Email Authentication & Spoofing",
                    severity=IndicatorSeverity.HIGH,
                    title="Missing DMARC Policy (Spoofing Vulnerable)",
                    evidence=f"No DMARC record found at _dmarc.{clean_domain}.",
                    description="Without DMARC enforcement, attackers can forge email headers to send phishing messages appearing directly from this authentic domain.",
                    mitigation=f"Publish a DMARC policy: 'v=DMARC1; p=reject; rua=mailto:dmarc-reports@{clean_domain}'."
                ))
            elif results["dmarc_policy"] == "none":
                indicators.append(ThreatIndicator(
                    category="Email Authentication & Spoofing",
                    severity=IndicatorSeverity.MEDIUM,
                    title="Permissive DMARC Policy (p=none)",
                    evidence=f"DMARC record specifies '{results['dmarc_record']}'.",
                    description="Policy 'p=none' operates in monitoring mode only and does not instruct mail servers to reject or quarantine fraudulent spoofed emails.",
                    mitigation="Upgrade DMARC policy to 'p=quarantine' or 'p=reject'."
                ))

            if not results["has_spf"]:
                indicators.append(ThreatIndicator(
                    category="Email Authentication & Spoofing",
                    severity=IndicatorSeverity.MEDIUM,
                    title="Missing SPF Record",
                    evidence=f"No SPF TXT record detected for '{clean_domain}'.",
                    description="Receiving mail transfer agents cannot verify which IP addresses are authorized to send email on behalf of this domain.",
                    mitigation=f"Configure SPF record: 'v=spf1 mx ~all'."
                ))

        return results, indicators
