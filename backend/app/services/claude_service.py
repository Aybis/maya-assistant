"""Anthropic Claude service"""

from anthropic import AsyncAnthropic
from typing import List, AsyncGenerator
from ..config import settings


class ClaudeService:
    """Service for Anthropic Claude models with streaming support"""

    def __init__(self):
        """Initialize Anthropic client"""
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def chat_completion_stream(
        self,
        messages: List[dict],
        model: str = "claude-3-sonnet-20240229",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Claude model name
            temperature: Response randomness (0-1)
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks from the model
        """
        try:
            # Separate system message if present
            system_message = None
            chat_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    chat_messages.append(msg)

            # Create streaming request
            stream_params = {
                "model": model,
                "messages": chat_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True
            }

            if system_message:
                stream_params["system"] = system_message

            async with self.client.messages.stream(**stream_params) as stream:
                async for text in stream.text_stream:
                    yield text

        except Exception as e:
            yield f"Error: {str(e)}"

    @staticmethod
    def get_available_models() -> List[dict]:
        """Return list of available Claude models"""
        return [
            {
                "id": "claude-3-opus-20240229",
                "name": "Claude 3 Opus",
                "provider": "anthropic",
                "description": "Most capable Claude model"
            },
            {
                "id": "claude-3-sonnet-20240229",
                "name": "Claude 3 Sonnet",
                "provider": "anthropic",
                "description": "Balanced performance and speed"
            },
            {
                "id": "claude-3-haiku-20240307",
                "name": "Claude 3 Haiku",
                "provider": "anthropic",
                "description": "Fastest Claude model"
            }
        ]
