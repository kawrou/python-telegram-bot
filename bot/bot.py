from dotenv import load_dotenv
import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

AGE_CONFIRMATION, TERMS_CONFIRMATION = range(2)
VERIFIED = {}

# Define states for the conversation
COLOR = range(1)

COMMANDS_LIST = {
    "help": "Show this help message",
    "pokemon": "Find a pokemon",
    "weather": "Get the weather for a city",
    "cat": "Get a photo of a cat by its colour",
}


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


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Hi {first_name} {last_name}"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "Available Commands:\n"
    for command, description in COMMANDS_LIST.items():
        help_text += f"/{command} - {description}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


# Function to start the conversation
async def start_cat_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id, text="Please provide a color for the cat photo."
    )
    return COLOR


async def handle_cat_colour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    colour = update.message.text.lower()
    cat_photo_url = fetch_cat_photo(colour)

    if cat_photo_url:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=cat_photo_url
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Sorry, couldn't find a photo"
        )

    return ConversationHandler.END


def fetch_cat_photo(colour: str) -> str:
    api_url = f"https://cataas.com/cat/{colour}"
    response = requests.get(api_url)
    if response.status_code == 200:
        # data = response.json()
        # return data.get("photo_url", None)
        return api_url
    else:
        return None


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

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

    greeting_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), greeting)

    help_command_handler = CommandHandler("help", help_command)

    cat_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("cat", start_cat_conversation)],
        states={
            COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cat_colour)],
        },
        fallbacks=[],
    )

    application.add_handler(conversation_handler)
    # application.add_handler(greeting_handler)
    application.add_handler(help_command_handler)
    application.add_handler(cat_conv_handler)

    application.run_polling()
