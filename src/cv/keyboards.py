from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.states import MAIN_MENU, CV

from .states import EXPERIENCE, EDUCATION, TECH_STACK, LANGUAGES

cv_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Experience 💼', callback_data=EXPERIENCE),
            InlineKeyboardButton('Education 🎓', callback_data=EDUCATION),
        ],
        [
            InlineKeyboardButton('Tech stack 🛠', callback_data=TECH_STACK),
            InlineKeyboardButton('Languages 🗣', callback_data=LANGUAGES),
        ],
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=MAIN_MENU)
        ]
    ]
)

reading_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=CV)
        ]
    ]
)
