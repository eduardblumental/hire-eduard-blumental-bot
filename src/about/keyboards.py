from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.states import MAIN_MENU, ABOUT

from .states import ABOUT_ME, ABOUT_BOT

about_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('About me 🏂', callback_data=ABOUT_ME),
            InlineKeyboardButton('About bot 🤖', callback_data=ABOUT_BOT),
        ],
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=MAIN_MENU)
        ]
    ]
)

watching_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=ABOUT)
        ]
    ]
)
