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

from .keyboards import social_media_keyboard


async def q_handle_start_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_kwargs = {
        'text': 'Online presence',
        'reply_markup': social_media_keyboard
    }

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(**message_kwargs)
        return SOCIAL
    else:
        await update.effective_message.reply_text(**message_kwargs)


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
        text=f'I am not sure what {update.message.text} means. Please, use the buttons 💁🏻‍♀️'
    )
    await q_handle_start_social(update, context)


social_handlers = [
    CallbackQueryHandler(callback=q_handle_start_social, pattern=f'^{SOCIAL}$'),
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_error, filters=filters.TEXT)
]
