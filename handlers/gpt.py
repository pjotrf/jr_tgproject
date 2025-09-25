from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.chatgpt import ask_gpt

router = Router()

class GptState(StatesGroup):
    waiting = State()

def gpt_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])

@router.callback_query(F.data == "gpt_open")
async def gpt_open(call: CallbackQuery, state: FSMContext):
    await state.set_state(GptState.waiting)
    if call.message:
        await call.message.edit_text("✍ Напиши сообщение для GPT:", reply_markup=gpt_menu_kb())

@router.message(GptState.waiting)
async def gpt_ask(msg: Message, state: FSMContext):
    q = (msg.text or "").strip()
    if not q:
        await msg.answer("Пусто 🤔 Напиши вопрос текстом.", reply_markup=gpt_menu_kb())
        return
    ans = await ask_gpt(q)
    await msg.answer(f"💡 {ans}", reply_markup=gpt_menu_kb())
