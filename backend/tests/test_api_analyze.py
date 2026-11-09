"""Tests for analysis API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_analyze_url(client, auth_headers):
    """Test URL analysis endpoint."""
    response = client.post(
        "/api/analyze/url",
        json={"url": "https://example.com", "deep_scan": False},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "url"
    assert data["target"] == "https://example.com"
    assert "risk_level" in data
    assert "risk_score" in data


@pytest.mark.asyncio
async def test_analyze_url_unauthorized(client):
    """Test URL analysis without authentication."""
    response = client.post(
        "/api/analyze/url",
        json={"url": "https://example.com"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_analyze_message(client, auth_headers):
    """Test message analysis endpoint."""
    response = client.post(
        "/api/analyze/message",
        json={
            "message_text": "Urgent! Verify your account now.",
            "message_type": "email"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "message"
    assert "risk_level" in data


@pytest.mark.asyncio
async def test_analyze_domain(client, auth_headers):
    """Test domain analysis endpoint."""
    response = client.post(
        "/api/analyze/domain",
        json={"domain": "example.com"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
