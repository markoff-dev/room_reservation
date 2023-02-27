## API для сервиса бронирования переговорок

Приложение предоставляет возможность бронировать помещения на определённый период времени.

### Рекомендуемый интерпретатор:
- Python 3.9.*

### Установка:
Клонировать репозиторий:
```
git clone git@github.com:markoff-dev/room_reservation.git
```

```
cd room_reservation
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости:

```
pip install -r requirements.txt
```

Для запуска на SQLite переименовать .env.example в .env либо настроить по себя:

```
APP_TITLE=Сервис бронирования переговорных комнат
DATABASE_URL=your_database
SECRET=your_secret
```

Примененить миграций:

```
alembic upgrade head
```

Запуск проекта:

```
uvicorn app.main:app --reload
```

Документация API:

```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```