from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import ABOUT, CV, SOCIAL, CONTACT_ME

main_menu_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('About 🔮', callback_data=ABOUT),
            InlineKeyboardButton('Resume 📋', callback_data=CV)
        ],
[
            InlineKeyboardButton('Social 🌐', callback_data=SOCIAL),
            InlineKeyboardButton('Contacts 👋🏻', callback_data=CONTACT_ME)
        ],
    ]
)
