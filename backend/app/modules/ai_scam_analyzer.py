import re
import uuid
from typing import Dict, List, Tuple
from app.schemas.threat import (
    MessageScanResult,
    ExtractedEntities,
    ThreatIndicator,
    IndicatorSeverity
)
from app.core.risk_engine import RiskEngine

# Regex patterns for high-risk IOCs
URL_REGEX = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
DOMAIN_REGEX = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_REGEX = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
BTC_REGEX = re.compile(r'\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{39,59})\b')
ETH_REGEX = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
TRON_REGEX = re.compile(r'\bT[A-Za-z1-9]{33}\b')
UPI_REGEX = re.compile(r'\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b')

# Psychological Coercion Word Lists
URGENCY_WORDS = [
    r"urgent", r"immediately", r"within 24 hours", r"suspended", r"blocked",
    r"action required", r"expires today", r"final warning", r"arrest", r"legal action",
    r"deactivation", r"last notice", r"frozen", r"unauthorized access detected"
]

FINANCIAL_WORDS = [
    r"refund", r"cashback", r"bonus", r"airdrop", r"lottery", r"winner",
    r"earn \$?\d+ daily", r"guaranteed return", r"investment opportunity",
    r"claim reward", r"crypto prize", r"part-time job", r"daily salary", r"payout"
]

AUTHORITY_WORDS = [
    r"federal reserve", r"reserve bank", r"cyber crime", r"police department",
    r"fraud division", r"income tax department", r"internal revenue", r"security team",
    r"customs", r"parcel dispatch", r"account administrator", r"support desk"
]

CREDENTIAL_WORDS = [
    r"otp", r"one-time password", r"pin code", r"verification code", r"password",
    r"private key", r"seed phrase", r"cvv", r"card number", r"secret recovery phrase",
    r"share the 6-digit code", r"kyc document"
]

ISOLATION_WORDS = [
    r"do not disclose", r"confidential", r"do not tell bank", r"keep this private",
    r"contact only via telegram", r"do not contact customer care", r"exclusive channel"
]

class AIScamAnalyzer:
    @staticmethod
    def extract_entities(text: str) -> ExtractedEntities:
        """Extracts digital forensic indicators and addresses from unformatted text."""
        urls = URL_REGEX.findall(text)
        emails = EMAIL_REGEX.findall(text)
        phones = PHONE_REGEX.findall(text)
        btc = BTC_REGEX.findall(text)
        eth = ETH_REGEX.findall(text)
        tron = TRON_REGEX.findall(text)
        
        # Check potential UPI handles (ignoring general emails)
        all_handles = UPI_REGEX.findall(text)
        upi = [h for h in all_handles if any(p in h.lower() for p in ["@ok", "@upi", "@paytm", "@ibl", "@ybl", "@axl"])]

        # Entity mentions
        impersonated = []
        known_entities = [
            "State Bank of India", "SBI", "PayPal", "HDFC Bank", "ICICI Bank",
            "Chase Bank", "Bank of America", "Amazon", "Netflix", "DHL Express",
            "FedEx", "MetaMask", "Binance", "Income Tax Department", "USPS", "Apple ID"
        ]
        for ent in known_entities:
            if re.search(r'\b' + re.escape(ent) + r'\b', text, re.IGNORECASE):
                impersonated.append(ent)

        return ExtractedEntities(
            urls=list(set(urls)),
            domains=[re.sub(r'^https?://', '', u).split('/')[0] for u in urls],
            emails=list(set(emails)),
            phone_numbers=list(set(phones)),
            crypto_addresses=list(set(btc + eth + tron)),
            upi_handles=list(set(upi)),
            impersonated_entities=list(set(impersonated))
        )

    @staticmethod
    def compute_coercion_scores(text: str) -> Tuple[Dict[str, int], List[ThreatIndicator]]:
        """Evaluates psychological persuasion tactics across 5 dimensions."""
        indicators: List[ThreatIndicator] = []
        lower = text.lower()

        def score_category(patterns: List[str]) -> Tuple[int, List[str]]:
            matches = [p for p in patterns if re.search(p, lower)]
            score = min(100, len(matches) * 35)
            return score, matches

        urgency_score, urg_matches = score_category(URGENCY_WORDS)
        financial_score, fin_matches = score_category(FINANCIAL_WORDS)
        authority_score, auth_matches = score_category(AUTHORITY_WORDS)
        credential_score, cred_matches = score_category(CREDENTIAL_WORDS)
        isolation_score, iso_matches = score_category(ISOLATION_WORDS)

        if urgency_score >= 50:
            indicators.append(ThreatIndicator(
                category="Social Engineering: Urgency & Coercion",
                severity=IndicatorSeverity.HIGH if urgency_score >= 70 else IndicatorSeverity.MEDIUM,
                title="Manufactured Urgency Detected",
                evidence=f"Text contains coercive timing triggers: {', '.join(urg_matches[:3])}",
                description="Scammers fabricate artificial deadlines to provoke panic and impair deliberate decision-making.",
                mitigation="Pause. Legitimate security emergencies are not resolved via arbitrary 24-hour countdowns."
            ))

        if credential_score >= 35:
            indicators.append(ThreatIndicator(
                category="Social Engineering: Credential Harvesting",
                severity=IndicatorSeverity.CRITICAL,
                title="Solicitation of Sensitive Credentials / OTP",
                evidence=f"Text requests private authenticators: {', '.join(cred_matches[:3])}",
                description="Financial institutions, tech providers, and government agencies will never ask you to disclose OTP codes, passwords, or recovery phrases.",
                mitigation="Never reveal OTPs, passwords, or recovery seeds to anyone under any circumstances."
            ))

        if financial_score >= 50:
            indicators.append(ThreatIndicator(
                category="Social Engineering: Financial Lure",
                severity=IndicatorSeverity.HIGH,
                title="Unrealistic Financial Bait / Prize Lure",
                evidence=f"Promises of unverified payouts or prizes: {', '.join(fin_matches[:3])}",
                description="Unsolicited employment or investment schemes offering guaranteed high yields are universally fraudulent advance-fee scams.",
                mitigation="Do not transfer funds or deposit crypto to unlock promised rewards."
            ))

        if authority_score >= 35:
            indicators.append(ThreatIndicator(
                category="Social Engineering: Authority Impersonation",
                severity=IndicatorSeverity.HIGH,
                title="Impersonation of Regulatory / Law Enforcement Entity",
                evidence=f"Mentions institutional authority: {', '.join(auth_matches[:3])}",
                description="Threat actors claim high institutional status to intimidate targets into immediate compliance.",
                mitigation="Confirm credentials via published telephone switchboards."
            ))

        coercion_scores = {
            "urgency": urgency_score,
            "financial_bait": financial_score,
            "authority_impersonation": authority_score,
            "credential_solicitation": credential_score,
            "isolation_tactics": isolation_score
        }

        return coercion_scores, indicators

    @classmethod
    def analyze_message(cls, message_text: str, channel_type: str = "generic") -> MessageScanResult:
        """Runs comprehensive AI heuristic evaluation on suspicious communication."""
        entities = cls.extract_entities(message_text)
        coercion_scores, indicators = cls.compute_coercion_scores(message_text)

        # Flag detected cryptocurrency deposit addresses
        if entities.crypto_addresses:
            indicators.append(ThreatIndicator(
                category="Cryptocurrency Scam Indicator",
                severity=IndicatorSeverity.CRITICAL,
                title="Irreversible Crypto Deposit Address Disclosed",
                evidence=f"Crypto addresses extracted: {', '.join(entities.crypto_addresses)}",
                description="Demands for payment via cryptocurrency in personal or job communications are almost universally associated with non-recoverable fraudulent operations.",
                mitigation="Never send cryptocurrency to unverified third parties."
            ))

        # Flag detected suspicious URLs inside message
        for u in entities.urls:
            indicators.append(ThreatIndicator(
                category="Embedded Suspicious URL",
                severity=IndicatorSeverity.HIGH,
                title="Embedded Link in Unsolicited Message",
                evidence=f"Link found: {u}",
                description="Embedded links in messages frequently redirect to deceptive phishing portals designed to steal login credentials.",
                mitigation="Analyze the URL separately in the AegisTrust URL Scanner before visiting."
            ))

        score, classification, confidence, verdict, explanation, actions = RiskEngine.calculate_message_risk(
            coercion_scores=coercion_scores,
            indicators=indicators,
            extracted_entities=entities.model_dump()
        )

        return MessageScanResult(
            scan_id=f"msg-{uuid.uuid4().hex[:12]}",
            risk_score=score,
            risk_classification=classification,
            confidence=confidence,
            summary_verdict=verdict,
            executive_explanation=explanation,
            coercion_scores=coercion_scores,
            extracted_entities=entities,
            indicators=indicators,
            recommended_actions=actions,
            limitations="AI message analysis evaluates linguistic manipulation and technical indicators. Contextual legitimacy should be confirmed with the purported sender."
        )
