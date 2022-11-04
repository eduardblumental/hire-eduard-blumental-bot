from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import MAIN_MENU

social_media_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Linkedin 🤵🏻‍♂️', url='https://www.linkedin.com/in/eduard-blumental-2b8898133/'),
            InlineKeyboardButton('Github 👨🏻‍💻', url='https://github.com/eduardblumental')
        ],
        [
            InlineKeyboardButton('Back to menu 👀', callback_data=MAIN_MENU)
        ]
    ]
)
