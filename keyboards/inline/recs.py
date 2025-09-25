from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def recs_category_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎬 Фильмы", callback_data="recs_cat_фильмы"),
            InlineKeyboardButton(text="📚 Книги", callback_data="recs_cat_книги"),
        ],
        [
            InlineKeyboardButton(text="🎧 Музыка", callback_data="recs_cat_музыка"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])

def recs_result_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👎 Не нравится", callback_data="recs_dislike"),
            InlineKeyboardButton(text="🔁 Другое", callback_data="recs_more"),
        ],
        [
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])
