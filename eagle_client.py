"""Eagle API client for MCP server."""

import logging
from typing import Any, Dict, Optional

import httpx
from config import EAGLE_API_BASE_URL, EAGLE_API_TIMEOUT

logger = logging.getLogger(__name__)


class EagleAPIError(Exception):
    """Exception raised for Eagle API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class EagleClient:
    """Client for communicating with Eagle API."""
    
    def __init__(self, base_url: str = EAGLE_API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=EAGLE_API_TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to Eagle API."""
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        try:
            logger.debug(f"GET {endpoint} with params: {params}")
            response = await self._client.get(endpoint, params=params)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"Response: {result.get('status', 'unknown')}")
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise EagleAPIError(f"HTTP {e.response.status_code}: {e.response.text}", e.response.status_code)
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise EagleAPIError(f"Request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise EagleAPIError(f"Unexpected error: {e}")
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request to Eagle API."""
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        try:
            logger.debug(f"POST {endpoint} with data: {data}")
            response = await self._client.post(endpoint, json=data)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"Response: {result.get('status', 'unknown')}")
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise EagleAPIError(f"HTTP {e.response.status_code}: {e.response.text}", e.response.status_code)
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise EagleAPIError(f"Request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise EagleAPIError(f"Unexpected error: {e}")
    
    async def health_check(self) -> bool:
        """Check if Eagle API is accessible."""
        try:
            result = await self.get("/api/application/info")
            return result.get("status") == "success"
        except Exception:
            return False