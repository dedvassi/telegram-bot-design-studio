"""
Модуль аутентификации пользователей Telegram-бота.
Проверяет доступ пользователей на основе white list.
"""
import logging
from config.config import Config

logger = logging.getLogger(__name__)

class Auth:
    """
    Класс для аутентификации пользователей Telegram-бота.
    """
    
    @staticmethod
    def is_user_allowed(user_id):
        """
        Проверяет, имеет ли пользователь доступ к боту.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            bool: True, если пользователь имеет доступ, иначе False.
        """
        if not Config.ALLOWED_USERS:
            logger.warning("Список разрешенных пользователей пуст. Доступ разрешен всем.")
            return True
        
        is_allowed = user_id in Config.ALLOWED_USERS
        
        if not is_allowed:
            logger.warning(f"Попытка несанкционированного доступа от пользователя {user_id}")
        
        return is_allowed
    
    @staticmethod
    def auth_required(func):
        """
        Декоратор для проверки доступа пользователя перед выполнением команды.
        
        Args:
            func: Функция-обработчик команды.
            
        Returns:
            function: Обернутая функция с проверкой доступа.
        """
        async def wrapper(message, *args, **kwargs):
            user_id = message.from_user.id
            
            if Auth.is_user_allowed(user_id):
                return await func(message, *args, **kwargs)
            else:
                # Исправлено: используем message.bot.send_message вместо message.reply
                await message.bot.send_message(message.chat.id, "У вас нет доступа к этому боту.")
                return None
        
        return wrapper
