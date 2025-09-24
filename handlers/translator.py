from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.chatgpt import ask_gpt

router = Router()

class TranslatorState(StatesGroup):
    translating = State()

LANGUAGES = {
    "en": "английский",
    "de": "немецкий",
    "fr": "французский",
    "es": "испанский"
}

@router.callback_query(F.data == "translator")
async def translator_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"lang_{code}") for code, name in LANGUAGES.items()]
    ])
    await callback.message.answer("🌐 Выберите язык перевода:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    code = callback.data.split("_", 1)[1]
    lang = LANGUAGES.get(code, "английский")
    await state.update_data(lang=lang)
    await state.set_state(TranslatorState.translating)
    await callback.message.answer(f"✅ Язык перевода: {lang}. Введите текст для перевода.")
    await callback.answer()

@router.message(TranslatorState.translating)
async def translate_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    text = message.text
    prompt = f"Переведи на {lang}: {text}"
    result = await ask_gpt(prompt)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="translator")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])
    await message.answer(f"🔤 Перевод:\n{result}", reply_markup=keyboard)
