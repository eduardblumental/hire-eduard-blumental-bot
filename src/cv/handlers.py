from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from src.keyboards import main_menu_keyboard
from src.states import CV, MAIN_MENU

from .keyboards import cv_keyboard, reading_keyboard
from .states import EXPERIENCE, EDUCATION, TECH_STACK, LANGUAGES, READING
from src.utils import go_to_menu, start_module, handle_error


async def q_handle_start_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='CV',
        reply_markup=cv_keyboard, return_value=CV
    )


async def q_handle_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.bot_data.get('experience.md'),
        parse_mode=ParseMode.HTML,
        reply_markup=reading_keyboard
    )

    return READING


async def q_handle_back_to_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='CV menu',
        reply_markup=cv_keyboard
    )

    return ConversationHandler.END


async def q_handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)


async def handle_cv_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=q_handle_start_cv,
                       error_message='Error')


cv_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_experience, pattern=f'^{EXPERIENCE}$'),
    ],
    states={
        READING: [
            CallbackQueryHandler(callback=q_handle_back_to_cv, pattern=f'^{CV}$'),
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_cv_error, filters=filters.ALL)
    ]
)

cv_handlers = [
    cv_conversation_handler,
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_cv_error, filters=filters.ALL)
]

