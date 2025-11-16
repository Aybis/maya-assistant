"""Conversation Summary data models"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class ConversationSummaryBase(BaseModel):
    """Base conversation summary model"""
    short_summary: str = Field(min_length=1, max_length=500)
    detailed_summary: Optional[str] = None
    key_topics: Optional[List[str]] = Field(default_factory=list)
    entities: Optional[Dict[str, Any]] = Field(default_factory=dict)
    sentiment: Optional[Literal["positive", "neutral", "negative", "mixed"]] = None
    importance_score: Optional[Decimal] = Field(default=Decimal("0.5"), ge=0, le=1)


class ConversationSummaryCreate(ConversationSummaryBase):
    """Model for creating a new conversation summary"""
    conversation_id: UUID


class ConversationSummaryUpdate(BaseModel):
    """Model for updating a conversation summary"""
    short_summary: Optional[str] = Field(default=None, max_length=500)
    detailed_summary: Optional[str] = None
    key_topics: Optional[List[str]] = None
    entities: Optional[Dict[str, Any]] = None
    sentiment: Optional[Literal["positive", "neutral", "negative", "mixed"]] = None
    importance_score: Optional[Decimal] = Field(default=None, ge=0, le=1)


class ConversationSummary(ConversationSummaryBase):
    """Full conversation summary model from database"""
    id: UUID
    conversation_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationSummaryResponse(ConversationSummary):
    """Conversation summary response model"""
    pass
