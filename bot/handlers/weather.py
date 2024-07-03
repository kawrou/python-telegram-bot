from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import logging
import requests

LOCATION = range(1)
logger = logging.getLogger(__name__)


# Start the weather conversation
async def start_weather_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    logger.info(f"Start weather conversation with chat_id: {chat_id}")
    await context.bot.send_message(
        chat_id=chat_id, text="What city would you like to know the weather for?"
    )
    return LOCATION


# Use users response to fetch weather data
async def handle_weather_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    location = update.message.text.lower()
    logger.info(f"Received location: {location} for chat_id: {chat_id}")

    try:
        response = requests.get(f"https://goweather.herokuapp.com/weather/{location}")
        if not response.content:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Sorry, I couldn't find weather data for that city.",
            )
            logger.info(f"No content in API response for location: {location}")
            return

        API_DATA = response.json()
        if not API_DATA:
            await context.bot.send_message(
                chat_id=chat_id, text="Sorry, I couldn't find that city."
            )
            logger.info(f"No weather data found for location: {location}")
            return

        for key, value in API_DATA.items():
            if key != "forecast":
                await context.bot.send_message(chat_id=chat_id, text=f"{key}:{value}")

            if key == "forecast":
                forecast_text = format_forecast(value)
                await context.bot.send_message(chat_id=chat_id, text=forecast_text)

        logger.info(f"Weather data sent to chat_id: {chat_id}")

    except requests.exceptions.RequestException as e:
        await context.bot.send_message(
            chat_id=chat_id, text=f"Sorry an error occured: {e}"
        )
        logger.error(f"RequestException: {e}")

    return ConversationHandler.END


def format_forecast(value):
    forecast_text = "Forecast:\n"
    for daily_forecast in value:
        forecast_text += f"Day {daily_forecast['day']} - Temperature:{daily_forecast['temperature']} - Wind:{daily_forecast['wind']}\n"
    return forecast_text


# Defines a conversation that is registered inside bot.py
weather_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("weather", start_weather_conversation)],
    states={
        LOCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_weather_location)
        ],
    },
    fallbacks=[],
)
