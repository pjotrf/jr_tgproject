from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.chatgpt import ask_gpt
from keyboards.inline.recs import recs_category_kb, recs_result_kb

router = Router()

class RecsState(StatesGroup):
    waiting_genre = State()
    recommending = State()

@router.callback_query(F.data == "recs_open")
async def recs_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text("🎬 Выбери категорию:", reply_markup=recs_category_kb())

@router.callback_query(F.data.startswith("recs_cat_"))
async def recs_cat(call: CallbackQuery, state: FSMContext):
    cat = call.data.split("_", 2)[-1]
    await state.update_data(cat=cat)
    await state.set_state(RecsState.waiting_genre)
    if call.message:
        await call.message.edit_text(f"✍ Напиши жанр для категории {cat}")

@router.message(RecsState.waiting_genre)
async def recs_genre(msg: Message, state: FSMContext):
    data = await state.get_data()
    cat = data.get("cat", "фильмы")
    await state.set_state(RecsState.recommending)
    recs = await ask_gpt(f"Дай рекомендации ({cat}) в жанре '{msg.text}'")
    await msg.answer(f"🎯 Рекомендации:\n{recs}", reply_markup=recs_result_kb())

@router.callback_query(F.data.in_(["recs_dislike", "recs_more"]))
async def recs_more_btn(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat = data.get("cat", "фильмы")
    if call.message:
        recs = await ask_gpt(f"Дай ещё рекомендации ({cat}), учитывая, что предыдущие не понравились")
        await call.message.edit_text(f"🎯 Новые рекомендации:\n{recs}", reply_markup=recs_result_kb())
