from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def quiz_topics_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📚 История", callback_data="quiz_topic_История"),
            InlineKeyboardButton(text="🔬 Наука", callback_data="quiz_topic_Наука"),
        ],
        [
            InlineKeyboardButton(text="🏟 Спорт", callback_data="quiz_topic_Спорт"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])

def quiz_answers_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data="quiz_ans_A"),
            InlineKeyboardButton(text="B", callback_data="quiz_ans_B"),
        ],
        [
            InlineKeyboardButton(text="C", callback_data="quiz_ans_C"),
            InlineKeyboardButton(text="D", callback_data="quiz_ans_D"),
        ],
    ])
