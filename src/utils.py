from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)


from keyboards import main_menu_keyboard


async def start_module(update: Update, context: ContextTypes.DEFAULT_TYPE, text, reply_markup):
    message_kwargs = {
        'text': text,
        'reply_markup': reply_markup
    }

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(**message_kwargs)
    else:
        await update.effective_message.reply_text(**message_kwargs)


async def go_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_kwargs = {
        'text': 'Main menu',
        'reply_markup': main_menu_keyboard
    }

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(**message_kwargs)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, **message_kwargs)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE, callback, error_message):
    await update.effective_message.reply_text(
        text=error_message
    )

    await callback(update, context)

