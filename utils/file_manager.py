"""
Утилита для управления файлами сессий.
"""
import os
import logging
import shutil
from config.config import Config

logger = logging.getLogger(__name__)

class FileManager:
    """
    Класс для управления файлами сессий.
    """
    
    @staticmethod
    def create_session_dir(user_id):
        """
        Создает директорию для сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            str: Путь к созданной директории.
        """
        session_dir = os.path.join(Config.SESSION_BASE_DIR, f"user_id={user_id}")
        
        # Если директория уже существует, удаляем ее
        if os.path.exists(session_dir):
            FileManager.delete_session_dir(user_id)
        
        # Создаем новую директорию
        os.makedirs(session_dir, exist_ok=True)
        
        logger.info(f"Создана директория для сессии пользователя {user_id}: {session_dir}")
        
        return session_dir
    
    @staticmethod
    def delete_session_dir(user_id):
        """
        Удаляет директорию сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            bool: True, если директория успешно удалена, иначе False.
        """
        session_dir = os.path.join(Config.SESSION_BASE_DIR, f"user_id={user_id}")
        
        if not os.path.exists(session_dir):
            logger.warning(f"Директория сессии пользователя {user_id} не найдена")
            return False
        
        try:
            shutil.rmtree(session_dir)
            logger.info(f"Директория сессии пользователя {user_id} удалена: {session_dir}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при удалении директории сессии пользователя {user_id}: {str(e)}")
            return False
    
    @staticmethod
    def save_voice_message(user_id, voice_file_data, file_name="voice_message.ogg"):
        """
        Сохраняет голосовое сообщение в директории сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            voice_file_data (bytes): Данные голосового сообщения.
            file_name (str): Имя файла для сохранения.
            
        Returns:
            str: Путь к сохраненному файлу или None в случае ошибки.
        """
        session_dir = os.path.join(Config.SESSION_BASE_DIR, f"user_id={user_id}")
        
        if not os.path.exists(session_dir):
            logger.warning(f"Директория сессии пользователя {user_id} не найдена")
            return None
        
        file_path = os.path.join(session_dir, file_name)
        
        try:
            with open(file_path, "wb") as f:
                f.write(voice_file_data)
            
            logger.info(f"Голосовое сообщение сохранено для пользователя {user_id}: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Ошибка при сохранении голосового сообщения для пользователя {user_id}: {str(e)}")
            return None
    
    @staticmethod
    def save_pdf(user_id, pdf_data, file_name="protocol.pdf"):
        """
        Сохраняет PDF-документ в директории сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            pdf_data (bytes): Данные PDF-документа.
            file_name (str): Имя файла для сохранения.
            
        Returns:
            str: Путь к сохраненному файлу или None в случае ошибки.
        """
        session_dir = os.path.join(Config.SESSION_BASE_DIR, f"user_id={user_id}")
        
        if not os.path.exists(session_dir):
            logger.warning(f"Директория сессии пользователя {user_id} не найдена")
            return None
        
        file_path = os.path.join(session_dir, file_name)
        
        try:
            with open(file_path, "wb") as f:
                f.write(pdf_data)
            
            logger.info(f"PDF-документ сохранен для пользователя {user_id}: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Ошибка при сохранении PDF-документа для пользователя {user_id}: {str(e)}")
            return None
