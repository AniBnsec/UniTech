"""Message and scam detection analyzer using AI."""

import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class MessageAnalyzer:
    """Analyzes messages for scam indicators using pattern matching and AI."""
    
    URGENCY_PATTERNS = [
        r'urgent', r'immediately', r'act now', r'limited time',
        r'expires? (today|soon|in \d+ hours?)', r'don\'?t miss',
        r'act fast', r'hurry', r'quick', r'asap'
    ]
    
    CREDENTIAL_PATTERNS = [
        r'verify (your )?account', r'confirm (your )?identity',
        r'update (your )?password', r'reset (your )?password',
        r'enter (your )?credentials', r'provide (your )?pin',
        r'send (your )?otp', r'authentication code'
    ]
    
    PAYMENT_PATTERNS = [
        r'send money', r'wire transfer', r'payment required',
        r'pay (now|immediately)', r'overdue payment', r'refund',
        r'claim (your )?(prize|reward|money)', r'won (\$|£|€|\d+)',
        r'bitcoin', r'cryptocurrency', r'wallet address'
    ]
    
    IMPERSONATION_KEYWORDS = [
        'bank', 'paypal', 'amazon', 'microsoft', 'apple', 'google',
        'irs', 'tax', 'government', 'police', 'security', 'support',
        'netflix', 'delivery', 'fedex', 'ups', 'dhl', 'customs'
    ]
    
    def __init__(self):
        """Initialize message analyzer."""
        pass
    
    def analyze_message(self, message_text: str, message_type: str = 'other', sender: str = None) -> Dict:
        """
        Analyze message for scam indicators.
        
        Args:
            message_text: The message content
            message_type: Type of message (email, sms, whatsapp, other)
            sender: Optional sender information
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            message_lower = message_text.lower()
            
            indicators = []
            suspicious_patterns = []
            risk_score = 0
            
            # Extract URLs, emails, and phone numbers
            extracted_indicators = self._extract_indicators(message_text)
            
            # Check for urgency manipulation
            urgency_found = self._check_patterns(message_lower, self.URGENCY_PATTERNS)
            if urgency_found:
                suspicious_patterns.append('Urgency manipulation')
                risk_score += 15
            
            # Check for credential requests
            credential_requests = self._check_patterns(message_lower, self.CREDENTIAL_PATTERNS)
            if credential_requests:
                suspicious_patterns.append('Requests credentials or sensitive information')
                risk_score += 25
                indicators.append({
                    'type': 'credential_request',
                    'value': 'Requests sensitive information',
                    'suspicious': True,
                    'reason': 'Legitimate organizations do not request credentials via message'
                })
            
            # Check for payment requests
            payment_requests = self._check_patterns(message_lower, self.PAYMENT_PATTERNS)
            if payment_requests:
                suspicious_patterns.append('Requests payment or financial action')
                risk_score += 20
                indicators.append({
                    'type': 'payment',
                    'value': 'Requests payment',
                    'suspicious': True,
                    'reason': 'Unexpected payment requests are common in scams'
                })
            
            # Check for brand impersonation
            impersonated_entity = self._check_impersonation(message_lower)
            impersonation_detected = impersonated_entity is not None
            
            if impersonation_detected:
                suspicious_patterns.append(f'Possible impersonation of {impersonated_entity}')
                risk_score += 15
            
            # Check extracted indicators
            for indicator in extracted_indicators:
                if indicator['suspicious']:
                    risk_score += 10
            
            # Grammar and spelling (basic check)
            if self._check_poor_grammar(message_text):
                suspicious_patterns.append('Poor grammar or spelling')
                risk_score += 5
            
            # Calculate risk level
            risk_level = self._calculate_risk_level(risk_score)
            
            # Generate AI-style analysis summary
            ai_analysis = self._generate_analysis_summary(
                risk_level, suspicious_patterns, impersonated_entity, extracted_indicators
            )
            
            recommendations = self._generate_recommendations(risk_level, suspicious_patterns)
            
            return {
                'message_type': message_type,
                'risk_level': risk_level,
                'risk_score': min(risk_score, 100),
                'suspicious_patterns': suspicious_patterns,
                'extracted_indicators': extracted_indicators,
                'impersonation_detected': impersonation_detected,
                'impersonated_entity': impersonated_entity,
                'urgency_manipulation': len(urgency_found) > 0,
                'ai_analysis': ai_analysis,
                'recommendations': recommendations,
                'analyzed_at': 'datetime.utcnow().isoformat()'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing message: {e}")
            return {
                'error': str(e),
                'risk_level': 'INCONCLUSIVE'
            }
    
    def _extract_indicators(self, text: str) -> List[Dict]:
        """Extract URLs, emails, and phone numbers from text."""
        indicators = []
        
        # Extract URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text, re.IGNORECASE)
        for url in urls:
            # Check if URL looks suspicious
            suspicious = any(keyword in url.lower() for keyword in ['bit.ly', 'tinyurl', 'login', 'verify', 'secure'])
            indicators.append({
                'type': 'url',
                'value': url,
                'suspicious': suspicious,
                'reason': 'URL shortener or suspicious keyword' if suspicious else None
            })
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        for email in emails:
            indicators.append({
                'type': 'email',
                'value': email,
                'suspicious': False,
                'reason': None
            })
        
        # Extract phone numbers (simple pattern)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            indicators.append({
                'type': 'phone',
                'value': phone,
                'suspicious': False,
                'reason': None
            })
        
        return indicators
    
    def _check_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """Check if any patterns match in text."""
        found = []
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(pattern)
        return found
    
    def _check_impersonation(self, text: str) -> str:
        """Check for brand impersonation."""
        for brand in self.IMPERSONATION_KEYWORDS:
            if brand in text:
                return brand.title()
        return None
    
    def _check_poor_grammar(self, text: str) -> bool:
        """Basic check for poor grammar (very simplistic)."""
        # Check for excessive punctuation
        if text.count('!') > 3 or text.count('?') > 2:
            return True
        
        # Check for all caps (more than 30% of text)
        if len([c for c in text if c.isupper()]) / max(len(text), 1) > 0.3:
            return True
        
        return False
    
    def _calculate_risk_level(self, score: int) -> str:
        """Calculate risk level from score."""
        if score >= 60:
            return 'HIGH_RISK'
        elif score >= 35:
            return 'SUSPICIOUS'
        elif score >= 15:
            return 'SUSPICIOUS'
        else:
            return 'LOW_RISK'
    
    def _generate_analysis_summary(self, risk_level: str, patterns: List[str], impersonation: str, indicators: List[Dict]) -> str:
        """Generate human-readable analysis summary."""
        if risk_level == 'HIGH_RISK':
            summary = "This message exhibits multiple characteristics commonly associated with scams and fraud. "
        elif risk_level == 'SUSPICIOUS':
            summary = "This message contains suspicious elements that warrant caution. "
        else:
            summary = "This message shows some characteristics that could be concerning, but may be legitimate. "
        
        if patterns:
            summary += f"Detected patterns include: {', '.join(patterns[:3])}. "
        
        if impersonation:
            summary += f"The message appears to impersonate {impersonation}. "
        
        suspicious_urls = [i for i in indicators if i['type'] == 'url' and i['suspicious']]
        if suspicious_urls:
            summary += f"Found {len(suspicious_urls)} suspicious URL(s). "
        
        summary += "Always verify sender identity through official channels before taking any action."
        
        return summary
    
    def _generate_recommendations(self, risk_level: str, patterns: List[str]) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        if risk_level in ['HIGH_RISK', 'SUSPICIOUS']:
            recommendations.append("Do not click on any links in this message")
            recommendations.append("Do not provide any personal or financial information")
            recommendations.append("Verify the sender through official contact channels")
            recommendations.append("Report this message to the appropriate authorities")
        
        if 'credential' in ' '.join(patterns).lower():
            recommendations.append("Never share passwords, PINs, or OTPs via message")
        
        if 'payment' in ' '.join(patterns).lower():
            recommendations.append("Verify payment requests directly with the organization")
        
        if not recommendations:
            recommendations.append("Exercise caution and verify sender identity")
            recommendations.append("Be skeptical of unexpected requests")
        
        return recommendations
