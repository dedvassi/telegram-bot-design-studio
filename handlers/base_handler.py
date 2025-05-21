"""
Базовый класс обработчика команд.
"""
import logging

logger = logging.getLogger(__name__)

class BaseHandler:
    """
    Базовый класс для обработчиков команд.
    """
    
    def __init__(self, bot, session_manager):
        """
        Инициализация базового обработчика.
        
        Args:
            bot: Объект Telegram-бота.
            session_manager: Объект менеджера сессий.
        """
        self.bot = bot
        self.session_manager = session_manager
        
        logger.info("Инициализирован базовый обработчик команд")
    
    async def handle_command(self, message):
        """
        Обработчик команды.
        
        Args:
            message: Объект сообщения Telegram.
        """
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")
