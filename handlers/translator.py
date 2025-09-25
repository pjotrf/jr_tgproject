from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.chatgpt import ask_gpt

router = Router()

class TrState(StatesGroup):
    translating = State()

LANGS = {
    "en": "английский",
    "de": "немецкий",
    "fr": "французский",
    "es": "испанский",
}

def tr_menu_kb() -> InlineKeyboardMarkup:
    row1 = [
        InlineKeyboardButton(text="🇬🇧 EN", callback_data="tr_set_en"),
        InlineKeyboardButton(text="🇩🇪 DE", callback_data="tr_set_de"),
    ]
    row2 = [
        InlineKeyboardButton(text="🇫🇷 FR", callback_data="tr_set_fr"),
        InlineKeyboardButton(text="🇪🇸 ES", callback_data="tr_set_es"),
    ]
    row3 = [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])

def tr_in_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="tr_open")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")],
    ])

@router.callback_query(F.data == "tr_open")
async def tr_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text("🌐 Выбери язык перевода:", reply_markup=tr_menu_kb())

@router.callback_query(F.data.startswith("tr_set_"))
async def tr_set_lang(call: CallbackQuery, state: FSMContext):
    code = call.data.split("_", 2)[-1]
    lang = LANGS.get(code, "английский")
    await state.update_data(lang=lang)
    await state.set_state(TrState.translating)
    if call.message:
        await call.message.edit_text(f"✅ Язык: {lang}\n✍ Отправь текст для перевода.", reply_markup=tr_in_kb())

@router.message(TrState.translating)
async def tr_translate(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "английский")
    src = (msg.text or "").strip()
    if not src:
        await msg.answer("Пусто 🤔 Введи текст для перевода.", reply_markup=tr_in_kb())
        return
    ans = await ask_gpt(f"Переведи на {lang}: {src}")
    await msg.answer(f"🔤 {ans}", reply_markup=tr_in_kb())
