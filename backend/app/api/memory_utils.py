"""Memory utility endpoints for testing and admin functions"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ..dependencies import get_current_user, get_supabase_service
from ..services.supabase_service import SupabaseService
from ..services.memory_service import MemoryService

router = APIRouter(prefix="/api/memory-utils", tags=["memory-utils"])


@router.post("/extract-from-conversation/{conversation_id}")
async def extract_memories_from_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """
    Extract memories from an existing conversation
    Useful for testing and populating initial data
    """
    # Verify conversation belongs to user
    conversation = await db.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"]
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Get messages
    messages = await db.get_messages(conversation_id=conversation_id)

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages found in conversation"
        )

    # Initialize memory service
    memory_service = MemoryService(db)

    # Extract memories
    extracted = await memory_service.extract_memories_from_conversation(
        user_id=current_user["user_id"],
        conversation_id=conversation_id,
        messages=messages
    )

    # Save extracted memories
    saved_memories = []
    for memory_data in extracted:
        saved = await memory_service.save_memory_from_text(
            user_id=current_user["user_id"],
            memory_type=memory_data["memory_type"],
            text=memory_data["content"],
            conversation_id=conversation_id,
            confidence=memory_data["confidence"]
        )
        if saved:
            saved_memories.append(saved)

    return {
        "conversation_id": conversation_id,
        "extracted_count": len(extracted),
        "saved_count": len(saved_memories),
        "memories": saved_memories
    }


@router.post("/summarize-conversation/{conversation_id}")
async def create_conversation_summary(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """
    Generate and save a summary for an existing conversation
    """
    # Verify conversation belongs to user
    conversation = await db.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user["user_id"]
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Get messages
    messages = await db.get_messages(conversation_id=conversation_id)

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages found in conversation"
        )

    # Initialize memory service
    memory_service = MemoryService(db)

    # Generate summary
    summary_text = await memory_service.generate_conversation_summary(
        conversation_id=conversation_id,
        messages=messages
    )

    if not summary_text:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate summary"
        )

    # Extract key topics (simple word extraction)
    all_text = " ".join([m.get("content", "") for m in messages]).lower()
    common_words = ["conversation", "chat", "message", "question", "answer", "help", "please", "thanks"]
    words = [w for w in all_text.split() if len(w) > 5 and w not in common_words]
    key_topics = list(set(words[:5]))  # Top 5 unique words

    # Calculate importance based on message count
    importance = min(len(messages) / 20.0, 1.0)  # Max out at 20 messages

    # Save summary
    saved_summary = await memory_service.save_conversation_summary(
        conversation_id=conversation_id,
        short_summary=summary_text,
        key_topics=key_topics,
        importance_score=importance
    )

    return {
        "conversation_id": conversation_id,
        "summary": saved_summary,
        "message_count": len(messages)
    }


@router.post("/process-all-conversations")
async def process_all_user_conversations(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """
    Process all user conversations to extract memories and create summaries
    Use with caution - this can take a while for users with many conversations
    """
    # Get user's conversations
    conversations = await db.get_conversations(
        user_id=current_user["user_id"],
        limit=limit
    )

    if not conversations:
        return {
            "message": "No conversations found",
            "processed": 0
        }

    memory_service = MemoryService(db)
    processed = {
        "conversations": 0,
        "memories_extracted": 0,
        "summaries_created": 0,
        "errors": []
    }

    for conv in conversations:
        conv_id = conv["id"]

        try:
            # Get messages
            messages = await db.get_messages(conversation_id=conv_id)

            if not messages or len(messages) < 2:
                continue

            # Extract memories
            extracted = await memory_service.extract_memories_from_conversation(
                user_id=current_user["user_id"],
                conversation_id=conv_id,
                messages=messages
            )

            # Save memories
            for memory_data in extracted:
                saved = await memory_service.save_memory_from_text(
                    user_id=current_user["user_id"],
                    memory_type=memory_data["memory_type"],
                    text=memory_data["content"],
                    conversation_id=conv_id,
                    confidence=memory_data["confidence"]
                )
                if saved:
                    processed["memories_extracted"] += 1

            # Generate summary
            summary_text = await memory_service.generate_conversation_summary(
                conversation_id=conv_id,
                messages=messages
            )

            if summary_text:
                # Extract topics
                all_text = " ".join([m.get("content", "") for m in messages]).lower()
                words = all_text.split()
                key_topics = list(set([w for w in words if len(w) > 5][:5]))

                # Save summary
                saved_summary = await memory_service.save_conversation_summary(
                    conversation_id=conv_id,
                    short_summary=summary_text,
                    key_topics=key_topics,
                    importance_score=min(len(messages) / 20.0, 1.0)
                )

                if saved_summary:
                    processed["summaries_created"] += 1

            processed["conversations"] += 1

        except Exception as e:
            processed["errors"].append({
                "conversation_id": conv_id,
                "error": str(e)
            })

    return processed


@router.get("/stats")
async def get_memory_stats(
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get statistics about user's memories and summaries"""

    try:
        # Get memory counts by type
        memories = await db.get_user_memories(user_id=current_user["user_id"])

        memory_counts = {
            "total": len(memories),
            "by_type": {
                "preference": 0,
                "fact": 0,
                "goal": 0,
                "context": 0,
                "interest": 0
            }
        }

        for memory in memories:
            mem_type = memory.get("memory_type", "context")
            memory_counts["by_type"][mem_type] = memory_counts["by_type"].get(mem_type, 0) + 1

        # Get summary count
        summaries = await db.get_recent_conversation_summaries(
            user_id=current_user["user_id"],
            limit=1000  # Get all summaries
        )

        # Get conversation count
        conversations = await db.get_conversations(user_id=current_user["user_id"], limit=1000)

        return {
            "memories": memory_counts,
            "summaries": {
                "total": len(summaries)
            },
            "conversations": {
                "total": len(conversations)
            }
        }
    except Exception as e:
        error_message = str(e).lower()

        # Check if it's a "table doesn't exist" error
        if "does not exist" in error_message or "not found" in error_message or "no such table" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Memory tables not found. Please run the database migration first. See /database/migration_add_memory.sql"
            )

        # For other errors, log and return generic error
        print(f"Error getting memory stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory stats: {str(e)}"
        )
