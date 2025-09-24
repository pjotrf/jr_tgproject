from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.chatgpt import ask_gpt

router = Router()

class QuizState(StatesGroup):
    waiting_choice = State()

QUIZ_TOPICS = ["История", "Наука", "Спорт"]

def quiz_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📚 {topic}", callback_data=f"quiz_{topic}") for topic in QUIZ_TOPICS],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])

def in_topic_kb(topic: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Ещё вопрос", callback_data=f"quiz_{topic}")],
        [InlineKeyboardButton(text="📚 Сменить тему", callback_data="quiz")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")]
    ])

async def _generate_mc_question(topic: str, asked_norm: set[str], retries: int = 4) -> dict | None:

    exclude_block = ""
    if asked_norm:
        exclude_block = "Не повторяй вопросы из этого списка:\n" + "\n".join(list(asked_norm)[-20:])

    for _ in range(retries):
        prompt = (
            f"Составь 1 НОВЫЙ вопрос по теме «{topic}» с 4 вариантами (A-D).\n"
            f"- Варианты краткие, одно предложение.\n"
            f"- Помимо вариантов, укажи правильный.\n"
            f"- Строгий формат (без лишнего текста):\n"
            f"Вопрос: ...\nA: ...\nB: ...\nC: ...\nD: ...\nПравильный ответ: X\n\n"
            f"{exclude_block}"
        )
        raw = await ask_gpt(prompt)
        if not raw:
            continue

        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        q, opts, ans = None, {}, None
        for line in lines:
            low = line.lower()
            if low.startswith("вопрос"):
                q = line.split(":", 1)[-1].strip()
            elif line.startswith("A:"):
                opts["A"] = line[2:].strip(" :")
            elif line.startswith("B:"):
                opts["B"] = line[2:].strip(" :")
            elif line.startswith("C:"):
                opts["C"] = line[2:].strip(" :")
            elif line.startswith("D:"):
                opts["D"] = line[2:].strip(" :")
            elif low.startswith("правильный"):
                ans = line.split(":", 1)[-1].strip().upper()

        if q and len(opts) == 4 and ans in ("A", "B", "C", "D"):
            if q.lower() not in asked_norm:
                return {"question": q, "options": opts, "answer": ans}

    return None

@router.callback_query(F.data == "quiz")
async def quiz_menu(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total", 0)
    await state.clear()
    if score or total:
        await state.update_data(score=score, total=total)
    await callback.message.answer("📝 Выберите тему квиза:", reply_markup=quiz_menu_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("quiz_"))
async def quiz_question(callback: types.CallbackQuery, state: FSMContext):
    topic = callback.data.split("_", 1)[1]

    data = await state.get_data()
    asked_by_topic: dict[str, list[str]] = data.get("asked_by_topic", {})
    asked_list = asked_by_topic.get(topic, [])
    asked_norm = {q.lower() for q in asked_list}

    qdata = await _generate_mc_question(topic, asked_norm, retries=4)

    if not qdata:
        await callback.message.answer(
            "🤔 Не удалось сгенерировать новый вопрос. Попробуйте ещё раз или смените тему.",
            reply_markup=in_topic_kb(topic),
        )
        await callback.answer()
        return

    asked_list.append(qdata["question"])
    asked_by_topic[topic] = asked_list
    await state.update_data(topic=topic, current_qdata=qdata, asked_by_topic=asked_by_topic)
    await state.set_state(QuizState.waiting_choice)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"A: {qdata['options']['A']}", callback_data="ans_A")],
        [InlineKeyboardButton(text=f"B: {qdata['options']['B']}", callback_data="ans_B")],
        [InlineKeyboardButton(text=f"C: {qdata['options']['C']}", callback_data="ans_C")],
        [InlineKeyboardButton(text=f"D: {qdata['options']['D']}", callback_data="ans_D")],
    ])

    await callback.message.answer(f"❓ {qdata['question']}", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("ans_"))
async def quiz_check_choice(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    qdata = data.get("current_qdata")
    topic = data.get("topic")

    score = int(data.get("score", 0))
    total = int(data.get("total", 0))

    if not qdata:
        await state.clear()
        await callback.message.answer("⚠ Ошибка состояния. Начните квиз заново:", reply_markup=quiz_menu_kb())
        await callback.answer()
        return

    chosen = callback.data.split("_", 1)[1]  # A/B/C/D
    correct = qdata["answer"]

    total += 1
    if chosen == correct:
        score += 1
        verdict = f"✅ Верно! Правильный ответ: {correct}: {qdata['options'][correct]}"
    else:
        verdict = f"❌ Неверно. Правильный ответ: {correct}: {qdata['options'][correct]}"

    # сохраняем обновлённый счёт
    await state.update_data(score=score, total=total)

    await callback.message.answer(
        f"{verdict}\n\n📊 Счёт: {score}/{total}",
        reply_markup=in_topic_kb(topic)
    )
    await callback.answer()
