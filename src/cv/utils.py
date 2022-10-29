import logging, os

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
            reply_markup=reading_keyboard,
            disable_web_page_preview=True
        )
        logger.info(msg=f'Read file "{file_name}".', extra={'username': update.effective_user.username})
    except BadRequest as e:
        await query.edit_message_text(
            text="The file isn't available yet. Please, try again later.",
            reply_markup=reading_keyboard
        )
        await context.bot.send_message(
            chat_id=os.environ.get('ADMIN_TELEGRAM_USER_ID'),
            text=f'File "{file_name}" is not available. Upload it ASAP.'
        )
        logger.error(msg=f'File "{file_name}" is not available.', extra={'username': update.effective_user.username})
