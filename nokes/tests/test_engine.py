"""Tests for Nokes engine"""

import pytest
from unittest.mock import patch, AsyncMock
from nokes.core.engine import NokesEngine
from nokes.models.chat import ChatMessage


@pytest.mark.asyncio
@patch('nokes.core.engine.get_llm_provider')
async def test_chat_basic(mock_llm):
    """Test basic chat functionality"""
    mock_provider = AsyncMock()
    mock_provider.generate = AsyncMock(return_value="Test response")
    mock_llm.return_value = mock_provider

    engine = NokesEngine()
    response = await engine.chat("Hello Nokes")

    assert response.content == "Test response"
    assert response.conversation_turn == 1
    assert len(engine.conversation_history) == 1


@pytest.mark.asyncio
@patch('nokes.core.engine.get_llm_provider')
async def test_multiple_turns(mock_llm):
    """Test multiple conversation turns"""
    mock_provider = AsyncMock()
    mock_provider.generate = AsyncMock(side_effect=["Response 1", "Response 2"])
    mock_llm.return_value = mock_provider

    engine = NokesEngine()
    resp1 = await engine.chat("First message")
    resp2 = await engine.chat("Second message")

    assert resp1.conversation_turn == 1
    assert resp2.conversation_turn == 2
    assert len(engine.conversation_history) == 2


def test_clear_history():
    """Test clearing conversation history"""
    with patch('nokes.core.engine.get_llm_provider'):
        engine = NokesEngine()
        engine.conversation_history = [ChatMessage(role="user", content="test")]
        engine.clear_history()
        assert len(engine.conversation_history) == 0
