import logging

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

from .keyboards import intro_keyboard
from .states import MY_JOURNEY, WHY_HIRE_ME, WATCHING
from .utils import send_video, safely_delete_message

logger = logging.getLogger('main_logger')


async def handle_start_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Watch a short video where I tell you more about myself 📺', reply_markup=intro_keyboard,
        log_msg='Entered section "Intro".'
    )
    return INTRO


async def handle_my_journey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(update=update, context=context, file_name='my_journey.mp4', caption='My journey 🏂')
    return WATCHING


async def handle_why_hire_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(update=update, context=context, file_name='why_hire_me.mp4', caption='Why hire me 🔮')
    return WATCHING


async def handle_back_to_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safely_delete_message(update, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Intro menu',
        reply_markup=intro_keyboard
    )
    logger.info(msg=f'Went back to "Intro".', extra={'username': update.effective_user.username})
    return ConversationHandler.END


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_watching_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_intro)
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
            MessageHandler(callback=handle_watching_error, filters=filters.ALL)
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_intro_error, filters=filters.ALL)
    ]
)

intro_handlers = [
    intro_conversation_handler,
    CallbackQueryHandler(callback=handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_intro_error, filters=filters.ALL)
]
