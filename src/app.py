import os
import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers import handle_load_data, handle_start, handle_error, main_conversation_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_logger')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()
    app.add_handler(CommandHandler(callback=handle_load_data, command='load_data'))
    app.add_handler(CommandHandler(callback=handle_start, command='start'))
    app.add_handler(main_conversation_handler)
    app.add_handler(MessageHandler(callback=handle_error, filters=filters.ALL))
    app.run_polling()
