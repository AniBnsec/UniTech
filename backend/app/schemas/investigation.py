"""Investigation and analysis schemas."""

from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime


class UrlAnalysisRequest(BaseModel):
    """Request schema for URL analysis."""
    url: str = Field(..., min_length=1, max_length=2048)
    deep_scan: bool = False


class DomainAnalysisRequest(BaseModel):
    """Request schema for domain analysis."""
    domain: str = Field(..., min_length=1, max_length=255)


class MessageAnalysisRequest(BaseModel):
    """Request schema for message analysis."""
    message_text: str = Field(..., min_length=1)
    message_type: Optional[str] = Field(None, pattern="^(email|sms|whatsapp|other)$")
    sender: Optional[str] = None


class TlsAnalysisRequest(BaseModel):
    """Request schema for TLS certificate analysis."""
    hostname: str = Field(..., min_length=1, max_length=255)


class SecurityAssessmentRequest(BaseModel):
    """Request schema for security assessment."""
    url: str = Field(..., min_length=1, max_length=2048)


class ThreatIndicatorResponse(BaseModel):
    """Response schema for threat indicator."""
    id: str
    type: str
    value: str
    severity: str
    description: str
    evidence: Optional[str]
    source: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)


class IntelligenceMatchResponse(BaseModel):
    """Response schema for intelligence match."""
    id: str
    source: str
    matched_value: str
    threat_type: str
    confidence: float
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]
    tags: Optional[List[str]]
    
    model_config = ConfigDict(from_attributes=True)


class InvestigationResponse(BaseModel):
    """Response schema for investigation."""
    id: str
    type: str
    target: str
    risk_level: Optional[str]
    risk_score: Optional[float]
    confidence: Optional[float]
    status: str
    result: Optional[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime]
    indicators: List[ThreatIndicatorResponse] = []
    intelligence_matches: List[IntelligenceMatchResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class PaginatedInvestigationsResponse(BaseModel):
    """Paginated list of investigations."""
    items: List[InvestigationResponse]
    total: int
    page: int
    page_size: int
    pages: int
