import os
import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers import handle_start, handle_main_menu_error, main_conversation_handler
from utils import configure_logging

from admin.handlers import admin_handlers

configure_logging(logger_name='main_logger', log_dir='logs', log_name='HEBB.log', log_level=logging.DEBUG)


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()
    app.add_handlers(admin_handlers)
    app.add_handler(CommandHandler(callback=handle_start, command='start'))
    app.add_handler(main_conversation_handler)
    app.add_handler(MessageHandler(callback=handle_main_menu_error, filters=filters.ALL))
    app.run_polling()
