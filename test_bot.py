"""
Модуль для тестирования функциональности Telegram-бота.
"""
import os
import logging
import asyncio
import unittest
from unittest.mock import MagicMock, patch
from config.config import Config
from core.session_manager import SessionManager
from core.auth import Auth
from services.whisper_service import WhisperService
from services.ollama_service import OllamaService
from utils.pdf_generator import PDFGenerator
from utils.file_manager import FileManager
from utils.text_formatter import TextFormatter

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TestSessionManager(unittest.TestCase):
    """
    Тесты для менеджера сессий.
    """
    
    def setUp(self):
        """
        Подготовка к тестам.
        """
        # Создаем временную директорию для тестов
        self.test_dir = "/tmp/test_sessions"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Подменяем директорию сессий
        self.original_session_dir = Config.SESSION_BASE_DIR
        Config.SESSION_BASE_DIR = self.test_dir
        
        # Создаем экземпляр менеджера сессий
        self.session_manager = SessionManager()
        
        # Тестовый пользователь
        self.test_user_id = 123456789
    
    def tearDown(self):
        """
        Очистка после тестов.
        """
        # Восстанавливаем оригинальную директорию сессий
        Config.SESSION_BASE_DIR = self.original_session_dir
        
        # Удаляем временную директорию
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_create_session(self):
        """
        Тест создания сессии.
        """
        # Создаем сессию
        session_dir = self.session_manager.create_session(self.test_user_id)
        
        # Проверяем, что директория создана
        self.assertTrue(os.path.exists(session_dir))
        
        # Проверяем, что файл данных сессии создан
        session_file = os.path.join(session_dir, "session.json")
        self.assertTrue(os.path.exists(session_file))
        
        # Проверяем данные сессии
        session_data = self.session_manager.get_session_data(self.test_user_id)
        self.assertEqual(session_data["user_id"], self.test_user_id)
        self.assertEqual(session_data["state"], "init")
    
    def test_update_session_data(self):
        """
        Тест обновления данных сессии.
        """
        # Создаем сессию
        self.session_manager.create_session(self.test_user_id)
        
        # Обновляем данные сессии
        self.session_manager.update_session_data(
            self.test_user_id,
            {"metadata": {"protocol_name": "Test Protocol"}}
        )
        
        # Проверяем обновленные данные
        session_data = self.session_manager.get_session_data(self.test_user_id)
        self.assertEqual(session_data["metadata"]["protocol_name"], "Test Protocol")
    
    def test_update_session_state(self):
        """
        Тест обновления состояния сессии.
        """
        # Создаем сессию
        self.session_manager.create_session(self.test_user_id)
        
        # Обновляем состояние сессии
        self.session_manager.update_session_state(self.test_user_id, "waiting_protocol_name")
        
        # Проверяем обновленное состояние
        state = self.session_manager.get_session_state(self.test_user_id)
        self.assertEqual(state, "waiting_protocol_name")
    
    def test_delete_session(self):
        """
        Тест удаления сессии.
        """
        # Создаем сессию
        session_dir = self.session_manager.create_session(self.test_user_id)
        
        # Проверяем, что директория создана
        self.assertTrue(os.path.exists(session_dir))
        
        # Удаляем сессию
        result = self.session_manager.delete_session(self.test_user_id)
        
        # Проверяем результат удаления
        self.assertTrue(result)
        
        # Проверяем, что директория удалена
        self.assertFalse(os.path.exists(session_dir))

class TestAuth(unittest.TestCase):
    """
    Тесты для аутентификации.
    """
    
    def setUp(self):
        """
        Подготовка к тестам.
        """
        # Сохраняем оригинальный список разрешенных пользователей
        self.original_allowed_users = Config.ALLOWED_USERS
        
        # Устанавливаем тестовый список разрешенных пользователей
        Config.ALLOWED_USERS = [123456789, 987654321]
    
    def tearDown(self):
        """
        Очистка после тестов.
        """
        # Восстанавливаем оригинальный список разрешенных пользователей
        Config.ALLOWED_USERS = self.original_allowed_users
    
    def test_is_user_allowed(self):
        """
        Тест проверки доступа пользователя.
        """
        # Проверяем разрешенного пользователя
        self.assertTrue(Auth.is_user_allowed(123456789))
        
        # Проверяем запрещенного пользователя
        self.assertFalse(Auth.is_user_allowed(111111111))
    
    def test_empty_allowed_users(self):
        """
        Тест проверки доступа при пустом списке разрешенных пользователей.
        """
        # Устанавливаем пустой список разрешенных пользователей
        Config.ALLOWED_USERS = []
        
        # Проверяем, что любой пользователь имеет доступ
        self.assertTrue(Auth.is_user_allowed(123456789))
        self.assertTrue(Auth.is_user_allowed(111111111))

class TestWhisperService(unittest.TestCase):
    """
    Тесты для сервиса Whisper.
    """
    
    def setUp(self):
        """
        Подготовка к тестам.
        """
        # Создаем экземпляр сервиса Whisper
        self.whisper_service = WhisperService()
        
        # Создаем временный аудиофайл
        self.test_audio_file = "/tmp/test_audio.ogg"
        with open(self.test_audio_file, "wb") as f:
            f.write(b"test audio data")
    
    def tearDown(self):
        """
        Очистка после тестов.
        """
        # Удаляем временный аудиофайл
        if os.path.exists(self.test_audio_file):
            os.unlink(self.test_audio_file)
    
    async def test_transcribe_audio(self):
        """
        Тест распознавания речи.
        """
        # Распознаем речь
        transcription = await self.whisper_service.transcribe_audio(self.test_audio_file)
        
        # Проверяем результат
        self.assertIsNotNone(transcription)
        self.assertIsInstance(transcription, str)
    
    async def test_transcribe_nonexistent_file(self):
        """
        Тест распознавания несуществующего файла.
        """
        # Распознаем несуществующий файл
        transcription = await self.whisper_service.transcribe_audio("/tmp/nonexistent.ogg")
        
        # Проверяем результат
        self.assertIsNone(transcription)

class TestOllamaService(unittest.TestCase):
    """
    Тесты для сервиса Ollama.
    """
    
    def setUp(self):
        """
        Подготовка к тестам.
        """
        # Создаем экземпляр сервиса Ollama
        self.ollama_service = OllamaService()
        
        # Тестовый текст
        self.test_text = "Вопрос первый. 3D-визуализация спальни. Вопрос второй. Подбор мебели в детскую."
    
    async def test_format_questions(self):
        """
        Тест форматирования вопросов.
        """
        # Форматируем текст
        formatted_text = await self.ollama_service.format_text(self.test_text, "questions")
        
        # Проверяем результат
        self.assertIsNotNone(formatted_text)
        self.assertIsInstance(formatted_text, str)
        self.assertIn("1.", formatted_text)
        self.assertIn("2.", formatted_text)
    
    async def test_format_decisions(self):
        """
        Тест форматирования решений.
        """
        # Форматируем текст
        formatted_text = await self.ollama_service.format_text(self.test_text, "decisions")
        
        # Проверяем результат
        self.assertIsNotNone(formatted_text)
        self.assertIsInstance(formatted_text, str)
        self.assertIn("1.", formatted_text)
        self.assertIn("2.", formatted_text)

class TestPDFGenerator(unittest.TestCase):
    """
    Тесты для генератора PDF.
    """
    
    def setUp(self):
        """
        Подготовка к тестам.
        """
        # Создаем экземпляр генератора PDF
        self.pdf_generator = PDFGenerator()
        
        # Тестовые данные
        self.metadata = {
            "protocol_name": "Test Protocol",
            "date": "01.01.2025",
            "project_number": "123",
            "contract_year": "2025",
            "project_type": "Test",
            "object_name": "Test Object",
            "client_name": "Test Client"
        }
        self.questions = "1. 3D-визуализация спальни\n2. Подбор мебели в детскую"
        self.decisions = "1. Подготовить 3D-визуализацию спальни к следующей встрече\n2. Составить список рекомендуемой мебели для детской"
        
        # Путь для сохранения PDF
        self.pdf_path = "/tmp/test_protocol.pdf"
    
    def tearDown(self):
        """
        Очистка после тестов.
        """
        # Удаляем тестовый PDF
        if os.path.exists(self.pdf_path):
            os.unlink(self.pdf_path)
    
    def test_generate_protocol_pdf(self):
        """
        Тест генерации PDF.
        """
        # Генерируем PDF
        result = self.pdf_generator.generate_protocol_pdf(
            self.metadata,
            self.questions,
            self.decisions,
            self.pdf_path
        )
        
        # Проверяем результат
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.pdf_path))
        
        # Проверяем размер файла
        self.assertGreater(os.path.getsize(self.pdf_path), 0)

class TestTextFormatter(unittest.TestCase):
    """
    Тесты для форматирования текста.
    """
    
    def test_format_questions_to_markdown(self):
        """
        Тест форматирования вопросов в Markdown.
        """
        # Тестовый текст
        text = "Вопрос первый. 3D-визуализация спальни. Вопрос второй. Подбор мебели в детскую."
        
        # Форматируем текст
        formatted_text = TextFormatter.format_questions_to_markdown(text)
        
        # Проверяем результат
        self.assertIsNotNone(formatted_text)
        self.assertIsInstance(formatted_text, str)
        self.assertIn("1.", formatted_text)
        self.assertIn("2.", formatted_text)
    
    def test_format_decisions_to_markdown(self):
        """
        Тест форматирования решений в Markdown.
        """
        # Тестовый текст
        text = "Решение первое. Подготовить 3D-визуализацию спальни к следующей встрече. Решение второе. Составить список рекомендуемой мебели для детской."
        
        # Форматируем текст
        formatted_text = TextFormatter.format_decisions_to_markdown(text)
        
        # Проверяем результат
        self.assertIsNotNone(formatted_text)
        self.assertIsInstance(formatted_text, str)
        self.assertIn("1.", formatted_text)
        self.assertIn("2.", formatted_text)

async def run_async_tests():
    """
    Запуск асинхронных тестов.
    """
    # Тесты для сервиса Whisper
    whisper_test = TestWhisperService()
    whisper_test.setUp()
    await whisper_test.test_transcribe_audio()
    await whisper_test.test_transcribe_nonexistent_file()
    whisper_test.tearDown()
    
    # Тесты для сервиса Ollama
    ollama_test = TestOllamaService()
    ollama_test.setUp()
    await ollama_test.test_format_questions()
    await ollama_test.test_format_decisions()

def run_tests():
    """
    Запуск всех тестов.
    """
    # Запуск синхронных тестов
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # Запуск асинхронных тестов
    asyncio.run(run_async_tests())

if __name__ == "__main__":
    run_tests()
