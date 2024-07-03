from dotenv import load_dotenv
import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
)

from handlers.help import help_command_handler
from handlers.start import conversation_handler
from handlers.cat import cat_conv_handler
from handlers.weather import weather_conv_handler
from handlers.greeting import greeting_handler

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    async def log_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info(f"Received update: {update}")

    application.add_handler(conversation_handler)
    application.add_handler(help_command_handler)
    application.add_handler(cat_conv_handler)
    application.add_handler(weather_conv_handler)
    application.add_handler(greeting_handler)

    application.run_polling()
