from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery

from config import TELEGRAM_TOKEN
from core.logger import setup_logger
from core.callback_map import CALLBACK_LABELS

logger = setup_logger()

bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

MAX_LOG_LEN = 200

def _clip(text: str, limit: int = MAX_LOG_LEN) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"

def _user_info(obj) -> str:
    u = getattr(obj, "from_user", None)
    if u:
        return f"{u.id} ({u.full_name or ''} @{u.username or '-'})"
    return "unknown"

async def _state_name(data) -> str | None:
    state = data.get("state")
    return await state.get_state() if state else None

@dp.message.outer_middleware()
async def log_messages(handler, event: Message, data):
    user = _user_info(event)
    state_name = await _state_name(data)
    logger.info(f"📩 {user} | state={state_name} | msg: {_clip(event.text or '')}")
    return await handler(event, data)

@dp.callback_query.outer_middleware()
async def log_callbacks(handler, event: CallbackQuery, data):
    user = _user_info(event)
    state_name = await _state_name(data)
    cb = event.data or ""
    label = CALLBACK_LABELS.get(cb, "")
    suffix = f" {label}" if label else ""
    logger.info(f"🖲 {user} | state={state_name} | cb: {cb}{suffix}")
    return await handler(event, data)

@dp.update.outer_middleware()
async def log_other_updates(handler, event, data):
    if isinstance(event, (Message, CallbackQuery)):
        return await handler(event, data)

    user = _user_info(event)
    state_name = await _state_name(data)
    logger.info(f"📨 {user} | state={state_name} | event: {event.__class__.__name__}")
    return await handler(event, data)
