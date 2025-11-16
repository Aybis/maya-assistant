"""User Memory data models"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class UserMemoryBase(BaseModel):
    """Base user memory model"""
    memory_type: Literal["preference", "fact", "goal", "context", "interest"]
    key: str = Field(min_length=1, max_length=500)
    value: str = Field(min_length=1)
    confidence: Optional[Decimal] = Field(default=Decimal("1.0"), ge=0, le=1)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserMemoryCreate(UserMemoryBase):
    """Model for creating a new user memory"""
    source_conversation_id: Optional[UUID] = None


class UserMemoryUpdate(BaseModel):
    """Model for updating a user memory"""
    value: Optional[str] = None
    confidence: Optional[Decimal] = Field(default=None, ge=0, le=1)
    metadata: Optional[Dict[str, Any]] = None


class UserMemory(UserMemoryBase):
    """Full user memory model from database"""
    id: UUID
    user_id: UUID
    source_conversation_id: Optional[UUID] = None
    last_accessed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserMemoryResponse(UserMemory):
    """User memory response model"""
    pass


class MemoryContextCreate(BaseModel):
    """Model for creating memory context link"""
    memory_id: UUID
    relevance_score: Optional[Decimal] = Field(default=Decimal("0.5"), ge=0, le=1)


class MemoryContext(BaseModel):
    """Full memory context model from database"""
    id: UUID
    conversation_id: UUID
    memory_id: UUID
    relevance_score: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
