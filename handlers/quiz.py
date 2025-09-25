from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.chatgpt import ask_gpt
from keyboards.inline.quiz import quiz_topics_kb, quiz_answers_kb

router = Router()

class QuizState(StatesGroup):
    answering = State()

@router.callback_query(F.data == "quiz_open")
async def quiz_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text("📚 Выбери тему квиза:", reply_markup=quiz_topics_kb())

@router.callback_query(F.data.startswith("quiz_topic_"))
async def quiz_topic(call: CallbackQuery, state: FSMContext):
    topic = call.data.split("_", 2)[-1]
    await state.update_data(topic=topic)
    await state.set_state(QuizState.answering)
    question = await ask_gpt(f"Задай вопрос по теме {topic} с 4 вариантами ответов (A,B,C,D).")
    if call.message:
        await call.message.edit_text(f"❓ {question}", reply_markup=quiz_answers_kb())

@router.callback_query(F.data.startswith("quiz_ans_"))
async def quiz_answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic", "")
    user_ans = call.data.split("_", 2)[-1]
    result = await ask_gpt(f"Тема: {topic}. Пользователь ответил {user_ans}. Верно ли? Ответь кратко.")
    if call.message:
        await call.message.edit_text(f"✅ Результат: {result}\n\nВыбери новый вопрос или тему:", reply_markup=quiz_topics_kb())
