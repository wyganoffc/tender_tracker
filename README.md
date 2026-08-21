# Tender Tracker API

> Микросервис для трекинга статусов тендеров с историей изменений

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 О проекте

**Tender Tracker API** — это бэкенд-сервис для управления тендерами и отслеживания их статусов. Разработан в рамках тестового задания для компании **Crown** (Задание №6: Микросервис трекинга статуса тендеров).

### 🎯 Функциональность

- ✅ Создание тендера со статусом `Черновик`
- ✅ Получение тендера по ID
- ✅ Обновление статуса тендера с валидацией переходов
- ✅ Получение истории изменений статуса
- ✅ Статус-машина с разрешёнными переходами
- ✅ Автоматическое логирование всех изменений

## 🚀 Статус-машина (Логика переходов)

### Статусы тендера:

- `draft` (Черновик) — начальный статус
- `active` (Активен) — тендер опубликован
- `won` (Выигран) — победа в тендере
- `lost` (Проигран) — проигрыш в тендере
- `cancelled` (Отменён) — тендер отменён

### Разрешённые переходы:


draft → active, cancelled
active → won, lost, cancelled
won → (финальный статус)
lost → (финальный статус)
cancelled → (финальный статус)

### Примеры валидных переходов:

- ✅ `draft` → `active`
- ✅ `active` → `won`
- ✅ `draft` → `cancelled`

### Примеры невалидных переходов:

- ❌ `draft` → `won` (нельзя пропустить `active`)
- ❌ `won` → `active` (финальный статус нельзя менять)
- ❌ `lost` → `won` (финальный статус нельзя менять)

## 🛠️ Технологический стек

| Компонент | Технология | Версия |
|-----------|------------|--------|
| **Язык** | Python | 3.11 |
| **Web-фреймворк** | FastAPI | 0.104 |
| **ORM** | SQLAlchemy | 2.0 |
| **База данных** | PostgreSQL | 15 |
| **Миграции** | Alembic | 1.12 |
| **Тестирование** | Pytest | 7.4 |
| **Контейнеризация** | Docker | 24.0 |
| **Оркестрация** | Docker Compose | 3.8 |
| **Линтер** | Flake8 / Black | — |
| **CI/CD** | GitHub Actions | — |

---

## 📁 Архитектура проекта

### Слои приложения
```text

┌─────────────────────────────────────────────────────────────┐
│                      HTTP Layer (FastAPI)                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  routers.py         (API эндпоинты)                 │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  schemas.py          (Pydantic валидация)           │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  crud.py            (CRUD операции)                 │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  status_machine.py  (Бизнес-логика статусов)        │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  models.py          (SQLAlchemy модели)             │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  PostgreSQL         (База данных)                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```
### Структура базы данных

```text
Таблица: tenders
├── id (UUID, PRIMARY KEY)
├── title (VARCHAR(255), NOT NULL)
├── description (TEXT, NOT NULL)
├── status (ENUM: draft, active, won, lost, cancelled)
├── created_by (UUID, NOT NULL)
├── created_at (TIMESTAMP WITH TIME ZONE)
└── updated_at (TIMESTAMP WITH TIME ZONE)

Таблица: status_history
├── id (UUID, PRIMARY KEY)
├── tender_id (UUID, FOREIGN KEY → tenders.id ON DELETE CASCADE)
├── old_status (VARCHAR(50), NOT NULL)
├── new_status (VARCHAR(50), NOT NULL)
├── changed_by (UUID, NOT NULL)
├── reason (TEXT, NOT NULL)
└── changed_at (TIMESTAMP WITH TIME ZONE)
```
## 📂 Структура проекта
```text
tender-tracker/
├── app/                          # Основной код приложения
│   ├── __init__.py
│   ├── main.py                  # Точка входа
│   ├── config.py                # Конфигурация (загрузка .env)
│   ├── database.py              # Подключение к PostgreSQL
│   ├── models.py                # SQLAlchemy модели
│   ├── schemas.py               # Pydantic схемы
│   ├── status_machine.py        # Логика переходов статусов
│   ├── crud.py                  # CRUD операции
│   └── routers.py               # API эндпоинты
│
├── tests/                        # Тесты
│   ├── __init__.py
│   ├── conftest.py              # Фикстуры для тестов
│   └── test_api.py              # Тесты API (9 тестов)
│
├── migrations/                   # Миграции Alembic
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── .github/workflows/            # CI/CD
│   └── ci.yml                   # GitHub Actions
│
├── results/                      # Результаты запусков
│   ├── pytest_output.txt
│   ├── coverage_report/
│   └── api_responses/
│
├── docker-compose.yml            # Оркестрация контейнеров
├── Dockerfile                    # Сборка образа
├── requirements.txt              # Зависимости
├── .env.example                  # Пример переменных окружения
├── .gitignore                    # Исключения Git
├── README.md                     # Документация
├── LICENSE                       # Лицензия MIT
└── alembic.ini                   # Настройки Alembic
```
## 🚀 Быстрый старт

### Предварительные требования

- **Docker** 24.0+ и **Docker Compose** 3.8+
- **Python** 3.11+ (для локального запуска)
- **PostgreSQL** 15+ (для локального запуска)

### Запуск через Docker (рекомендуется)
```text
# 1. Клонировать репозиторий
git clone https://github.com/wyganoffc/tender_tracker.git
cd tender-tracker

# 2. Создать .env файл
cp .env.example .env

# 3. Запустить через Docker Compose
docker-compose up -d --build

# 4. Применить миграции
docker-compose exec app alembic upgrade head

# 5. Проверить работу
curl http://localhost:8000/
# Ответ: {"message":"Tender Tracker API","docs":"/docs","redoc":"/redoc"}

# 6. Открыть документацию в браузере
# http://localhost:8000/docs
```
### Локальный запуск (без Docker)
```text
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Настроить .env
cp .env.example .env
# Отредактировать DATABASE_URL

# 3. Создать БД и применить миграции
createdb tenders
alembic upgrade head

# 4. Запустить приложение
python -m app.main
# или
uvicorn app.routers:app --reload

# 5. Открыть Swagger
# http://localhost:8000/docs
```

## 📡 API Эндпоинты

| Метод | Эндпоинт | Описание | Статус |
|-------|----------|----------|--------|
| `POST` | `/tenders` | Создать тендер | 201 Created |
| `GET` | `/tenders/{id}` | Получить тендер | 200 OK |
| `PATCH` | `/tenders/{id}/status` | Обновить статус | 200 OK |
| `GET` | `/tenders/{id}/history` | Получить историю | 200 OK |
| `GET` | `/` | Корневой эндпоинт | 200 OK |
| `GET` | `/docs` | Swagger UI | — |
| `GET` | `/redoc` | ReDoc | — |


## 📝 Примеры запросов

### 1. Создание тендера
```bash
curl -X POST http://localhost:8000/tenders \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Разработка CRM для госорганов",
    "description": "Веб-приложение на Python с интеграцией ЕСИА",
    "created_by": "550e8400-e29b-41d4-a716-446655440000"
  }'
  ```
Ответ:

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Разработка CRM для госорганов",
  "description": "Веб-приложение на Python с интеграцией ЕСИА",
  "status": "draft",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```
2. Получение тендера
```bash
curl http://localhost:8000/tenders/123e4567-e89b-12d3-a456-426614174000
```
Ответ (200 OK):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Разработка CRM для госорганов",
  "description": "Веб-приложение на Python с интеграцией ЕСИА",
  "status": "draft",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```
### 3. Обновление статуса
```bash
curl -X PATCH http://localhost:8000/tenders/123e4567-e89b-12d3-a456-426614174000/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active",
    "reason": "Проект согласован с заказчиком",
    "changed_by": "550e8400-e29b-41d4-a716-446655440000"
  }'
  ```
Ответ (200 OK):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Разработка CRM для госорганов",
  "description": "Веб-приложение на Python с интеграцией ЕСИА",
  "status": "active",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```
4. Получение истории
```bash
curl http://localhost:8000/tenders/123e4567-e89b-12d3-a456-426614174000/history
```
Ответ (200 OK):

```json
[
  {
    "id": "789e4567-e89b-12d3-a456-426614174000",
    "tender_id": "123e4567-e89b-12d3-a456-426614174000",
    "old_status": "draft",
    "new_status": "active",
    "changed_by": "550e8400-e29b-41d4-a716-446655440000",
    "reason": "Проект согласован с заказчиком",
    "changed_at": "2024-01-15T10:35:00Z"
  }
]
```

## 🧪 Тестирование
```text
# Запустить все тесты
pytest tests/ -v

# Запустить с покрытием
pytest tests/ --cov=app --cov-report=html

# Запустить конкретный тест
pytest tests/test_api.py::test_create_tender -v
Результат:

============================= test session starts ==============================
collected 9 items

test_api.py::test_create_tender PASSED                                 [ 11%]
test_api.py::test_get_tender PASSED                                   [ 22%]
test_api.py::test_get_tender_not_found PASSED                         [ 33%]
test_api.py::test_update_status_draft_to_active PASSED                [ 44%]
test_api.py::test_update_status_active_to_won PASSED                  [ 55%]
test_api.py::test_update_status_invalid_transition PASSED             [ 66%]
test_api.py::test_get_history PASSED                                  [ 77%]
test_api.py::test_get_history_tender_not_found PASSED                 [ 88%]
test_api.py::test_update_status_tender_not_found PASSED               [100%]

============================== 9 passed in 2.34s ===============================
Покрытие тестов
Модуль	Покрытие
app/routers.py	100%
app/crud.py	95%
app/status_machine.py	100%
app/schemas.py	100%
app/models.py	90%
Общее	95%
```
## 📦 Команды для разработки

### Docker
```text
docker-compose up -d             # Запустить в фоне
docker-compose up                # Запустить с логами
docker-compose down              # Остановить
docker-compose down -v           # Остановить + удалить данные БД
docker-compose logs -f           # Смотреть логи
docker-compose exec app bash     # Зайти в контейнер приложения
docker-compose exec db psql -U postgres  # Зайти в БД
docker-compose up -d --build     # Пересобрать и запустить
Миграции
bash
alembic init migrations          # Инициализировать (первый раз)
alembic revision --autogenerate -m "message"  # Создать миграцию
alembic upgrade head              # Применить миграции
alembic downgrade -1              # Откатить последнюю
alembic history                   # Показать историю
alembic current                   # Показать текущую версию
Линтеры
bash
flake8 app/ tests/               # Проверить стиль
black app/ tests/                # Отформатировать код
mypy app/                        # Проверить типы
```
## 🐳 Docker-стек

| Сервис | Контейнер | Порт | Назначение |
|--------|-----------|------|------------|
| **app** | `tender_app` | 8000 | FastAPI приложение |
| **db** | `tender_db` | 5432 | PostgreSQL |

### Переменные окружения в Docker

# .env
```text
DATABASE_URL=postgresql://postgres:postgres@db:5432/tenders
SECRET_KEY=your-secret-key
```
🔒 Безопасность
Реализовано
✅ Переменные окружения для секретов (.env)

✅ Валидация входных данных (Pydantic)

✅ Обработка ошибок (HTTPException)

✅ Каскадное удаление (ON DELETE CASCADE)

✅ UUID вместо автоинкремента (безопаснее для API)

Рекомендации для продакшена
⚠️ Использовать надёжный SECRET_KEY

⚠️ Настроить CORS

⚠️ Добавить аутентификацию (JWT)

⚠️ Использовать HTTPS

⚠️ Ограничить количество запросов (Rate Limiting)

🔄 CI/CD (GitHub Actions)
yaml
name: CI

on: [push, pull_request]
```text
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: flake8 app/ tests/
      - run: black --check app/ tests/
      - run: pytest tests/ --cov=app
```

## 🤝 Как внести вклад

1. Fork репозитория
2. Создать ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитить изменения (`git commit -m 'Add amazing feature'`)
4. Запушить в ветку (`git push origin feature/amazing-feature`)
5. Открыть Pull Request

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT**. Подробнее в файле [LICENSE](LICENSE).

---

## 👤 Автор

**Дмитрий**
- GitHub: [@wyganoffc](https://github.com/wyganoffc)

---

## 🙏 Благодарности

- **Crown** — за интересное тестовое задание
- **FastAPI** — за прекрасный фреймворк
- **SQLAlchemy** — за мощный ORM

---

## 📧 Контакты

По вопросам сотрудничества:
- Email: serofdima2000@gmail.com

---

**Сделано с ❤️ для Crown**