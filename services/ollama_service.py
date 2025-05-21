"""
Сервис для обработки текста через Ollama (LLaMA3).
"""
import logging
import aiohttp
import json
from config.config import Config

logger = logging.getLogger(__name__)

class OllamaService:
    """
    Класс для работы с Ollama API для обработки текста.
    """
    
    def __init__(self):
        """
        Инициализация сервиса Ollama.
        """
        self.model = Config.OLLAMA_MODEL
        self.api_url = Config.OLLAMA_API_URL
        logger.info(f"Инициализирован сервис Ollama с моделью {self.model}")
    
    async def format_text(self, text, format_type="questions"):
        """
        Форматирует текст с использованием Ollama.
        
        Args:
            text (str): Исходный текст для форматирования.
            format_type (str): Тип форматирования ("questions" или "decisions").
            
        Returns:
            str: Отформатированный текст в формате Markdown или None в случае ошибки.
        """
        try:
            # Подготавливаем промпт в зависимости от типа форматирования
            if format_type == "questions":
                prompt = (
                    f"Преобразуй следующий текст в нумерованный список вопросов в формате Markdown. "
                    f"Каждый вопрос должен начинаться с номера и точки. "
                    f"Исходный текст: \"{text}\""
                )
            else:  # decisions
                prompt = (
                    f"Преобразуй следующий текст в нумерованный список решений в формате Markdown. "
                    f"Каждое решение должно начинаться с номера и точки. "
                    f"Исходный текст: \"{text}\""
                )
            
            # Здесь будет код для вызова Ollama API
            # В реальном проекте здесь будет использоваться локальный Ollama через API
            
            # Для демонстрации используем имитацию форматирования
            logger.info(f"Имитация форматирования текста через Ollama: {text[:50]}...")
            
            # Имитация форматирования текста
            if format_type == "questions":
                # Пример форматирования вопросов
                formatted_text = self._format_questions_example(text)
            else:
                # Пример форматирования решений
                formatted_text = self._format_decisions_example(text)
            
            return formatted_text
            
        except Exception as e:
            logger.error(f"Ошибка при форматировании текста через Ollama: {str(e)}")
            return None
    
    def _format_questions_example(self, text):
        """
        Пример форматирования вопросов (для демонстрации).
        
        Args:
            text (str): Исходный текст.
            
        Returns:
            str: Отформатированный текст в формате Markdown.
        """
        # Простая логика для демонстрации
        # В реальном проекте здесь будет результат от Ollama
        
        # Разбиваем текст на части, ищем ключевые слова "вопрос" и номера
        parts = text.lower().replace(".", ". ").split()
        questions = []
        current_question = ""
        
        for i, word in enumerate(parts):
            if "вопрос" in word and i + 1 < len(parts):
                # Если нашли слово "вопрос" и текущий вопрос не пустой, сохраняем его
                if current_question:
                    questions.append(current_question.strip())
                current_question = ""
            elif current_question or (i > 0 and "вопрос" in parts[i-1]):
                current_question += word + " "
        
        # Добавляем последний вопрос, если он есть
        if current_question:
            questions.append(current_question.strip())
        
        # Форматируем вопросы в Markdown
        formatted_questions = ""
        for i, question in enumerate(questions, 1):
            formatted_questions += f"{i}. {question.capitalize()}\n"
        
        return formatted_questions
    
    def _format_decisions_example(self, text):
        """
        Пример форматирования решений (для демонстрации).
        
        Args:
            text (str): Исходный текст.
            
        Returns:
            str: Отформатированный текст в формате Markdown.
        """
        # Простая логика для демонстрации
        # В реальном проекте здесь будет результат от Ollama
        
        # Разбиваем текст на части, ищем ключевые слова "решение" и номера
        parts = text.lower().replace(".", ". ").split()
        decisions = []
        current_decision = ""
        
        for i, word in enumerate(parts):
            if "решение" in word and i + 1 < len(parts):
                # Если нашли слово "решение" и текущее решение не пустое, сохраняем его
                if current_decision:
                    decisions.append(current_decision.strip())
                current_decision = ""
            elif current_decision or (i > 0 and "решение" in parts[i-1]):
                current_decision += word + " "
        
        # Добавляем последнее решение, если оно есть
        if current_decision:
            decisions.append(current_decision.strip())
        
        # Если решений не найдено, разбиваем текст по точкам
        if not decisions:
            decisions = [s.strip() for s in text.split(".") if s.strip()]
        
        # Форматируем решения в Markdown
        formatted_decisions = ""
        for i, decision in enumerate(decisions, 1):
            formatted_decisions += f"{i}. {decision.capitalize()}\n"
        
        return formatted_decisions
