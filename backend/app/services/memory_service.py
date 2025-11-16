"""Memory Service for managing AI context and conversation memory"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .supabase_service import SupabaseService
from ..models.memory import UserMemoryCreate
from ..models.conversation_summary import ConversationSummaryCreate
from decimal import Decimal


class MemoryService:
    """Service for managing conversation memory and context"""

    def __init__(self, db: SupabaseService):
        self.db = db

    async def build_memory_context(
        self,
        user_id: str,
        current_conversation_id: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """
        Build a memory context string to inject into AI prompts

        Args:
            user_id: User ID
            current_conversation_id: Current conversation ID (to avoid self-reference)
            limit: Max number of memories to include

        Returns:
            Formatted memory context string
        """
        # Get relevant memories
        memories = await self.db.get_relevant_memories(user_id=user_id, limit=limit)

        if not memories:
            return ""

        # Get recent conversation summaries
        summaries = await self.db.get_recent_conversation_summaries(
            user_id=user_id,
            limit=5
        )

        # Filter out current conversation
        if current_conversation_id:
            summaries = [s for s in summaries
                        if s.get("conversation_id") != current_conversation_id]

        # Build context string
        context_parts = []

        # Add user facts and preferences
        preferences = [m for m in memories if m["memory_type"] == "preference"]
        facts = [m for m in memories if m["memory_type"] == "fact"]
        goals = [m for m in memories if m["memory_type"] == "goal"]
        interests = [m for m in memories if m["memory_type"] == "interest"]

        if preferences:
            pref_text = "\n".join([f"- {m['value']}" for m in preferences[:5]])
            context_parts.append(f"User Preferences:\n{pref_text}")

        if facts:
            facts_text = "\n".join([f"- {m['value']}" for m in facts[:5]])
            context_parts.append(f"About the User:\n{facts_text}")

        if goals:
            goals_text = "\n".join([f"- {m['value']}" for m in goals[:3]])
            context_parts.append(f"User Goals:\n{goals_text}")

        if interests:
            interests_text = "\n".join([f"- {m['value']}" for m in interests[:5]])
            context_parts.append(f"User Interests:\n{interests_text}")

        # Add recent conversation summaries
        if summaries:
            summaries_text = "\n".join([
                f"- {s.get('short_summary', 'Previous conversation')}"
                for s in summaries[:3]
            ])
            context_parts.append(f"Recent Conversations:\n{summaries_text}")

        if not context_parts:
            return ""

        # Combine all parts
        full_context = "\n\n".join(context_parts)

        return f"""
[CONTEXT FROM PREVIOUS INTERACTIONS]
{full_context}
[END CONTEXT]

Please use this context to provide more personalized and contextually aware responses.
""".strip()

    async def extract_memories_from_conversation(
        self,
        user_id: str,
        conversation_id: str,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract potential memories from a conversation
        This is a simple keyword-based extraction.
        In production, you'd use an AI model for better extraction.

        Args:
            user_id: User ID
            conversation_id: Conversation ID
            messages: List of messages

        Returns:
            List of extracted memories
        """
        extracted_memories = []

        # Keywords for different memory types
        preference_keywords = ["prefer", "like", "love", "hate", "dislike", "favorite", "favourite"]
        fact_keywords = ["i am", "i'm", "my name is", "i work", "i live", "i have"]
        goal_keywords = ["want to", "planning to", "goal", "trying to", "working on"]
        interest_keywords = ["interested in", "passionate about", "hobby", "enjoy"]

        for message in messages:
            if message.get("role") != "user":
                continue

            content = message.get("content", "").lower()

            # Extract preferences
            if any(keyword in content for keyword in preference_keywords):
                memory = {
                    "memory_type": "preference",
                    "content": message.get("content"),
                    "confidence": 0.7
                }
                extracted_memories.append(memory)

            # Extract facts
            if any(keyword in content for keyword in fact_keywords):
                memory = {
                    "memory_type": "fact",
                    "content": message.get("content"),
                    "confidence": 0.8
                }
                extracted_memories.append(memory)

            # Extract goals
            if any(keyword in content for keyword in goal_keywords):
                memory = {
                    "memory_type": "goal",
                    "content": message.get("content"),
                    "confidence": 0.7
                }
                extracted_memories.append(memory)

            # Extract interests
            if any(keyword in content for keyword in interest_keywords):
                memory = {
                    "memory_type": "interest",
                    "content": message.get("content"),
                    "confidence": 0.7
                }
                extracted_memories.append(memory)

        return extracted_memories

    async def save_memory_from_text(
        self,
        user_id: str,
        memory_type: str,
        text: str,
        conversation_id: Optional[str] = None,
        confidence: float = 1.0
    ) -> Optional[Dict[str, Any]]:
        """
        Save a memory extracted from text

        Args:
            user_id: User ID
            memory_type: Type of memory (preference, fact, goal, etc.)
            text: The memory text
            conversation_id: Source conversation ID
            confidence: Confidence score

        Returns:
            Created memory or None
        """
        # Generate a key from the text (simple hash)
        key = f"{memory_type}_{hash(text.lower()[:100])}"

        memory = UserMemoryCreate(
            memory_type=memory_type,
            key=key,
            value=text,
            confidence=Decimal(str(confidence)),
            source_conversation_id=conversation_id
        )

        try:
            return await self.db.create_user_memory(user_id=user_id, memory=memory)
        except Exception as e:
            print(f"Error saving memory: {e}")
            return None

    async def generate_conversation_summary(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Generate a simple summary of a conversation
        In production, you'd use an AI model for better summarization

        Args:
            conversation_id: Conversation ID
            messages: List of messages

        Returns:
            Summary text or None
        """
        if not messages:
            return None

        # Simple summary: count messages and extract topics
        user_messages = [m for m in messages if m.get("role") == "user"]
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]

        # Extract common words as topics (very basic)
        all_text = " ".join([m.get("content", "") for m in messages]).lower()

        # Create simple summary
        summary = f"Conversation with {len(user_messages)} user messages and {len(assistant_messages)} AI responses"

        # Try to extract first user message as context
        if user_messages:
            first_message = user_messages[0].get("content", "")[:100]
            summary += f". Started with: {first_message}"

        return summary

    async def save_conversation_summary(
        self,
        conversation_id: str,
        short_summary: str,
        detailed_summary: Optional[str] = None,
        key_topics: Optional[List[str]] = None,
        importance_score: float = 0.5
    ) -> Optional[Dict[str, Any]]:
        """
        Save a conversation summary

        Args:
            conversation_id: Conversation ID
            short_summary: Brief summary
            detailed_summary: Detailed summary
            key_topics: List of topics
            importance_score: Importance score

        Returns:
            Created summary or None
        """
        summary = ConversationSummaryCreate(
            conversation_id=conversation_id,
            short_summary=short_summary,
            detailed_summary=detailed_summary,
            key_topics=key_topics or [],
            importance_score=Decimal(str(importance_score))
        )

        try:
            return await self.db.create_conversation_summary(summary=summary)
        except Exception as e:
            print(f"Error saving conversation summary: {e}")
            return None
