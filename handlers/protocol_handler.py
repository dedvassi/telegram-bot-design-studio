"""
Обработчик команды /protocol.
Реализует сценарий протоколирования встречи.
"""
import os
import logging
import asyncio
from telebot import types
from core.auth import Auth
from services.whisper_service import WhisperService
from services.ollama_service import OllamaService
from utils.pdf_generator import PDFGenerator
from utils.file_manager import FileManager
from utils.text_formatter import TextFormatter

logger = logging.getLogger(__name__)

class ProtocolHandler:
    """
    Класс для обработки команды /protocol.
    """
    
    def __init__(self, bot, session_manager):
        """
        Инициализация обработчика команды /protocol.
        
        Args:
            bot: Объект Telegram-бота.
            session_manager: Объект менеджера сессий.
        """
        self.bot = bot
        self.session_manager = session_manager
        self.whisper_service = WhisperService()
        self.ollama_service = OllamaService()
        self.pdf_generator = PDFGenerator()
        
        logger.info("Инициализирован обработчик команды /protocol")
    
    async def handle_protocol_start(self, message):
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
    
    async def handle_text_message(self, message):
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
            await self._handle_protocol_name(message, text)
        elif state == "waiting_date":
            await self._handle_date(message, text)
        elif state == "waiting_project_number":
            await self._handle_project_number(message, text)
        elif state == "waiting_contract_year":
            await self._handle_contract_year(message, text)
        elif state == "waiting_project_type":
            await self._handle_project_type(message, text)
        elif state == "waiting_object_name":
            await self._handle_object_name(message, text)
        elif state == "waiting_client_name":
            await self._handle_client_name(message, text)
        elif state == "waiting_questions_confirmation":
            await self._handle_questions_confirmation(message, text)
        elif state == "waiting_decisions_confirmation":
            await self._handle_decisions_confirmation(message, text)
    
    async def handle_voice_message(self, message):
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
            await self._handle_questions_voice(message)
        elif state == "waiting_decisions_voice":
            await self._handle_decisions_voice(message)
    
    async def _handle_protocol_name(self, message, text):
        """
        Обработчик ввода названия протокола.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_date(self, message, text):
        """
        Обработчик ввода даты.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_project_number(self, message, text):
        """
        Обработчик ввода номера проекта.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_contract_year(self, message, text):
        """
        Обработчик ввода года договора.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_project_type(self, message, text):
        """
        Обработчик ввода типа проекта.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_object_name(self, message, text):
        """
        Обработчик ввода названия ЖК/объекта.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_client_name(self, message, text):
        """
        Обработчик ввода имени заказчика.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_questions_voice(self, message):
        """
        Обработчик голосового сообщения с вопросами.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        
        # Отправляем сообщение о начале обработки
        processing_msg = await self.bot.send_message(
            message.chat.id,
            "Обрабатываю голосовое сообщение..."
        )
        
        try:
            # Получаем информацию о голосовом сообщении
            file_info = await self.bot.get_file(message.voice.file_id)
            
            # Скачиваем файл
            downloaded_file = await self.bot.download_file(file_info.file_path)
            
            # Сохраняем файл в директории сессии
            voice_file_path = FileManager.save_voice_message(user_id, downloaded_file)
            
            if not voice_file_path:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при сохранении голосового сообщения. Пожалуйста, попробуйте еще раз."
                )
                return
            
            # Распознаем речь
            transcription = await self.whisper_service.transcribe_audio(voice_file_path)
            
            if not transcription:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при распознавании речи. Пожалуйста, попробуйте еще раз."
                )
                return
            
            # Форматируем текст
            formatted_text = await self.ollama_service.format_text(transcription, "questions")
            
            if not formatted_text:
                # Используем резервный метод форматирования
                formatted_text = TextFormatter.format_questions_to_markdown(transcription)
            
            # Сохраняем форматированный текст
            self.session_manager.update_session_data(
                user_id,
                {"questions": formatted_text}
            )
            
            # Отправляем результат пользователю
            await self.bot.send_message(
                message.chat.id,
                f"Распознанный текст:\n\n{formatted_text}\n\nВсё верно?"
            )
            
            # Переходим к подтверждению списка вопросов
            self.session_manager.update_session_state(user_id, "waiting_questions_confirmation")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке голосового сообщения: {str(e)}")
            await self.bot.send_message(
                message.chat.id,
                "Произошла ошибка при обработке голосового сообщения. Пожалуйста, попробуйте еще раз."
            )
    
    async def _handle_questions_confirmation(self, message, text):
        """
        Обработчик подтверждения списка вопросов.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
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
    
    async def _handle_decisions_voice(self, message):
        """
        Обработчик голосового сообщения с решениями.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        
        # Отправляем сообщение о начале обработки
        processing_msg = await self.bot.send_message(
            message.chat.id,
            "Обрабатываю голосовое сообщение..."
        )
        
        try:
            # Получаем информацию о голосовом сообщении
            file_info = await self.bot.get_file(message.voice.file_id)
            
            # Скачиваем файл
            downloaded_file = await self.bot.download_file(file_info.file_path)
            
            # Сохраняем файл в директории сессии
            voice_file_path = FileManager.save_voice_message(user_id, downloaded_file, "decisions_voice.ogg")
            
            if not voice_file_path:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при сохранении голосового сообщения. Пожалуйста, попробуйте еще раз."
                )
                return
            
            # Распознаем речь
            transcription = await self.whisper_service.transcribe_audio(voice_file_path)
            
            if not transcription:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при распознавании речи. Пожалуйста, попробуйте еще раз."
                )
                return
            
            # Форматируем текст
            formatted_text = await self.ollama_service.format_text(transcription, "decisions")
            
            if not formatted_text:
                # Используем резервный метод форматирования
                formatted_text = TextFormatter.format_decisions_to_markdown(transcription)
            
            # Сохраняем форматированный текст
            self.session_manager.update_session_data(
                user_id,
                {"decisions": formatted_text}
            )
            
            # Отправляем результат пользователю
            await self.bot.send_message(
                message.chat.id,
                f"Распознанный текст:\n\n{formatted_text}\n\nВсё верно?"
            )
            
            # Переходим к подтверждению списка решений
            self.session_manager.update_session_state(user_id, "waiting_decisions_confirmation")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке голосового сообщения: {str(e)}")
            await self.bot.send_message(
                message.chat.id,
                "Произошла ошибка при обработке голосового сообщения. Пожалуйста, попробуйте еще раз."
            )
    
    async def _handle_decisions_confirmation(self, message, text):
        """
        Обработчик подтверждения списка решений.
        
        Args:
            message: Объект сообщения Telegram.
            text: Текст сообщения.
        """
        user_id = message.from_user.id
        
        # Обработка подтверждения списка решений
        if text.lower() in ["да", "хорошо", "верно", "ок", "ok", "yes"]:
            # Переходим к генерации PDF
            self.session_manager.update_session_state(user_id, "generating_pdf")
            
            await self.bot.send_message(
                message.chat.id,
                "Генерирую итоговый PDF-документ..."
            )
            
            # Генерируем и отправляем PDF
            await self._generate_and_send_pdf(message)
        else:
            # Возвращаемся к запросу голосового сообщения с решениями
            self.session_manager.update_session_state(user_id, "waiting_decisions_voice")
            
            await self.bot.send_message(
                message.chat.id,
                "Пожалуйста, отправьте голосовое сообщение с принятыми решениями повторно."
            )
    
    async def _generate_and_send_pdf(self, message):
        """
        Генерирует и отправляет PDF-документ.
        
        Args:
            message: Объект сообщения Telegram.
        """
        user_id = message.from_user.id
        
        try:
            # Получаем данные сессии
            session_data = self.session_manager.get_session_data(user_id)
            
            if not session_data:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при получении данных сессии. Пожалуйста, начните сценарий заново."
                )
                return
            
            # Получаем метаданные, вопросы и решения
            metadata = session_data.get("metadata", {})
            questions = session_data.get("questions", "")
            decisions = session_data.get("decisions", "")
            
            # Получаем путь к директории сессии
            session_dir = self.session_manager.get_session_dir(user_id)
            
            if not session_dir:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при получении директории сессии. Пожалуйста, начните сценарий заново."
                )
                return
            
            # Путь для сохранения PDF
            pdf_path = os.path.join(session_dir, "protocol.pdf")
            
            # Генерируем PDF
            success = self.pdf_generator.generate_protocol_pdf(
                metadata,
                questions,
                decisions,
                pdf_path
            )
            
            if not success:
                await self.bot.send_message(
                    message.chat.id,
                    "Ошибка при генерации PDF. Пожалуйста, попробуйте еще раз."
                )
                return
            
            # Отправляем PDF пользователю
            with open(pdf_path, "rb") as pdf_file:
                await self.bot.send_document(
                    message.chat.id,
                    pdf_file,
                    caption=f"Протокол встречи: {metadata.get('protocol_name', 'Протокол')}"
                )
            
            # Отправляем сообщение об успешном завершении
            await self.bot.send_message(
                message.chat.id,
                "Протокол успешно сгенерирован и отправлен. Сессия завершена."
            )
            
            # Удаляем сессию
            self.session_manager.delete_session(user_id)
            
        except Exception as e:
            logger.error(f"Ошибка при генерации и отправке PDF: {str(e)}")
            await self.bot.send_message(
                message.chat.id,
                "Произошла ошибка при генерации и отправке PDF. Пожалуйста, попробуйте еще раз."
            )
