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
from .states import REACH_OUT, COMPANY_NAME, POSITION_NAME, POSITION_DESCRIPTION, SALARY_RANGE, CONTACT_PERSON, FULL_FORM, SUBMIT


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


async def handle_cantact_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact_person'] = update.message.text

    form = f"""<b>Company name<b>\n{context.user_data.get('company_name')}\n
    <b>Position name<b>\n{context.user_data.get('position_name')}\n
    <b>Position description<b>\n{context.user_data.get('position_description')}\n
    <b>Salary range<b>\n{context.user_data.get('salary_range')}\n
    <b>Contact person<b>\n{context.user_data.get('contact_person')}\n
    Is everything correct?
    """

    await update.message.reply_text(
        text=form,
        parse_mode=ParseMode.HTML,
        reply_markup=submit_keyboard
    )

    return ConversationHandler.END


async def q_handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Please, type in your company name.',
        reply_markup=form_keyboard
    )

    return COMPANY_NAME


async def q_handle_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['company_name'] = update.message.text
    await update.message.reply_text(
        text='Thank you for reaching out. I will get back to you at my earliest convenience. Main menu.',
        reply_markup=main_menu_keyboard
    )

    return ConversationHandler.END


async def q_handle_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
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
            MessageHandler(callback=handle_salary_range, filters=filters.Regex(r'\d+-\d+ [NIS|USD|EUR]') and ~filters.COMMAND)
        ],
        CONTACT_PERSON: [
            MessageHandler(callback=handle_salary_range, filters=filters.TEXT and ~filters.COMMAND)
        ]
    },
    fallbacks=[
        MessageHandler(callback=handle_error, filters=filters.ALL)
    ]
)

cv_handlers = [
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{MAIN_MENU}$'),
    contact_me_conversation_handler,
    MessageHandler(callback=handle_error, filters=filters.ALL)
]

