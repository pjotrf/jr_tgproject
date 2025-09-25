from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.chatgpt import ask_gpt

router = Router()

class QuizState(StatesGroup):
    waiting_choice = State()

TOPICS = ["История", "Наука", "Спорт"]

def quiz_menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text="📚 История", callback_data="quiz_topic_История"),
            InlineKeyboardButton(text="🔬 Наука", callback_data="quiz_topic_Наука"),
        ],
        [
            InlineKeyboardButton(text="🏟 Спорт", callback_data="quiz_topic_Спорт"),
            InlineKeyboardButton(text="🏠 В меню", callback_data="start"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def quiz_in_topic_kb(topic: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Ещё вопрос", callback_data=f"quiz_topic_{topic}")],
        [InlineKeyboardButton(text="📚 Сменить тему", callback_data="quiz_open")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="start")],
    ])

async def _generate_mc(topic: str, asked_norm: set[str], retries: int = 5) -> dict | None:

    exclude = ""
    if asked_norm:
        prev = "\n".join(f"- {x}" for x in list(asked_norm)[-20:])
        exclude = f"\nНе повторяй ни вопрос, ни смысл из списка:\n{prev}\n"

    for _ in range(retries):
        prompt = (
            f"Составь 1 НОВЫЙ вопрос по теме «{topic}» с 4 вариантами (A-D). "
            f"Формат строго:\n"
            f"Вопрос: ...\nA: ...\nB: ...\nC: ...\nD: ...\nПравильный ответ: X\n"
            f"Только этот формат, без лишних комментариев.{exclude}"
        )
        raw = await ask_gpt(prompt)
        if not raw:
            continue

        lines = [l.strip() for l in raw.splitlines() if l.strip()]
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

        if q and len(opts) == 4 and ans in ("A", "B", "C", "D") and q.lower() not in asked_norm:
            return {"question": q, "options": opts, "answer": ans}
    return None

@router.callback_query(F.data == "quiz_open")
async def quiz_open(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total", 0)
    await state.clear()
    if score or total:
        await state.update_data(score=score, total=total)
    if call.message:
        await call.message.edit_text("📝 Выбери тему:", reply_markup=quiz_menu_kb())

@router.callback_query(F.data.startswith("quiz_topic_"))
async def quiz_question(call: CallbackQuery, state: FSMContext):
    topic = call.data.split("quiz_topic_", 1)[1]

    data = await state.get_data()
    asked_by_topic = data.get("asked_by_topic", {})
    asked_list = asked_by_topic.get(topic, [])
    asked_norm = {q.lower() for q in asked_list}

    qdata = await _generate_mc(topic, asked_norm, retries=5)
    if not qdata:
        if call.message:
            await call.message.edit_text("🤔 Не удалось сгенерировать новый вопрос. Нажми «Ещё вопрос» или смени тему.",
                                         reply_markup=quiz_in_topic_kb(topic))
        return

    asked_list.append(qdata["question"])
    asked_by_topic[topic] = asked_list
    await state.update_data(topic=topic, current_q=qdata, asked_by_topic=asked_by_topic)
    await state.set_state(QuizState.waiting_choice)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"A: {qdata['options']['A']}", callback_data="quiz_ans_A"),
            InlineKeyboardButton(text=f"B: {qdata['options']['B']}", callback_data="quiz_ans_B"),
        ],
        [
            InlineKeyboardButton(text=f"C: {qdata['options']['C']}", callback_data="quiz_ans_C"),
            InlineKeyboardButton(text=f"D: {qdata['options']['D']}", callback_data="quiz_ans_D"),
        ],
    ])

    if call.message:
        await call.message.edit_text(f"❓ {qdata['question']}", reply_markup=kb)

@router.callback_query(F.data.startswith("quiz_ans_"))
async def quiz_answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    qdata = data.get("current_q")
    topic = data.get("topic", "")
    score = int(data.get("score", 0))
    total = int(data.get("total", 0))

    if not qdata:
        if call.message:
            await call.message.edit_text("⚠ Ошибка состояния. Открой квиз снова.", reply_markup=quiz_menu_kb())
        await state.clear()
        return

    chosen = call.data.split("_", 2)[-1]  # A/B/C/D
    correct = qdata["answer"]
    total += 1

    if chosen == correct:
        score += 1
        verdict = f"✅ Верно! Правильный ответ: {correct}: {qdata['options'][correct]}"
    else:
        verdict = f"❌ Неверно. Правильный ответ: {correct}: {qdata['options'][correct]}"

    await state.update_data(score=score, total=total)

    if call.message:
        await call.message.edit_text(f"{verdict}\n\n📊 Счёт: {score}/{total}",
                                     reply_markup=quiz_in_topic_kb(topic))
