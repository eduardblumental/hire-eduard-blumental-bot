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

from src.keyboards import main_menu_keyboard
from src.states import CONTACT_ME, MAIN_MENU

from .keyboards import form_keyboard, reach_out_keyboard, submit_keyboard
from .states import REACH_OUT, COMPANY_NAME, POSITION_NAME, POSITION_DESCRIPTION, SALARY_RANGE, CONTACT_PERSON, SUBMIT


async def q_handle_start_contact_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_kwargs = {
        'text': 'My contacts',
        'reply_markup': reach_out_keyboard
    }

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(**message_kwargs)
        return CONTACT_ME
    else:
        await update.effective_message.reply_text(**message_kwargs)


async def q_handle_reach_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def q_handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await q_handle_start_contact_me(update, context)

    return ConversationHandler.END


async def q_handle_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user
    msg = f"New vacancy from @{sender.username} a.k.a. {sender.first_name} " \
          f"{sender.last_name}\n\n{context.user_data.get('form')}"

    await context.bot.send_message(
        chat_id=os.environ.get('TELEGRAM_USER_ID'),
        text=msg,
        parse_mode=ParseMode.HTML
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Thank you for reaching out. I will get back to you at my earliest convenience.'
    )

    await q_handle_back_to_menu(update, context)


async def q_handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Main menu',
        reply_markup=main_menu_keyboard
    )

    return ConversationHandler.END


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        text=f'I am not sure what {update.message.text} means. Please, use the buttons 💁🏻‍♀️'
    )

    await q_handle_start_contact_me(update, context)


contact_me_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_reach_out, pattern=f'^{REACH_OUT}$')
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
        CallbackQueryHandler(callback=q_handle_cancel, pattern=f'^{CONTACT_ME}$'),
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)

contact_me_handlers = [
    contact_me_conversation_handler,
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    CallbackQueryHandler(callback=q_handle_submit, pattern=f'^{SUBMIT}$'),
    CallbackQueryHandler(callback=q_handle_start_contact_me, pattern=f'^{CONTACT_ME}$'),
    MessageHandler(callback=handle_error, filters=filters.ALL)
]
