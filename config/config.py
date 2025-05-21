import os
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурационные параметры
class Config:
    # Токен Telegram бота
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # ADMIN_ID
    ADMIN_ID = os.getenv('ADMIN_ID')
    
    # Настройки Whisper
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'large')
    
    # Настройки Ollama
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
    OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
    
    # Настройки безопасности
    # Список разрешенных пользователей
    ALLOWED_USERS = [int(user_id) for user_id in os.getenv('ALLOWED_USERS', '').split(',') if user_id]
    
    # Настройки сессий
    SESSION_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sessions')
    
    # Настройки PDF
    PDF_LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates', 'logo.png')
    PDF_PRIMARY_COLOR = (41, 128, 185)  # RGB цвет для брендирования (синий)
    PDF_SECONDARY_COLOR = (52, 73, 94)  # RGB цвет для брендирования (темно-серый)
    
    @classmethod
    def validate(cls):
        """Проверка наличия всех необходимых конфигурационных параметров"""
        if not cls.TELEGRAM_BOT_TOKEN:
            logger.error("Не указан токен Telegram бота (TELEGRAM_BOT_TOKEN)")
            return False
        
        if not cls.ALLOWED_USERS:
            logger.warning("Не указаны разрешенные пользователи (ALLOWED_USERS)")
        
        return True
