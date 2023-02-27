from datetime import datetime

import pytest


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
])
def test_create_meeting_room_incorrect(superuser_client, json):
    response = superuser_client.post('/meeting_rooms/', json=json)
    assert response.status_code == 422, (
        'При некорректном теле POST-запроса к эндпоинту `/meeting_rooms/` '
        'должен вернуться статус-код 422.'
    )


# def test_get_meeting_rooms(user_client, meeting_room):
#     response = user_client.get('/meeting_rooms/')
#     assert response.status_code == 200, (
#         'При получении списка переговорок должен вернуться статус-код 200.'
#     )
#     assert isinstance(response.json(), list), (
#         'При получении списка переговорок должен возвращаться объект типа `list`.'
#     )
#     assert len(response.json()) == 1, (
#         'При корректном GET-запросе к эндпоинту `/meeting_rooms/` не создаётся объект в БД.'
#         'Проверьте модель `MeetingRoom`.'
#     )