from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.chatgpt import ask_gpt
from keyboards.inline.translator import translator_langs_kb

router = Router()

class TranslatorState(StatesGroup):
    waiting_text = State()

@router.callback_query(F.data == "tr_open")
async def tr_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text("🌐 Выбери язык для перевода:", reply_markup=translator_langs_kb())

@router.callback_query(F.data.startswith("tr_set_"))
async def tr_set(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_", 2)[-1]
    await state.update_data(lang=lang)
    await state.set_state(TranslatorState.waiting_text)
    if call.message:
        await call.message.edit_text(f"✍ Напиши текст для перевода на {lang.upper()}")

@router.message(TranslatorState.waiting_text)
async def tr_translate(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    translated = await ask_gpt(f"Переведи на {lang}: {msg.text}")
    await msg.answer(f"🌐 Перевод: {translated}", reply_markup=translator_langs_kb())
