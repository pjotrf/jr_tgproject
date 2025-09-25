from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.chatgpt import ask_gpt
from keyboards.inline.main_menu import inline_main_menu

router = Router()

class GptState(StatesGroup):
    waiting = State()

@router.callback_query(F.data == "gpt_open")
async def gpt_open(call: CallbackQuery, state: FSMContext):
    await state.set_state(GptState.waiting)
    if call.message:
        await call.message.edit_text("✍ Напиши сообщение для GPT:", reply_markup=inline_main_menu())

@router.message(GptState.waiting)
async def gpt_answer(msg: Message, state: FSMContext):
    ans = await ask_gpt(msg.text, temperature=0.7)
    await msg.answer(f"🤖 {ans}", reply_markup=inline_main_menu())
