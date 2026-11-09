"""URL and domain threat analysis engine."""

import re
import tldextract
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse, parse_qs
import socket
import logging

logger = logging.getLogger(__name__)


class UrlAnalyzer:
    """Analyzes URLs and domains for security threats."""
    
    SUSPICIOUS_TLDS = {
        'tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'work', 'click',
        'link', 'pw', 'country', 'stream', 'download', 'review'
    }
    
    SUSPICIOUS_KEYWORDS = [
        'login', 'signin', 'account', 'verify', 'secure', 'update',
        'bank', 'payment', 'credential', 'password', 'confirm',
        'wallet', 'bitcoin', 'crypto', 'prize', 'winner', 'urgent'
    ]
    
    KNOWN_BRANDS = [
        'google', 'facebook', 'microsoft', 'apple', 'amazon', 'paypal',
        'netflix', 'instagram', 'twitter', 'linkedin', 'dropbox',
        'adobe', 'oracle', 'cisco', 'ebay', 'wells-fargo', 'chase',
        'bank-of-america', 'citibank', 'usbank'
    ]
    
    def __init__(self):
        """Initialize URL analyzer."""
        pass
    
    def analyze_url(self, url: str) -> Dict:
        """
        Perform comprehensive URL analysis.
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
            
            indicators = []
            risk_score = 0
            
            # Normalize URL
            normalized_url = self._normalize_url(url)
            
            # Extract domain info
            domain_info = {
                'domain': extracted.domain,
                'subdomain': extracted.subdomain,
                'tld': extracted.suffix,
                'registered_domain': extracted.registered_domain,
                'hostname': parsed.netloc,
            }
            
            # Check for suspicious TLD
            if extracted.suffix.lower() in self.SUSPICIOUS_TLDS:
                indicators.append({
                    'type': 'suspicious_tld',
                    'value': extracted.suffix,
                    'severity': 'medium',
                    'description': f'Domain uses suspicious TLD: .{extracted.suffix}',
                    'evidence': f'TLD .{extracted.suffix} is commonly associated with phishing',
                    'source': 'url_analyzer'
                })
                risk_score += 10
            
            # Check for typosquatting
            typosquat = self._check_typosquatting(extracted.domain)
            if typosquat:
                indicators.append({
                    'type': 'typosquatting',
                    'value': typosquat,
                    'severity': 'high',
                    'description': f'Possible typosquatting of {typosquat}',
                    'evidence': f'Domain name closely resembles known brand: {typosquat}',
                    'source': 'url_analyzer'
                })
                risk_score += 20
            
            # Check for suspicious keywords
            suspicious_keywords = self._check_suspicious_keywords(url.lower())
            if suspicious_keywords:
                indicators.append({
                    'type': 'suspicious_keywords',
                    'value': ', '.join(suspicious_keywords),
                    'severity': 'medium',
                    'description': f'URL contains suspicious keywords: {", ".join(suspicious_keywords)}',
                    'evidence': 'These keywords are commonly used in phishing attacks',
                    'source': 'url_analyzer'
                })
                risk_score += 5 * len(suspicious_keywords)
            
            # Check for IP address as hostname
            if self._is_ip_address(parsed.netloc):
                indicators.append({
                    'type': 'ip_address_url',
                    'value': parsed.netloc,
                    'severity': 'medium',
                    'description': 'URL uses IP address instead of domain name',
                    'evidence': 'Legitimate websites typically use domain names',
                    'source': 'url_analyzer'
                })
                risk_score += 15
            
            # Check for excessive subdomains
            subdomain_count = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
            if subdomain_count > 2:
                indicators.append({
                    'type': 'excessive_subdomains',
                    'value': extracted.subdomain,
                    'severity': 'low',
                    'description': f'Excessive subdomain levels: {subdomain_count}',
                    'evidence': 'Multiple subdomain levels can indicate obfuscation',
                    'source': 'url_analyzer'
                })
                risk_score += 5
            
            # Check for suspicious URL patterns
            suspicious_patterns = self._check_url_patterns(url)
            for pattern in suspicious_patterns:
                indicators.append(pattern)
                risk_score += 8
            
            # Check for homograph attacks
            homograph = self._check_homograph(extracted.domain)
            if homograph:
                indicators.append({
                    'type': 'homograph_attack',
                    'value': extracted.domain,
                    'severity': 'high',
                    'description': 'Domain contains look-alike characters',
                    'evidence': homograph,
                    'source': 'url_analyzer'
                })
                risk_score += 20
            
            # Determine risk level
            risk_level = self._calculate_risk_level(risk_score)
            
            return {
                'normalized_url': normalized_url,
                'domain_info': domain_info,
                'indicators': indicators,
                'risk_score': min(risk_score, 100),
                'risk_level': risk_level,
                'confidence': 0.85
            }
            
        except Exception as e:
            logger.error(f"Error analyzing URL: {e}")
            return {
                'error': str(e),
                'risk_level': 'INCONCLUSIVE'
            }
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for consistent processing."""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url
    
    def _is_ip_address(self, hostname: str) -> bool:
        """Check if hostname is an IP address."""
        # Remove port if present
        hostname = hostname.split(':')[0]
        try:
            socket.inet_aton(hostname)
            return True
        except socket.error:
            return False
    
    def _check_typosquatting(self, domain: str) -> Optional[str]:
        """Check for typosquatting of known brands."""
        domain_lower = domain.lower()
        
        for brand in self.KNOWN_BRANDS:
            brand_clean = brand.replace('-', '')
            domain_clean = domain_lower.replace('-', '')
            
            # Check for close matches
            if brand_clean != domain_clean and self._is_similar(brand_clean, domain_clean):
                return brand
        
        return None
    
    def _is_similar(self, s1: str, s2: str, threshold: int = 2) -> bool:
        """Check if two strings are similar (Levenshtein distance)."""
        if abs(len(s1) - len(s2)) > threshold:
            return False
        
        # Simple Levenshtein distance calculation
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        
        distances = range(len(s2) + 1)
        for i1, c1 in enumerate(s1):
            new_distances = [i1 + 1]
            for i2, c2 in enumerate(s2):
                if c1 == c2:
                    new_distances.append(distances[i2])
                else:
                    new_distances.append(1 + min(distances[i2], distances[i2 + 1], new_distances[-1]))
            distances = new_distances
        
        return distances[-1] <= threshold
    
    def _check_suspicious_keywords(self, url: str) -> List[str]:
        """Check for suspicious keywords in URL."""
        found = []
        for keyword in self.SUSPICIOUS_KEYWORDS:
            if keyword in url:
                found.append(keyword)
        return found
    
    def _check_url_patterns(self, url: str) -> List[Dict]:
        """Check for suspicious URL patterns."""
        patterns = []
        
        # Check for @ symbol (authentication bypass attempt)
        if '@' in url:
            patterns.append({
                'type': 'at_symbol',
                'value': '@',
                'severity': 'high',
                'description': 'URL contains @ symbol, possible authentication bypass',
                'evidence': 'The @ symbol can be used to obscure the real destination',
                'source': 'url_analyzer'
            })
        
        # Check for excessive dots
        if url.count('.') > 4:
            patterns.append({
                'type': 'excessive_dots',
                'value': str(url.count('.')),
                'severity': 'low',
                'description': f'URL contains {url.count(".")} dots',
                'evidence': 'Excessive dots can indicate domain obfuscation',
                'source': 'url_analyzer'
            })
        
        # Check for URL shortener patterns
        shortener_patterns = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly']
        for pattern in shortener_patterns:
            if pattern in url.lower():
                patterns.append({
                    'type': 'url_shortener',
                    'value': pattern,
                    'severity': 'low',
                    'description': 'URL uses URL shortening service',
                    'evidence': 'Shortened URLs can hide malicious destinations',
                    'source': 'url_analyzer'
                })
                break
        
        return patterns
    
    def _check_homograph(self, domain: str) -> Optional[str]:
        """Check for homograph attacks using look-alike characters."""
        # Check for common homograph characters
        suspicious_chars = {
            'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c',  # Cyrillic
            'і': 'i', 'ј': 'j', 'ѕ': 's', 'х': 'x', 'у': 'y',
        }
        
        found = []
        for char, latin in suspicious_chars.items():
            if char in domain:
                found.append(f'{char} looks like {latin}')
        
        if found:
            return '; '.join(found)
        
        return None
    
    def _calculate_risk_level(self, score: int) -> str:
        """Calculate risk level from score."""
        if score >= 70:
            return 'HIGH_RISK'
        elif score >= 40:
            return 'SUSPICIOUS'
        elif score >= 20:
            return 'SUSPICIOUS'
        else:
            return 'LOW_RISK'
