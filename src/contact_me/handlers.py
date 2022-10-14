import os

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from src.states import CONTACT_ME, MAIN_MENU
from src.utils import go_to_menu, start_module, handle_error

from .keyboards import form_keyboard, reach_out_keyboard, submit_keyboard
from .states import REACH_OUT, COMPANY_NAME, POSITION_NAME, POSITION_DESCRIPTION, SALARY_RANGE, CONTACT_PERSON, SUBMIT


async def handle_start_contact_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_module(
        update=update, context=context,
        text='Contact me', reply_markup=reach_out_keyboard
    )
    return CONTACT_ME


async def handle_reach_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Please, type in your company name.',
        reply_markup=form_keyboard
    )

    return COMPANY_NAME


async def handle_company_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['company_name'] = update.message.text
    await update.message.reply_text(
        text='Please, type in position name.',
        reply_markup=form_keyboard
    )

    return POSITION_NAME


async def handle_position_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['position_name'] = update.message.text
    await update.message.reply_text(
        text='Please, type in position description & requirements.',
        reply_markup=form_keyboard
    )

    return POSITION_DESCRIPTION


async def handle_position_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['position_description'] = update.message.text
    await update.message.reply_text(
        text='What is the monthly salary range for the above mentioned position? Format: "min-max NIS/USD/EUR"',
        reply_markup=form_keyboard
    )

    return SALARY_RANGE


async def handle_salary_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['salary_range'] = update.message.text
    await update.message.reply_text(
        text='What is the name of the contact person for the above mentioned position? Format: "Name Surname, Position"',
        reply_markup=form_keyboard
    )

    return CONTACT_PERSON


async def handle_contact_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact_person'] = update.message.text
    context.user_data['form'] = f"<b>Company name</b>\n{context.user_data.get('company_name')}\n\n" \
                                f"<b>Position name</b>\n{context.user_data.get('position_name')}\n\n" \
                                f"<b>Position description</b>\n{context.user_data.get('position_description')}\n\n" \
                                f"<b>Salary range</b>\n{context.user_data.get('salary_range')}\n\n" \
                                f"<b>Contact person</b>\n{context.user_data.get('contact_person')}"

    await update.message.reply_text(
        text=f"{context.user_data.get('form')}\n\nIs everything correct?",
        parse_mode=ParseMode.HTML,
        reply_markup=submit_keyboard
    )

    return ConversationHandler.END


async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await handle_start_contact_me(update, context)

    return ConversationHandler.END


async def handle_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user
    msg = f"New vacancy from @{sender.username} a.k.a. {sender.first_name} " \
          f"{sender.last_name}\n\n{context.user_data.get('form')}"

    await context.bot.send_message(
        chat_id=os.environ.get('TELEGRAM_USER_ID'),
        text=msg,
        parse_mode=ParseMode.HTML
    )

    await update.callback_query.edit_message_text(
        text='Thank you for reaching out. I will get back to you at my earliest convenience.'
    )

    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await go_to_menu(update, context)
    return ConversationHandler.END


async def handle_contact_me_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_error(update=update, context=context, callback=handle_start_contact_me,
                       error_message='Error')


contact_me_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=handle_reach_out, pattern=f'^{REACH_OUT}$')
    ],
    states={
        COMPANY_NAME: [
            MessageHandler(callback=handle_company_name, filters=filters.TEXT and ~filters.COMMAND),
        ],
        POSITION_NAME: [
            MessageHandler(callback=handle_position_name, filters=filters.TEXT and ~filters.COMMAND)
        ],
        POSITION_DESCRIPTION: [
            MessageHandler(callback=handle_position_description, filters=filters.TEXT and ~filters.COMMAND)
        ],
        SALARY_RANGE: [
            MessageHandler(callback=handle_salary_range,
                           filters=filters.Regex(r'\d+-\d+ [NIS|USD|EUR]') and ~filters.COMMAND)
        ],
        CONTACT_PERSON: [
            MessageHandler(callback=handle_contact_person, filters=filters.TEXT and ~filters.COMMAND)
        ]
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