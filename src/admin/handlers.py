import os

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    filters
)


async def handle_load_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Uploading data...')
    video_dir = os.path.join('..', 'static', 'videos')
    markdown_dir = os.path.join('..', 'static', 'markdown')
    update.message.video.file_id

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


admin_handlers = [
    CommandHandler(callback=handle_load_data, command='load_data')
]
