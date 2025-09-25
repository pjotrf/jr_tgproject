from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from services.chatgpt import ask_gpt

router = Router()

def fact_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Ещё факт", callback_data="fact_random"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ]
    ])

@router.callback_query(F.data == "fact_random")
async def fact_random(call: CallbackQuery):
    text = await ask_gpt("Расскажи один краткий редкий научный факт простыми словами.")
    if call.message:
        await call.message.edit_text(f"✨ {text}", reply_markup=fact_kb())
