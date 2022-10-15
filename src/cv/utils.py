from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from .keyboards import reading_keyboard


async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=context.bot_data.get(file_name),
        parse_mode=ParseMode.HTML,
        reply_markup=reading_keyboard
    )
