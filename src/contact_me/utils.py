from datetime import date
import os


def create_form_from_user_data(user_data):
    form = f"<b>Company name</b>\n{user_data.get('company_name')}\n\n" \
           f"<b>Position name</b>\n{user_data.get('position_name')}\n\n" \
           f"<b>Position description</b>\n{user_data.get('position_description')}\n\n" \
           f"<b>Salary range</b>\n{user_data.get('salary_range')}\n\n" \
           f"<b>Contact person</b>\n{user_data.get('contact_person_name')}, " \
           f"{user_data.get('contact_person_position')}\n{user_data.get('contact_person_email')}"

    return form


def create_msg_from_sender_and_form(sender, form):
    msg = f"New vacancy from @{sender.username} a.k.a. {sender.first_name} " \
          f"{sender.last_name}\n\n{form}"

    return msg


def save_msg_to_file(dir_name, user_data, msg):
    dir_path = os.path.join('..', dir_name)
    file_name = f"{date.today()}_{user_data.get('company_name')}_at_{user_data.get('position_name')}.md"

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    with open(os.path.join(dir_path, file_name), 'w', encoding='utf-8') as f:
        f.write(msg)
