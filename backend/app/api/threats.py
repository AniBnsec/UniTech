"""Threat intelligence API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.threat import ThreatGraphResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/graph", response_model=ThreatGraphResponse)
async def get_threat_graph(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get threat correlation graph."""
    # Return empty graph for now
    return ThreatGraphResponse(
        entities=[],
        relationships=[]
    )
