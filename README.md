# Foodgram - Платформа для обмена рецептами

## Адрес сервиса: 
- https://foodgram.vadim-polegaev-kittygram.ru/

## Описание проекта

Foodgram - это веб-платформа для обмена кулинарными рецептами, построенная на Django REST Framework. Пользователи могут создавать, просматривать, сохранять в избранное рецепты, подписываться на авторов и формировать список покупок.

## Основные возможности

### Пользователи
- Регистрация и аутентификация через email
- Профиль пользователя с аватаром
- Подписки на других авторов
- Просмотр списка подписчиков и подписок

### Рецепты
- Создание, редактирование и удаление рецептов
- Загрузка изображений в формате Base64
- Добавление ингредиентов с указанием количества
- Тегирование рецептов
- Указание времени приготовления

### Избранное
- Добавление рецептов в избранное
- Просмотр списка избранных рецептов

### Список покупок
- Добавление рецептов в список покупок
- Скачивание списка покупок в формате PDF
- Автоматический подсчет необходимых ингредиентов

### Ингредиенты и теги
- Предустановленная база ингредиентов
- Система тегов для категоризации рецептов
- Уникальные ограничения для предотвращения дублирования

## Технологический стек

### Backend
- **Python 3.13**
- **Django 5.2**
- **Django REST Framework 3.15.2**
- **Djoser 2.3.1**
- **PostgreSQL**
- **Pillow 11.2.1**
- **Poetry**

### Аутентификация
- Token-based аутентификация
- JWT токены (djangorestframework-simplejwt)
- Кастомизированная система регистрации

## Структура проекта

```
foodgram/
├── api/                    # API приложение
│   ├── recipes/           # API для рецептов
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users/             # API для пользователей
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── recipes/               # Приложение рецептов
│   ├── models.py         # Модели данных
│   ├── admin.py          # Админ-панель
│   ├── fields.py         # Кастомные поля
│   └── management/       # Команды управления
├── users/                # Приложение пользователей
│   ├── models.py         # Кастомная модель пользователя
│   └── admin.py          # Админ-панель
├── project_root/         # Основные настройки проекта
│   ├── settings.py       # Настройки Django
│   ├── urls.py           # Главные URL-маршруты
│   └── wsgi.py           # WSGI конфигурация
├── data/                 # Данные для импорта
│   ├── ingredients.json  # JSON с ингредиентами
│   └── ingredients.csv   # CSV с ингредиентами
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── requirements.txt      # Зависимости (альтернатива)
├── pyproject.toml        # Poetry конфигурация
├── Dockerfile           # Docker конфигурация
└── manage.py            # Django CLI
```

## Модели данных

### User (Пользователь)
- Расширенная модель пользователя Django
- Email как основное поле для входа
- Поддержка аватаров

### Recipe (Рецепт)
- Связь с автором (User)
- Название, описание, изображение
- Время приготовления
- Связи с ингредиентами и тегами

### Ingredient (Ингредиент)
- Название и единица измерения
- Уникальное ограничение на комбинацию полей

### Tag (Тег)
- Название, цвет (HEX), slug
- Используется для категоризации рецептов

### RecipeIngredient (Связь рецепт-ингредиент)
- Промежуточная модель для связи рецептов и ингредиентов
- Количество ингредиента в рецепте

### Favorite (Избранное)
- Связь пользователь-рецепт для избранного

### ShoppingCart (Список покупок)
- Связь пользователь-рецепт для списка покупок

### Subscription (Подписка)
- Связь между пользователями для подписок

## Установка и запуск

### Предварительные требования
- Python 3.13
- Poetry
- PostgreSQL

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd foodgram
```

### 2. Установка зависимостей
```bash
# Установка Poetry (если не установлен)
pip install poetry

# Установка зависимостей проекта
poetry install
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# База данных (для PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Для SQLite (по умолчанию)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

### 4. Применение миграций
```bash
poetry run python manage.py migrate
```

### 5. Создание суперпользователя
```bash
poetry run python manage.py createsuperuser
```

### 6. Импорт данных (опционально)
```bash
# Импорт ингредиентов из JSON
poetry run python manage.py load_ingredients data/ingredients.json

# Импорт ингредиентов из CSV
poetry run python manage.py load_ingredients data/ingredients.csv
```

### 7. Запуск сервера
```bash
poetry run python manage.py runserver
```

## API Эндпоинты

### Аутентификация
- `POST /api/users/` - Регистрация пользователя
- `POST /api/auth/token/login/` - Получение токена
- `POST /api/auth/token/logout/` - Выход

### Пользователи
- `GET /api/users/` - Список пользователей
- `GET /api/users/{id}/` - Профиль пользователя
- `GET /api/users/me/` - Текущий пользователь
- `PATCH /api/users/me/` - Обновление профиля

### Подписки
- `GET /api/users/subscriptions/` - Мои подписки
- `POST /api/users/{id}/subscribe/` - Подписаться на пользователя
- `DELETE /api/users/{id}/subscribe/` - Отписаться от пользователя

### Рецепты
- `GET /api/recipes/` - Список рецептов
- `POST /api/recipes/` - Создание рецепта
- `GET /api/recipes/{id}/` - Детали рецепта
- `PATCH /api/recipes/{id}/` - Обновление рецепта
- `DELETE /api/recipes/{id}/` - Удаление рецепта

### Избранное
- `GET /api/recipes/favorite/` - Мои избранные рецепты
- `POST /api/recipes/{id}/favorite/` - Добавить в избранное
- `DELETE /api/recipes/{id}/favorite/` - Удалить из избранного

### Список покупок
- `GET /api/recipes/download_shopping_cart/` - Скачать список покупок
- `POST /api/recipes/{id}/shopping_cart/` - Добавить в список покупок
- `DELETE /api/recipes/{id}/shopping_cart/` - Удалить из списка покупок

### Ингредиенты и теги
- `GET /api/ingredients/` - Список ингредиентов
- `GET /api/tags/` - Список тегов

## Docker

### Сборка и запуск с Docker
```bash
# Сборка образа
docker build -t foodgram .

# Запуск контейнера
docker run -p 8000:8000 foodgram
```

## Команды управления

### Импорт данных
```bash
# Импорт ингредиентов
poetry run python manage.py load_ingredients <file_path>

# Создание тегов
poetry run python manage.py create_tags
```

## Лицензия
Проект разработан в образовательных целях.

## Автор
*Полегаев Вадим*