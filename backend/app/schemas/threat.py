"""Threat report and correlation schemas."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class ThreatReportCreate(BaseModel):
    """Schema for creating a threat report."""
    investigation_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    threat_type: str = Field(..., min_length=1, max_length=100)
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    iocs: Optional[Dict[str, Any]] = None
    public: bool = True


class ThreatReportResponse(BaseModel):
    """Response schema for threat report."""
    id: str
    user_id: str
    investigation_id: Optional[str]
    title: str
    description: str
    threat_type: str
    severity: str
    iocs: Optional[Dict[str, Any]]
    verified: bool
    public: bool
    blockchain_registered: bool
    report_hash: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


class ThreatEntityResponse(BaseModel):
    """Response schema for threat entity."""
    id: str
    type: str
    value: str
    risk_level: Optional[str]
    first_seen: datetime
    last_seen: datetime
    occurrence_count: int
    
    model_config = ConfigDict(from_attributes=True)


class ThreatRelationshipResponse(BaseModel):
    """Response schema for threat relationship."""
    id: str
    source_id: str
    target_id: str
    relationship_type: str
    confidence: float
    evidence: Optional[str]
    discovered_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ThreatGraphResponse(BaseModel):
    """Response schema for threat graph."""
    entities: List[ThreatEntityResponse]
    relationships: List[ThreatRelationshipResponse]
