import pytest
import datetime
import asyncio
from unittest.mock import AsyncMock, call
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes, ConversationHandler
from bot.bot import (
    start_command,
    age_confirmation,
    terms_confirmation,
    greeting,
    AGE_CONFIRMATION,
    TERMS_CONFIRMATION,
)

@pytest.fixture
def mock_update(mocker):
    mock_message = mocker.MagicMock(spec=Message)
    mock_message.text = "/start"  # Start with "/start" command
    mock_message.chat = Chat(id=456, type='private')
    update = Update(update_id=1,message=mock_message)
    return update

@pytest.fixture
def mock_context(mocker):
    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.send_message = AsyncMock()
    return context

@pytest.mark.asyncio
async def test_conversation_flow(mock_update, mock_context):
    # Start the conversation
    state = await start_command(mock_update, mock_context)
    assert state == AGE_CONFIRMATION
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=456,
        text="Please confirm your age. If you are over 18 reply with a 'yes'.",
    )

    # Provide age confirmation
    mock_update.message.text = "yes"
    state = await age_confirmation(mock_update, mock_context)
    assert state == TERMS_CONFIRMATION
    mock_context.bot.send_message.assert_called_with(
        chat_id=456,
        text="Please accept the terms of service. Reply with 'yes' or 'no'.",
    )

    # Accept terms
    mock_update.message.text = "yes"
    state = await terms_confirmation(mock_update, mock_context)
    assert state == ConversationHandler.END

    expected_calls = [
        call(chat_id=456, text="Thank you for accepting our terms of service"),
        call(chat_id=456, text="Here are a list of commands"),
    ]

    mock_context.bot.send_message.assert_has_calls(expected_calls)
    assert mock_context.bot.send_message.call_count == 4