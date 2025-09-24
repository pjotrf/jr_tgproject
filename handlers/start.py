from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎲 Факт", callback_data="random"),
            InlineKeyboardButton(text="💬 GPT", callback_data="gpt"),
        ],
        [
            InlineKeyboardButton(text="🧑‍🎓 Личность", callback_data="talk"),
            InlineKeyboardButton(text="📝 Квиз", callback_data="quiz"),
        ],
        [
            InlineKeyboardButton(text="🌐 Переводчик", callback_data="translator"),
            InlineKeyboardButton(text="🎬 Рекомендации", callback_data="recs"),
        ]
    ])

def reply_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Меню")]],
        resize_keyboard=True
    )

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я твой помощник ChatGPT 🤖\nВыбери режим ниже ⬇️",
        reply_markup=main_menu_kb()
    )
    await message.answer("Для возврата всегда жми кнопку 🏠 Меню ⬇️", reply_markup=reply_menu_kb())

@router.callback_query(F.data == "start")
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "🏠 Главное меню. Выбери режим ⬇️",
        reply_markup=main_menu_kb()
    )
    await callback.message.answer("Для возврата всегда жми кнопку 🏠 Меню ⬇️", reply_markup=reply_menu_kb())
    await callback.answer()

@router.message(F.text == "🏠 Меню")
async def menu_button_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Главное меню. Выбери режим ⬇️",
        reply_markup=main_menu_kb()
    )
