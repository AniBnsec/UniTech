"""Blockchain verification models."""

from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class BlockchainRecord(Base):
    """Blockchain registration record for threat reports."""
    
    __tablename__ = "blockchain_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("threat_reports.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Report hash
    report_hash = Column(String(64), nullable=False, unique=True, index=True)
    
    # Blockchain transaction details
    transaction_hash = Column(String(66), nullable=False, unique=True, index=True)
    block_number = Column(BigInteger, nullable=False)
    chain_id = Column(Integer, nullable=False)
    contract_address = Column(String(42), nullable=False)
    
    # Submitter information
    submitter_address = Column(String(42), nullable=False)
    
    # Verification status
    verified = Column(Boolean, default=False)
    verification_attempts = Column(Integer, default=0)
    last_verification = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<BlockchainRecord {self.transaction_hash[:10]}...>"
