from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext
from processing import process_image


# Valid message handler
async def handle_valid_message(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        # Get the file ID of the photo
        file_id = update.message.photo[-1].file_id

        # Download the photo
        file = await context.bot.get_file(file_id)
        file_bytearray = await file.download_as_bytearray()

        # Send the photo for further processing
        acne, areas = process_image(file_bytearray)

        # Create InputMediaPhoto objects for each byte array
        media1 = InputMediaPhoto(media=acne)
        media2 = InputMediaPhoto(media=areas)

        # Send the result back to the user
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[media1, media2],
            caption="🔵 - ance and pimples, 🟢 - damaged and suspicious areas"
        )
    else:
        await update.message.reply_text(invalid_input_message)


# Handler used to reject invalid messages
async def reject_invalid_message(update: Update, context: CallbackContext) -> None:
    if not update.message.media_group_id:
        await update.message.reply_text("Please, send a photo")
