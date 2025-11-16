"""Tests for conversations API endpoints"""

import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_get_conversations(authenticated_client, mock_supabase_service, sample_conversation):
    """Test getting all conversations for authenticated user"""
    mock_supabase_service.get_conversations.return_value = [sample_conversation]

    response = authenticated_client.get("/api/conversations")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_conversation(authenticated_client, mock_supabase_service, sample_conversation):
    """Test creating a new conversation"""
    mock_supabase_service.create_conversation.return_value = sample_conversation

    new_conversation = {
        "title": "New Chat",
        "model": "gpt-4"
    }

    response = authenticated_client.post("/api/conversations", json=new_conversation)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_conversation["title"]


@pytest.mark.asyncio
async def test_create_conversation_failure(authenticated_client, mock_supabase_service):
    """Test conversation creation failure"""
    mock_supabase_service.create_conversation.return_value = None

    response = authenticated_client.post("/api/conversations", json={"title": "Test", "model": "gpt-4"})

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_conversation_by_id(authenticated_client, mock_supabase_service, sample_conversation):
    """Test getting a single conversation by ID"""
    mock_supabase_service.get_conversation.return_value = sample_conversation

    response = authenticated_client.get(f"/api/conversations/{sample_conversation['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_conversation["id"]


@pytest.mark.asyncio
async def test_get_conversation_not_found(authenticated_client, mock_supabase_service):
    """Test getting non-existent conversation returns 404"""
    mock_supabase_service.get_conversation.return_value = None

    response = authenticated_client.get("/api/conversations/non-existent-id")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_conversation(authenticated_client, mock_supabase_service, sample_conversation):
    """Test updating a conversation"""
    updated_conv = sample_conversation.copy()
    updated_conv["title"] = "Updated Title"
    mock_supabase_service.update_conversation.return_value = updated_conv

    response = authenticated_client.put(
        f"/api/conversations/{sample_conversation['id']}",
        json={"title": "Updated Title"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_conversation(authenticated_client, mock_supabase_service, sample_conversation):
    """Test deleting a conversation"""
    mock_supabase_service.delete_conversation.return_value = True

    response = authenticated_client.delete(f"/api/conversations/{sample_conversation['id']}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_conversation_not_found(authenticated_client, mock_supabase_service):
    """Test deleting non-existent conversation returns 404"""
    mock_supabase_service.delete_conversation.return_value = False

    response = authenticated_client.delete("/api/conversations/non-existent-id")

    assert response.status_code == 404
