"""Supabase database service"""

from supabase import create_client, Client
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from ..config import settings
from ..models.conversation import ConversationCreate, ConversationUpdate
from ..models.message import MessageCreate
from ..models.memory import UserMemoryCreate, UserMemoryUpdate
from ..models.conversation_summary import ConversationSummaryCreate, ConversationSummaryUpdate


class SupabaseService:
    """Service for interacting with Supabase database"""

    def __init__(self):
        """Initialize Supabase client with service role key (bypasses RLS)"""
        supabase_key = settings.get_supabase_key()
        if not supabase_key:
            raise ValueError("No Supabase key configured. Please set SUPABASE_SERVICE_ROLE_KEY or SUPABASE_KEY in .env")

        self.client: Client = create_client(
            settings.SUPABASE_URL,
            supabase_key
        )

    # Conversation methods
    async def create_conversation(
        self,
        user_id: str,
        conversation: ConversationCreate
    ) -> dict:
        """Create a new conversation"""
        data = {
            "user_id": user_id,
            "title": conversation.title,
            "model": conversation.model,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            response = self.client.table("conversations").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating conversation: {e}")
            print(f"Data: {data}")
            raise

    async def get_conversations(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[dict]:
        """Get all conversations for a user"""
        response = (
            self.client.table("conversations")
            .select("*, messages(count)")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return response.data if response.data else []

    async def get_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> Optional[dict]:
        """Get a single conversation by ID"""
        response = (
            self.client.table("conversations")
            .select("*")
            .eq("id", conversation_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        return response.data if response.data else None

    async def update_conversation(
        self,
        conversation_id: str,
        user_id: str,
        update: ConversationUpdate
    ) -> Optional[dict]:
        """Update a conversation"""
        data = {
            "updated_at": datetime.utcnow().isoformat()
        }

        if update.title is not None:
            data["title"] = update.title
        if update.model is not None:
            data["model"] = update.model

        response = (
            self.client.table("conversations")
            .update(data)
            .eq("id", conversation_id)
            .eq("user_id", user_id)
            .execute()
        )
        return response.data[0] if response.data else None

    async def delete_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> bool:
        """Delete a conversation"""
        response = (
            self.client.table("conversations")
            .delete()
            .eq("id", conversation_id)
            .eq("user_id", user_id)
            .execute()
        )
        return len(response.data) > 0 if response.data else False

    # Message methods
    async def create_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        model: Optional[str] = None
    ) -> dict:
        """Create a new message"""
        data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "model": model,
            "created_at": datetime.utcnow().isoformat()
        }

        response = self.client.table("messages").insert(data).execute()

        # Update conversation's updated_at timestamp
        await self.touch_conversation(conversation_id)

        return response.data[0] if response.data else None

    async def get_messages(
        self,
        conversation_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get all messages for a conversation"""
        response = (
            self.client.table("messages")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=False)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return response.data if response.data else []

    async def touch_conversation(self, conversation_id: str):
        """Update conversation's updated_at timestamp"""
        self.client.table("conversations").update({
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", conversation_id).execute()

    # User Memory methods
    async def create_user_memory(
        self,
        user_id: str,
        memory: UserMemoryCreate
    ) -> dict:
        """Create a new user memory entry"""
        data = {
            "user_id": user_id,
            "memory_type": memory.memory_type,
            "key": memory.key,
            "value": memory.value,
            "confidence": float(memory.confidence) if memory.confidence else 1.0,
            "source_conversation_id": str(memory.source_conversation_id) if memory.source_conversation_id else None,
            "metadata": memory.metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            response = self.client.table("user_memory").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user memory: {e}")
            # If duplicate key, update instead
            if "duplicate key" in str(e).lower():
                return await self.update_user_memory_by_key(user_id, memory.key, UserMemoryUpdate(
                    value=memory.value,
                    confidence=memory.confidence
                ))
            raise

    async def get_user_memories(
        self,
        user_id: str,
        memory_type: Optional[str] = None,
        limit: int = 100
    ) -> List[dict]:
        """Get all memories for a user, optionally filtered by type"""
        try:
            query = self.client.table("user_memory").select("*").eq("user_id", user_id)

            if memory_type:
                query = query.eq("memory_type", memory_type)

            response = query.order("last_accessed_at", desc=True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting user memories: {e}")
            # Re-raise to let the caller handle it
            raise

    async def get_user_memory(
        self,
        memory_id: str,
        user_id: str
    ) -> Optional[dict]:
        """Get a single user memory by ID"""
        response = (
            self.client.table("user_memory")
            .select("*")
            .eq("id", memory_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        if response.data:
            # Update last_accessed_at
            await self.touch_user_memory(memory_id)

        return response.data if response.data else None

    async def update_user_memory(
        self,
        memory_id: str,
        user_id: str,
        update: UserMemoryUpdate
    ) -> Optional[dict]:
        """Update a user memory"""
        data = {
            "updated_at": datetime.utcnow().isoformat()
        }

        if update.value is not None:
            data["value"] = update.value
        if update.confidence is not None:
            data["confidence"] = float(update.confidence)
        if update.metadata is not None:
            data["metadata"] = update.metadata

        response = (
            self.client.table("user_memory")
            .update(data)
            .eq("id", memory_id)
            .eq("user_id", user_id)
            .execute()
        )
        return response.data[0] if response.data else None

    async def update_user_memory_by_key(
        self,
        user_id: str,
        key: str,
        update: UserMemoryUpdate
    ) -> Optional[dict]:
        """Update a user memory by key"""
        data = {
            "updated_at": datetime.utcnow().isoformat()
        }

        if update.value is not None:
            data["value"] = update.value
        if update.confidence is not None:
            data["confidence"] = float(update.confidence)
        if update.metadata is not None:
            data["metadata"] = update.metadata

        response = (
            self.client.table("user_memory")
            .update(data)
            .eq("user_id", user_id)
            .eq("key", key)
            .execute()
        )
        return response.data[0] if response.data else None

    async def delete_user_memory(
        self,
        memory_id: str,
        user_id: str
    ) -> bool:
        """Delete a user memory"""
        response = (
            self.client.table("user_memory")
            .delete()
            .eq("id", memory_id)
            .eq("user_id", user_id)
            .execute()
        )
        return len(response.data) > 0 if response.data else False

    async def touch_user_memory(self, memory_id: str):
        """Update memory's last_accessed_at timestamp"""
        self.client.table("user_memory").update({
            "last_accessed_at": datetime.utcnow().isoformat()
        }).eq("id", memory_id).execute()

    # Conversation Summary methods
    async def create_conversation_summary(
        self,
        summary: ConversationSummaryCreate
    ) -> dict:
        """Create a conversation summary"""
        data = {
            "conversation_id": str(summary.conversation_id),
            "short_summary": summary.short_summary,
            "detailed_summary": summary.detailed_summary,
            "key_topics": summary.key_topics or [],
            "entities": summary.entities or {},
            "sentiment": summary.sentiment,
            "importance_score": float(summary.importance_score) if summary.importance_score else 0.5,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            response = self.client.table("conversation_summaries").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating conversation summary: {e}")
            raise

    async def get_conversation_summary(
        self,
        conversation_id: str
    ) -> Optional[dict]:
        """Get summary for a conversation"""
        response = (
            self.client.table("conversation_summaries")
            .select("*")
            .eq("conversation_id", conversation_id)
            .single()
            .execute()
        )
        return response.data if response.data else None

    async def update_conversation_summary(
        self,
        conversation_id: str,
        update: ConversationSummaryUpdate
    ) -> Optional[dict]:
        """Update a conversation summary"""
        data = {
            "updated_at": datetime.utcnow().isoformat()
        }

        if update.short_summary is not None:
            data["short_summary"] = update.short_summary
        if update.detailed_summary is not None:
            data["detailed_summary"] = update.detailed_summary
        if update.key_topics is not None:
            data["key_topics"] = update.key_topics
        if update.entities is not None:
            data["entities"] = update.entities
        if update.sentiment is not None:
            data["sentiment"] = update.sentiment
        if update.importance_score is not None:
            data["importance_score"] = float(update.importance_score)

        response = (
            self.client.table("conversation_summaries")
            .update(data)
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response.data[0] if response.data else None

    async def get_recent_conversation_summaries(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[dict]:
        """Get recent conversation summaries for a user"""
        try:
            # First get user's conversations
            conversations = await self.get_conversations(user_id=user_id, limit=limit)
            conversation_ids = [c["id"] for c in conversations]

            if not conversation_ids:
                return []

            # Then get summaries for those conversations
            response = (
                self.client.table("conversation_summaries")
                .select("*")
                .in_("conversation_id", conversation_ids)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting recent conversation summaries: {e}")
            return []

    # Memory Context methods
    async def link_memory_to_conversation(
        self,
        conversation_id: str,
        memory_id: str,
        relevance_score: float = 0.5
    ) -> dict:
        """Link a memory to a conversation"""
        data = {
            "conversation_id": conversation_id,
            "memory_id": memory_id,
            "relevance_score": relevance_score,
            "created_at": datetime.utcnow().isoformat()
        }

        try:
            response = self.client.table("memory_context").insert(data).execute()
            # Update memory's last_accessed_at
            await self.touch_user_memory(memory_id)
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error linking memory to conversation: {e}")
            return None

    async def get_conversation_memories(
        self,
        conversation_id: str
    ) -> List[dict]:
        """Get all memories linked to a conversation"""
        response = (
            self.client.table("memory_context")
            .select("*, user_memory(*)")
            .eq("conversation_id", conversation_id)
            .order("relevance_score", desc=True)
            .execute()
        )
        return response.data if response.data else []

    async def get_relevant_memories(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[dict]:
        """Get most recently accessed/relevant memories for a user"""
        response = (
            self.client.table("user_memory")
            .select("*")
            .eq("user_id", user_id)
            .order("last_accessed_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data if response.data else []
