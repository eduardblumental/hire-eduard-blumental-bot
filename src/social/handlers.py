from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)


from src.keyboards import main_menu_keyboard
from src.states import SOCIAL, MAIN_MENU
from src.utils import go_to_menu, start_module, handle_error

from .keyboards import social_media_keyboard


async def q_handle_start_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Online Presence',
        reply_markup=social_media_keyboard, return_value=SOCIAL
    )


async def q_handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Main menu',
        reply_markup=main_menu_keyboard
    )

    return ConversationHandler.END


async def handle_social_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=q_handle_start_social,
                       error_message='Error')


social_handlers = [
    CallbackQueryHandler(callback=q_handle_start_social, pattern=f'^{SOCIAL}$'),
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_social_error, filters=filters.TEXT)
]
