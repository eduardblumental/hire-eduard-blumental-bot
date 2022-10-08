from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.states import MAIN_MENU, CONTACT_ME

from .states import REACH_OUT, SUBMIT


reach_out_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Reach out directly 🚀', callback_data=REACH_OUT)
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
            InlineKeyboardButton('Retry 🔄', callback_data=REACH_OUT),

        ],
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=MAIN_MENU)
        ]
    ]
)
