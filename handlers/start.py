from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

router = Router()

def inline_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎲 Факт", callback_data="fact_random"),
            InlineKeyboardButton(text="💬 GPT", callback_data="gpt_open"),
        ],
        [
            InlineKeyboardButton(text="🧑‍🎓 Личность", callback_data="talk_open"),
            InlineKeyboardButton(text="📝 Квиз", callback_data="quiz_open"),
        ],
        [
            InlineKeyboardButton(text="🌐 Переводчик", callback_data="tr_open"),
            InlineKeyboardButton(text="🎬 Рекомендации", callback_data="recs_open"),
        ],
    ])

def reply_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Меню")]],
        resize_keyboard=True
    )

@router.message(Command("start"))
async def start_cmd(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("👋 Привет! Я твой помощник ChatGPT 🤖", reply_markup=reply_menu())
    await msg.answer("Выбери режим ниже ⬇️", reply_markup=inline_main_menu())

@router.callback_query(F.data == "start")
async def start_cb(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message:
        await call.message.edit_text("🏠 Главное меню. Выбери режим ⬇️", reply_markup=inline_main_menu())

@router.message(F.text == "🏠 Меню")
async def reply_menu_btn(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("🏠 Главное меню. Выбери режим ⬇️", reply_markup=inline_main_menu())
