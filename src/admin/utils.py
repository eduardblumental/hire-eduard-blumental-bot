import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def send_files_to_admin_from_dir(update: Update, context: ContextTypes.DEFAULT_TYPE, dir_name):
    dir_path = os.path.join('..', dir_name)
    for file_name in os.listdir(dir_path):
        with open(os.path.join(dir_path, file_name), 'r', encoding='utf-8') as f:
            contents = f.read()
            await update.message.reply_text(text=contents, parse_mode=ParseMode.HTML)
