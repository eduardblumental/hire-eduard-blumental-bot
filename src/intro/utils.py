from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from .keyboards import watching_keyboard


async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name, caption):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    try:
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=context.bot_data.get(file_name),
            caption=caption,
            reply_markup=watching_keyboard
        )
    except BadRequest as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The video isn't available yet. Please, try again later.",
            reply_markup=watching_keyboard
        )
