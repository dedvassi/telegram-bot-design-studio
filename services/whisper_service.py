"""
Сервис для распознавания речи через Whisper.
"""
import os
import logging
import aiohttp
import json
import asyncio
import tempfile
from config.config import Config

logger = logging.getLogger(__name__)

class WhisperService:
    """
    Класс для работы с Whisper API для распознавания речи.
    """
    
    def __init__(self):
        """
        Инициализация сервиса Whisper.
        """
        self.model = Config.WHISPER_MODEL
        logger.info(f"Инициализирован сервис Whisper с моделью {self.model}")
    
    async def transcribe_audio(self, audio_file_path):
        """
        Распознает речь из аудиофайла.
        
        Args:
            audio_file_path (str): Путь к аудиофайлу.
            
        Returns:
            str: Распознанный текст или None в случае ошибки.
        """
        try:
            # Проверяем существование файла
            if not os.path.exists(audio_file_path):
                logger.error(f"Аудиофайл не найден: {audio_file_path}")
                return None
            
            # Здесь будет код для вызова Whisper API
            # В реальном проекте здесь будет использоваться локальный Whisper через CLI или API
            
            # Для демонстрации используем имитацию распознавания
            logger.info(f"Имитация распознавания речи из файла: {audio_file_path}")
            
            # Имитация задержки распознавания
            await asyncio.sleep(2)
            
            # Возвращаем пример распознанного текста
            # В реальном проекте здесь будет результат распознавания Whisper
            return "Вопрос первый. 3D-визуализация спальни. Вопрос второй. Подбор мебели в детскую."
            
        except Exception as e:
            logger.error(f"Ошибка при распознавании речи: {str(e)}")
            return None
    
    async def transcribe_voice_message(self, voice_file_data):
        """
        Распознает речь из голосового сообщения Telegram.
        
        Args:
            voice_file_data (bytes): Данные голосового сообщения.
            
        Returns:
            str: Распознанный текст или None в случае ошибки.
        """
        try:
            # Сохраняем голосовое сообщение во временный файл
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                temp_file.write(voice_file_data)
                temp_file_path = temp_file.name
            
            # Распознаем речь из файла
            transcription = await self.transcribe_audio(temp_file_path)
            
            # Удаляем временный файл
            os.unlink(temp_file_path)
            
            return transcription
            
        except Exception as e:
            logger.error(f"Ошибка при распознавании голосового сообщения: {str(e)}")
            return None
