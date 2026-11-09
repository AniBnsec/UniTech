"""URLhaus threat intelligence integration."""

import httpx
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class URLhausClient:
    """Client for URLhaus API."""
    
    def __init__(self, api_url: str = "https://urlhaus-api.abuse.ch/v1/"):
        """Initialize URLhaus client."""
        self.api_url = api_url
        self.timeout = 10
    
    async def query_url(self, url: str) -> Optional[Dict]:
        """
        Query URLhaus for URL information.
        
        Args:
            url: URL to query
            
        Returns:
            Dictionary with threat intelligence or None
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}url/",
                    data={"url": url}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("query_status") == "ok":
                        return {
                            'source': 'URLhaus',
                            'matched': True,
                            'threat_type': data.get('threat', 'malware'),
                            'tags': data.get('tags', []),
                            'first_seen': data.get('date_added'),
                            'status': data.get('url_status'),
                            'confidence': 0.9
                        }
                
                return None
                
        except Exception as e:
            logger.error(f"URLhaus query error: {e}")
            return None
