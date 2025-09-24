from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.chatgpt import ask_gpt

router = Router()

class GptState(StatesGroup):
    waiting = State()

def gpt_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])

@router.message(Command("gpt"))
async def gpt_command(message: types.Message, state: FSMContext):
    await state.set_state(GptState.waiting)
    await message.answer("✍ Напиши свой вопрос для GPT:", reply_markup=gpt_kb())

@router.callback_query(F.data == "gpt")
async def gpt_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(GptState.waiting)
    await callback.message.answer("✍ Напиши свой вопрос для GPT:", reply_markup=gpt_kb())
    await callback.answer()

@router.message(GptState.waiting)
async def gpt_chat(message: types.Message, state: FSMContext):
    user_text = message.text.strip()
    if not user_text:
        await message.answer("Пусто 🤔 Напиши текстовый вопрос.", reply_markup=gpt_kb())
        return

    answer = await ask_gpt(user_text)
    await message.answer(f"💡 Ответ GPT:\n{answer}", reply_markup=gpt_kb())
