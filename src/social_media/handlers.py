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
from src.states import SOCIAL_MEDIA

from .keyboards import social_media_keyboard
from .states import BACK_TO_MENU


async def q_handle_start_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Online presence',
        reply_markup=social_media_keyboard
    )

    return SOCIAL_MEDIA


async def q_handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Main menu',
        reply_markup=main_menu_keyboard
    )

    return ConversationHandler.END


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        text='I am not sure what {} means. Please, use the buttons 😊',
        reply_markup=social_media_keyboard
    )


social_media_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=q_handle_start_social, pattern=f'^{SOCIAL_MEDIA}$')],
    states={
        SOCIAL_MEDIA: [CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{BACK_TO_MENU}$')]
    },
    fallbacks=[MessageHandler(callback=handle_error, filters=filters.TEXT)]
)
