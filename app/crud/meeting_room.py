from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CustomException
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession,
) -> MeetingRoom:
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)
    session.add(db_room)

    try:
        await session.commit()
    except exc.IntegrityError as ex:
        if 'unique' in str(ex.orig).lower():
            raise CustomException(
                422,
                'Переговорка с таким именем уже существует!',
            )

    await session.refresh(db_room)

    return db_room


async def read_all_rooms_from_db(session: AsyncSession) -> list[MeetingRoom]:
    db_rooms = await session.scalars(select(MeetingRoom))
    return db_rooms.all()


async def get_meeting_room_by_id(
        room_id: int,
        session: AsyncSession,
) -> Optional[MeetingRoom]:
    db_room = await session.get(MeetingRoom, room_id)
    return db_room


async def update_meeting_room(
        db_room: MeetingRoom,
        room_in: MeetingRoomUpdate,
        session: AsyncSession,
) -> MeetingRoom:
    obj_data = jsonable_encoder(db_room)
    update_data = room_in.dict(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_room, field, update_data[field])

    session.add(db_room)

    try:
        await session.commit()
    except exc.IntegrityError as ex:
        if 'unique' in str(ex.orig).lower():
            raise CustomException(
                422,
                'Переговорка с таким именем уже существует!',
            )

    await session.refresh(db_room)
    return db_room


async def delete_meeting_room(
        db_room: MeetingRoom,
        session: AsyncSession,
) -> MeetingRoom:
    await session.delete(db_room)
    await session.commit()
    return db_room
