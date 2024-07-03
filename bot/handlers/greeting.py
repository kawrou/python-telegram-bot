from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Hi {first_name} {last_name}"
    )


greeting_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), greeting)
