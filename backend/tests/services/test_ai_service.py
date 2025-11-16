"""Tests for AI service routing"""

import pytest
from app.services.ai_service import AIService
from unittest.mock import patch


def test_get_provider_from_gpt_model():
    """Test provider detection for GPT models"""
    service = AIService()
    assert service.get_provider_from_model("gpt-4") == "openai"
    assert service.get_provider_from_model("gpt-3.5-turbo") == "openai"
    assert service.get_provider_from_model("GPT-4") == "openai"


def test_get_provider_from_claude_model():
    """Test provider detection for Claude models"""
    service = AIService()
    assert service.get_provider_from_model("claude-3-opus") == "anthropic"
    assert service.get_provider_from_model("claude-2") == "anthropic"
    assert service.get_provider_from_model("CLAUDE-3-SONNET") == "anthropic"


def test_get_provider_from_gemini_model():
    """Test provider detection for Gemini models"""
    service = AIService()
    assert service.get_provider_from_model("gemini-pro") == "google"
    assert service.get_provider_from_model("gemini-1.5-pro") == "google"
    assert service.get_provider_from_model("GEMINI-PRO") == "google"


def test_get_provider_from_unknown_model():
    """Test provider detection for unknown models"""
    service = AIService()
    assert service.get_provider_from_model("unknown-model") is None
    assert service.get_provider_from_model("") is None


@patch('app.services.ai_service.settings')
def test_service_initialization_without_api_keys(mock_settings):
    """Test service initialization when no API keys are configured"""
    mock_settings.OPENAI_API_KEY = None
    mock_settings.ANTHROPIC_API_KEY = None
    mock_settings.GOOGLE_API_KEY = None

    service = AIService()
    assert len(service.services) == 0


@patch('app.services.ai_service.settings')
@patch('app.services.ai_service.OpenAIService')
def test_service_initialization_with_openai_key(mock_openai_class, mock_settings):
    """Test service initialization with OpenAI API key"""
    mock_settings.OPENAI_API_KEY = "test-key"
    mock_settings.ANTHROPIC_API_KEY = None
    mock_settings.GOOGLE_API_KEY = None

    service = AIService()
    assert 'openai' in service.services


@pytest.mark.asyncio
async def test_chat_completion_stream_unknown_model():
    """Test chat completion with unknown model yields error"""
    service = AIService()

    chunks = []
    async for chunk in service.chat_completion_stream(
        messages=[{"role": "user", "content": "test"}],
        model="unknown-model"
    ):
        chunks.append(chunk)

    assert len(chunks) == 1
    assert "Unknown model" in chunks[0]


@pytest.mark.asyncio
async def test_chat_completion_stream_unconfigured_service():
    """Test chat completion with unconfigured service yields error"""
    service = AIService()
    service.services = {}  # Empty services

    chunks = []
    async for chunk in service.chat_completion_stream(
        messages=[{"role": "user", "content": "test"}],
        model="gpt-4"
    ):
        chunks.append(chunk)

    assert len(chunks) == 1
    assert "service not configured" in chunks[0]
