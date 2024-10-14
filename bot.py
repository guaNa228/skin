from telegram import Update
from telegram import ReplyKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import os
import time
import asyncio
from dotenv import load_dotenv
from telegram.ext import CallbackContext
from bot_handlers import handle_valid_message, reject_invalid_message
from io import BytesIO

load_dotenv()


async def main():
    # Getting bot token
    TOKEN = os.getenv('BOT_TOKEN')

    application = Application.builder().token(TOKEN).build()

    # Handling messages with a picture as valid messages
    application.add_handler(MessageHandler(
        filters.PHOTO & ~filters.TEXT, handle_valid_message))

    # Handling messages without a picture as invalid ones
    application.add_handler(MessageHandler(
        filters.ALL & ~filters.PHOTO, reject_invalid_message))

    # Initializing bot application and starting to poll
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        # Creating execution loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
