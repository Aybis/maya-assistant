"""AI Models API endpoints"""

from fastapi import APIRouter, Depends
from typing import List, Dict
from collections import defaultdict
from ..dependencies import get_current_user
from ..services.ai_service import AIService

router = APIRouter(prefix="/api", tags=["models"])


@router.get("/models")
async def get_available_models(
    current_user: dict = Depends(get_current_user)
) -> Dict:
    """Get list of available AI models grouped by brand"""
    ai_service = AIService()
    all_models = ai_service.get_available_models()

    # Group models by brand
    grouped_models = defaultdict(lambda: defaultdict(list))

    for model in all_models:
        brand = model.get("brand", model.get("provider", "Other"))
        category = model.get("category", "Other")
        grouped_models[brand][category].append(model)

    # Convert to regular dict with sorted structure
    result = {
        "grouped": dict(grouped_models),
        "flat": all_models  # Keep flat list for backward compatibility
    }

    return result


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Maya Assistant API is running"}
