from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.chatgpt import ask_gpt

router = Router()

class PersonaState(StatesGroup):
    chatting = State()

PERSONAS = {
    "einstein": "Представь, что ты Альберт Эйнштейн.",
    "pushkin": "Ты Александр Пушкин, поэт.",
    "jobs": "Ты Стив Джобс, отвечай жёстко и вдохновляюще."
}

def persona_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧑‍🔬 Эйнштейн", callback_data="persona_einstein")],
        [InlineKeyboardButton(text="✒ Пушкин", callback_data="persona_pushkin")],
        [InlineKeyboardButton(text="🍏 Стив Джобс", callback_data="persona_jobs")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")],
    ])

@router.callback_query(F.data == "talk")
async def talk_menu(callback: types.CallbackQuery):
    await callback.message.answer("👤 С кем поболтаем?", reply_markup=persona_menu_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("persona_"))
async def set_persona(callback: types.CallbackQuery, state: FSMContext):
    persona_key = callback.data.split("_", 1)[1]
    system_prompt = PERSONAS.get(persona_key)
    if not system_prompt:
        await callback.message.answer("⚠ Неизвестная персона. Выберите из меню.")
        await callback.answer()
        return

    await state.update_data(persona=system_prompt)
    await state.set_state(PersonaState.chatting)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])
    await callback.message.answer(
        f"✅ Вы выбрали: {persona_key.capitalize()}\n✍ Напишите сообщение — персона ответит в своём стиле.",
        reply_markup=kb
    )
    await callback.answer()

@router.message(PersonaState.chatting)
async def persona_chat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    persona = data.get("persona")
    if not persona:
        await state.clear()
        await message.answer("⚠ Персона не выбрана. Нажмите «🧑‍🎓 Диалог с личностью» и выберите персону.")
        return

    prompt = f"{persona}\n\nПользователь: {message.text}"
    answer = await ask_gpt(prompt)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])
    await message.answer(f"👤 {answer}", reply_markup=kb)
