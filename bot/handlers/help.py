from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.command_list import COMMANDS_LIST


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "Available Commands:\n"
    for command, description in COMMANDS_LIST.items():
        help_text += f"/{command} - {description}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


help_command_handler = CommandHandler("help", help_command)
