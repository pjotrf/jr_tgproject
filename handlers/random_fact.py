from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.chatgpt import ask_gpt

router = Router()
FACT_PROMPT = "Расскажи интересный научный факт простыми словами."

@router.callback_query(F.data == "random")
async def random_fact_handler(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Хочу ещё", callback_data="random")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])
    answer = await ask_gpt(FACT_PROMPT)
    await callback.message.answer(f"✨ Интересный факт:\n\n{answer}", reply_markup=keyboard)
    await callback.answer()
