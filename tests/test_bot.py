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
    help_command,
    AGE_CONFIRMATION,
    TERMS_CONFIRMATION,
)


@pytest.fixture
def mock_context(mocker):
    context = mocker.Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.send_message = AsyncMock()
    return context


@pytest.fixture
def create_mock_update(mocker):
    def _create_mock_update(text: str):
        mock_user = User(
            id=123,
            first_name="first_name",
            last_name="last_name",
            is_bot=False,
            username="username",
        )
        mock_chat = Chat(id=456, type="private")

        mock_message = mocker.MagicMock(spec=Message)
        mock_message.text = text
        mock_message.chat = mock_chat
        mock_message.from_user = mock_user

        update = Update(update_id=1, message=mock_message)
        return update

    return _create_mock_update


@pytest.mark.asyncio
async def test_start_command(create_mock_update, mock_context):
    mock_update = create_mock_update("/start")
    state = await start_command(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=456,
        text="Please confirm your age. If you are over 18 reply with a 'yes'.",
    )
    assert state == AGE_CONFIRMATION


@pytest.mark.asyncio
async def test_age_confirmation(create_mock_update, mock_context):
    mock_update = create_mock_update("yes")
    state = await age_confirmation(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=456,
        text="Please accept the terms of service. Reply with 'yes' or 'no'.",
    )

    assert state == TERMS_CONFIRMATION


@pytest.mark.asyncio
async def test_terms_confirm(create_mock_update, mock_context):
    mock_update = create_mock_update("yes")
    state = await terms_confirmation(mock_update, mock_context)
    expected_calls = [
        call(chat_id=456, text="Thank you for accepting our terms of service"),
        call(chat_id=456, text="Here are a list of commands"),
    ]

    mock_context.bot.send_message.assert_has_calls(expected_calls)
    assert mock_context.bot.send_message.call_count == 2
    assert state == ConversationHandler.END


@pytest.mark.asyncio
async def test_greeting(create_mock_update, mock_context):
    mock_update = create_mock_update("hi")
    await greeting(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=456, text="Hi first_name last_name"
    )


@pytest.mark.asyncio
async def test_help_command(create_mock_update, mock_context):
    mock_update = create_mock_update("/help")
    await help_command(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=456,
        text="/help - Show this help message\n/pokemon - Find a pokemon\n/weather - Get the weather for a city\n/cat - Get a photo of a cat by its colour\n",
    )

# @pytest.mark.asyncio
# async def test_handle_cat_colour(create_mock_update, mock_context):
#     mock_update = create_mock_update("orange")
#     await handle_cat_colour(mock_update, mock_context)
#     mock_context.bot.send_photo(chat_id=456, photo="")
