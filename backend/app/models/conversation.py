"""Conversation data models"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ConversationBase(BaseModel):
    """Base conversation model"""
    title: Optional[str] = Field(default="New Chat", max_length=200)
    model: Optional[str] = Field(default="gpt-5", max_length=50)
    summary: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation"""
    pass


class ConversationUpdate(BaseModel):
    """Model for updating a conversation"""
    title: Optional[str] = Field(default=None, max_length=200)
    model: Optional[str] = Field(default=None, max_length=50)
    summary: Optional[str] = None
    tags: Optional[List[str]] = None


class Conversation(ConversationBase):
    """Full conversation model from database"""
    id: UUID
    user_id: UUID
    message_count: Optional[int] = 0
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
    summary: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    message_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
