from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def translator_langs_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 Английский", callback_data="tr_set_en"),
            InlineKeyboardButton(text="🇩🇪 Немецкий", callback_data="tr_set_de"),
        ],
        [
            InlineKeyboardButton(text="🇫🇷 Французский", callback_data="tr_set_fr"),
            InlineKeyboardButton(text="🇪🇸 Испанский", callback_data="tr_set_es"),
        ],
        [
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])
