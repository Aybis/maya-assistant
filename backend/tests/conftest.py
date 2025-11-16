"""Pytest configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from app.main import app
from app.dependencies import get_current_user, get_supabase_service


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def mock_user():
    """Mock authenticated user"""
    return {
        "user_id": "test-user-id-123",
        "email": "test@example.com",
        "role": "authenticated"
    }


@pytest.fixture
def mock_supabase_service():
    """Mock Supabase service"""
    service = Mock()
    service.get_conversations = AsyncMock(return_value=[])
    service.create_conversation = AsyncMock()
    service.get_conversation = AsyncMock()
    service.update_conversation = AsyncMock()
    service.delete_conversation = AsyncMock()
    service.get_messages = AsyncMock(return_value=[])
    service.create_message = AsyncMock()
    return service


@pytest.fixture
def authenticated_client(client, mock_user, mock_supabase_service):
    """Client with authentication dependency overridden"""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_supabase_service] = lambda: mock_supabase_service
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_conversation():
    """Sample conversation data"""
    return {
        "id": "conv-123",
        "user_id": "test-user-id-123",
        "title": "Test Conversation",
        "model": "gpt-4",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_message():
    """Sample message data"""
    return {
        "id": "msg-123",
        "conversation_id": "conv-123",
        "role": "user",
        "content": "Hello, AI!",
        "created_at": "2024-01-01T00:00:00Z"
    }
