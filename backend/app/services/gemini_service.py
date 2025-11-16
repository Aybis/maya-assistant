"""Google Gemini service"""

import google.generativeai as genai
from typing import List, AsyncGenerator
from ..config import settings


class GeminiService:
    """Service for Google Gemini models with streaming support"""

    def __init__(self):
        """Initialize Gemini client"""
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not configured")

        genai.configure(api_key=settings.GOOGLE_API_KEY)

    async def chat_completion_stream(
        self,
        messages: List[dict],
        model: str = "gemini-pro",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat completion

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Gemini model name
            temperature: Response randomness (0-1)
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks from the model
        """
        try:
            # Initialize model
            gemini_model = genai.GenerativeModel(model)

            # Convert messages to Gemini format
            chat_history = []
            last_message = None

            for msg in messages:
                if msg["role"] == "system":
                    # Gemini doesn't have system role, prepend to first user message
                    continue
                elif msg["role"] == "user":
                    role = "user"
                elif msg["role"] == "assistant":
                    role = "model"
                else:
                    continue

                if role == "user" and len(chat_history) == 0:
                    # First message - will be sent separately
                    last_message = msg["content"]
                else:
                    chat_history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

            # Start chat
            chat = gemini_model.start_chat(history=chat_history)

            # Get the last user message
            if not last_message and messages:
                last_message = messages[-1]["content"]

            if not last_message:
                yield "Error: No user message found"
                return

            # Generate streaming response
            response = chat.send_message(
                last_message,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"Error: {str(e)}"

    @staticmethod
    def get_available_models() -> List[dict]:
        """Return list of available Gemini models"""
        return [
            # Gemini 2.5 Models
            {
                "id": "gemini-2.5-flash",
                "name": "Flash 2.5",
                "provider": "google",
                "brand": "Gemini",
                "category": "Gemini 2.5",
                "description": "Lightning-fast Gemini 2.5"
            },
            {
                "id": "gemini-2.5-pro",
                "name": "Pro 2.5",
                "provider": "google",
                "brand": "Gemini",
                "category": "Gemini 2.5",
                "description": "Most capable Gemini 2.5"
            },
            # Gemini 1.5 Models
            {
                "id": "gemini-1.5-flash",
                "name": "Flash 1.5",
                "provider": "google",
                "brand": "Gemini",
                "category": "Gemini 1.5",
                "description": "Fast and efficient"
            },
            {
                "id": "gemini-1.5-pro",
                "name": "Pro 1.5",
                "provider": "google",
                "brand": "Gemini",
                "category": "Gemini 1.5",
                "description": "Advanced reasoning"
            },
            # Gemini 1.0 Models
            {
                "id": "gemini-pro",
                "name": "Pro",
                "provider": "google",
                "brand": "Gemini",
                "category": "Gemini 1.0",
                "description": "Balanced performance"
            },
            {
                "id": "gemini-pro-vision",
                "name": "Pro Vision",
                "provider": "google",
                "brand": "Gemini",
                "category": "Gemini 1.0",
                "description": "Multimodal with vision"
            }
        ]
