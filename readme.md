# TeamFinder

Платформа для поиска команды и совместной работы над проектами. Пользователи могут создавать проекты, указывать необходимые навыки, находить единомышленников и присоединяться к существующим проектам.

## Функциональность

### Для пользователей
- Регистрация и аутентификация
- Редактирование профиля с указанием навыков (добавление/удаление)
- Автоматическая генерация аватаров при регистрации
- Просмотр списка всех пользователей с фильтрацией по навыкам
- Поиск навыков через автодополнение

### Для проектов
- Создание и редактирование проектов
- Просмотр списка всех проектов с пагинацией
- Детальная информация о проекте
- Присоединение к проектам и выход из них
- Завершение проектов автором
- Указание ссылки на GitHub репозиторий

## Стек технологий

- **Python 3**
- **Django** — веб-фреймворк
- **PostgreSQL** — база данных
- **Docker** — контейнеризация
- **Pillow** — обработка изображений (генерация аватаров)
- **python-decouple** — управление переменными окружения

## Развертывание проекта

### 1. Клонирование репозитория

git clone https://github.com/your-username/teamfinder.git
cd teamfinder

### 2. Виртуальное окружение

Создайте и активируйте виртуальное окружение:

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

Windows (PowerShell):
python -m venv venv
venv\Scripts\Activate.ps1

Windows (cmd):
python -m venv venv
venv\Scripts\activate

Установите зависимости:
pip install -r requirements.txt

### 3. Переменные окружения

Создайте файл .env в корне проекта:
cp .env_example .env

Заполните .env своими значениями:

DJANGO_SECRET_KEY - Секретный ключ Django. Можно сгенерировать: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DJANGO_DEBUG - Режим отладки (True или False)
DJANGO_ALLOWED_HOSTS - Разрешённые хосты через запятую (localhost,127.0.0.1)
POSTGRES_DB - Имя базы данных
POSTGRES_USER - Пользователь базы данных
POSTGRES_PASSWORD - Пароль базы данных
POSTGRES_HOST - Хост базы данных (localhost)
POSTGRES_PORT - Порт базы данных (5432)

### 4. Запуск PostgreSQL в Docker

docker compose up -d

Остановка:
docker compose down

### 5. Миграции и запуск сервера

python manage.py migrate
python manage.py runserver

Проект доступен по адресу http://localhost:8000

## Структура проекта

teamfinder/
├── constants/          # Константы и валидаторы
├── projects/           # Приложение проектов
├── static/             # Статические файлы (CSS, JS, шрифты)
├── team_finder/        # Основные настройки Django
├── templates/          # HTML-шаблоны
├── users/              # Приложение пользователей
├── .env_example        # Пример файла с переменными окружения
├── docker-compose.yml  # Конфигурация Docker
├── manage.py           # Управление Django
├── README.md           # Документация
└── requirements.txt    # Зависимости проекта

## Автор

- Имя Фамилия
- GitHub: https://github.com/your-username
- Email: your-email@example.com
