import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def send_files_to_admin_from_dir(update: Update, context: ContextTypes.DEFAULT_TYPE, dir_name):
    dir_path = os.path.join('..', dir_name)
    if os.path.exists(dir_path):
        for file_name in os.listdir(dir_path):
            with open(os.path.join(dir_path, file_name), 'r', encoding='utf-8') as f:
                contents = f.read()
                named_contents = f'<b>{file_name}</b>\n\n{contents[-4000:]}'
                await update.message.reply_text(text=named_contents, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text=f'Directory "{dir_name}" doesn\'t exist yet.')
