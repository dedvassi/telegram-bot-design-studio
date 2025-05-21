"""
Точка входа в приложение.
Инициализирует и запускает Telegram-бота.
"""
import os
import logging
import asyncio
from core.bot import TelegramBot
from config.config import Config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """
    Основная функция для запуска бота.
    """
    # Проверка наличия директории для сессий
    os.makedirs(Config.SESSION_BASE_DIR, exist_ok=True)
    
    # Инициализация и запуск бота
    bot = TelegramBot()
    await bot.run()

if __name__ == "__main__":
    # Запуск асинхронной функции main
    asyncio.run(main())
