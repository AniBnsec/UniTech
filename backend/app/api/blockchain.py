"""Blockchain verification API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib
import json
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.blockchain import BlockchainRecord
from app.models.threat import ThreatReport
from app.schemas.blockchain import (
    BlockchainRegisterRequest,
    BlockchainVerifyRequest,
    BlockchainRecordResponse,
    VerificationResult
)
from app.utils.auth import get_current_user

router = APIRouter()


@router.post("/register", response_model=BlockchainRecordResponse)
async def register_on_blockchain(
    request: BlockchainRegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Register investigation report on blockchain.
    
    - **investigation_id**: ID of investigation to register
    """
    # For demonstration, create a mock blockchain record
    # In production, this would interact with actual smart contract
    
    report_hash = hashlib.sha256(
        json.dumps({'investigation_id': request.investigation_id, 'user_id': str(current_user.id)}).encode()
    ).hexdigest()
    
    # Mock transaction hash
    tx_hash = f"0x{hashlib.sha256(report_hash.encode()).hexdigest()}"
    
    # Check if already registered
    existing = db.query(BlockchainRecord).filter(BlockchainRecord.report_hash == report_hash).first()
    if existing:
        return existing
    
    # Create blockchain record
    record = BlockchainRecord(
        report_id=request.investigation_id,
        user_id=current_user.id,
        report_hash=report_hash,
        transaction_hash=tx_hash,
        block_number=123456,  # Mock block number
        chain_id=11155111,  # Sepolia testnet
        contract_address="0x0000000000000000000000000000000000000000",
        submitter_address="0x0000000000000000000000000000000000000000",
        verified=True
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return record


@router.post("/verify", response_model=VerificationResult)
async def verify_blockchain_record(
    request: BlockchainVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verify a report hash against blockchain records.
    
    - **report_hash**: SHA-256 hash of report to verify
    """
    record = db.query(BlockchainRecord).filter(BlockchainRecord.report_hash == request.report_hash).first()
    
    if record:
        return VerificationResult(
            valid=True,
            on_chain=True,
            hash_match=True,
            registered_at=record.registered_at,
            transaction_hash=record.transaction_hash,
            message="Report hash verified on blockchain"
        )
    else:
        return VerificationResult(
            valid=False,
            on_chain=False,
            hash_match=False,
            message="Report hash not found in blockchain records"
        )


@router.get("/records")
async def get_blockchain_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get blockchain records for current user."""
    records = db.query(BlockchainRecord).filter(BlockchainRecord.user_id == current_user.id).all()
    return {"items": records, "total": len(records)}
