"""Security assessment and TLS certificate models."""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class SecurityFinding(Base):
    """Security assessment finding."""
    
    __tablename__ = "security_findings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    severity = Column(String(20), nullable=False)  # info, low, medium, high, critical
    category = Column(String(100), nullable=False)  # e.g., 'headers', 'tls', 'configuration'
    
    description = Column(Text, nullable=False)
    evidence = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)
    remediation = Column(Text, nullable=True)
    
    # Additional metadata
    cvss_score = Column(Float, nullable=True)
    cwe_id = Column(String(20), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SecurityFinding {self.title} - {self.severity}>"


class TlsCertificate(Base):
    """TLS/SSL certificate information."""
    
    __tablename__ = "tls_certificates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id"), nullable=True)
    
    # Certificate identifiers
    hostname = Column(String(255), nullable=False, index=True)
    fingerprint_sha256 = Column(String(64), nullable=False, unique=True, index=True)
    serial_number = Column(String(100), nullable=False)
    
    # Certificate details
    subject = Column(String(500), nullable=False)
    issuer = Column(String(500), nullable=False)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    
    # Key information
    signature_algorithm = Column(String(100), nullable=True)
    public_key_algorithm = Column(String(100), nullable=True)
    key_size = Column(Integer, nullable=True)
    
    # Subject Alternative Names
    subject_alt_names = Column(JSON, nullable=True)
    
    # Trust and validation
    hostname_match = Column(Boolean, nullable=True)
    expired = Column(Boolean, nullable=False)
    self_signed = Column(Boolean, nullable=True)
    certificate_transparency = Column(Boolean, nullable=True)
    revoked = Column(Boolean, nullable=True)
    
    # Certificate chain
    chain_valid = Column(Boolean, nullable=True)
    chain_data = Column(JSON, nullable=True)
    
    # Timestamps
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<TlsCertificate {self.hostname}>"
