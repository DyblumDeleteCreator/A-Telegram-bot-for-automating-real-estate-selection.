# A-Telegram-bot-for-automating-real-estate-selection.
# Telegram-бот для подбора недвижимости

Бот на Python + aiogram + SQLite (aiosqlite) для админ-панели и подбора объектов недвижимости.

## Возможности

- **Админ-панель**:
  - добавить объект в БД;
  - посмотреть содержимое БД;
  - удалить объект.
- **Подборка**:
  - пользователь проходит анкету;
  - бот ищет подходящие объекты в БД;
  - отправляет найденные объекты.

## Технологии

- Python
- aiogram 3
- aiosqlite
- pydantic

## Как запустить

1. `pip install -r requirements.txt`
2. Создать `.env` с `BOT_TOKEN` и `ADMIN_PASSWORD`.
3. `python main.py`

## Структура

- `main.py` — точка входа.
- `DB/database.py` — работа с БД.
- `Handlers/routes.py` — хендлеры.
- `information/user.py` — FSM-состояния.

## Статус

MVP: добавление, просмотр, удаление и подборка работают на уровне кода.
