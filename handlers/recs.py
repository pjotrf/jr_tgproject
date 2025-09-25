from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.chatgpt import ask_gpt

router = Router()

class RecsState(StatesGroup):
    waiting_genre = State()

CATS = ["фильмы", "книги", "музыка"]

def recs_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎬 Фильмы", callback_data="recs_cat_фильмы"),
            InlineKeyboardButton(text="📚 Книги", callback_data="recs_cat_книги"),
        ],
        [
            InlineKeyboardButton(text="🎧 Музыка", callback_data="recs_cat_музыка"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ],
    ])

def recs_in_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👎 Не нравится", callback_data="recs_dislike")],
        [InlineKeyboardButton(text="🔁 Другое", callback_data="recs_more")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")],
    ])

@router.callback_query(F.data == "recs_open")
async def recs_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text("🎯 Выбери категорию:", reply_markup=recs_menu_kb())

@router.callback_query(F.data.startswith("recs_cat_"))
async def recs_set_cat(call: CallbackQuery, state: FSMContext):
    cat = call.data.split("_", 2)[-1]
    await state.update_data(cat=cat, dislikes=[], last_result="")
    await state.set_state(RecsState.waiting_genre)
    if call.message:
        await call.message.edit_text(f"📖 Введи жанр для категории: {cat}", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🏠 В меню", callback_data="start")]]
        ))

@router.message(RecsState.waiting_genre)
async def recs_genre(msg: Message, state: FSMContext):
    data = await state.get_data()
    cat = data.get("cat", "")
    dislikes = data.get("dislikes", [])
    genre = (msg.text or "").strip()

    prompt = f"Посоветуй {cat} в жанре {genre}. Не предлагай: {', '.join(dislikes)}. Формат: список до 5 пунктов."
    res = await ask_gpt(prompt)

    await state.update_data(last_result=res)
    await msg.answer(f"🎯 Попробуй это:\n{res}", reply_markup=recs_in_kb())

@router.callback_query(F.data == "recs_dislike")
async def recs_dislike(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last = data.get("last_result", "")
    dislikes = data.get("dislikes", [])
    dislikes.append(last)
    await state.update_data(dislikes=dislikes)
    if call.message:
        await call.message.edit_text("🗒 Добавил в «не нравится». Нажми «🔁 Другое» для новых рекомендаций.", reply_markup=recs_in_kb())

@router.callback_query(F.data == "recs_more")
async def recs_more(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat = data.get("cat", "")
    dislikes = data.get("dislikes", [])

    prompt = f"Посоветуй другие {cat}, не предлагай: {', '.join(dislikes)}. Формат: список до 5 пунктов."
    res = await ask_gpt(prompt)
    await state.update_data(last_result=res)

    if call.message:
        await call.message.edit_text(f"🎯 Новые варианты:\n{res}", reply_markup=recs_in_kb())
