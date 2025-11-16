"""Conversation data models"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ConversationBase(BaseModel):
    """Base conversation model"""
    title: Optional[str] = Field(default="New Chat", max_length=200)
    model: Optional[str] = Field(default="gpt-3.5-turbo", max_length=50)


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation"""
    pass


class ConversationUpdate(BaseModel):
    """Model for updating a conversation"""
    title: Optional[str] = Field(default=None, max_length=200)
    model: Optional[str] = Field(default=None, max_length=50)


class Conversation(ConversationBase):
    """Full conversation model from database"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Conversation response with message count"""
    id: UUID
    user_id: UUID
    title: str
    model: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

    class Config:
        from_attributes = True
