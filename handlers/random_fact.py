from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from services.chatgpt import ask_gpt
from keyboards.inline.main_menu import inline_main_menu

router = Router()

FACT_PROMPT = "Расскажи один интересный случайный факт. Кратко, 2–3 предложения."

@router.callback_query(F.data == "fact_random")
async def fact_random(call: CallbackQuery):
    response = await ask_gpt(FACT_PROMPT)
    if call.message:
        await call.message.edit_text(
            f"🎲 Факт:\n{response}",
            reply_markup=inline_main_menu()
        )

@router.message(F.text == "/random")
async def fact_random_cmd(msg: Message):
    response = await ask_gpt(FACT_PROMPT)
    await msg.answer(f"🎲 Факт:\n{response}", reply_markup=inline_main_menu())
