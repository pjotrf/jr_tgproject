from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.chatgpt import ask_gpt

router = Router()

class PersonaState(StatesGroup):
    chatting = State()

PERSONAS = {
    "einstein": "Представь, что ты Альберт Эйнштейн. Отвечай как он.",
    "pushkin": "Ты Александр Пушкин. Отвечай поэтично и изящно.",
    "jobs": "Ты Стив Джобс. Отвечай резко, ёмко и вдохновляюще.",
}

def talk_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑‍🔬 Эйнштейн", callback_data="talk_set_einstein"),
            InlineKeyboardButton(text="✒ Пушкин", callback_data="talk_set_pushkin"),
        ],
        [
            InlineKeyboardButton(text="🍏 Стив Джобс", callback_data="talk_set_jobs"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])

def talk_in_chat_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])

@router.callback_query(F.data == "talk_open")
async def talk_open(call: CallbackQuery):
    if call.message:
        await call.message.edit_text("👤 Выбери личность:", reply_markup=talk_menu_kb())

@router.callback_query(F.data.startswith("talk_set_"))
async def talk_set(call: CallbackQuery, state: FSMContext):
    key = call.data.split("_", 2)[-1]
    persona = PERSONAS.get(key)
    if not persona:
        if call.message:
            await call.message.edit_text("⚠ Неизвестная персона. Выбери из списка.", reply_markup=talk_menu_kb())
        return
    await state.update_data(persona=persona)
    await state.set_state(PersonaState.chatting)
    if call.message:
        await call.message.edit_text(f"✅ Персона выбрана. Напиши сообщение — отвечу в стиле персонажа.", reply_markup=talk_in_chat_kb())

@router.message(PersonaState.chatting)
async def talk_chat(msg: Message, state: FSMContext):
    data = await state.get_data()
    persona = data.get("persona", "")
    prompt = f"{persona}\n\nПользователь: {msg.text}"
    ans = await ask_gpt(prompt)
    await msg.answer(f"👤 {ans}", reply_markup=talk_in_chat_kb())
