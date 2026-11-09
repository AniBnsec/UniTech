"""Dashboard statistics API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.investigation import Investigation, RiskLevel
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics for current user."""
    
    # Count investigations by risk level
    total_investigations = db.query(Investigation).filter(Investigation.user_id == current_user.id).count()
    
    low_risk_count = db.query(Investigation).filter(
        Investigation.user_id == current_user.id,
        Investigation.risk_level == RiskLevel.LOW_RISK
    ).count()
    
    suspicious_count = db.query(Investigation).filter(
        Investigation.user_id == current_user.id,
        Investigation.risk_level == RiskLevel.SUSPICIOUS
    ).count()
    
    high_risk_count = db.query(Investigation).filter(
        Investigation.user_id == current_user.id,
        Investigation.risk_level.in_([RiskLevel.HIGH_RISK, RiskLevel.CRITICAL])
    ).count()
    
    malicious_count = db.query(Investigation).filter(
        Investigation.user_id == current_user.id,
        Investigation.risk_level == RiskLevel.MALICIOUS
    ).count()
    
    # Get recent investigations
    recent_investigations = db.query(Investigation).filter(
        Investigation.user_id == current_user.id
    ).order_by(Investigation.created_at.desc()).limit(10).all()
    
    # Get threat categories
    threat_categories = [
        {"category": "Phishing", "count": suspicious_count + high_risk_count},
        {"category": "Malware", "count": malicious_count},
        {"category": "Suspicious", "count": suspicious_count},
    ]
    
    # Get daily activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_activity = []
    
    for i in range(7):
        date = seven_days_ago + timedelta(days=i)
        count = db.query(Investigation).filter(
            Investigation.user_id == current_user.id,
            func.date(Investigation.created_at) == date.date()
        ).count()
        daily_activity.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return {
        "total_investigations": total_investigations,
        "low_risk_count": low_risk_count,
        "suspicious_count": suspicious_count,
        "high_risk_count": high_risk_count,
        "malicious_count": malicious_count,
        "recent_investigations": recent_investigations,
        "threat_categories": threat_categories,
        "daily_activity": daily_activity
    }
