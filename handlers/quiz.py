import json
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.chatgpt import ask_gpt
from keyboards.inline.quiz import quiz_topics_kb, quiz_answers_kb, quiz_result_kb

router = Router()

class QuizState(StatesGroup):
    waiting_choice = State()

MAX_HISTORY = 5  # сколько последних вопросов помнить


# ---------- генерация вопроса ----------
async def _generate_mc_question(topic: str, avoid: list[str]) -> dict | None:
    """
    Возвращает структуру:
    {
      "question": "Текст вопроса",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "answer": "A" | "B" | "C" | "D"
    }
    """
    avoid_clause = ""
    if avoid:
        joined = "; ".join(avoid[-MAX_HISTORY:])
        avoid_clause = f"Не используй эти вопросы: {joined}."

    prompt = (
        f"Сгенерируй ОДИН новый вопрос-викторину по теме «{topic}» с 4 вариантами ответов (A–D). "
        f"{avoid_clause}\n\n"
        "Верни СТРОГО ТОЛЬКО JSON без лишнего текста:\n"
        "{{\n"
        '  "question": "…",\n'
        '  "options": {{"A": "…", "B": "…", "C": "…", "D": "…"}},\n'
        '  "answer": "A"\n'
        "}}\n"
        "- Вопросы должны быть разнообразными.\n"
        "- Не добавляй пояснений/префиксов до или после JSON."
    )

    raw = await ask_gpt(prompt, temperature=1.2)
    if not raw:
        return None

    try:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1:
            return None
        data = json.loads(raw[start:end + 1])
    except Exception:
        return None

    if (
        isinstance(data, dict)
        and "question" in data
        and "options" in data
        and "answer" in data
        and isinstance(data["options"], dict)
        and all(k in data["options"] for k in ("A", "B", "C", "D"))
        and data["answer"] in ("A", "B", "C", "D")
    ):
        return data

    return None


# ---------- открыть меню тем ----------
@router.callback_query(F.data == "quiz_open")
async def quiz_open(call: CallbackQuery, state: FSMContext):
    if call.message:
        await call.message.edit_text("📝 Выбери тему квиза:", reply_markup=quiz_topics_kb())


# ---------- запросить вопрос по теме ----------
@router.callback_query(F.data.startswith("quiz_topic_"))
async def quiz_question(call: CallbackQuery, state: FSMContext):
    topic = call.data.split("quiz_topic_", 1)[1]

    data = await state.get_data()
    asked = data.get("asked_questions", [])

    qdata = await _generate_mc_question(topic, asked)
    if not qdata:
        if call.message:
            await call.message.edit_text(
                "🤔 Не удалось сгенерировать вопрос. Попробуй ещё раз или смени тему.",
                reply_markup=quiz_topics_kb()
            )
        return

    # сохраняем вопрос в историю
    asked.append(qdata["question"])
    if len(asked) > MAX_HISTORY:
        asked = asked[-MAX_HISTORY:]

    await state.update_data(topic=topic, current_q=qdata, asked_questions=asked)
    await state.set_state(QuizState.waiting_choice)

    if call.message:
        text = (
            f"❓ {qdata['question']}\n\n"
            f"A) {qdata['options']['A']}\n"
            f"B) {qdata['options']['B']}\n"
            f"C) {qdata['options']['C']}\n"
            f"D) {qdata['options']['D']}"
        )
        await call.message.edit_text(text, reply_markup=quiz_answers_kb())


# ---------- пользователь выбрал A/B/C/D ----------
@router.callback_query(F.data.startswith("quiz_ans_"))
async def quiz_check(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    qdata = data.get("current_q")
    topic = data.get("topic", "")

    if not qdata:
        if call.message:
            await call.message.edit_text("⚠️ Сессия квиза потеряна. Выбери тему заново:", reply_markup=quiz_topics_kb())
        await state.clear()
        return

    chosen = call.data.split("quiz_ans_", 1)[1]
    correct = qdata["answer"]

    score = int(data.get("score", 0))
    total = int(data.get("total", 0))
    total += 1

    chosen_text = qdata["options"][chosen]
    correct_text = qdata["options"][correct]

    if chosen == correct:
        score += 1
        verdict = f"✅ Верно!\nПравильный ответ: {correct}) {correct_text}"
    else:
        verdict = (
            f"❌ Неверно.\n"
            f"Ты выбрал {chosen}) {chosen_text}\n"
            f"Правильный ответ: {correct}) {correct_text}"
        )

    await state.update_data(score=score, total=total, current_q=None)

    if call.message:
        msg = (
            f"{verdict}\n\n"
            f"📊 Счёт: {score}/{total}\n\n"
            f"Тема: {topic}"
        )
        await call.message.edit_text(msg, reply_markup=quiz_result_kb(topic))
