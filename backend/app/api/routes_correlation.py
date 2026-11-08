from typing import Optional
from fastapi import APIRouter
from app.schemas.threat import ThreatGraphData
from app.modules.threat_correlator import correlator

router = APIRouter(prefix="", tags=["Threat Intelligence Correlation"])

@router.get("/threats/graph", response_model=ThreatGraphData)
async def get_threat_graph(focus_domain: Optional[str] = None):
    """
    Returns the correlated topological graph linking malicious domains, IPs, CAs, and campaigns.
    """
    return correlator.generate_correlation_graph(focus_domain=focus_domain)
