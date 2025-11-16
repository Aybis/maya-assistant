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
            {
                "id": "gpt-4-turbo-preview",
                "name": "GPT-4 Turbo",
                "provider": "openai",
                "description": "Most capable GPT-4 model"
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "provider": "openai",
                "description": "High intelligence model"
            },
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "provider": "openai",
                "description": "Fast and efficient"
            }
        ]
