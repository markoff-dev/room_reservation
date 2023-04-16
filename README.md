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

Для запуска с SQLite и настройками по умолчанию, переименовать .env.example 
в .env:

```
mv .env.example .env
```

Или настроить .env под себя:
```
APP_TITLE=Имя сервиса
DATABASE_URL=DSN нужной DB
SECRET=Ключ шифрования (любая строка)
FIRST_SUPERUSER_EMAIL=Почта суперпользователя
FIRST_SUPERUSER_PASSWORD=Пароль суперпользователя
```

Применить миграции:

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
