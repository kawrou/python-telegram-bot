from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from utils.api_helpers import fetch_cat_photo


COLOR = range(1)


# Function to start the cat conversation
async def start_cat_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
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


cat_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("cat", start_cat_conversation)],
    states={
        COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cat_colour)],
    },
    fallbacks=[],
)
