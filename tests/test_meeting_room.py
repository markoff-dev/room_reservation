import time
from datetime import datetime

import pytest

from conftest import TestingSessionLocal
from app.models.meeting_room import MeetingRoom


def test_get_meeting_rooms_all_users(get_all_users, create_meeting_room,
                                     create_another_meeting_room):
    """Тест проверяет, что при GET запросе от любого типа пользователя получаем
    корректный код ответа, а содержимое ответа соответствует ожидаемому"""
    for type_user, user_client in get_all_users.items():
        response = user_client.get('/meeting_rooms/')
        assert response.status_code == 200, (
            f'Запрос от {type_user}. При получении списка переговорок должен '
            f'вернуться статус-код 200.'
        )
        assert isinstance(response.json(), list), (
            f'Запрос от {type_user}. При получении списка переговорок должен '
            f'возвращаться объект типа `list`.'
        )
        assert len(response.json()) == 2, (
            f'Запрос от {type_user}. При корректном GET-запросе к эндпоинту '
            '`/meeting_rooms/` не создаётся объект в БД.'
            'Проверьте модель `MeetingRoom`.'
        )
        data = response.json()[0]
        keys = sorted([
            'name',
            'description',
            'id',
        ])
        assert sorted(list(data.keys())) == keys, (
            f'Запрос от {type_user}. При получении списка переговорок в '
            f'ответе должны быть ключи `{keys}`.'
        )
        assert response.json() == [
            {
                'name': 'Test room 1',
                'description': 'Test room description 1',
                'id': 1,
            },
            {
                'name': 'Test room 2',
                'id': 2,
            }
        ], (f'Запрос от {type_user}. При получении списка переговорок тело '
            'ответа API отличается от ожидаемого.')


@pytest.mark.parametrize('json, keys, expected_data', [
    (
            {'name': 'test_room_1'},
            ['name', 'id'],
            {'name': 'test_room_1', 'id': 1},
    ),
    (
            {'name': 'test_room_2', 'description': 'To you for chimigas'},
            ['name', 'id', 'description'],
            {'name': 'test_room_2', 'id': 1,
             'description': 'To you for chimigas'},
    ),
])
def test_create_meeting_room(superuser_client, json, keys, expected_data):
    """Тест проверяет, что при POST запросе от суперпользователя получаем
    корректный код ответа, а содержимое ответа соответствует ожидаемому"""
    response = superuser_client.post('/meeting_rooms/', json=json)
    assert response.status_code == 200, (
        'При создании переговорки должен возвращаться статус-код 200.'
    )
    data = response.json()
    assert sorted(list(data.keys())) == sorted(keys), (
        f'При создании переговорки в ответе должны быть ключи `{keys}`.'
    )
    assert data == expected_data, (
        'При создании переговорки тело ответа API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'description': 'To you for chimigas'},
    {'name': None, 'description': 'To you for chimigas'},
    {'id': 3},
    {'name': '', 'description': 'To you for chimigas'},
    {'name': 'Test' * 100, 'description': 'To you for chimigas'},
])
def test_create_meeting_room_incorrect(superuser_client, json):
    """Тест проверяет, что при некорректном теле POST запроса от
    суперпользователя получаем корректный код ошибки"""
    response = superuser_client.post('/meeting_rooms/', json=json)
    assert response.status_code == 422, (
        'При некорректном теле POST-запроса к эндпоинту `/meeting_rooms/` '
        'должен вернуться статус-код 422.'
    )


def test_create_meeting_room_duplicate(superuser_client, create_meeting_room):
    """Тест проверяет, что нельзя создать переговорку с одинаковыми именами"""
    response = superuser_client.post(
        '/meeting_rooms/',
        json={'name': create_meeting_room.name}
    )
    data = response.json()
    assert response.status_code == 422, (
        'При создании переговорки c существующим именем должны получить код '
        'ответа 422'
    )
    expected_data = {"detail": "Переговорка с таким именем уже существует!"}
    assert data == expected_data, (
        'При создании переговорки c существующим именем тело ответа API '
        'отличается от ожидаемого.')


def test_path_meeting_room(superuser_client, create_another_meeting_room):
    """Тест проверяет, возможность редактирования суперпользователем
    существующей переговорки"""
    current_meeting_room_id = create_another_meeting_room.id
    new_meeting_room = {
        'name': 'new_name',
        'description': 'new_description',
    }
    response = superuser_client.patch(
        f'/meeting_rooms/{current_meeting_room_id}',
        json=new_meeting_room
    )
    assert response.status_code == 200, (
        'При успешном изменении переговорки должен возвращаться статус-код 200'
    )
    data = response.json()
    new_meeting_room.update({'id': current_meeting_room_id})
    assert data == new_meeting_room, (
        'При изменении переговорки c существующим именем тело ответа API '
        'отличается от ожидаемого.')


def test_path_meeting_room_not_found(superuser_client):
    """Тест проверяет, что при PATH запроса от суперпользователя по
    несуществующему ID получаем правильный код ошибки и тело ответа"""
    meeting_room_id = 1

    response = superuser_client.patch(
        f'/meeting_rooms/{meeting_room_id}',
        json={'name': 'test_room_2', 'description': 'To you for chimigas'}
    )

    assert response.status_code == 404, (
        'При попытке редактирования несуществующей переговорки должны '
        'получить код 404'
    )
    data = response.json()
    expected_data = {"detail": "Переговорка не найдена!"}
    assert data == expected_data, (
        'При попытке редактирования несуществующей переговорки тело ответа '
        'API отличается от ожидаемого.')


@pytest.mark.parametrize('json', [
    {'name': 'Test' * 100, 'description': 'To you for chimigas'},
    {'name': '', 'description': 'To you for chimigas'},
])
def test_path_meeting_room_incorrect(superuser_client, json,
                                     create_meeting_room):
    """Тест проверяет, что при некорректном теле PATH запроса от
    суперпользователя получаем корректный код ошибки"""
    response = superuser_client.patch(
        f'/meeting_rooms/{create_meeting_room.id}', json=json)
    assert response.status_code == 422, (
        'При некорректном теле PATH-запроса к эндпоинту `/meeting_rooms/` '
        'должен вернуться статус-код 422.'
    )


async def test_delete_meeting_room(
        superuser_client,
        create_another_meeting_room
):
    """Возможность удаления суперпользователем
    существующей переговорки"""
    current_meeting_room_id = create_another_meeting_room.id
    response = superuser_client.delete(
        f'/meeting_rooms/{current_meeting_room_id}'
    )
    assert response.status_code == 200, (
        'При успешном удалении переговорки должен возвращаться статус-код 200'
    )

    # запрос к базе на существование ранее созданной переговорки
    async with TestingSessionLocal() as session:
        db_data = await session.get(MeetingRoom, current_meeting_room_id)
    assert db_data is None, 'Переговорка не была удалена'


def test_delete_meeting_room_not_found(superuser_client):
    """При DELETE запросе от суперпользователя по
    несуществующему ID получаем правильный код ошибки и тело ответа"""
    meeting_room_id = 1

    response = superuser_client.delete(
        f'/meeting_rooms/{meeting_room_id}'
    )

    assert response.status_code == 404, (
        'При попытке удаления несуществующей переговорки должны '
        'получить код 404'
    )
    data = response.json()
    expected_data = {"detail": "Переговорка не найдена!"}
    assert data == expected_data, (
        'При попытке удаления несуществующей переговорки тело ответа '
        'API отличается от ожидаемого.')


async def test_get_all_meeting_room_reserved(
        superuser_client,
        create_meeting_room,
        create_actual_reserved_meeting_room,
        create_another_actual_reserved_meeting_room,
):
    response = superuser_client.get(
        f'/meeting_rooms/{create_meeting_room.id}/reservations'
    )
    data = response.json()
    assert response.status_code == 200, (
        f'При получении списка переговорок должен вернуться статус-код 200.'
    )
    assert isinstance(data, list), (
        'При получении списка переговорок должен возвращаться объект '
        'типа `list`.'
    )
    assert len(data) == 2, (
        f'При корректном GET-запросе к эндпоинту '
        f'`/meeting_rooms/{create_meeting_room.id}/reservations` не '
        f'создаётся объект в БД. Проверьте модель `Reservation`.'
    )
    data = response.json()[0]
    keys = sorted([
        'from_reserve',
        'to_reserve',
        'id',
        'meetingroom_id'
    ])
    assert sorted(list(data.keys())) == keys, (
        f'При получении списка переговорок в ответе должны быть ключи `{keys}`'
    )

    assert response.json() == [
        {
            'from_reserve':
                create_actual_reserved_meeting_room.from_reserve.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f'),
            'to_reserve':
                create_actual_reserved_meeting_room.to_reserve.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f'),
            'id': create_actual_reserved_meeting_room.id,
            'meetingroom_id':
                create_actual_reserved_meeting_room.meetingroom_id
        },
        {
            'from_reserve':
                create_another_actual_reserved_meeting_room.
                from_reserve.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'to_reserve':
                create_another_actual_reserved_meeting_room.to_reserve.
                strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'id': create_another_actual_reserved_meeting_room.id,
            'meetingroom_id':
                create_actual_reserved_meeting_room.meetingroom_id
        }
    ], (f'При получении списка переговорок тело ответа API отличается от '
        f'ожидаемого.')
