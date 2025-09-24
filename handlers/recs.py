from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.chatgpt import ask_gpt

router = Router()

class RecsState(StatesGroup):
    waiting_genre = State()

CATEGORIES = ["фильмы", "книги", "музыка"]

@router.callback_query(F.data == "recs")
async def recs_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🎬 {cat.capitalize()}", callback_data=f"recs_{cat}") for cat in CATEGORIES]
    ])
    await callback.message.answer("🎯 Выберите категорию рекомендаций:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("recs_"))
async def recs_genre(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_", 1)[1]
    await state.update_data(category=category, dislikes=[])
    await state.set_state(RecsState.waiting_genre)
    await callback.message.answer(f"📖 Введите жанр для {category}.")
    await callback.answer()

@router.message(RecsState.waiting_genre)
async def recs_recommend(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    dislikes = data.get("dislikes", [])
    genre = message.text

    prompt = f"Посоветуй {category} в жанре {genre}. Не предлагай: {', '.join(dislikes)}"
    result = await ask_gpt(prompt)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👎 Не нравится", callback_data="recs_dislike")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])
    await state.update_data(last_result=result)
    await message.answer(f"🎯 Попробуй это:\n{result}", reply_markup=keyboard)

@router.callback_query(F.data == "recs_dislike")
async def recs_dislike(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_result = data.get("last_result", "")
    dislikes = data.get("dislikes", [])
    dislikes.append(last_result)
    await state.update_data(dislikes=dislikes)

    category = data["category"]
    prompt = f"Посоветуй другие {category}, не предлагай: {', '.join(dislikes)}"
    result = await ask_gpt(prompt)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👎 Не нравится", callback_data="recs_dislike")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])
    await state.update_data(last_result=result)
    await callback.message.answer(f"🎯 Попробуй это:\n{result}", reply_markup=keyboard)
    await callback.answer()
