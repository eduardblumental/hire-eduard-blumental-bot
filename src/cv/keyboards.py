from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import MAIN_MENU, CV

from .states import EXPERIENCE, EDUCATION, TECH_STACK, SOFT_SKILLS

cv_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Experience ðž', callback_data=EXPERIENCE),
            InlineKeyboardButton('Education ð', callback_data=EDUCATION),
        ],
        [
            InlineKeyboardButton('Tech Stack ð ', callback_data=TECH_STACK),
            InlineKeyboardButton('Soft Skills ðŠķ', callback_data=SOFT_SKILLS),
        ],
        [
            InlineKeyboardButton('Back to menu ð', callback_data=MAIN_MENU)
        ]
    ]
)

reading_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Back to menu ð', callback_data=CV)
        ]
    ]
)
