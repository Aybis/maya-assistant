"""Messages API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
from ..models.message import MessageCreate, MessageResponse
from ..models.conversation import ConversationUpdate
from ..dependencies import get_current_user, get_supabase_service
from ..services.supabase_service import SupabaseService
from ..services.ai_service import AIService
from ..services.memory_service import MemoryService
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

    # Get conversation history (last 50 messages to ensure we have enough context)
    messages = await db.get_messages(conversation_id=conversation_id, limit=50)

    # Initialize memory service
    memory_service = MemoryService(db)

    # Build memory context from previous conversations
    memory_context = await memory_service.build_memory_context(
        user_id=current_user["user_id"],
        current_conversation_id=conversation_id,
        limit=10
    )

    # Build system message with memory context
    system_content = "You are a helpful AI assistant. Remember and use information from the conversation history to provide contextual responses. If the user mentions their name or personal details, remember and use them in future responses."

    if memory_context:
        system_content += f"\n\n{memory_context}"

    # Add system message for context awareness
    ai_messages = [
        {
            "role": "system",
            "content": system_content
        }
    ]

    # Format conversation history for AI
    ai_messages.extend([
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
    ])

    # Log the conversation context for debugging
    print(f"Sending {len(ai_messages)} messages to AI (including system message)")
    print(f"Conversation ID: {conversation_id}")

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

        # Auto-generate title after first exchange (when there are exactly 2 messages)
        all_messages = await db.get_messages(conversation_id=conversation_id)
        if len(all_messages) == 2 and conversation.get("title") == "New Chat":
            # Generate a concise title from the user's first message
            user_message = all_messages[0]["content"]
            title_prompt = [
                {"role": "system", "content": "Generate a concise 3-5 word title for this conversation. Only respond with the title, no punctuation."},
                {"role": "user", "content": f"First message: {user_message[:200]}"}
            ]

            # Use the current model to generate title
            title_chunks = []
            async for chunk in ai_service.chat_completion_stream(
                messages=title_prompt,
                model=model,
                temperature=0.7,
                max_tokens=50
            ):
                title_chunks.append(chunk)

            generated_title = "".join(title_chunks).strip()[:60]  # Limit to 60 chars

            # Update conversation title
            await db.update_conversation(
                conversation_id=conversation_id,
                user_id=current_user["user_id"],
                update=ConversationUpdate(title=generated_title)
            )

        # Auto-extract memories after every 5 messages (configurable)
        if len(all_messages) % 5 == 0 and len(all_messages) >= 5:
            print(f"Auto-extracting memories from conversation {conversation_id}")
            try:
                # Extract memories from recent messages
                extracted = await memory_service.extract_memories_from_conversation(
                    user_id=current_user["user_id"],
                    conversation_id=conversation_id,
                    messages=all_messages[-10:]  # Last 10 messages
                )

                # Save extracted memories
                for memory_data in extracted:
                    await memory_service.save_memory_from_text(
                        user_id=current_user["user_id"],
                        memory_type=memory_data["memory_type"],
                        text=memory_data["content"],
                        conversation_id=conversation_id,
                        confidence=memory_data["confidence"]
                    )

                if extracted:
                    print(f"Extracted {len(extracted)} memories from conversation")
            except Exception as e:
                print(f"Error auto-extracting memories: {e}")

        # Auto-generate summary after conversation ends (e.g., 10+ messages)
        if len(all_messages) >= 10 and len(all_messages) % 10 == 0:
            print(f"Auto-generating summary for conversation {conversation_id}")
            try:
                # Check if summary already exists
                existing_summary = await db.get_conversation_summary(conversation_id)

                if not existing_summary:
                    # Generate summary
                    summary_text = await memory_service.generate_conversation_summary(
                        conversation_id=conversation_id,
                        messages=all_messages
                    )

                    if summary_text:
                        # Extract key topics
                        all_text = " ".join([m.get("content", "") for m in all_messages]).lower()
                        words = all_text.split()
                        common_words = ["conversation", "chat", "message", "question", "answer", "help", "please", "thanks"]
                        key_topics = list(set([w for w in words if len(w) > 5 and w not in common_words][:5]))

                        # Save summary
                        await memory_service.save_conversation_summary(
                            conversation_id=conversation_id,
                            short_summary=summary_text,
                            key_topics=key_topics,
                            importance_score=min(len(all_messages) / 20.0, 1.0)
                        )
                        print(f"Generated summary for conversation")
            except Exception as e:
                print(f"Error auto-generating summary: {e}")

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
