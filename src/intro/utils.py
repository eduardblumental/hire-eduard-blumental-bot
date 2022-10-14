from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)


async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, filename, caption, reply_markup):
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=context.bot_data.get(filename),
        caption=caption,
        reply_markup=reply_markup
    )
