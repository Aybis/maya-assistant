"""Conversations API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.conversation import (
    ConversationCreate,
    ConversationUpdate,
    Conversation,
    ConversationResponse
)
from ..dependencies import get_current_user, get_supabase_service
from ..services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get all conversations for the current user"""
    conversations = await db.get_conversations(
        user_id=current_user["user_id"],
        limit=limit,
        offset=offset
    )
    return conversations


@router.post("", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Create a new conversation"""
    new_conversation = await db.create_conversation(
        user_id=current_user["user_id"],
        conversation=conversation
    )

    if not new_conversation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )

    return new_conversation


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get a single conversation by ID"""
    conversation = await db.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"]
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation


@router.put("/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str,
    update: ConversationUpdate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Update a conversation"""
    updated_conversation = await db.update_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"],
        update=update
    )

    if not updated_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return updated_conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Delete a conversation"""
    success = await db.delete_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"]
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return None
