import json, os

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


def backup_data(bot_data, backup_dir_path, backup_file_name):
    if not os.path.exists(backup_dir_path):
        os.mkdir(backup_dir_path)

    backup_file_path = os.path.join(backup_dir_path, backup_file_name)
    with open(backup_file_path, 'w', encoding='utf-8') as f:
        json.dump(bot_data, f)


async def recover_data_from_backup(update: Update, context: ContextTypes.DEFAULT_TYPE, backup_dir_path, backup_file_name):
    backup_file_path = os.path.join(backup_dir_path, backup_file_name)
    if os.path.exists(backup_file_path):
        with open(backup_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key, value in data.items():
                context.bot_data[key] = value
        await update.message.reply_text(f'Data has been successfully recovered.')
    else:
        await update.message.reply_text(f'There is no data to be recovered.')
