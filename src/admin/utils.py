import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def send_files_to_admin_from_dir(update: Update, context: ContextTypes.DEFAULT_TYPE, dir_name):
    dir_path = os.path.join('..', dir_name)
    for num, file_name in enumerate(os.listdir(dir_path)):
        with open(os.path.join(dir_path, file_name), 'r', encoding='utf-8') as f:
            contents = f.read()
            enumerated_contents = f'{num+1}. {contents[-4000:]}'
            await update.message.reply_text(text=enumerated_contents, parse_mode=ParseMode.HTML)
