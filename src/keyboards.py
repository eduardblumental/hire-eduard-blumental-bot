from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import INTRO, CV, SOCIAL, CONTACT_ME

main_menu_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Intro 👋🏻', callback_data=INTRO),
            InlineKeyboardButton('CV 📋', callback_data=CV)
        ],
[
            InlineKeyboardButton('Social 🌐', callback_data=SOCIAL),
            InlineKeyboardButton('Contact me ✉️', callback_data=CONTACT_ME)
        ],
    ]
)
