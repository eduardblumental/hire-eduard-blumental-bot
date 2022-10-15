from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from src.states import INTRO, MAIN_MENU
from src.utils import go_to_menu, start_module, handle_error

from .keyboards import intro_keyboard, watching_keyboard
from .states import MY_JOURNEY, WHY_HIRE_ME, WATCHING
from .utils import send_video


async def handle_start_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Introduction', reply_markup=intro_keyboard
    )
    return INTRO


async def handle_my_journey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(
        update=update, context=context, filename='my_journey.mp4', caption='My journey 🏂',
        reply_markup=watching_keyboard
    )
    return WATCHING


async def handle_why_hire_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(
        update=update, context=context, filename='why_hire_me.mp4', caption='Why hire me 🔮',
        reply_markup=watching_keyboard
    )
    return WATCHING


async def handle_back_to_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await handle_error(update=update, context=context, callback=handle_start_intro)


intro_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_my_journey, pattern=f'^{MY_JOURNEY}$'),
        CallbackQueryHandler(callback=handle_why_hire_me, pattern=f'^{WHY_HIRE_ME}$')
    ],
    states={
        WATCHING: [
            CallbackQueryHandler(callback=handle_back_to_intro, pattern=f'^{INTRO}$'),
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

