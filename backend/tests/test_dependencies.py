"""Tests for authentication and dependency injection"""

import pytest
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from app.dependencies import get_current_user
from app.config import settings
from unittest.mock import Mock


def test_get_current_user_with_valid_token():
    """Test user extraction from valid JWT token"""
    # Create a valid token
    payload = {
        "sub": "user-123",
        "email": "test@example.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")

    # Mock credentials
    credentials = Mock()
    credentials.credentials = token

    # Test
    result = get_current_user(credentials)
    assert result["user_id"] == "user-123"
    assert result["email"] == "test@example.com"
    assert result["role"] == "authenticated"


def test_get_current_user_with_invalid_token():
    """Test that invalid token raises HTTPException"""
    credentials = Mock()
    credentials.credentials = "invalid-token"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials)

    assert exc_info.value.status_code == 401


def test_get_current_user_with_missing_user_id():
    """Test that token without user_id raises HTTPException"""
    # Create token without 'sub' claim
    payload = {
        "email": "test@example.com",
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")

    credentials = Mock()
    credentials.credentials = token

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials)

    assert exc_info.value.status_code == 401
    assert "Invalid authentication credentials" in exc_info.value.detail
