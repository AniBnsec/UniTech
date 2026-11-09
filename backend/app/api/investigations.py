"""Investigations API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.database import get_db
from app.models.user import User
from app.models.investigation import Investigation
from app.schemas.investigation import InvestigationResponse, PaginatedInvestigationsResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=PaginatedInvestigationsResponse)
async def get_investigations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get paginated list of user's investigations."""
    # Query investigations for current user
    query = db.query(Investigation).filter(Investigation.user_id == current_user.id)
    total = query.count()
    
    # Paginate
    investigations = query.order_by(Investigation.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    pages = math.ceil(total / page_size)
    
    return PaginatedInvestigationsResponse(
        items=investigations,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.get("/{investigation_id}", response_model=InvestigationResponse)
async def get_investigation(
    investigation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific investigation by ID."""
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id,
        Investigation.user_id == current_user.id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    return investigation
