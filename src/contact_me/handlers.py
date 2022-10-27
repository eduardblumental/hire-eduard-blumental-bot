import logging
import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from src.states import CONTACT_ME, MAIN_MENU
from src.utils import go_to_menu, start_module, handle_error

from .keyboards import form_keyboard, reach_out_keyboard, submit_keyboard
from .states import REACH_OUT, COMPANY_NAME, POSITION_DESCRIPTION, SALARY_RANGE, \
    CONTACT_PERSON_NAME, CONTACT_PERSON_POSITION, CONTACT_PERSON_EMAIL, SUBMIT
from .utils import process_form_entry, create_form_from_user_data, create_msg_from_sender_and_form, save_msg_to_file

logger = logging.getLogger('main_logger')


async def handle_start_contact_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Contact me', reply_markup=reach_out_keyboard,
        log_msg='Entered section "Contact me".'
    )
    return CONTACT_ME


async def handle_reach_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Please, type in your company name.',
        reply_markup=form_keyboard
    )
    logger.info(msg=f'Reached out directly.', extra={'username': update.effective_user.username})
    return COMPANY_NAME


async def handle_company_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_form_entry(
        update=update, context=context, entry_name='company_name',
        next_question='Please, type in position description & requirements.',
        log_msg='Entered company name'
    )
    return POSITION_DESCRIPTION


async def handle_position_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_form_entry(
        update=update, context=context, entry_name='position_description',
        next_question='Please, type in salary range for the given position? min-max NIS/USD',
        log_msg='Entered position description.', log_response=False
    )
    return SALARY_RANGE


async def handle_salary_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_form_entry(
        update=update, context=context, entry_name='salary_range',
        next_question='Please, type in contact person\'s full name.',
        log_msg='Entered salary range'
    )
    return CONTACT_PERSON_NAME


async def handle_contact_person_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_form_entry(
        update=update, context=context, entry_name='contact_person_name',
        next_question='Please, type in contact person\'s position.',
        log_msg='Entered contact person\'s full name'
    )
    return CONTACT_PERSON_POSITION


async def handle_contact_person_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_form_entry(
        update=update, context=context, entry_name='contact_person_position',
        next_question='Please, type in contact person\'s email.',
        log_msg='Entered contact person\'s position'
    )
    return CONTACT_PERSON_EMAIL


async def handle_contact_person_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact_person_email'] = update.message.text
    context.user_data['form'] = create_form_from_user_data(context.user_data)

    await update.message.reply_text(
        text=f"{context.user_data.get('form')}\n\nIs everything correct?",
        parse_mode=ParseMode.HTML,
        reply_markup=submit_keyboard
    )
    logger.info(msg=f'Entered contact person\'s email "{context.user_data.get("contact_person_email")}".',
                extra={'username': update.effective_user.username})
    return ConversationHandler.END


async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    logger.info(msg=f'Canceled reaching out process.', extra={'username': update.effective_user.username})

    await handle_start_contact_me(update, context)
    return ConversationHandler.END


async def handle_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = create_msg_from_sender_and_form(sender=update.effective_user, form=context.user_data.get('form'))
    save_msg_to_file(dir_name='msgs', user_data=context.user_data, msg=msg)
    context.user_data.clear()
    logger.info(msg=f'Submitted form.', extra={'username': update.effective_user.username})

    await context.bot.send_message(
        chat_id=os.environ.get('ADMIN_TELEGRAM_USER_ID'),
        text=msg,
        parse_mode=ParseMode.HTML
    )
    await go_to_menu(
        update=update, context=context,
        text='Thank you for reaching out. I will get back to you at my earliest convenience.'
    )
    return ConversationHandler.END


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_salary_range_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_position_description,
                       error_message='Please, use the following format: min-max NIS/USD')


async def handle_contact_person_email_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_contact_person_position,
                       error_message='Please, enter a valid email. Example: email@email.com')


async def handle_contact_me_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_contact_me)


contact_me_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_reach_out, pattern=f'^{REACH_OUT}$')
    ],
    states={
        COMPANY_NAME: [
            MessageHandler(callback=handle_company_name, filters=filters.TEXT & ~filters.COMMAND)
        ],
        POSITION_DESCRIPTION: [
            MessageHandler(callback=handle_position_description, filters=filters.TEXT & ~filters.COMMAND)
        ],
        SALARY_RANGE: [
            MessageHandler(callback=handle_salary_range, filters=filters.Regex(r"^\d+-\d+ (NIS|USD)$")),
            MessageHandler(callback=handle_salary_range_error, filters=filters.ALL)
        ],
        CONTACT_PERSON_NAME: [
            MessageHandler(callback=handle_contact_person_name, filters=filters.TEXT & ~filters.COMMAND)
        ],
        CONTACT_PERSON_POSITION: [
            MessageHandler(callback=handle_contact_person_position, filters=filters.TEXT & ~filters.COMMAND)
        ],
        CONTACT_PERSON_EMAIL: [
            MessageHandler(callback=handle_contact_person_email,
                           filters=filters.Regex(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]{2,63}\.[a-zA-Z0-9-.]+$")),
            MessageHandler(callback=handle_contact_person_email_error, filters=filters.ALL)
        ],
    },
    fallbacks=[
        CallbackQueryHandler(callback=handle_cancel, pattern=f'^{CONTACT_ME}$'),
        MessageHandler(callback=handle_contact_me_error, filters=filters.ALL)
    ]
)

contact_me_handlers = [
    contact_me_conversation_handler,
    CallbackQueryHandler(callback=handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    CallbackQueryHandler(callback=handle_submit, pattern=f'^{SUBMIT}$'),
    CallbackQueryHandler(callback=handle_start_contact_me, pattern=f'^{CONTACT_ME}$'),
    MessageHandler(callback=handle_contact_me_error, filters=filters.ALL)
]
