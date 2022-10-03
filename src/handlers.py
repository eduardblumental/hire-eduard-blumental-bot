from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from intro.handlers import q_handle_start_intro, intro_conversation_handler
from social.handlers import q_handle_start_social, social_media_handlers

from keyboards import main_menu_keyboard
from states import INTRO, SOCIAL_MEDIA


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text='Hi!',
        reply_markup=main_menu_keyboard
    )


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        text=f'I am not sure what "{update.message.text}" means. Please, use the buttons 💁🏻‍♀️'
    )
    await handle_start(update, context)


main_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_start_social, pattern=f'^{SOCIAL_MEDIA}$')
    ],
    states={
        INTRO: intro_conversation_handler,
        SOCIAL_MEDIA: social_media_handlers
    },
    fallbacks=[
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)
