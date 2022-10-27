import logging
from logging.handlers import TimedRotatingFileHandler
import os

from telegram import Update
from telegram.ext import ContextTypes

from keyboards import main_menu_keyboard

logger = logging.getLogger('main_logger')


async def start_module(update: Update, context: ContextTypes.DEFAULT_TYPE, text, reply_markup, log_msg):
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

    logger.info(log_msg, extra={'username': update.effective_user.username})


async def go_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     text='Main Menu', log_msg='Went back to menu.'):
    await start_module(update, context, text, main_menu_keyboard, log_msg)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE, callback, error_message=None):
    if not error_message:
        error_message = f'I am not sure what "{update.message.text}" means. Please, use the buttons 💁🏻‍♀️'

    await update.effective_message.reply_text(text=error_message)
    logger.warning(msg=f'USER ERROR: {error_message}',
                   extra={'username': update.effective_user.username})
    logger.warning(msg=f'USER ERROR handled by "{callback.__name__}".',
                   extra={'username': update.effective_user.username})
    await callback(update, context)


def get_log_file_path(log_dir, log_name):
    log_dir_path = os.path.join('..', log_dir)
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    return os.path.join(log_dir_path, log_name)


def configure_logging(logger_name, log_dir, log_name, log_level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    log_file_path = get_log_file_path(log_dir, log_name)
    log_handler = TimedRotatingFileHandler(filename=log_file_path, when="midnight", encoding='utf-8')

    log_handler_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname).3s | %(username)s | %(message)s',
        datefmt="%Y.%m.%d %H:%M:%S"
    )
    log_handler.setFormatter(log_handler_formatter)
    log_handler.suffix = "%Y-%m-%d"

    logger.addHandler(log_handler)
