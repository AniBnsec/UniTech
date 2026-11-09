"""Threat correlation and relationship models."""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base


class ThreatEntityType(str, enum.Enum):
    """Types of threat entities."""
    URL = "url"
    DOMAIN = "domain"
    MESSAGE = "message"
    CERTIFICATE = "certificate"
    INDICATOR = "indicator"
    IP_ADDRESS = "ip_address"


class ThreatEntity(Base):
    """Unique threat entity for correlation."""
    
    __tablename__ = "threat_entities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(SQLEnum(ThreatEntityType), nullable=False, index=True)
    value = Column(String(2048), nullable=False, index=True)
    normalized_value = Column(String(2048), nullable=True, index=True)  # For matching
    
    risk_level = Column(String(50), nullable=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    occurrence_count = Column(Integer, default=1)
    
    # Additional metadata
    extra_metadata = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<ThreatEntity {self.type.value}: {self.value[:50]}>"


class ThreatRelationship(Base):
    """Relationship between threat entities."""
    
    __tablename__ = "threat_relationships"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("threat_entities.id"), nullable=False, index=True)
    target_id = Column(UUID(as_uuid=True), ForeignKey("threat_entities.id"), nullable=False, index=True)
    
    relationship_type = Column(String(100), nullable=False)  # e.g., 'redirects_to', 'shares_infrastructure'
    confidence = Column(Float, nullable=False)
    evidence = Column(Text, nullable=True)
    
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional metadata
    extra_metadata = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<ThreatRelationship {self.relationship_type}>"


class ThreatReport(Base):
    """Community-submitted threat reports."""
    
    __tablename__ = "threat_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    threat_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    
    # Indicators of Compromise
    iocs = Column(JSON, nullable=True)
    
    # Report status
    verified = Column(Boolean, default=False)
    public = Column(Boolean, default=True)
    
    # Blockchain registration
    blockchain_registered = Column(Boolean, default=False)
    report_hash = Column(String(64), nullable=True, unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ThreatReport {self.title}>"
