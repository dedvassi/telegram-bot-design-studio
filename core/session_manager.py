"""
Модуль управления сессиями пользователей Telegram-бота.
Создает и управляет сессиями, хранит временные данные и файлы.
"""
import os
import shutil
import logging
import json
from config.config import Config

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Класс для управления сессиями пользователей Telegram-бота.
    """
    
    def __init__(self):
        """
        Инициализация менеджера сессий.
        Создает базовую директорию для сессий, если она не существует.
        """
        os.makedirs(Config.SESSION_BASE_DIR, exist_ok=True)
    
    def create_session(self, user_id):
        """
        Создает новую сессию для пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            str: Путь к директории сессии.
        """
        session_dir = os.path.join(Config.SESSION_BASE_DIR, f"user_id={user_id}")
        
        # Если сессия уже существует, удаляем ее
        if os.path.exists(session_dir):
            self.delete_session(user_id)
        
        # Создаем директорию для новой сессии
        os.makedirs(session_dir, exist_ok=True)
        
        # Инициализируем данные сессии
        session_data = {
            "user_id": user_id,
            "metadata": {},
            "state": "init"
        }
        
        # Сохраняем данные сессии
        self._save_session_data(user_id, session_data)
        
        logger.info(f"Создана новая сессия для пользователя {user_id}")
        
        return session_dir
    
    def get_session_dir(self, user_id):
        """
        Возвращает путь к директории сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            str: Путь к директории сессии или None, если сессия не существует.
        """
        session_dir = os.path.join(Config.SESSION_BASE_DIR, f"user_id={user_id}")
        
        if not os.path.exists(session_dir):
            logger.warning(f"Сессия для пользователя {user_id} не найдена")
            return None
        
        return session_dir
    
    def delete_session(self, user_id):
        """
        Удаляет сессию пользователя и все связанные файлы.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            bool: True, если сессия успешно удалена, иначе False.
        """
        session_dir = self.get_session_dir(user_id)
        
        if not session_dir:
            return False
        
        try:
            shutil.rmtree(session_dir)
            logger.info(f"Сессия пользователя {user_id} удалена")
            return True
        except Exception as e:
            logger.error(f"Ошибка при удалении сессии пользователя {user_id}: {str(e)}")
            return False
    
    def get_session_data(self, user_id):
        """
        Получает данные сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            dict: Данные сессии или пустой словарь, если сессия не существует.
        """
        session_dir = self.get_session_dir(user_id)
        
        if not session_dir:
            return {}
        
        session_file = os.path.join(session_dir, "session.json")
        
        if not os.path.exists(session_file):
            logger.warning(f"Файл данных сессии для пользователя {user_id} не найден")
            return {}
        
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка при чтении данных сессии пользователя {user_id}: {str(e)}")
            return {}
    
    def update_session_data(self, user_id, data_update):
        """
        Обновляет данные сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            data_update (dict): Словарь с обновлениями данных сессии.
            
        Returns:
            bool: True, если данные успешно обновлены, иначе False.
        """
        session_data = self.get_session_data(user_id)
        
        if not session_data:
            logger.warning(f"Невозможно обновить данные: сессия для пользователя {user_id} не найдена")
            return False
        
        # Обновляем данные сессии
        for key, value in data_update.items():
            if key == "metadata" and isinstance(value, dict) and "metadata" in session_data:
                # Для метаданных обновляем только указанные поля
                session_data["metadata"].update(value)
            else:
                # Для остальных полей заменяем значение полностью
                session_data[key] = value
        
        # Сохраняем обновленные данные
        return self._save_session_data(user_id, session_data)
    
    def update_session_state(self, user_id, state):
        """
        Обновляет состояние сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            state (str): Новое состояние сессии.
            
        Returns:
            bool: True, если состояние успешно обновлено, иначе False.
        """
        return self.update_session_data(user_id, {"state": state})
    
    def get_session_state(self, user_id):
        """
        Получает текущее состояние сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            
        Returns:
            str: Текущее состояние сессии или None, если сессия не существует.
        """
        session_data = self.get_session_data(user_id)
        
        if not session_data:
            return None
        
        return session_data.get("state")
    
    def save_file(self, user_id, file_data, file_name):
        """
        Сохраняет файл в директории сессии пользователя.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            file_data (bytes): Данные файла.
            file_name (str): Имя файла.
            
        Returns:
            str: Путь к сохраненному файлу или None, если сессия не существует.
        """
        session_dir = self.get_session_dir(user_id)
        
        if not session_dir:
            logger.warning(f"Невозможно сохранить файл: сессия для пользователя {user_id} не найдена")
            return None
        
        file_path = os.path.join(session_dir, file_name)
        
        try:
            with open(file_path, "wb") as f:
                f.write(file_data)
            
            logger.info(f"Файл {file_name} сохранен для пользователя {user_id}")
            return file_path
        except Exception as e:
            logger.error(f"Ошибка при сохранении файла {file_name} для пользователя {user_id}: {str(e)}")
            return None
    
    def _save_session_data(self, user_id, session_data):
        """
        Сохраняет данные сессии в файл.
        
        Args:
            user_id (int): Идентификатор пользователя Telegram.
            session_data (dict): Данные сессии.
            
        Returns:
            bool: True, если данные успешно сохранены, иначе False.
        """
        session_dir = self.get_session_dir(user_id)
        
        if not session_dir:
            logger.warning(f"Невозможно сохранить данные: сессия для пользователя {user_id} не найдена")
            return False
        
        session_file = os.path.join(session_dir, "session.json")
        
        try:
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных сессии пользователя {user_id}: {str(e)}")
            return False
