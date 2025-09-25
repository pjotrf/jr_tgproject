from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.inline.main_menu import inline_main_menu
from keyboards.reply.main_menu import reply_menu

router = Router()

WELCOME_TEXT = (
    "👋 Привет! Я твой помощник ChatGPT 🤖\n\n"
    "Вот что я умею:\n"
    "• 🎲 Случайный факт — расскажу интересное знание\n"
    "• 💬 GPT — задай любой вопрос ИИ\n"
    "• 🧑‍🎓 Личность — общение в стиле Эйнштейна, Пушкина или Джобса\n"
    "• 📝 Квиз — викторина с вариантами ответов\n"
    "• 🌐 Переводчик — переведу текст на разные языки\n"
    "• 🎬 Рекомендации — подскажу фильмы, книги и музыку\n\n"
    "Выбери режим ниже ⬇️"
)

@router.message(Command("start"))
async def start_cmd(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(WELCOME_TEXT, reply_markup=reply_menu())
    await msg.answer("📌 Главное меню:", reply_markup=inline_main_menu())

@router.callback_query(F.data == "start")
async def start_cb(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text(WELCOME_TEXT, reply_markup=inline_main_menu())

@router.message(F.text == "🏠 Меню")
async def reply_menu_btn(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(WELCOME_TEXT, reply_markup=inline_main_menu())
