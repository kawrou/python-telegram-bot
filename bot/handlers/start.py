from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters,
)
from utils.command_list import COMMANDS_LIST

AGE_CONFIRMATION, TERMS_CONFIRMATION = range(2)


VERIFIED = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please confirm your age. If you are over 18 reply with a 'yes'.",
    )

    return AGE_CONFIRMATION


async def age_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.lower() in ["yes"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please accept the terms of service. Reply with 'yes' or 'no'.",
        )
        return TERMS_CONFIRMATION


async def terms_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.message.text.lower() in ["yes"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Thank you for accepting our terms of service",
        )
        help_text = "Available Commands:\n"
        for command, description in COMMANDS_LIST.items():
            help_text += f"/{command} - {description}\n"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        AGE_CONFIRMATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, age_confirmation)
        ],
        TERMS_CONFIRMATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, terms_confirmation)
        ],
    },
    fallbacks=[],
)
