"""AI Models API endpoints"""

from fastapi import APIRouter, Depends
from typing import List, Dict
from ..dependencies import get_current_user
from ..services.ai_service import AIService

router = APIRouter(prefix="/api", tags=["models"])


@router.get("/models")
async def get_available_models(
    current_user: dict = Depends(get_current_user)
) -> List[Dict]:
    """Get list of available AI models"""
    ai_service = AIService()
    return ai_service.get_available_models()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Maya Assistant API is running"}
