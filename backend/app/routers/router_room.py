from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from schemas.rooms import RoomCreateResponse
from services.room_service import create_room

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("", response_model=RoomCreateResponse)
async def create_room_endpoint(db:AsyncSession=Depends(get_db)):
    room = await create_room(db)
    return RoomCreateResponse(roomId=room.id)