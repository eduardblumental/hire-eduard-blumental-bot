import logging, os

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from .keyboards import watching_keyboard

logger = logging.getLogger('main_logger')


async def safely_delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.delete_message()
    except BadRequest as e:
        await context.bot.send_message(
            chat_id=os.environ.get('ADMIN_TELEGRAM_USER_ID'),
            text=f'WARNING: "{e}". Can be ignored.'
        )
        logger.warning(msg=f'No message to delete: "{e}".', extra={'username': update.effective_user.username})


async def try_sending_video(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name, caption):
    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=context.bot_data.get(file_name),
        caption=caption,
        reply_markup=watching_keyboard
    )
    logger.info(msg=f'Watched video "{file_name}".', extra={'username': update.effective_user.username})


async def handle_video_is_not_available_error(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The video isn't available yet. Please, try again later.",
        reply_markup=watching_keyboard
    )
    await context.bot.send_message(
        chat_id=os.environ.get('ADMIN_TELEGRAM_USER_ID'),
        text=f'ERROR: Video "{file_name}" is not available. Upload it ASAP.'
    )
    logger.error(msg=f'Video "{file_name}" is not available.', extra={'username': update.effective_user.username})


async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name, caption):
    await safely_delete_message(update, context)
    try:
        await try_sending_video(update, context, file_name, caption)
    except BadRequest as e:
        await handle_video_is_not_available_error(update, context, file_name)
