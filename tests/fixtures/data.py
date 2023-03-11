from datetime import datetime, timedelta

import pytest

@pytest.fixture
def create_meeting_room(mixer):
    return mixer.blend(
        'app.models.meeting_room.MeetingRoom',
        name='Test room 1',
        description='Test room description 1',
    )


@pytest.fixture
def create_another_meeting_room(mixer):
    return mixer.blend(
        'app.models.meeting_room.MeetingRoom',
        name='Test room 2',
    )


@pytest.fixture
def create_actual_reserved_meeting_room(mixer):
    return mixer.blend(
        'app.models.reservation.Reservation',
        from_reserve=datetime.now() + timedelta(hours=1),
        to_reserve=datetime.now() + timedelta(hours=2),
        meetingroom_id=1,
        user_id=1
    )


@pytest.fixture
def create_another_actual_reserved_meeting_room(mixer):
    return mixer.blend(
        'app.models.reservation.Reservation',
        from_reserve=datetime.now() + timedelta(hours=2),
        to_reserve=datetime.now() + timedelta(hours=3),
        meetingroom_id=1,
        user_id=1
    )


@pytest.fixture
def create_not_actual_reserved_meeting_room(mixer):
    return mixer.blend(
        'app.models.reservation.Reservation',
        from_reserve=datetime.now() - timedelta(hours=2),
        to_reserve=datetime.now() - timedelta(hours=1),
        meetingroom_id=1,
        user_id=1
    )