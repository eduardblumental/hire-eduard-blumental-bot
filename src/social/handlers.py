import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from states import SOCIAL, MAIN_MENU
from utils import go_to_menu, start_module, handle_error

from .keyboards import social_media_keyboard

logger = logging.getLogger('main_logger')


async def handle_start_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Connect on social media 📡', reply_markup=social_media_keyboard,
        log_msg='Entered section "Social".'
    )
    return SOCIAL


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_social_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_social)


social_handlers = [
    CallbackQueryHandler(callback=handle_start_social, pattern=f'^{SOCIAL}$'),
    CallbackQueryHandler(callback=handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_social_error, filters=filters.TEXT)
]
