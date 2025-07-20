"""Test Eagle API client."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from eagle_client import EagleClient, EagleAPIError


@pytest.mark.asyncio
async def test_eagle_client_health_check():
    """Test Eagle client health check."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status = MagicMock()
        mock_instance.get.return_value = mock_response
        
        async with EagleClient() as client:
            result = await client.health_check()
            assert result is True


@pytest.mark.asyncio
async def test_eagle_client_get_success():
    """Test successful GET request."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "data": []}
        mock_response.raise_for_status = MagicMock()
        mock_instance.get.return_value = mock_response
        
        async with EagleClient() as client:
            result = await client.get("/api/test")
            assert result["status"] == "success"