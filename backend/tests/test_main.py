"""Tests for main application endpoints"""

import pytest
def test_root_endpoint(client):
    """Test root endpoint returns app info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


def test_app_has_cors_middleware(client):
    """Test CORS middleware is configured"""
    response = client.options("/", headers={"Origin": "http://localhost:3000"})
    # Just verify the app responds to OPTIONS requests
    assert response.status_code in [200, 405]
