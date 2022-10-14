from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from src.states import CV, MAIN_MENU

from .keyboards import cv_keyboard, reading_keyboard
from .states import EXPERIENCE, EDUCATION, TECH_STACK, LANGUAGES, READING
from src.utils import go_to_menu, start_module, handle_error


async def handle_start_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='CV', reply_markup=cv_keyboard
    )
    return CV


async def handle_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=context.bot_data.get('experience.md'),
        parse_mode=ParseMode.HTML,
        reply_markup=reading_keyboard
    )
    return READING


async def handle_back_to_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_start_cv(update, context)
    return ConversationHandler.END


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_reading_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_cv)
    return ConversationHandler.END


async def handle_cv_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_cv)


cv_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_experience, pattern=f'^{EXPERIENCE}$'),
    ],
    states={
        READING: [
            CallbackQueryHandler(callback=handle_back_to_cv, pattern=f'^{CV}$'),
            MessageHandler(callback=handle_reading_error, filters=filters.ALL)
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_cv_error, filters=filters.ALL)
    ]
)

cv_handlers = [
    cv_conversation_handler,
    CallbackQueryHandler(callback=handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_cv_error, filters=filters.ALL)
]

