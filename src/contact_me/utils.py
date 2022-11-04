from datetime import datetime
import logging, os

from telegram import Update
from telegram.ext import ContextTypes

from .keyboards import form_keyboard

logger = logging.getLogger('main_logger')


async def process_form_entry(update:Update, context: ContextTypes.DEFAULT_TYPE,
                             entry_name, next_question, log_msg, log_response=True):
    if not context.user_data.get(entry_name):
        context.user_data[entry_name] = update.message.text
    await update.message.reply_text(text=next_question, reply_markup=form_keyboard)

    if log_response:
        log_msg = f'{log_msg} "{context.user_data.get(entry_name)}".'
    logger.info(msg=log_msg, extra={'username': update.effective_user.username})


def create_form_from_user_data(user_data):
    form = f"<b>Company name</b>\n{user_data.get('company_name')}\n\n" \
           f"<b>Position description</b>\n{user_data.get('position_description')}\n\n" \
           f"<b>Salary range</b>\n{user_data.get('salary_range')}\n\n" \
           f"<b>Contact person</b>\n{user_data.get('contact_person_name')}, " \
           f"{user_data.get('contact_person_email')}"

    return form


def create_msg_from_sender_and_form(sender, form):
    msg = f"New vacancy from @{sender.username} a.k.a. {sender.first_name} " \
          f"{sender.last_name}\n\n{form}"

    return msg


def save_msg_to_file(dir_name, user_data, msg):
    dir_path = os.path.join('..', dir_name)
    seconds_since_1970 = str(round((datetime.now() - datetime(1970, 1, 1)).total_seconds(), 3)).zfill(14)
    file_name = f"{seconds_since_1970}_{user_data.get('company_name').replace(' ', '_')}.md"

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    with open(os.path.join(dir_path, file_name), 'w', encoding='utf-8') as f:
        f.write(msg)
