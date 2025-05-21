"""
Модуль аутентификации пользователей Telegram-бота.
Проверяет доступ пользователей на основе white list.
"""
import logging
from functools import wraps
from core.user_manager import UserManager

logger = logging.getLogger(__name__)

class Auth:
    """
    Класс для аутентификации пользователей Telegram-бота.
    """

    def __init__(self, user_manager: UserManager, admin_handlers=None):
        """
        Инициализация аутентификации.

        Args:
            user_manager (UserManager): Менеджер пользователей.
            admin_handlers: Обработчики команд администратора.
        """
        self.user_manager = user_manager
        self.admin_handlers = admin_handlers

    def auth_required(self, bot):
        """
        Декоратор для проверки доступа пользователя перед выполнением команды.

        Args:
            bot (AsyncTeleBot): Экземпляр асинхронного Telegram-бота.

        Returns:
            function: Декоратор.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(message, *args, **kwargs):
                user_id = message.from_user.id
                username = message.from_user.username or message.from_user.first_name

                if self.user_manager.is_user_allowed(user_id):
                    return await func(message, *args, **kwargs)
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="⛔ У вас нет доступа к этому боту. Обратитесь к администратору."
                    )

                    # Отправляем уведомление админу с кнопками
                    if self.admin_handlers:
                        await self.admin_handlers.handle_unauthorized_access(user_id, username)

                    return None
            return wrapper
        return decorator

    def admin_required(self, bot):
        """
        Декоратор для проверки прав администратора перед выполнением команды.

        Args:
            bot (AsyncTeleBot): Экземпляр асинхронного Telegram-бота.

        Returns:
            function: Декоратор.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(message, *args, **kwargs):
                user_id = message.from_user.id

                if self.user_manager.is_admin(user_id):
                    return await func(message, *args, **kwargs)
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="⛔ У вас нет прав администратора."
                    )
                    return None
            return wrapper
        return decorator
