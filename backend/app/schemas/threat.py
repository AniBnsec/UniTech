from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RiskClassification(str, Enum):
    LOW_RISK = "Low Risk"
    SUSPICIOUS = "Suspicious"
    HIGH_RISK = "High Risk"
    CONFIRMED_MALICIOUS = "Confirmed Malicious"
    INCONCLUSIVE = "Inconclusive"

class IndicatorSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ThreatIndicator(BaseModel):
    category: str = Field(..., description="Category, e.g., 'Homoglyph Attack', 'Typosquatting', 'Untrusted CA', 'Urgency Coercion'")
    severity: IndicatorSeverity
    title: str
    description: str
    evidence: str
    mitigation: Optional[str] = None

class RedirectHop(BaseModel):
    hop_number: int
    url: str
    status_code: int
    domain: str
    ip_address: Optional[str] = None
    is_cross_domain: bool = False

class SecurityHeaderFinding(BaseModel):
    header_name: str
    status: str  # "PASS", "WARN", "FAIL"
    severity: IndicatorSeverity
    value: Optional[str] = None
    impact: str
    remediation: str

class CertificateDetails(BaseModel):
    subject_cn: Optional[str] = None
    subject_alt_names: List[str] = []
    issuer_org: Optional[str] = None
    issuer_cn: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    days_until_expiration: Optional[int] = None
    signature_algorithm: Optional[str] = None
    public_key_bits: Optional[int] = None
    public_key_type: Optional[str] = None
    is_expired: bool = False
    is_self_signed: bool = False
    is_hostname_mismatch: bool = False
    is_compromised_ca: bool = False
    ca_incident_notes: Optional[str] = None
    raw_trust_chain: List[Dict[str, str]] = []
    certificate_transparency_present: bool = True

class OnChainProof(BaseModel):
    report_hash: str
    indicator_hash: str
    risk_score: int
    risk_class: RiskClassification
    timestamp: int
    reporter: str
    tx_hash: Optional[str] = None
    contract_address: Optional[str] = None
    is_verified_on_chain: bool = False
    network: str = "AegisTrust Local EVM / Sepolia"

class URLScanRequest(BaseModel):
    url: str
    allow_redirects: bool = True
    record_on_chain: bool = False

class URLScanResult(BaseModel):
    scan_id: str
    target_url: str
    normalized_url: str
    domain: str
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    risk_score: int = Field(..., ge=0, le=100)
    risk_classification: RiskClassification
    confidence: float = Field(..., ge=0.0, le=1.0)
    summary_verdict: str
    executive_explanation: str
    indicators: List[ThreatIndicator] = []
    redirect_chain: List[RedirectHop] = []
    certificate: Optional[CertificateDetails] = None
    security_headers: List[SecurityHeaderFinding] = []
    recommended_precautions: List[str] = []
    limitations: str
    on_chain_proof: Optional[OnChainProof] = None

class MessageScanRequest(BaseModel):
    message_text: str
    channel_type: Optional[str] = "generic"  # "email", "sms", "whatsapp", "job_offer", "crypto_alert"
    record_on_chain: bool = False

class ExtractedEntities(BaseModel):
    urls: List[str] = []
    domains: List[str] = []
    emails: List[str] = []
    phone_numbers: List[str] = []
    crypto_addresses: List[str] = []
    upi_handles: List[str] = []
    impersonated_entities: List[str] = []

class MessageScanResult(BaseModel):
    scan_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    risk_score: int = Field(..., ge=0, le=100)
    risk_classification: RiskClassification
    confidence: float
    summary_verdict: str
    executive_explanation: str
    coercion_scores: Dict[str, int] = {}  # Urgency, Financial Bait, Authority, Credential Request, Isolation
    extracted_entities: ExtractedEntities = ExtractedEntities()
    indicators: List[ThreatIndicator] = []
    recommended_actions: List[str] = []
    limitations: str
    on_chain_proof: Optional[OnChainProof] = None

class GraphNode(BaseModel):
    id: str
    label: str
    node_type: str  # "DOMAIN", "IP", "CA", "PAYMENT", "CAMPAIGN", "MESSAGE"
    risk_level: str
    details: Optional[Dict[str, Any]] = None

class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str  # "RESOLVES_TO", "SIGNED_BY", "REDIRECTS_TO", "REUSES_PAYMENT", "PART_OF_CAMPAIGN"

class ThreatGraphData(BaseModel):
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    campaign_name: Optional[str] = None
    correlated_incidents_count: int = 0
