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

Для запуска на SQLite переименовать .env.example в .env и настроить под себя:

```
APP_TITLE=Сервис бронирования переговорных комнат
DATABASE_URL=your_database
SECRET=your_secret
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin
```

Примененить миграций:

```
alembic upgrade head
```

Запуск проекта:

```
uvicorn app.main:app --reload
```

После первого запуска произойдёт автоматическое создание
суперпользователя заданного в .env. 
При авторизации в качестве username используется email.

Документация API:

```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```
