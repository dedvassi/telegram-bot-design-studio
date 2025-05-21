"""
Основной класс Telegram-бота.
Инициализирует бота, регистрирует обработчики команд и запускает его.
"""
import logging
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config.config import Config
from core.session_manager import SessionManager
from core.auth import Auth
from core.user_manager import UserManager  # Новый импорт
from handlers.admin_handlers import AdminHandlers  # Новый импорт

logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Класс для работы с Telegram-ботом.
    """

    def __init__(self):
        """
        Инициализация Telegram-бота.
        """
        self.bot = AsyncTeleBot(Config.TELEGRAM_BOT_TOKEN)
        self.session_manager = SessionManager()

        # Инициализация менеджера пользователей
        self.user_manager = UserManager(
            Config.USERS_FILE_PATH,
            int(Config.ADMIN_ID) if Config.ADMIN_ID else None
        )

        # Инициализация обработчиков команд администратора
        self.admin_handlers = AdminHandlers(self.bot, self.user_manager)

        # Инициализация аутентификации с передачей менеджера пользователей и обработчиков админа
        self.auth = Auth(self.user_manager, self.admin_handlers)

        # Регистрация обработчиков команд
        self._register_handlers()

        logger.info("Telegram-бот инициализирован")

    def _register_handlers(self):
        """
        Регистрация обработчиков команд.
        """
        # Создаем декораторы для проверки прав доступа
        auth_decorator = self.auth.auth_required(self.bot)
        admin_decorator = self.auth.admin_required(self.bot)  # Новый декоратор для админа

        # Обработчик команды /start
        @self.bot.message_handler(commands=['start'])
        @auth_decorator
        async def start_command(message):
            await self._handle_start(message)

        # Обработчик команды /help
        @self.bot.message_handler(commands=['help'])
        @auth_decorator
        async def help_command(message):
            await self._handle_help(message)

        # Обработчик команды /protocol
        @self.bot.message_handler(commands=['protocol'])
        @auth_decorator
        async def protocol_command(message):
            await self._handle_protocol_start(message)

        # НОВЫЕ ОБРАБОТЧИКИ КОМАНД АДМИНИСТРАТОРА

        # Обработчик команды /admin - показывает меню администратора
        @self.bot.message_handler(commands=['admin'])
        @auth_decorator  # Используем auth_decorator, но внутри метода проверяем права админа
        async def admin_command(message):
            await self.admin_handlers.handle_admin_command(message)

        # Обработчик команды /users - показывает список разрешенных пользователей
        @self.bot.message_handler(commands=['users'])
        @auth_decorator  # Используем auth_decorator, но внутри метода проверяем права админа
        async def users_command(message):
            await self.admin_handlers.handle_users_command(message)

        # Обработчик команды /adduser - добавляет пользователя по ID
        @self.bot.message_handler(commands=['adduser'])
        @auth_decorator  # Используем auth_decorator, но внутри метода проверяем права админа
        async def add_user_command(message):
            await self.admin_handlers.handle_add_user_command(message)

        # Обработчик команды /removeuser - удаляет пользователя по ID
        @self.bot.message_handler(commands=['removeuser'])
        @auth_decorator  # Используем auth_decorator, но внутри метода проверяем права админа
        async def remove_user_command(message):
            await self.admin_handlers.handle_remove_user_command(message)

        # Обработчик текстовых сообщений
        @self.bot.message_handler(content_types=['text'])
        @auth_decorator
        async def text_message(message):
            await self._handle_text_message(message)

        # Обработчик голосовых сообщений
        @self.bot.message_handler(content_types=['voice'])
        @auth_decorator
        async def voice_message(message):
            await self._handle_voice_message(message)

        # НОВЫЙ ОБРАБОТЧИК CALLBACK-ЗАПРОСОВ

        # Обработчик callback-запросов от кнопок
        @self.bot.callback_query_handler(func=lambda call: True)
        async def callback_handler(call):
            # Проверяем, относится ли callback к командам администратора
            if (call.data.startswith('admin_') or
                call.data.startswith('remove_user_') or
                call.data.startswith('add_user_') or
                call.data.startswith('block_user_')):
                await self.admin_handlers.handle_admin_callback(call)

        logger.info("Обработчики команд зарегистрированы")

    async def _handle_start(self, message):
        """
        Обработчик команды /start.

        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        # Добавляем информацию о командах администратора, если пользователь - админ
        admin_commands = ""
        if self.user_manager.is_admin(user_id):
            admin_commands = "\n\n🔐 Команды администратора:\n" \
                             "/admin - Меню администратора\n" \
                             "/users - Список разрешенных пользователей\n" \
                             "/adduser ID - Добавить пользователя\n" \
                             "/removeuser ID - Удалить пользователя"

        await self.bot.send_message(
            message.chat.id,
            f"Привет, {username}! Я бот для бизнес-задач дизайн-студии.\n\n"
            "Доступные команды:\n"
            "/protocol - Запуск сценария протоколирования встречи\n"
            "/help - Показать справку" + admin_commands
        )

        logger.info(f"Пользователь {user_id} запустил бота")

    async def _handle_help(self, message):
        """
        Обработчик команды /help.

        Args:
            message: Объект сообщения Telegram.
        """
        # Добавляем информацию о командах администратора, если пользователь - админ
        admin_help = ""
        if self.user_manager.is_admin(message.from_user.id):
            admin_help = "\n\n🔐 Команды администратора:\n" \
                         "/admin - Меню администратора с интерактивными кнопками\n" \
                         "/users - Показать список разрешенных пользователей\n" \
                         "/adduser ID - Добавить пользователя по ID\n" \
                         "/removeuser ID - Удалить пользователя по ID\n\n" \
                         "При попытке несанкционированного доступа администратор " \
                         "получает уведомление с кнопками для быстрого добавления пользователя."

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
            "/help - Показать эту справку" + admin_help
        )
        
        logger.info(f"Пользователь {message.from_user.id} запросил справку")
    
    async def _handle_protocol_start(self, message):
        """
        Обработчик команды /protocol.
        Запускает сценарий протоколирования встречи.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        
        # Создаем новую сессию для пользователя
        self.session_manager.create_session(user_id)
        
        # Устанавливаем начальное состояние сессии
        self.session_manager.update_session_state(user_id, "waiting_protocol_name")
        
        # Запрашиваем название протокола
        await self.bot.send_message(
            message.chat.id,
            "Введите название протокола:"
        )
        
        logger.info(f"Пользователь {user_id} запустил сценарий протоколирования встречи")
    
    async def _handle_text_message(self, message):
        """
        Обработчик текстовых сообщений.
        Обрабатывает сообщения в зависимости от текущего состояния сессии.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        text = message.text
        
        # Получаем текущее состояние сессии
        state = self.session_manager.get_session_state(user_id)
        
        if not state:
            # Если сессия не найдена, предлагаем начать сценарий
            await self.bot.send_message(
                message.chat.id,
                "Для начала работы используйте команду /protocol"
            )
            return
        
        # Обработка сообщения в зависимости от состояния сессии
        if state == "waiting_protocol_name":
            # Сохраняем название протокола
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"protocol_name": text}}
            )
            
            # Переходим к следующему шагу - запрос даты
            self.session_manager.update_session_state(user_id, "waiting_date")
            
            await self.bot.send_message(
                message.chat.id,
                "Введите дату встречи:"
            )
        
        elif state == "waiting_date":
            # Сохраняем дату
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"date": text}}
            )
            
            # Переходим к следующему шагу - запрос номера проекта
            self.session_manager.update_session_state(user_id, "waiting_project_number")
            
            await self.bot.send_message(
                message.chat.id,
                "Введите номер проекта:"
            )
        
        elif state == "waiting_project_number":
            # Сохраняем номер проекта
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"project_number": text}}
            )
            
            # Переходим к следующему шагу - запрос года договора
            self.session_manager.update_session_state(user_id, "waiting_contract_year")
            
            await self.bot.send_message(
                message.chat.id,
                "Введите год договора:"
            )
        
        elif state == "waiting_contract_year":
            # Сохраняем год договора
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"contract_year": text}}
            )
            
            # Переходим к следующему шагу - запрос типа проекта
            self.session_manager.update_session_state(user_id, "waiting_project_type")
            
            await self.bot.send_message(
                message.chat.id,
                "Введите тип проекта:"
            )
        
        elif state == "waiting_project_type":
            # Сохраняем тип проекта
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"project_type": text}}
            )
            
            # Переходим к следующему шагу - запрос названия ЖК/объекта
            self.session_manager.update_session_state(user_id, "waiting_object_name")
            
            await self.bot.send_message(
                message.chat.id,
                "Введите название ЖК/объекта:"
            )
        
        elif state == "waiting_object_name":
            # Сохраняем название ЖК/объекта
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"object_name": text}}
            )
            
            # Переходим к следующему шагу - запрос имени заказчика
            self.session_manager.update_session_state(user_id, "waiting_client_name")
            
            await self.bot.send_message(
                message.chat.id,
                "Введите имя заказчика:"
            )
        
        elif state == "waiting_client_name":
            # Сохраняем имя заказчика
            self.session_manager.update_session_data(
                user_id,
                {"metadata": {"client_name": text}}
            )
            
            # Переходим к следующему шагу - запрос голосового сообщения с вопросами
            self.session_manager.update_session_state(user_id, "waiting_questions_voice")
            
            await self.bot.send_message(
                message.chat.id,
                "Теперь отправьте голосовое сообщение с ключевыми вопросами встречи, указывая нумерацию вопросов."
            )
        
        elif state == "waiting_questions_confirmation":
            # Обработка подтверждения списка вопросов
            if text.lower() in ["да", "хорошо", "верно", "ок", "ok", "yes"]:
                # Переходим к следующему шагу - запрос голосового сообщения с решениями
                self.session_manager.update_session_state(user_id, "waiting_decisions_voice")
                
                await self.bot.send_message(
                    message.chat.id,
                    "Теперь отправьте голосовое сообщение с принятыми решениями, указывая нумерацию решений."
                )
            else:
                # Возвращаемся к запросу голосового сообщения с вопросами
                self.session_manager.update_session_state(user_id, "waiting_questions_voice")
                
                await self.bot.send_message(
                    message.chat.id,
                    "Пожалуйста, отправьте голосовое сообщение с ключевыми вопросами встречи повторно."
                )
        
        elif state == "waiting_decisions_confirmation":
            # Обработка подтверждения списка решений
            if text.lower() in ["да", "хорошо", "верно", "ок", "ok", "yes"]:
                # Переходим к генерации PDF
                self.session_manager.update_session_state(user_id, "generating_pdf")
                
                await self.bot.send_message(
                    message.chat.id,
                    "Генерирую итоговый PDF-документ..."
                )
                
                # Здесь будет вызов функции генерации PDF
                # await self._generate_and_send_pdf(message)
                
                # Временная заглушка
                await self.bot.send_message(
                    message.chat.id,
                    "Функция генерации PDF будет реализована на следующем этапе."
                )
                
                # Удаляем сессию
                self.session_manager.delete_session(user_id)
            else:
                # Возвращаемся к запросу голосового сообщения с решениями
                self.session_manager.update_session_state(user_id, "waiting_decisions_voice")
                
                await self.bot.send_message(
                    message.chat.id,
                    "Пожалуйста, отправьте голосовое сообщение с принятыми решениями повторно."
                )
    
    async def _handle_voice_message(self, message):
        """
        Обработчик голосовых сообщений.
        Обрабатывает голосовые сообщения в зависимости от текущего состояния сессии.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        
        # Получаем текущее состояние сессии
        state = self.session_manager.get_session_state(user_id)
        
        if not state:
            # Если сессия не найдена, предлагаем начать сценарий
            await self.bot.send_message(
                message.chat.id,
                "Для начала работы используйте команду /protocol"
            )
            return
        
        # Обработка голосового сообщения в зависимости от состояния сессии
        if state == "waiting_questions_voice":
            # Здесь будет обработка голосового сообщения с вопросами
            # Скачивание файла, распознавание речи через Whisper, форматирование через Ollama
            
            # Временная заглушка
            await self.bot.send_message(
                message.chat.id,
                "Распознавание речи и обработка текста будут реализованы на следующем этапе.\n\n"
                "Пример распознанного текста:\n"
                "1. 3D-визуализация спальни\n"
                "2. Подбор мебели в детскую\n\n"
                "Всё верно?"
            )
            
            # Переходим к подтверждению списка вопросов
            self.session_manager.update_session_state(user_id, "waiting_questions_confirmation")
            
            # Сохраняем пример списка вопросов
            self.session_manager.update_session_data(
                user_id,
                {"questions": "1. 3D-визуализация спальни\n2. Подбор мебели в детскую"}
            )
        
        elif state == "waiting_decisions_voice":
            # Здесь будет обработка голосового сообщения с решениями
            # Скачивание файла, распознавание речи через Whisper, форматирование через Ollama
            
            # Временная заглушка
            await self.bot.send_message(
                message.chat.id,
                "Распознавание речи и обработка текста будут реализованы на следующем этапе.\n\n"
                "Пример распознанного текста:\n"
                "1. Подготовить 3D-визуализацию спальни к следующей встрече\n"
                "2. Составить список рекомендуемой мебели для детской\n\n"
                "Всё верно?"
            )
            
            # Переходим к подтверждению списка решений
            self.session_manager.update_session_state(user_id, "waiting_decisions_confirmation")
            
            # Сохраняем пример списка решений
            self.session_manager.update_session_data(
                user_id,
                {"decisions": "1. Подготовить 3D-визуализацию спальни к следующей встрече\n2. Составить список рекомендуемой мебели для детской"}
            )
    
    async def run(self):
        """
        Запуск бота.
        """
        # Проверка конфигурации
        if not Config.validate():
            logger.error("Ошибка в конфигурации бота")
            return
        
        logger.info("Запуск Telegram-бота")
        
        # Запуск бота в режиме polling
        await self.bot.polling(non_stop=True)
