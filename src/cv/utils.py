from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from .keyboards import reading_keyboard


async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name):
    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            text=context.bot_data.get(file_name),
            parse_mode=ParseMode.HTML,
            reply_markup=reading_keyboard
        )
    except BadRequest as e:
        await query.edit_message_text(
            text="The file isn't available yet. Please, try again later.",
            reply_markup=reading_keyboard
        )
