import logging
import os
from datetime import datetime

# Создаём папку для логов если нет
os.makedirs("logs", exist_ok=True)

# Настраиваем logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # Логи в файл
        logging.FileHandler(
            f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log",
            encoding="utf-8"
        ),
        # Логи в терминал
        logging.StreamHandler()
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)