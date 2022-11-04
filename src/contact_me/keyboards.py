from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import MAIN_MENU, CONTACT_ME

from .states import START_FORM, SUBMIT


reach_out_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Submit vacancy directly 🔥', callback_data=START_FORM)
        ],
        [

            InlineKeyboardButton('Telegram 🚀', url='https://t.me/eduard_b7'),
            InlineKeyboardButton('LinkedIn 👨🏻‍💻', url='https://www.linkedin.com/in/eduard-blumental-2b8898133/')
        ],
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=MAIN_MENU)
        ]
    ]
)


form_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Cancel 🙅🏻‍♀️', callback_data=CONTACT_ME)
        ]
    ]
)


submit_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Submit 🕊', callback_data=SUBMIT),
            InlineKeyboardButton('Retry 🔄', callback_data=START_FORM),

        ],
        [
            InlineKeyboardButton('Cancel  🙅🏻‍♀️', callback_data=CONTACT_ME)
        ]
    ]
)
