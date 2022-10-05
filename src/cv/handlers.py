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


async def q_handle_start_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_kwargs = {
        'text': 'CV',
        'reply_markup': cv_keyboard
    }

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(**message_kwargs)
        return CV
    else:
        await update.effective_message.reply_text(**message_kwargs)


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

    await q_handle_start_cv(update, context)


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
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)

cv_handlers = [
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    cv_conversation_handler
]

