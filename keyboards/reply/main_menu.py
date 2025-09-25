from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def reply_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Меню")]],
        resize_keyboard=True
    )
