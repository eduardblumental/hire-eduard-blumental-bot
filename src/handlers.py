import os

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from intro.handlers import handle_start_intro, intro_handlers
from social.handlers import handle_start_social, social_handlers
from cv.handlers import handle_start_cv, cv_handlers
from contact_me.handlers import handle_start_contact_me, contact_me_handlers

from states import INTRO, SOCIAL, CV, CONTACT_ME
from utils import go_to_menu, handle_error


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)


async def handle_main_menu_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start)


main_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_start_intro, pattern=f'^{INTRO}$'),
        CallbackQueryHandler(callback=handle_start_social, pattern=f'^{SOCIAL}$'),
        CallbackQueryHandler(callback=handle_start_cv, pattern=f'^{CV}$'),
        CallbackQueryHandler(callback=handle_start_contact_me, pattern=f'^{CONTACT_ME}$')
    ],
    states={
        INTRO: intro_handlers,
        SOCIAL: social_handlers,
        CV: cv_handlers,
        CONTACT_ME: contact_me_handlers
    },
    fallbacks=[
        MessageHandler(callback=handle_main_menu_error, filters=filters.ALL)
    ]
)
