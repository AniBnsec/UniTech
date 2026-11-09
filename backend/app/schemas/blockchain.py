"""Blockchain verification schemas."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class BlockchainRegisterRequest(BaseModel):
    """Request schema for blockchain registration."""
    investigation_id: str = Field(..., min_length=1)


class BlockchainVerifyRequest(BaseModel):
    """Request schema for blockchain verification."""
    report_hash: str = Field(..., min_length=64, max_length=64)


class BlockchainRecordResponse(BaseModel):
    """Response schema for blockchain record."""
    id: str
    report_id: str
    report_hash: str
    transaction_hash: str
    block_number: int
    chain_id: int
    submitter_address: str
    verified: bool
    registered_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class VerificationResult(BaseModel):
    """Response schema for verification result."""
    valid: bool
    on_chain: bool
    hash_match: bool
    registered_at: Optional[datetime]
    transaction_hash: Optional[str]
    message: str
