"""Conversation Summaries API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.conversation_summary import (
    ConversationSummaryCreate,
    ConversationSummaryUpdate,
    ConversationSummary,
    ConversationSummaryResponse
)
from ..dependencies import get_current_user, get_supabase_service
from ..services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/summaries", tags=["summaries"])


@router.post("", response_model=ConversationSummaryResponse, status_code=status.HTTP_201_CREATED)
async def create_summary(
    summary: ConversationSummaryCreate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Create a conversation summary"""
    # Verify the conversation belongs to the user
    conversation = await db.get_conversation(
        conversation_id=str(summary.conversation_id),
        user_id=current_user["user_id"]
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    new_summary = await db.create_conversation_summary(summary=summary)

    if not new_summary:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create summary"
        )

    return new_summary


@router.get("/recent")
async def get_recent_summaries(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get recent conversation summaries for the user"""
    summaries = await db.get_recent_conversation_summaries(
        user_id=current_user["user_id"],
        limit=limit
    )
    return summaries


@router.get("/{conversation_id}", response_model=ConversationSummaryResponse)
async def get_summary(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get summary for a specific conversation"""
    # Verify the conversation belongs to the user
    conversation = await db.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"]
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    summary = await db.get_conversation_summary(conversation_id=conversation_id)

    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )

    return summary


@router.put("/{conversation_id}", response_model=ConversationSummaryResponse)
async def update_summary(
    conversation_id: str,
    update: ConversationSummaryUpdate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Update a conversation summary"""
    # Verify the conversation belongs to the user
    conversation = await db.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"]
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    updated_summary = await db.update_conversation_summary(
        conversation_id=conversation_id,
        update=update
    )

    if not updated_summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )

    return updated_summary
