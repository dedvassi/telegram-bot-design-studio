"""
Утилита для генерации PDF-документов.
"""
import os
import logging
from fpdf import FPDF
from config.config import Config

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Класс для генерации PDF-документов.
    """
    
    def __init__(self):
        """
        Инициализация генератора PDF.
        """
        self.primary_color = Config.PDF_PRIMARY_COLOR
        self.secondary_color = Config.PDF_SECONDARY_COLOR
        self.logo_path = Config.PDF_LOGO_PATH
        
        logger.info("Инициализирован генератор PDF")
    
    def generate_protocol_pdf(self, metadata, questions, decisions, output_path):
        """
        Генерирует PDF-документ протокола встречи.
        
        Args:
            metadata (dict): Метаданные протокола.
            questions (str): Список вопросов в формате Markdown.
            decisions (str): Список решений в формате Markdown.
            output_path (str): Путь для сохранения PDF-документа.
            
        Returns:
            bool: True, если PDF успешно сгенерирован, иначе False.
        """
        try:
            # Создаем PDF-документ
            pdf = FPDF()
            
            # Добавляем шрифт с поддержкой кириллицы
            pdf.add_font("DejaVu", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=10)
            
            # Добавляем страницу
            pdf.add_page()
            
            # Генерируем заголовок и шапку
            self._add_header(pdf, metadata)
            
            # Добавляем блок вопросов
            self._add_questions_section(pdf, questions)
            
            # Добавляем блок решений
            self._add_decisions_section(pdf, decisions)
            
            # Добавляем подпись
            self._add_signature(pdf, metadata)
            
            # Сохраняем PDF
            pdf.output(output_path)
            
            logger.info(f"PDF-документ успешно сгенерирован: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при генерации PDF: {str(e)}")
            return False
    
    def _add_header(self, pdf, metadata):
        """
        Добавляет заголовок и шапку в PDF-документ.
        
        Args:
            pdf: Объект FPDF.
            metadata (dict): Метаданные протокола.
        """
        # Устанавливаем цвет для заголовка
        pdf.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        
        # Добавляем логотип, если он существует
        if os.path.exists(self.logo_path):
            pdf.image(self.logo_path, x=10, y=10, w=30)
            pdf.ln(35)
        else:
            pdf.ln(10)
        
        # Добавляем заголовок
        pdf.set_font("DejaVu", size=16)
        pdf.cell(0, 10, "ПРОТОКОЛ ВСТРЕЧИ", ln=True, align="C")
        
        # Добавляем название протокола
        pdf.set_font("DejaVu", size=14)
        pdf.cell(0, 10, metadata.get("protocol_name", ""), ln=True, align="C")
        
        # Добавляем метаданные
        pdf.set_font("DejaVu", size=10)
        pdf.set_text_color(self.secondary_color[0], self.secondary_color[1], self.secondary_color[2])
        
        pdf.ln(5)
        pdf.cell(40, 8, "Дата:", ln=0)
        pdf.cell(0, 8, metadata.get("date", ""), ln=1)
        
        pdf.cell(40, 8, "Номер проекта:", ln=0)
        pdf.cell(0, 8, metadata.get("project_number", ""), ln=1)
        
        pdf.cell(40, 8, "Год договора:", ln=0)
        pdf.cell(0, 8, metadata.get("contract_year", ""), ln=1)
        
        pdf.cell(40, 8, "Тип проекта:", ln=0)
        pdf.cell(0, 8, metadata.get("project_type", ""), ln=1)
        
        pdf.cell(40, 8, "Название объекта:", ln=0)
        pdf.cell(0, 8, metadata.get("object_name", ""), ln=1)
        
        pdf.cell(40, 8, "Заказчик:", ln=0)
        pdf.cell(0, 8, metadata.get("client_name", ""), ln=1)
        
        pdf.ln(10)
    
    def _add_questions_section(self, pdf, questions):
        """
        Добавляет блок вопросов в PDF-документ.
        
        Args:
            pdf: Объект FPDF.
            questions (str): Список вопросов в формате Markdown.
        """
        # Устанавливаем цвет для заголовка раздела
        pdf.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        
        # Добавляем заголовок раздела
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, "КЛЮЧЕВЫЕ ВОПРОСЫ", ln=True)
        
        # Устанавливаем цвет для текста
        pdf.set_text_color(0, 0, 0)
        
        # Добавляем список вопросов
        pdf.set_font("DejaVu", size=10)
        
        # Разбиваем текст на строки
        lines = questions.strip().split("\n")
        
        for line in lines:
            pdf.multi_cell(0, 8, line)
        
        pdf.ln(10)
    
    def _add_decisions_section(self, pdf, decisions):
        """
        Добавляет блок решений в PDF-документ.
        
        Args:
            pdf: Объект FPDF.
            decisions (str): Список решений в формате Markdown.
        """
        # Устанавливаем цвет для заголовка раздела
        pdf.set_text_color(self.primary_color[0], self.primary_color[1], self.primary_color[2])
        
        # Добавляем заголовок раздела
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, "ПРИНЯТЫЕ РЕШЕНИЯ", ln=True)
        
        # Устанавливаем цвет для текста
        pdf.set_text_color(0, 0, 0)
        
        # Добавляем список решений
        pdf.set_font("DejaVu", size=10)
        
        # Разбиваем текст на строки
        lines = decisions.strip().split("\n")
        
        for line in lines:
            pdf.multi_cell(0, 8, line)
        
        pdf.ln(10)
    
    def _add_signature(self, pdf, metadata):
        """
        Добавляет блок подписи в PDF-документ.
        
        Args:
            pdf: Объект FPDF.
            metadata (dict): Метаданные протокола.
        """
        # Устанавливаем цвет для текста
        pdf.set_text_color(0, 0, 0)
        
        # Добавляем линию для подписи
        pdf.line(20, pdf.get_y(), 80, pdf.get_y())
        pdf.line(120, pdf.get_y(), 180, pdf.get_y())
        
        # Добавляем подписи
        pdf.set_font("DejaVu", size=8)
        pdf.cell(80, 5, "Подпись представителя студии", ln=0, align="C")
        pdf.cell(40, 5, "", ln=0)
        pdf.cell(80, 5, f"Подпись заказчика ({metadata.get('client_name', '')})", ln=1, align="C")
