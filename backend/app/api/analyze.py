"""Analysis API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import get_db
from app.models.user import User
from app.models.investigation import Investigation, InvestigationType, InvestigationStatus, ThreatIndicator
from app.schemas.investigation import (
    UrlAnalysisRequest,
    DomainAnalysisRequest,
    MessageAnalysisRequest,
    TlsAnalysisRequest,
    SecurityAssessmentRequest,
    InvestigationResponse
)
from app.utils.auth import get_current_user
from app.analyzers.url_analyzer import UrlAnalyzer
from app.analyzers.tls_analyzer import TlsAnalyzer
from app.analyzers.message_analyzer import MessageAnalyzer
from app.intelligence.urlhaus import URLhausClient

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/url", response_model=InvestigationResponse)
async def analyze_url(
    request: UrlAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a URL for security threats.
    
    - **url**: URL to analyze
    - **deep_scan**: Perform additional checks (optional)
    """
    # Create investigation record
    investigation = Investigation(
        user_id=current_user.id,
        type=InvestigationType.URL,
        target=request.url,
        status=InvestigationStatus.IN_PROGRESS
    )
    db.add(investigation)
    db.commit()
    
    try:
        # Run URL analysis
        url_analyzer = UrlAnalyzer()
        analysis_result = url_analyzer.analyze_url(request.url)
        
        # Query threat intelligence
        urlhaus = URLhausClient()
        threat_intel = await urlhaus.query_url(request.url)
        
        if threat_intel and threat_intel['matched']:
            analysis_result['risk_score'] = min(analysis_result.get('risk_score', 0) + 50, 100)
            analysis_result['risk_level'] = 'MALICIOUS'
            
            # Add threat intelligence as indicator
            analysis_result['indicators'].append({
                'type': 'threat_intelligence_match',
                'value': 'URLhaus',
                'severity': 'critical',
                'description': f"Matched in URLhaus as {threat_intel['threat_type']}",
                'evidence': f"Status: {threat_intel.get('status', 'unknown')}",
                'source': 'URLhaus'
            })
        
        # Add AI-generated summary
        ai_summary = _generate_url_summary(analysis_result)
        analysis_result['ai_summary'] = ai_summary
        analysis_result['recommendations'] = _generate_url_recommendations(analysis_result)
        
        # Save indicators
        for indicator_data in analysis_result.get('indicators', []):
            indicator = ThreatIndicator(
                investigation_id=investigation.id,
                type=indicator_data['type'],
                value=indicator_data['value'],
                severity=indicator_data['severity'],
                description=indicator_data['description'],
                evidence=indicator_data.get('evidence'),
                source=indicator_data.get('source')
            )
            db.add(indicator)
        
        # Update investigation
        investigation.status = InvestigationStatus.COMPLETED
        investigation.risk_level = analysis_result['risk_level']
        investigation.risk_score = analysis_result['risk_score']
        investigation.confidence = analysis_result.get('confidence', 0.85)
        investigation.result = analysis_result
        investigation.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(investigation)
        
        return investigation
        
    except Exception as e:
        logger.error(f"URL analysis error: {e}")
        investigation.status = InvestigationStatus.FAILED
        investigation.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/domain", response_model=InvestigationResponse)
async def analyze_domain(
    request: DomainAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze a domain for security threats."""
    # Convert domain to URL and analyze
    url_request = UrlAnalysisRequest(url=f"http://{request.domain}", deep_scan=True)
    return await analyze_url(url_request, db, current_user)


@router.post("/message", response_model=InvestigationResponse)
async def analyze_message(
    request: MessageAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a message for scam indicators.
    
    - **message_text**: Message content to analyze
    - **message_type**: Type of message (email, sms, whatsapp, other)
    - **sender**: Optional sender information
    """
    investigation = Investigation(
        user_id=current_user.id,
        type=InvestigationType.MESSAGE,
        target=request.message_text[:200] + "..." if len(request.message_text) > 200 else request.message_text,
        status=InvestigationStatus.IN_PROGRESS
    )
    db.add(investigation)
    db.commit()
    
    try:
        # Run message analysis
        message_analyzer = MessageAnalyzer()
        analysis_result = message_analyzer.analyze_message(
            request.message_text,
            request.message_type or 'other',
            request.sender
        )
        
        # Update investigation
        investigation.status = InvestigationStatus.COMPLETED
        investigation.risk_level = analysis_result['risk_level']
        investigation.risk_score = analysis_result['risk_score']
        investigation.confidence = 0.80
        investigation.result = analysis_result
        investigation.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(investigation)
        
        return investigation
        
    except Exception as e:
        logger.error(f"Message analysis error: {e}")
        investigation.status = InvestigationStatus.FAILED
        investigation.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/tls", response_model=InvestigationResponse)
async def analyze_tls(
    request: TlsAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze TLS certificate for a hostname.
    
    - **hostname**: Hostname to analyze
    """
    investigation = Investigation(
        user_id=current_user.id,
        type=InvestigationType.TLS,
        target=request.hostname,
        status=InvestigationStatus.IN_PROGRESS
    )
    db.add(investigation)
    db.commit()
    
    try:
        # Run TLS analysis
        tls_analyzer = TlsAnalyzer()
        analysis_result = tls_analyzer.analyze_certificate(request.hostname)
        
        # Update investigation
        investigation.status = InvestigationStatus.COMPLETED
        investigation.risk_level = analysis_result['risk_level']
        investigation.risk_score = 20 if analysis_result['risk_level'] == 'LOW_RISK' else 60
        investigation.confidence = 0.95
        investigation.result = analysis_result
        investigation.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(investigation)
        
        return investigation
        
    except Exception as e:
        logger.error(f"TLS analysis error: {e}")
        investigation.status = InvestigationStatus.FAILED
        investigation.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/security", response_model=InvestigationResponse)
async def assess_security(
    request: SecurityAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Perform security assessment on a website.
    
    - **url**: Website URL to assess
    """
    investigation = Investigation(
        user_id=current_user.id,
        type=InvestigationType.SECURITY,
        target=request.url,
        status=InvestigationStatus.IN_PROGRESS
    )
    db.add(investigation)
    db.commit()
    
    try:
        # For now, return a basic security assessment
        # In production, this would check headers, TLS config, etc.
        analysis_result = {
            'url': request.url,
            'https_enabled': request.url.startswith('https://'),
            'headers': [],
            'findings': [],
            'risk_level': 'LOW_RISK',
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        investigation.status = InvestigationStatus.COMPLETED
        investigation.risk_level = 'LOW_RISK'
        investigation.risk_score = 20
        investigation.confidence = 0.75
        investigation.result = analysis_result
        investigation.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(investigation)
        
        return investigation
        
    except Exception as e:
        logger.error(f"Security assessment error: {e}")
        investigation.status = InvestigationStatus.FAILED
        investigation.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")


def _generate_url_summary(analysis: Dict) -> str:
    """Generate AI-style summary for URL analysis."""
    risk_level = analysis.get('risk_level', 'INCONCLUSIVE')
    indicators = analysis.get('indicators', [])
    
    if risk_level == 'MALICIOUS':
        summary = "This URL has been identified as malicious by threat intelligence sources. "
    elif risk_level == 'HIGH_RISK':
        summary = "This URL exhibits multiple high-risk characteristics indicating potential threat. "
    elif risk_level == 'SUSPICIOUS':
        summary = "This URL shows suspicious patterns that warrant caution. "
    else:
        summary = "This URL analysis shows low risk indicators, but verification is always recommended. "
    
    if indicators:
        top_indicators = [i['type'] for i in indicators[:3]]
        summary += f"Key findings: {', '.join(top_indicators)}. "
    
    summary += "Always verify URLs before clicking, especially in unsolicited messages."
    
    return summary


def _generate_url_recommendations(analysis: Dict) -> list:
    """Generate recommendations for URL analysis."""
    risk_level = analysis.get('risk_level', 'LOW_RISK')
    recommendations = []
    
    if risk_level in ['MALICIOUS', 'HIGH_RISK']:
        recommendations.append("Do not visit this URL")
        recommendations.append("Block this URL in your security systems")
        recommendations.append("Report this URL to appropriate authorities")
    elif risk_level == 'SUSPICIOUS':
        recommendations.append("Exercise extreme caution")
        recommendations.append("Verify the URL through official channels")
        recommendations.append("Do not enter sensitive information")
    else:
        recommendations.append("Verify URL legitimacy before entering sensitive data")
        recommendations.append("Ensure HTTPS connection when available")
    
    return recommendations
