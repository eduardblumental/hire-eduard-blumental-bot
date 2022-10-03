from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from social_media.handlers import social_media_conversation_handler

from keyboards import main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text='Hi!',
        reply_markup=main_menu_keyboard
    )

main_conversation_handlers = [
    CommandHandler(command='start', callback=start),
    social_media_conversation_handler
]
