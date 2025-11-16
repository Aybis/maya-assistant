"""OpenAI service for GPT models"""

from openai import AsyncOpenAI
from typing import List, AsyncGenerator
from ..config import settings


class OpenAIService:
    """Service for OpenAI GPT models with streaming support"""

    def __init__(self):
        """Initialize OpenAI client"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")

        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def chat_completion_stream(
        self,
        messages: List[dict],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: OpenAI model name
            temperature: Response randomness (0-2)
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks from the model
        """
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"Error: {str(e)}"

    @staticmethod
    def get_available_models() -> List[dict]:
        """Return list of available OpenAI models"""
        return [
            # GPT-5 Models
            {
                "id": "gpt-5-nano",
                "name": "GPT-5 Nano",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-5",
                "description": "Ultra-fast, lightweight GPT-5"
            },
            {
                "id": "gpt-5-mini",
                "name": "GPT-5 Mini",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-5",
                "description": "Compact GPT-5 model"
            },
            {
                "id": "gpt-5",
                "name": "GPT-5",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-5",
                "description": "Next-generation GPT model"
            },
            # GPT-4 Models
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-4",
                "description": "Most capable GPT-4 model"
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-4",
                "description": "Advanced reasoning model"
            },
            {
                "id": "gpt-4o",
                "name": "GPT-4o",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-4",
                "description": "Optimized GPT-4 variant"
            },
            {
                "id": "gpt-4o-mini",
                "name": "GPT-4o Mini",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-4",
                "description": "Efficient GPT-4o variant"
            },
            # GPT-3.5 Models
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "provider": "openai",
                "brand": "GPT",
                "category": "GPT-3.5",
                "description": "Fast and cost-effective"
            }
        ]
