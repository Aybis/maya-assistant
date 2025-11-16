"""Memory API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..models.memory import (
    UserMemoryCreate,
    UserMemoryUpdate,
    UserMemory,
    UserMemoryResponse
)
from ..dependencies import get_current_user, get_supabase_service
from ..services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("", response_model=List[UserMemoryResponse])
async def get_user_memories(
    memory_type: Optional[str] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get all memories for the current user"""
    memories = await db.get_user_memories(
        user_id=current_user["user_id"],
        memory_type=memory_type,
        limit=limit
    )
    return memories


@router.post("", response_model=UserMemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory: UserMemoryCreate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Create a new user memory"""
    new_memory = await db.create_user_memory(
        user_id=current_user["user_id"],
        memory=memory
    )

    if not new_memory:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create memory"
        )

    return new_memory


@router.get("/relevant")
async def get_relevant_memories(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get most relevant/recent memories for context"""
    memories = await db.get_relevant_memories(
        user_id=current_user["user_id"],
        limit=limit
    )
    return memories


@router.get("/{memory_id}", response_model=UserMemoryResponse)
async def get_memory(
    memory_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get a single memory by ID"""
    memory = await db.get_user_memory(
        memory_id=memory_id,
        user_id=current_user["user_id"]
    )

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found"
        )

    return memory


@router.put("/{memory_id}", response_model=UserMemoryResponse)
async def update_memory(
    memory_id: str,
    update: UserMemoryUpdate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Update a memory"""
    updated_memory = await db.update_user_memory(
        memory_id=memory_id,
        user_id=current_user["user_id"],
        update=update
    )

    if not updated_memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found"
        )

    return updated_memory


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Delete a memory"""
    success = await db.delete_user_memory(
        memory_id=memory_id,
        user_id=current_user["user_id"]
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found"
        )

    return None


@router.get("/conversation/{conversation_id}")
async def get_conversation_memories(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get all memories linked to a specific conversation"""
    memories = await db.get_conversation_memories(conversation_id=conversation_id)
    return memories


@router.post("/conversation/{conversation_id}/link/{memory_id}")
async def link_memory_to_conversation(
    conversation_id: str,
    memory_id: str,
    relevance_score: float = 0.5,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Link a memory to a conversation"""
    link = await db.link_memory_to_conversation(
        conversation_id=conversation_id,
        memory_id=memory_id,
        relevance_score=relevance_score
    )

    if not link:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to link memory to conversation"
        )

    return link
