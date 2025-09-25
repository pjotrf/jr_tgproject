from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.chatgpt import ask_gpt
from keyboards.inline.talk import talk_menu_kb, talk_chat_kb

router = Router()

class PersonaState(StatesGroup):
    chatting = State()

PERSONAS = {
    "einstein": "Представь, что ты Альберт Эйнштейн. Отвечай как он.",
    "pushkin": "Ты Александр Пушкин. Отвечай поэтично и изящно.",
    "jobs": "Ты Стив Джобс. Отвечай резко, ёмко и вдохновляюще.",
}

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
            await call.message.edit_text("⚠ Неизвестная персона. Выбери снова:", reply_markup=talk_menu_kb())
        return
    await state.update_data(persona=persona)
    await state.set_state(PersonaState.chatting)
    if call.message:
        await call.message.edit_text(
            "✅ Персона выбрана. Пиши сообщение — я отвечу в её стиле.",
            reply_markup=talk_chat_kb()
        )

@router.message(PersonaState.chatting)
async def talk_chat(msg: Message, state: FSMContext):
    data = await state.get_data()
    persona = data.get("persona", "")
    prompt = f"{persona}\n\nПользователь: {msg.text}"
    ans = await ask_gpt(prompt, temperature=1.0)
    await msg.answer(f"👤 {ans}", reply_markup=talk_chat_kb())
