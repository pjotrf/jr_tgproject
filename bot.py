import asyncio
from core.dispatcher import dp, bot, logger
from handlers import start, random_fact, gpt, talk, quiz, translator, recs

async def main():
    logger.info("🚀 Bot starting...")

    dp.include_router(start.router)
    dp.include_router(random_fact.router)
    dp.include_router(gpt.router)
    dp.include_router(talk.router)
    dp.include_router(quiz.router)
    dp.include_router(translator.router)
    dp.include_router(recs.router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"❌ Bot crashed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
