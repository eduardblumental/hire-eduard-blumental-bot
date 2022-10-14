import os

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

from .keyboards import intro_keyboard, watching_keyboard
from .states import MY_JOURNEY, WHY_HIRE_ME, WATCHING
from src.utils import go_to_menu, start_module, handle_error


async def q_handle_start_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Introduction', reply_markup=intro_keyboard
    )
    return INTRO


async def q_handle_my_journey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=context.bot_data.get('my_journey.mp4'),
        caption='My journey 🏂',
        reply_markup=watching_keyboard
    )

    return WATCHING


async def q_handle_why_hire_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=context.bot_data.get('why_hire_me.mp4'),
        caption='Why hire me 🔮',
        reply_markup=watching_keyboard
    )

    return WATCHING


async def q_handle_back_to_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Intro menu',
        reply_markup=intro_keyboard
    )

    return ConversationHandler.END


async def q_handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_intro_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=q_handle_start_intro,
                       error_message='Error')


intro_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_my_journey, pattern=f'^{MY_JOURNEY}$'),
        CallbackQueryHandler(callback=q_handle_why_hire_me, pattern=f'^{WHY_HIRE_ME}$')
    ],
    states={
        WATCHING: [
            CallbackQueryHandler(callback=q_handle_back_to_intro, pattern=f'^{INTRO}$'),
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_intro_error, filters=filters.ALL)
    ]
)

intro_handlers = [
    intro_conversation_handler,
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_intro_error, filters=filters.ALL)
]

