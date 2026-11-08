from typing import List, Tuple
from app.schemas.threat import (
    RiskClassification,
    ThreatIndicator,
    IndicatorSeverity,
    SecurityHeaderFinding
)

class RiskEngine:
    @staticmethod
    def calculate_url_risk(
        indicators: List[ThreatIndicator],
        header_findings: List[SecurityHeaderFinding],
        has_reachable_host: bool = True
    ) -> Tuple[int, RiskClassification, float, str, str, List[str]]:
        """
        Calculates holistic risk score and explainable classification based on empirical evidence.
        """
        if not has_reachable_host and not indicators:
            return (
                0,
                RiskClassification.INCONCLUSIVE,
                0.3,
                "Inconclusive: Host Unreachable",
                "The target host did not respond to network probes, and insufficient domain signals were present to establish a baseline.",
                ["Verify the hostname or IP connectivity.", "Perform manual DNS lookup."]
            )

        score = 0
        weights = {
            IndicatorSeverity.CRITICAL: 40,
            IndicatorSeverity.HIGH: 22,
            IndicatorSeverity.MEDIUM: 12,
            IndicatorSeverity.LOW: 5,
            IndicatorSeverity.INFO: 0
        }

        # Weight technical indicators
        for ind in indicators:
            score += weights.get(ind.severity, 5)

        # Minor penalty for missing key security headers
        for h in header_findings:
            if h.status == "FAIL" and h.header_name in ["Content-Security-Policy", "Strict-Transport-Security"]:
                score += 4
            elif h.status == "WARN":
                score += 2

        # Clamp between 0 and 100
        risk_score = min(100, max(0, score))

        # Risk Classification assignment
        has_critical = any(ind.severity == IndicatorSeverity.CRITICAL for ind in indicators)
        has_high = any(ind.severity == IndicatorSeverity.HIGH for ind in indicators)

        if has_critical or risk_score >= 80:
            classification = RiskClassification.CONFIRMED_MALICIOUS
        elif has_high or risk_score >= 55:
            classification = RiskClassification.HIGH_RISK
        elif risk_score >= 21:
            classification = RiskClassification.SUSPICIOUS
        else:
            classification = RiskClassification.LOW_RISK

        # Confidence calculation based on evidence volume
        evidence_count = len(indicators) + len(header_findings)
        confidence = min(0.98, max(0.55, 0.65 + (evidence_count * 0.03)))

        # Executive summary & recommendations
        precautions = []
        if classification in [RiskClassification.CONFIRMED_MALICIOUS, RiskClassification.HIGH_RISK]:
            summary_verdict = f"{classification.value}: Significant threat signals identified."
            explanation = (
                f"AegisTrust identified {len(indicators)} technical threat indicators. "
                "The target exhibits deceptive infrastructure patterns, cryptographic anomalies, or direct impersonation cues."
            )
            precautions = [
                "DO NOT enter passwords, financial numbers, or OTP codes on this website.",
                "Verify the domain directly against authentic organizational bookmarks.",
                "Report this domain to your IT/Security team and block it in network firewalls."
            ]
        elif classification == RiskClassification.SUSPICIOUS:
            summary_verdict = "Suspicious: Elevated anomaly indicators detected."
            explanation = (
                "The website displays atypical characteristics, such as brand keyword embedding, "
                "missing defensive headers, or redirects that warrant careful verification."
            )
            precautions = [
                "Inspect the address bar carefully for unexpected domain suffixes.",
                "Ensure HTTPS padlock reflects the expected organization, not an anonymous certificate.",
                "Avoid downloading executable attachments or software."
            ]
        else:
            summary_verdict = "Low Risk: No active malicious indicators detected in available checks."
            explanation = (
                "Technical inspection observed valid certificate chains, standard domain structures, and no matches "
                "against current phishing and fraud repositories."
            )
            precautions = [
                "Always verify the destination domain matches your intended recipient before authenticating.",
                "Keep browser and security patches up to date."
            ]

        return risk_score, classification, round(confidence, 2), summary_verdict, explanation, precautions

    @staticmethod
    def calculate_message_risk(
        coercion_scores: dict,
        indicators: List[ThreatIndicator],
        extracted_entities: dict
    ) -> Tuple[int, RiskClassification, float, str, str, List[str]]:
        """
        Calculates risk score for social engineering and scam communication.
        """
        urgency = coercion_scores.get("urgency", 0)
        financial = coercion_scores.get("financial_bait", 0)
        authority = coercion_scores.get("authority_impersonation", 0)
        credential = coercion_scores.get("credential_solicitation", 0)
        isolation = coercion_scores.get("isolation_tactics", 0)

        # Baseline composite score
        composite_coercion = (urgency * 0.25) + (financial * 0.25) + (authority * 0.20) + (credential * 0.30) + (isolation * 0.10)

        tech_boost = 0
        for ind in indicators:
            if ind.severity == IndicatorSeverity.CRITICAL:
                tech_boost += 35
            elif ind.severity == IndicatorSeverity.HIGH:
                tech_boost += 20
            elif ind.severity == IndicatorSeverity.MEDIUM:
                tech_boost += 10

        # High-risk combinations: OTP/credential solicitation + high urgency or crypto payment
        has_critical_indicators = any(ind.severity == IndicatorSeverity.CRITICAL for ind in indicators)
        if credential >= 50 or (urgency >= 70 and len(indicators) >= 2) or has_critical_indicators:
            total_score = min(100, max(75, int(composite_coercion + tech_boost * 0.5)))
        else:
            total_score = min(100, int(composite_coercion * 0.6 + tech_boost * 0.4))

        if total_score >= 80 or (has_critical_indicators and credential >= 50):
            classification = RiskClassification.CONFIRMED_MALICIOUS
        elif total_score >= 55 or urgency >= 70:
            classification = RiskClassification.HIGH_RISK
        elif total_score >= 25:
            classification = RiskClassification.SUSPICIOUS
        else:
            classification = RiskClassification.LOW_RISK

        confidence = round(min(0.96, max(0.65, 0.70 + (len(indicators) * 0.05))), 2)

        if classification in [RiskClassification.CONFIRMED_MALICIOUS, RiskClassification.HIGH_RISK]:
            verdict = f"{classification.value}: Social Engineering and Scam Pattern Detected."
            explanation = (
                "The message exhibits hallmark characteristics of fraud: synthetic urgency, "
                "unauthorized entity impersonation, or solicitation of sensitive payment/credential artifacts."
            )
            actions = [
                "DO NOT click any embedded links or dial provided phone numbers.",
                "NEVER share OTP codes, two-factor authentication tokens, or private keys.",
                "Contact the claimed organization directly via official verified phone numbers or apps."
            ]
        elif classification == RiskClassification.SUSPICIOUS:
            verdict = "Suspicious: Unverified urgency or speculative offer detected."
            explanation = (
                "The communication employs persuasive language or speculative promises that require secondary verification."
            )
            actions = [
                "Verify the sender's identity through independent communication channels.",
                "Inspect any attached links before visiting."
            ]
        else:
            verdict = "Low Risk: Standard communication characteristics."
            explanation = "No high-urgency manipulation or credential-harvesting indicators were identified in the text."
            actions = ["Maintain standard digital hygiene."]

        return total_score, classification, confidence, verdict, explanation, actions
