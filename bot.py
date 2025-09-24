import asyncio
from core.dispatcher import bot, dp
from handlers import routers

async def main():
    for r in routers:
        dp.include_router(r)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
