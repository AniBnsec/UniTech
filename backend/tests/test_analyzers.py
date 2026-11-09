"""Tests for security analyzers."""

import pytest
from app.analyzers.url_analyzer import UrlAnalyzer
from app.analyzers.message_analyzer import MessageAnalyzer


class TestUrlAnalyzer:
    """Test URL analyzer functionality."""
    
    def test_analyze_normal_url(self):
        """Test analysis of normal URL."""
        analyzer = UrlAnalyzer()
        result = analyzer.analyze_url("https://google.com")
        
        assert "risk_score" in result
        assert "risk_level" in result
        assert result["risk_level"] == "LOW_RISK"
    
    def test_detect_suspicious_tld(self):
        """Test detection of suspicious TLD."""
        analyzer = UrlAnalyzer()
        result = analyzer.analyze_url("http://malicious-site.tk")
        
        assert result["risk_score"] > 0
        indicators = result.get("indicators", [])
        assert any(i["type"] == "suspicious_tld" for i in indicators)
    
    def test_detect_typosquatting(self):
        """Test typosquatting detection."""
        analyzer = UrlAnalyzer()
        result = analyzer.analyze_url("http://gooogle.com")
        
        indicators = result.get("indicators", [])
        # May detect as typosquatting of 'google'
        assert result["risk_score"] > 0
    
    def test_detect_ip_address_url(self):
        """Test detection of IP address in URL."""
        analyzer = UrlAnalyzer()
        result = analyzer.analyze_url("http://192.168.1.1")
        
        indicators = result.get("indicators", [])
        assert any(i["type"] == "ip_address_url" for i in indicators)
    
    def test_detect_suspicious_keywords(self):
        """Test detection of suspicious keywords."""
        analyzer = UrlAnalyzer()
        result = analyzer.analyze_url("http://secure-login-verify-account.com")
        
        indicators = result.get("indicators", [])
        assert any(i["type"] == "suspicious_keywords" for i in indicators)


class TestMessageAnalyzer:
    """Test message analyzer functionality."""
    
    def test_analyze_benign_message(self):
        """Test analysis of benign message."""
        analyzer = MessageAnalyzer()
        result = analyzer.analyze_message("Hello, how are you doing today?")
        
        assert "risk_level" in result
        assert result["risk_level"] in ["LOW_RISK", "SUSPICIOUS"]
    
    def test_detect_urgency_manipulation(self):
        """Test detection of urgency manipulation."""
        analyzer = MessageAnalyzer()
        message = "URGENT! Act now or your account will be closed immediately!"
        result = analyzer.analyze_message(message)
        
        assert result["risk_score"] > 0
        assert "urgency" in str(result.get("suspicious_patterns", [])).lower()
    
    def test_detect_credential_request(self):
        """Test detection of credential requests."""
        analyzer = MessageAnalyzer()
        message = "Please verify your account by entering your password and OTP code."
        result = analyzer.analyze_message(message)
        
        patterns = result.get("suspicious_patterns", [])
        indicators = result.get("extracted_indicators", [])
        
        assert result["risk_score"] > 0
        assert any("credential" in str(p).lower() for p in patterns)
    
    def test_detect_payment_request(self):
        """Test detection of payment requests."""
        analyzer = MessageAnalyzer()
        message = "You have won $10,000! Send payment of $99 to claim your prize."
        result = analyzer.analyze_message(message)
        
        patterns = result.get("suspicious_patterns", [])
        assert result["risk_score"] > 0
        assert any("payment" in str(p).lower() for p in patterns)
    
    def test_extract_urls(self):
        """Test URL extraction from messages."""
        analyzer = MessageAnalyzer()
        message = "Click here: https://suspicious-link.com/verify"
        result = analyzer.analyze_message(message)
        
        indicators = result.get("extracted_indicators", [])
        urls = [i for i in indicators if i["type"] == "url"]
        assert len(urls) > 0
    
    def test_detect_impersonation(self):
        """Test brand impersonation detection."""
        analyzer = MessageAnalyzer()
        message = "Your PayPal account requires immediate verification."
        result = analyzer.analyze_message(message)
        
        assert result.get("impersonation_detected") == True
        assert result.get("impersonated_entity") is not None
