from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def inline_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎲 Факт", callback_data="fact_random"),
            InlineKeyboardButton(text="💬 GPT", callback_data="gpt_open"),
        ],
        [
            InlineKeyboardButton(text="🧑‍🎓 Личность", callback_data="talk_open"),
            InlineKeyboardButton(text="📝 Квиз", callback_data="quiz_open"),
        ],
        [
            InlineKeyboardButton(text="🌐 Переводчик", callback_data="tr_open"),
            InlineKeyboardButton(text="🎬 Рекомендации", callback_data="recs_open"),
        ],
    ])
