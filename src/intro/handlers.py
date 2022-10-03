from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from src.keyboards import main_menu_keyboard
from src.states import INTRO, MAIN_MENU

from .keyboards import intro_keyboard, video_menu_keyboard
from .states import MY_JOURNEY, WHY_HIRE_ME, VIDEO_MENU


async def q_handle_start_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_kwargs = {
        'text': 'Introduction',
        'reply_markup': intro_keyboard
    }

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(**message_kwargs)
        return INTRO
    else:
        await update.effective_message.reply_text(**message_kwargs)


async def q_handle_my_journey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


async def q_handle_why_hire_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


async def q_handle_back_to_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Intro menu',
        reply_markup=intro_keyboard
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

    await q_handle_start_intro(update, context)


intro_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_my_journey, pattern=f'^{MY_JOURNEY}$'),
        CallbackQueryHandler(callback=q_handle_why_hire_me, pattern=f'^{WHY_HIRE_ME}$'),
    ],
    states={
        VIDEO_MENU: [
            CallbackQueryHandler(callback=q_handle_back_to_intro, pattern=f'^{INTRO}$'),
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)
