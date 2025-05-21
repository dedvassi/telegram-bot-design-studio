# Telegram-бот для дизайн-студии

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

Telegram-бот для автоматизации бизнес-процессов дизайн-студии. Основная функция — протоколирование встреч с заказчиками, включая запись ключевых вопросов и решений через голосовые сообщения с последующей генерацией PDF-документа.

## 📋 Содержание

- [Функциональность](#-функциональность)
- [Требования](#-требования)
- [Установка](#-установка)
- [Настройка](#-настройка)
- [Запуск](#-запуск)
- [Использование](#-использование)
- [Архитектура](#-архитектура)
- [Разработка](#-разработка)
- [FAQ](#-faq)

## 🚀 Функциональность

### Сценарий "Протокол встречи"

1. **Сбор метаданных**:
   - Название протокола
   - Дата встречи
   - Номер проекта
   - Год договора
   - Тип проекта
   - Название ЖК/объекта
   - Имя заказчика

2. **Запись ключевых вопросов**:
   - Отправка голосового сообщения
   - Распознавание речи через Whisper
   - Форматирование текста через LLaMA3 (Ollama)
   - Подтверждение результатов

3. **Запись принятых решений**:
   - Аналогичная процедура с голосовым сообщением
   - Распознавание и форматирование

4. **Генерация PDF-документа**:
   - Брендированный PDF с логотипом компании
   - Структурированное представление метаданных, вопросов и решений

## 📦 Требования

### Системные требования

- Python 3.10 или выше
- ffmpeg (необходим для обработки аудио и работы с Whisper)
- Доступ к API Telegram

### Зависимости Python

- pyTelegramBotAPI==4.14.0
- python-dotenv==1.0.0
- fpdf2==2.7.6
- requests==2.31.0
- aiohttp==3.9.1

### Внешние сервисы

- **Whisper** - для распознавания речи
- **Ollama с моделью LLaMA3** - для обработки и форматирования текста

## 💻 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/dedvassi/telegram-bot-design-studio.git
cd telegram-bot-design-studio
```

### 2. Установка ffmpeg

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS (с Homebrew)
```bash
brew install ffmpeg
```

#### Windows
Скачайте и установите ffmpeg с официального сайта: https://ffmpeg.org/download.html
Или используйте Chocolatey:
```bash
choco install ffmpeg
```

### 3. Установка Ollama и модели LLaMA3

1. Установите Ollama с официального сайта: https://ollama.ai/download
2. Загрузите модель LLaMA3:
```bash
ollama pull llama3
```

### 4. Установка зависимостей Python

```bash
pip install -r requirements.txt
```

## ⚙️ Настройка

### 1. Создание бота в Telegram

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните полученный токен

### 2. Настройка конфигурации

1. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

2. Отредактируйте файл `.env`:
```
# Токен Telegram-бота
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Список разрешенных пользователей (ID через запятую)
ALLOWED_USERS=123456789,987654321

# Настройки Whisper
WHISPER_MODEL=base
WHISPER_LANGUAGE=ru

# Настройки Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# Настройки PDF
COMPANY_NAME=Ваша Дизайн-Студия
COMPANY_LOGO_PATH=/path/to/logo.png
```

## 🚀 Запуск

### Запуск бота

```bash
python main.py
```

### Запуск в фоновом режиме (Linux/macOS)

```bash
nohup python main.py > bot.log 2>&1 &
```

### Запуск как службу (Linux с systemd)

1. Создайте файл службы:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

2. Добавьте следующее содержимое (замените пути на свои):
```
[Unit]
Description=Telegram Bot for Design Studio
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/telegram-bot-design-studio
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Включите и запустите службу:
```bash
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
```

## 📱 Использование

### Команды бота

- `/start` - Начало работы с ботом
- `/help` - Показать справку
- `/protocol` - Запуск сценария протоколирования встречи

### Сценарий "Протокол встречи"

1. Отправьте команду `/protocol`
2. Последовательно введите запрашиваемые метаданные
3. Отправьте голосовое сообщение с ключевыми вопросами
4. Подтвердите результат распознавания
5. Отправьте голосовое сообщение с принятыми решениями
6. Подтвердите результат распознавания
7. Получите готовый PDF-документ

## 🏗️ Архитектура

Проект имеет модульную структуру:

```
telegram_bot_project/
├── .env                      # Конфигурационный файл
├── main.py                   # Точка входа в приложение
├── requirements.txt          # Зависимости проекта
├── README.md                 # Документация
├── config/                   # Конфигурационные файлы
├── core/                     # Ядро бота
├── handlers/                 # Обработчики команд
├── services/                 # Сервисы для работы с внешними API
├── utils/                    # Вспомогательные утилиты
└── templates/                # Шаблоны для PDF
```

Подробное описание архитектуры доступно в файле [architecture.md](architecture.md).

## 🛠️ Разработка

### Тестирование

```bash
python test_bot.py
```

### Добавление новых функций

1. Создайте новый обработчик в директории `handlers/`
2. Зарегистрируйте обработчик в `core/bot.py`
3. При необходимости добавьте новые сервисы в `services/`

## ❓ FAQ

### Как добавить нового пользователя в white list?

Добавьте ID пользователя в переменную `ALLOWED_USERS` в файле `.env`.

### Как узнать ID пользователя Telegram?

Отправьте сообщение боту @userinfobot в Telegram.

### Как изменить логотип в PDF?

Замените путь к логотипу в переменной `COMPANY_LOGO_PATH` в файле `.env`.

### Что делать, если распознавание речи работает некорректно?

1. Убедитесь, что ffmpeg установлен и доступен в системе
2. Проверьте настройки Whisper в файле `.env`
3. Попробуйте использовать более качественную модель Whisper (medium или large)

### Как изменить формат PDF?

Отредактируйте класс `PDFGenerator` в файле `utils/pdf_generator.py`.

## 📄 Лицензия

MIT License

## 👨‍💻 Авторы

- [dedvassi](https://github.com/dedvassi) - Основной разработчик

## 🙏 Благодарности

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - За отличную библиотеку для работы с Telegram API
- [Whisper](https://github.com/openai/whisper) - За мощный инструмент распознавания речи
- [Ollama](https://ollama.ai/) - За возможность локального запуска LLM
- [FPDF2](https://github.com/py-pdf/fpdf2) - За простую генерацию PDF
