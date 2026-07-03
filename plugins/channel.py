# MY code/plugins/channel.py

from pyrogram import Client, filters
from info import INDEX_CHANNELS, INDEX_EXTENSIONS
from database.ia_filterdb import save_file
import asyncio

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(INDEX_CHANNELS) & media_filter)
async def media(bot, message):
    # 1. Wait for the Media Info bot to finish its work (5-7 seconds)
    await asyncio.sleep(8) 

    # 2. Re-fetch the message from Telegram to get the UPDATED caption
    try:
        updated_message = await bot.get_messages(message.chat.id, message.id)
    except Exception:
        # If message was deleted in the meantime
        return

    # 3. Use the updated message for processing
    media = getattr(updated_message, updated_message.media.value, None)
    if media and (str(media.file_name).lower()).endswith(tuple(INDEX_EXTENSIONS)):
        # Pass the newly fetched caption
        media.caption = updated_message.caption 
        await save_file(media, updated_message.chat.id, updated_message.id)
