from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import SOCIAL_MEDIA, MY_CV, MY_JOURNEY, CONTACT_ME

welcome_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Social media 👤', callback_data=SOCIAL_MEDIA),
            InlineKeyboardButton('My CV 📋', callback_data=MY_CV)
        ],
[
            InlineKeyboardButton('My journey 🏂', callback_data=MY_JOURNEY),
            InlineKeyboardButton('Contact me ✉️', callback_data=CONTACT_ME)
        ],
    ]
)