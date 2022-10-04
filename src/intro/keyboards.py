from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.states import MAIN_MENU, INTRO

from .states import MY_JOURNEY, WHY_HIRE_ME

intro_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('My journey 🏂', callback_data=MY_JOURNEY),
            InlineKeyboardButton('Why hire me 🔮', callback_data=WHY_HIRE_ME),
        ],
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=MAIN_MENU)
        ]
    ]
)

video_menu_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=INTRO)
        ]
    ]
)
