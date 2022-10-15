from telegram import Update
from telegram.ext import ContextTypes

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


async def go_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None):
    if not text:
        text = 'Main menu'
    await start_module(update=update, context=context, text=text, reply_markup=main_menu_keyboard)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE, callback, error_message=None):
    if not error_message:
        error_message = f'I am not sure what "{update.message.text}" means. Please, use the buttons 💁🏻‍♀️'
    await update.effective_message.reply_text(text=error_message)
    await callback(update, context)
