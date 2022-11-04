import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from states import ABOUT, MAIN_MENU
from utils import go_to_menu, start_module, handle_error

from .keyboards import about_keyboard
from .states import ABOUT_ME, ABOUT_BOT, WATCHING
from .utils import send_video, safely_delete_message

logger = logging.getLogger('main_logger')


async def handle_start_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Watch a short video 📽', reply_markup=about_keyboard,
        log_msg='Entered section "About".'
    )
    return ABOUT


async def handle_about_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(update=update, context=context, file_name='about_me.mp4', caption='About me 🏂')
    return WATCHING


async def handle_about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(update=update, context=context, file_name='about_bot.mp4', caption='About bot 🤖')
    return WATCHING


async def handle_back_to_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safely_delete_message(update, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Watch a short video 📽',
        reply_markup=about_keyboard
    )
    logger.info(msg=f'Went back to "About".', extra={'username': update.effective_user.username})
    return ConversationHandler.END


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_watching_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_about)
    return ConversationHandler.END


async def handle_about_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_about)


about_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_about_me, pattern=f'^{ABOUT_ME}$'),
        CallbackQueryHandler(callback=handle_about_bot, pattern=f'^{ABOUT_BOT}$')
    ],
    states={
        WATCHING: [
            CallbackQueryHandler(callback=handle_back_to_about, pattern=f'^{ABOUT}$'),
            MessageHandler(callback=handle_watching_error, filters=filters.ALL)
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_about_error, filters=filters.ALL)
    ]
)

about_handlers = [
    about_conversation_handler,
    CallbackQueryHandler(callback=handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_about_error, filters=filters.ALL)
]
