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

from intro.handlers import q_handle_start_intro, intro_handlers
from social.handlers import q_handle_start_social, social_handlers

from keyboards import main_menu_keyboard
from states import INTRO, SOCIAL


async def handle_load_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Uploading data...')

    for video in os.listdir('../static'):
        msg = await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=open(os.path.join('../static', video), 'rb'),
            read_timeout=10000,
            write_timeout=10000
        )

        context.bot_data[video] = msg.video.file_id

    await update.message.reply_text('Data has been uploaded..')


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
        CallbackQueryHandler(callback=q_handle_start_intro, pattern=f'^{INTRO}$'),
        CallbackQueryHandler(callback=q_handle_start_social, pattern=f'^{SOCIAL}$')
    ],
    states={
        INTRO: intro_handlers,
        SOCIAL: social_handlers
    },
    fallbacks=[
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)
