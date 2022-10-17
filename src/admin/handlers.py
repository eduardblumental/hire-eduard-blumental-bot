import os

from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from telegram.constants import ParseMode

from src.handlers import handle_main_menu_error, handle_error

from .states import LOAD_FILE, LOAD_VIDEO
from .utils import send_files_to_admin_from_dir


async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.environ.get('TELEGRAM_USER_ID') != str(update.effective_user.id):
        await handle_main_menu_error(update, context)
        return

    available_commands = "<b>Available commands</b>\n" \
                         "List all commands: /admin\n" \
                         "Start bot: /start\n" \
                         "Upload file: /load_file\n" \
                         "Upload video: /load_video\n" \
                         "View positions: /msgs\n" \
                         "View logs: /logs"

    await update.message.reply_text(text=available_commands, parse_mode=ParseMode.HTML)


async def handle_load_file_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.environ.get('TELEGRAM_USER_ID') != str(update.effective_user.id):
        await handle_main_menu_error(update, context)
        return

    await update.message.reply_text('Please, upload file. Use caption to rename the file on the fly.')
    return LOAD_FILE


async def handle_load_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.environ.get('TELEGRAM_USER_ID') != str(update.effective_user.id):
        await handle_main_menu_error(update, context)
        return

    await update.message.reply_text('Please, upload video. Use caption to rename the video on the fly.')
    return LOAD_VIDEO


async def handle_load_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_name = update.message.caption if update.message.caption else update.message.document.file_name
    context.bot_data[file_name] = update.message.document.file_id

    await update.message.reply_text(f'File {file_name} has been successfully loaded.')
    await handle_admin(update, context)

    return ConversationHandler.END


async def handle_load_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_name = update.message.caption if update.message.caption else update.message.video.file_name
    context.bot_data[file_name] = update.message.video.file_id

    await update.message.reply_text(f'Video {file_name} has been successfully loaded.')
    await handle_admin(update, context)

    return ConversationHandler.END


async def handle_view_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.environ.get('TELEGRAM_USER_ID') != str(update.effective_user.id):
        await handle_main_menu_error(update, context)
        return

    await send_files_to_admin_from_dir(update=update, context=context, dir_name='msgs')
    await handle_admin(update, context)


async def handle_view_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.environ.get('TELEGRAM_USER_ID') != str(update.effective_user.id):
        await handle_main_menu_error(update, context)
        return

    await send_files_to_admin_from_dir(update=update, context=context, dir_name='logs')
    await handle_admin(update, context)


async def handle_admin_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_admin)
    return ConversationHandler.END


load_data_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(callback=handle_load_file_command, command='load_file'),
        CommandHandler(callback=handle_load_video_command, command='load_video'),
    ],
    states={
        LOAD_FILE: [MessageHandler(callback=handle_load_file, filters=filters.Document.ALL)],
        LOAD_VIDEO: [MessageHandler(callback=handle_load_video, filters=filters.VIDEO)]
    },
    fallbacks=[
        MessageHandler(callback=handle_admin_error, filters=filters.ALL)
    ]
)


admin_handlers = [
    CommandHandler(callback=handle_admin, command='admin'),
    load_data_conversation,
    CommandHandler(callback=handle_view_msgs, command='msgs'),
    CommandHandler(callback=handle_view_logs, command='logs')
]
