from fastapi import APIRouter, HTTPException
from app.modules.web3_service import web3_service
from app.core.config import settings

router = APIRouter(prefix="/blockchain", tags=["Decentralized Threat Registry (Web3)"])

@router.get("/verify/{report_hash}")
async def verify_report_integrity_endpoint(report_hash: str):
    """
    Independently verifies the tamper-evident integrity of a registered threat report
    against its on-chain Keccak-256 cryptographic commitment.
    """
    clean_hash = report_hash.strip()
    proof = web3_service.verify_report(clean_hash)
    if not proof:
        raise HTTPException(
            status_code=404,
            detail=f"Report commitment '{clean_hash}' was not found in the ThreatReportRegistry or has expired."
        )
    return {
        "status": "VALID_AND_TAMPER_PROOF",
        "verified": True,
        "details": proof
    }

@router.get("/status")
async def get_blockchain_status():
    """Returns the connected EVM network, contract address, and ledger status."""
    return {
        "network": "EVM Threat Registry (Local / Sepolia)",
        "contract_address": settings.CONTRACT_ADDRESS,
        "is_connected": web3_service.w3.is_connected(),
        "zero_pii_policy": "ENFORCED: No raw URLs, personal names, or messages committed on-chain."
    }

