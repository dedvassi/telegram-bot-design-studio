"""
Модуль аутентификации пользователей Telegram-бота.
Проверяет доступ пользователей на основе white list.
"""
import logging
from functools import wraps
from config.config import Config

logger = logging.getLogger(__name__)

class Auth:
    """
    Класс для аутентификации пользователей Telegram-бота.
    """

    @staticmethod
    def is_user_allowed(user_id: int) -> bool:
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
    def auth_required(bot):
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

                if Auth.is_user_allowed(user_id):
                    return await func(message, *args, **kwargs)
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="⛔ У вас нет доступа к этому боту. Обратитесь к администратору."
                    )
                    # Отправляем уведомление админу
                    admin_id = Config.ADMIN_ID
                    if admin_id:
                        try:
                            await bot.send_message(
                                chat_id=int(admin_id),
                                text=f"⚠️ Попытка несанкционированного доступа от пользователя {user_id} (@{message.from_user.username or 'без ника'})"
                            )
                        except Exception as e:
                            logger.info(f"Уведомление о попытке несанкционированного доступа  отправлено админу")
                    return None
            return wrapper
        return decorator
