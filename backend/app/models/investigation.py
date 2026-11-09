"""Investigation and analysis result models."""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base


class InvestigationType(str, enum.Enum):
    """Types of security investigations."""
    URL = "url"
    DOMAIN = "domain"
    MESSAGE = "message"
    TLS = "tls"
    SECURITY = "security"


class RiskLevel(str, enum.Enum):
    """Risk classification levels."""
    LOW_RISK = "LOW_RISK"
    SUSPICIOUS = "SUSPICIOUS"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL = "CRITICAL"
    MALICIOUS = "MALICIOUS"
    INCONCLUSIVE = "INCONCLUSIVE"


class InvestigationStatus(str, enum.Enum):
    """Investigation processing status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Investigation(Base):
    """Main investigation record."""
    
    __tablename__ = "investigations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(InvestigationType), nullable=False)
    target = Column(String(2048), nullable=False)  # URL, domain, or message identifier
    risk_level = Column(SQLEnum(RiskLevel), nullable=True)
    risk_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    status = Column(SQLEnum(InvestigationStatus), default=InvestigationStatus.PENDING)
    
    # Analysis results stored as JSON
    result = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    indicators = relationship("ThreatIndicator", back_populates="investigation", cascade="all, delete-orphan")
    intelligence_matches = relationship("IntelligenceMatch", back_populates="investigation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Investigation {self.type.value}: {self.target[:50]}>"


class ThreatIndicator(Base):
    """Individual threat indicator detected during analysis."""
    
    __tablename__ = "threat_indicators"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=False)
    
    type = Column(String(100), nullable=False)  # e.g., 'typosquatting', 'suspicious_url_pattern'
    value = Column(String(1024), nullable=False)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    description = Column(Text, nullable=False)
    evidence = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation", back_populates="indicators")
    
    def __repr__(self):
        return f"<ThreatIndicator {self.type}: {self.severity}>"


class IntelligenceMatch(Base):
    """Threat intelligence matches from external sources."""
    
    __tablename__ = "intelligence_matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=False)
    
    source = Column(String(100), nullable=False)  # e.g., 'URLhaus', 'Google Safe Browsing'
    matched_value = Column(String(1024), nullable=False)
    threat_type = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Additional metadata
    first_seen = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    tags = Column(JSON, nullable=True)
    extra_metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    investigation = relationship("Investigation", back_populates="intelligence_matches")
    
    def __repr__(self):
        return f"<IntelligenceMatch {self.source}: {self.threat_type}>"
