import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from src.states import CV, MAIN_MENU
from src.utils import go_to_menu, start_module, handle_error

from .keyboards import cv_keyboard
from .states import EXPERIENCE, EDUCATION, TECH_STACK, SOFT_SKILLS, READING
from .utils import send_file

logger = logging.getLogger('main_logger')


async def handle_start_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='View my credentials 🔍', reply_markup=cv_keyboard,
        log_msg='Entered section "CV".'
    )
    return CV


async def handle_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update=update, context=context, file_name='experience.md')
    return READING


async def handle_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update=update, context=context, file_name='education.md')
    return READING


async def handle_tech_stack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update=update, context=context, file_name='tech_stack.md')
    return READING


async def handle_soft_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_file(update=update, context=context, file_name='soft_skills.md')
    return READING


async def handle_back_to_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_start_cv(update, context)
    return ConversationHandler.END


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_reading_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_cv)
    return ConversationHandler.END


async def handle_cv_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_cv)


cv_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_experience, pattern=f'^{EXPERIENCE}$'),
        CallbackQueryHandler(callback=handle_education, pattern=f'^{EDUCATION}$'),
        CallbackQueryHandler(callback=handle_tech_stack, pattern=f'^{TECH_STACK}$'),
        CallbackQueryHandler(callback=handle_soft_skills, pattern=f'^{SOFT_SKILLS}$'),
    ],
    states={
        READING: [
            CallbackQueryHandler(callback=handle_back_to_cv, pattern=f'^{CV}$'),
            MessageHandler(callback=handle_reading_error, filters=filters.ALL)
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_cv_error, filters=filters.ALL)
    ]
)

cv_handlers = [
    cv_conversation_handler,
    CallbackQueryHandler(callback=handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    MessageHandler(callback=handle_cv_error, filters=filters.ALL)
]

