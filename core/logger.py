import logging
import sys

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,  # или DEBUG для отладки
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("bot.log", encoding="utf-8")
        ]
    )
    return logging.getLogger("bot")
