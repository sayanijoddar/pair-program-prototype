import uuid 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Room

async def create_room(db:AsyncSession):
    room_id = uuid.uuid4().hex[:8]

    stmt = select(Room).where(Room.id == room_id)
    result = await db.execute(stmt)

    while result.scalar_one_or_none() is not None:
        room_id = uuid.uuid4().hex[:8]
        result = await db.execute(select(Room).where(Room.id == room_id))

    room = Room(id = room_id, code = "")
    db.add(room)
    await db.commit()
    await db.refresh(room) 
    
    return room