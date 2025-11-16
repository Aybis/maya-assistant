"""AI Service factory for routing to different AI providers"""

from typing import List, AsyncGenerator, Optional
from .openai_service import OpenAIService
from .claude_service import ClaudeService
from .gemini_service import GeminiService
from ..config import settings


class AIService:
    """Factory service to route requests to appropriate AI provider"""

    def __init__(self):
        """Initialize available AI services"""
        self.services = {}

        # Initialize OpenAI if API key is available
        if settings.OPENAI_API_KEY:
            try:
                self.services['openai'] = OpenAIService()
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")

        # Initialize Anthropic if API key is available
        if settings.ANTHROPIC_API_KEY:
            try:
                self.services['anthropic'] = ClaudeService()
            except Exception as e:
                print(f"Failed to initialize Anthropic: {e}")

        # Initialize Google if API key is available
        if settings.GOOGLE_API_KEY:
            try:
                self.services['google'] = GeminiService()
            except Exception as e:
                print(f"Failed to initialize Google: {e}")

    def get_provider_from_model(self, model: str) -> Optional[str]:
        """Determine provider from model name"""
        model_lower = model.lower()

        if model_lower.startswith('gpt'):
            return 'openai'
        elif model_lower.startswith('claude'):
            return 'anthropic'
        elif model_lower.startswith('gemini'):
            return 'google'

        return None

    async def chat_completion_stream(
        self,
        messages: List[dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """
        Route chat completion to appropriate service

        Args:
            messages: List of message dicts
            model: Model identifier
            temperature: Response randomness
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks from the model
        """
        provider = self.get_provider_from_model(model)

        if not provider:
            yield f"Error: Unknown model '{model}'"
            return

        if provider not in self.services:
            yield f"Error: {provider} service not configured"
            return

        service = self.services[provider]

        async for chunk in service.chat_completion_stream(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        ):
            yield chunk

    def get_available_models(self) -> List[dict]:
        """Get all available models from configured services"""
        models = []

        if 'openai' in self.services:
            models.extend(OpenAIService.get_available_models())

        if 'anthropic' in self.services:
            models.extend(ClaudeService.get_available_models())

        if 'google' in self.services:
            models.extend(GeminiService.get_available_models())

        return models
