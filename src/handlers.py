import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from about.handlers import handle_start_about, about_handlers
from social.handlers import handle_start_social, social_handlers
from cv.handlers import handle_start_cv, cv_handlers
from contact_me.handlers import handle_start_contact_me, contact_me_handlers

from states import ABOUT, SOCIAL, CV, CONTACT_ME
from utils import go_to_menu, handle_error

logger = logging.getLogger('main_logger')


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(
        update=update, context=context,
        text="Welcome! My name is HireEduardBlumentalBot. I am here to tell you more about Eduard " \
             "and help you make a hiring decision of a lifetime. Have fun! 😉",
        log_msg='Started using the bot.'
    )


async def handle_main_menu_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start)


main_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_start_about, pattern=f'^{ABOUT}$'),
        CallbackQueryHandler(callback=handle_start_social, pattern=f'^{SOCIAL}$'),
        CallbackQueryHandler(callback=handle_start_cv, pattern=f'^{CV}$'),
        CallbackQueryHandler(callback=handle_start_contact_me, pattern=f'^{CONTACT_ME}$')
    ],
    states={
        ABOUT: about_handlers,
        SOCIAL: social_handlers,
        CV: cv_handlers,
        CONTACT_ME: contact_me_handlers
    },
    fallbacks=[
        MessageHandler(callback=handle_main_menu_error, filters=filters.ALL)
    ]
)
