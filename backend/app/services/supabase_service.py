"""Supabase database service"""

from supabase import create_client, Client
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..config import settings
from ..models.conversation import ConversationCreate, ConversationUpdate
from ..models.message import MessageCreate


class SupabaseService:
    """Service for interacting with Supabase database"""

    def __init__(self):
        """Initialize Supabase client"""
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
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

        response = self.client.table("conversations").insert(data).execute()
        return response.data[0] if response.data else None

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
