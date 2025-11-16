"""Messages API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
from ..models.message import MessageCreate, MessageResponse
from ..dependencies import get_current_user, get_supabase_service
from ..services.supabase_service import SupabaseService
from ..services.ai_service import AIService
from ..utils.streaming import create_sse_response

router = APIRouter(prefix="/api/conversations", tags=["messages"])


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: str,
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """Get all messages for a conversation"""
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

    messages = await db.get_messages(
        conversation_id=conversation_id,
        limit=limit,
        offset=offset
    )

    return messages


@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: str,
    message: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: SupabaseService = Depends(get_supabase_service)
):
    """
    Send a message and get streaming AI response

    Returns a Server-Sent Events (SSE) stream
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

    # Save user message
    await db.create_message(
        conversation_id=conversation_id,
        role="user",
        content=message.content,
        model=None
    )

    # Get conversation history
    messages = await db.get_messages(conversation_id=conversation_id)

    # Format messages for AI
    ai_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
    ]

    # Determine model to use
    model = message.model or conversation.get("model", "gpt-3.5-turbo")

    # Initialize AI service
    ai_service = AIService()

    # Collect the full response for storage
    full_response = []

    async def response_generator():
        """Generator that streams response and collects it"""
        async for chunk in ai_service.chat_completion_stream(
            messages=ai_messages,
            model=model
        ):
            full_response.append(chunk)
            yield chunk

        # After streaming is complete, save assistant message
        complete_response = "".join(full_response)
        await db.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=complete_response,
            model=model
        )

    # Return streaming response
    return StreamingResponse(
        create_sse_response(response_generator()),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
