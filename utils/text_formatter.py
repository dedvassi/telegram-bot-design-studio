"""
Утилита для форматирования текста.
"""
import logging
import re

logger = logging.getLogger(__name__)

class TextFormatter:
    """
    Класс для форматирования текста.
    """
    
    @staticmethod
    def format_questions_to_markdown(text):
        """
        Форматирует текст с вопросами в Markdown.
        
        Args:
            text (str): Исходный текст с вопросами.
            
        Returns:
            str: Отформатированный текст в формате Markdown.
        """
        try:
            # Разбиваем текст на предложения
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
            # Ищем вопросы по ключевым словам
            questions = []
            for sentence in sentences:
                # Проверяем, содержит ли предложение ключевые слова "вопрос" или цифры с точкой
                if re.search(r'вопрос|вопроса|вопросы|\d+\.', sentence.lower()):
                    # Удаляем слова "вопрос первый", "вопрос 1" и т.д.
                    cleaned = re.sub(r'вопрос\s+(?:первый|второй|третий|четвертый|пятый|\d+)\.?\s*', '', sentence, flags=re.IGNORECASE)
                    questions.append(cleaned.strip())
                elif sentence.strip():
                    # Если предложение не пустое и не содержит ключевых слов, добавляем его как есть
                    questions.append(sentence.strip())
            
            # Форматируем вопросы в Markdown
            markdown_text = ""
            for i, question in enumerate(questions, 1):
                markdown_text += f"{i}. {question}\n"
            
            return markdown_text
            
        except Exception as e:
            logger.error(f"Ошибка при форматировании вопросов: {str(e)}")
            return text
    
    @staticmethod
    def format_decisions_to_markdown(text):
        """
        Форматирует текст с решениями в Markdown.
        
        Args:
            text (str): Исходный текст с решениями.
            
        Returns:
            str: Отформатированный текст в формате Markdown.
        """
        try:
            # Разбиваем текст на предложения
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
            # Ищем решения по ключевым словам
            decisions = []
            for sentence in sentences:
                # Проверяем, содержит ли предложение ключевые слова "решение" или цифры с точкой
                if re.search(r'решение|решения|\d+\.', sentence.lower()):
                    # Удаляем слова "решение первое", "решение 1" и т.д.
                    cleaned = re.sub(r'решение\s+(?:первое|второе|третье|четвертое|пятое|\d+)\.?\s*', '', sentence, flags=re.IGNORECASE)
                    decisions.append(cleaned.strip())
                elif sentence.strip():
                    # Если предложение не пустое и не содержит ключевых слов, добавляем его как есть
                    decisions.append(sentence.strip())
            
            # Форматируем решения в Markdown
            markdown_text = ""
            for i, decision in enumerate(decisions, 1):
                markdown_text += f"{i}. {decision}\n"
            
            return markdown_text
            
        except Exception as e:
            logger.error(f"Ошибка при форматировании решений: {str(e)}")
            return text
