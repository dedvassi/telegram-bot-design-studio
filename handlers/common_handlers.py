"""
Обработчик общих команд.
"""
import logging
from handlers.base_handler import BaseHandler

logger = logging.getLogger(__name__)

class CommonHandlers(BaseHandler):
    """
    Класс для обработки общих команд.
    """
    
    async def handle_start(self, message):
        """
        Обработчик команды /start.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        
        await self.bot.send_message(
            message.chat.id,
            f"Привет, {username}! Я бот для бизнес-задач дизайн-студии.\n\n"
            "Доступные команды:\n"
            "/protocol - Запуск сценария протоколирования встречи\n"
            "/help - Показать справку"
        )
        
        logger.info(f"Пользователь {user_id} запустил бота")
    
    async def handle_help(self, message):
        """
        Обработчик команды /help.
        
        Args:
            message: Объект сообщения Telegram.
        """
        await self.bot.send_message(
            message.chat.id,
            "Справка по командам бота:\n\n"
            "/protocol - Запуск сценария протоколирования встречи\n"
            "  Этот сценарий позволяет создать протокол встречи с заказчиком.\n"
            "  Бот последовательно запросит необходимые данные, включая:\n"
            "  - Название протокола\n"
            "  - Метаданные (дата, номер проекта, год договора и т.д.)\n"
            "  - Ключевые вопросы (через голосовое сообщение)\n"
            "  - Принятые решения (через голосовое сообщение)\n"
            "  После подтверждения всех блоков бот сгенерирует PDF-документ.\n\n"
            "/help - Показать эту справку"
        )
        
        logger.info(f"Пользователь {message.from_user.id} запросил справку")
