"""Message data models"""

from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from uuid import UUID


class MessageBase(BaseModel):
    """Base message model"""
    role: Literal["user", "assistant"]
    content: str
    model: Optional[str] = None


class MessageCreate(BaseModel):
    """Model for creating a new message"""
    content: str = Field(min_length=1)
    model: Optional[str] = None


class Message(MessageBase):
    """Full message model from database"""
    id: UUID
    conversation_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(Message):
    """Message response model"""
    pass
