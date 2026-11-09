"""TLS/SSL certificate analysis engine."""

import ssl
import socket
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class TlsAnalyzer:
    """Analyzes TLS certificates and configurations."""
    
    def __init__(self):
        """Initialize TLS analyzer."""
        self.timeout = 15
    
    def analyze_certificate(self, hostname: str) -> Dict:
        """
        Analyze TLS certificate for a hostname.
        
        Args:
            hostname: Hostname to analyze
            
        Returns:
            Dictionary containing certificate analysis
        """
        try:
            # Remove protocol if present
            hostname = hostname.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
            
            context = ssl.create_default_context()
            warnings = []
            
            with socket.create_connection((hostname, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    # Parse certificate
                    subject = dict(x[0] for x in cert['subject'])
                    issuer = dict(x[0] for x in cert['issuer'])
                    
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    
                    # Check expiration
                    now = datetime.utcnow()
                    expired = now > not_after
                    days_until_expiry = (not_after - now).days if not expired else 0
                    
                    if expired:
                        warnings.append('Certificate has expired')
                    elif days_until_expiry < 30:
                        warnings.append(f'Certificate expires soon ({days_until_expiry} days)')
                    
                    # Check hostname match
                    san = cert.get('subjectAltName', [])
                    san_dns = [name for typ, name in san if typ == 'DNS']
                    hostname_match = self._check_hostname_match(hostname, subject.get('commonName', ''), san_dns)
                    
                    if not hostname_match:
                        warnings.append('Hostname does not match certificate')
                    
                    # Build result
                    certificate_data = {
                        'subject': subject.get('commonName', 'Unknown'),
                        'issuer': issuer.get('commonName', 'Unknown'),
                        'valid_from': not_before.isoformat(),
                        'valid_until': not_after.isoformat(),
                        'serial_number': cert.get('serialNumber', 'Unknown'),
                        'subject_alt_names': san_dns,
                        'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown'),
                    }
                    
                    risk_level = 'HIGH_RISK' if expired or not hostname_match else 'LOW_RISK'
                    
                    return {
                        'hostname': hostname,
                        'https_available': True,
                        'certificate': certificate_data,
                        'hostname_match': hostname_match,
                        'expired': expired,
                        'days_until_expiry': days_until_expiry,
                        'tls_version': version,
                        'cipher_suite': cipher[0] if cipher else 'Unknown',
                        'warnings': warnings,
                        'risk_level': risk_level,
                        'analyzed_at': datetime.utcnow().isoformat()
                    }
                    
        except ssl.SSLError as e:
            logger.error(f"SSL error analyzing {hostname}: {e}")
            return {
                'hostname': hostname,
                'https_available': False,
                'error': f'SSL error: {str(e)}',
                'risk_level': 'SUSPICIOUS',
                'warnings': [f'SSL/TLS error: {str(e)}'],
                'analyzed_at': datetime.utcnow().isoformat()
            }
        except socket.timeout:
            return {
                'hostname': hostname,
                'https_available': False,
                'error': 'Connection timeout',
                'risk_level': 'INCONCLUSIVE',
                'warnings': ['Connection timeout - could not analyze certificate'],
                'analyzed_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing TLS for {hostname}: {e}")
            return {
                'hostname': hostname,
                'https_available': False,
                'error': str(e),
                'risk_level': 'INCONCLUSIVE',
                'warnings': [f'Analysis error: {str(e)}'],
                'analyzed_at': datetime.utcnow().isoformat()
            }
    
    def _check_hostname_match(self, hostname: str, common_name: str, san_list: List[str]) -> bool:
        """Check if hostname matches certificate CN or SAN."""
        hostname = hostname.lower()
        
        # Check common name
        if common_name and self._match_hostname(hostname, common_name.lower()):
            return True
        
        # Check SAN entries
        for san in san_list:
            if self._match_hostname(hostname, san.lower()):
                return True
        
        return False
    
    def _match_hostname(self, hostname: str, pattern: str) -> bool:
        """Match hostname against certificate pattern (supports wildcards)."""
        if pattern == hostname:
            return True
        
        if pattern.startswith('*.'):
            # Wildcard match
            pattern_parts = pattern[2:].split('.')
            hostname_parts = hostname.split('.')
            
            if len(hostname_parts) == len(pattern_parts) + 1:
                return '.'.join(hostname_parts[1:]) == '.'.join(pattern_parts)
        
        return False
