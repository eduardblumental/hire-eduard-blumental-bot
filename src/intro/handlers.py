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
        CallbackQueryHandler(callback=q_handle_why_hire_me, pattern=f'^{WHY_HIRE_ME}$')
    ],
    states={
        WATCHING: [
            CallbackQueryHandler(callback=q_handle_back_to_intro, pattern=f'^{INTRO}$'),
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)

intro_handlers = [
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    intro_conversation_handler
]

