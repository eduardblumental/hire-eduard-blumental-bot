import logging

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from .keyboards import reading_keyboard

logger = logging.getLogger('main_logger')


async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name):
    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            text=context.bot_data.get(file_name),
            parse_mode=ParseMode.HTML,
            reply_markup=reading_keyboard
        )
        logger.info(f'User {update.effective_user.username} read "{file_name}".')
    except BadRequest as e:
        await query.edit_message_text(
            text="The file isn't available yet. Please, try again later.",
            reply_markup=reading_keyboard
        )
        logger.error(f'File "{file_name}" is not available. User {update.effective_user.username} could not read it.')
