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
from cv.handlers import q_handle_start_cv, cv_handlers
from contact_me.handlers import q_handle_start_contact_me, contact_me_handlers

from states import INTRO, SOCIAL, CV, CONTACT_ME
from utils import go_to_menu


async def handle_load_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Uploading data...')
    video_dir = os.path.join('..', 'static', 'videos')
    markdown_dir = os.path.join('..', 'static', 'markdown')

    for video in os.listdir(video_dir):
        msg = await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=open(os.path.join(video_dir, video), 'rb'),
            read_timeout=10000,
            write_timeout=10000
        )

        context.bot_data[video] = msg.video.file_id

    for file in os.listdir(markdown_dir):
        with open(os.path.join(markdown_dir, file), 'r') as f:
            context.bot_data[file] = f.read()

    await update.message.reply_text('Data has been uploaded..')


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        text=f'I am not sure what "{update.message.text}" means. Please, use the buttons 💁🏻‍♀️'
    )
    await handle_start(update, context)


main_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_start_intro, pattern=f'^{INTRO}$'),
        CallbackQueryHandler(callback=q_handle_start_social, pattern=f'^{SOCIAL}$'),
        CallbackQueryHandler(callback=q_handle_start_cv, pattern=f'^{CV}$'),
        CallbackQueryHandler(callback=q_handle_start_contact_me, pattern=f'^{CONTACT_ME}$')
    ],
    states={
        INTRO: intro_handlers,
        SOCIAL: social_handlers,
        CV: cv_handlers,
        CONTACT_ME: contact_me_handlers
    },
    fallbacks=[
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)
