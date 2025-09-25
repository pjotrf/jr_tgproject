from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def talk_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑‍🔬 Эйнштейн", callback_data="talk_set_einstein"),
            InlineKeyboardButton(text="✒ Пушкин", callback_data="talk_set_pushkin"),
        ],
        [
            InlineKeyboardButton(text="🍏 Стив Джобс", callback_data="talk_set_jobs"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])

def talk_chat_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏁 Закончить", callback_data="start")]
    ])
