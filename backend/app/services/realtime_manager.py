from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Room

class RealtimeRoomManager:
    def __init__(self):
        self.active_rooms: Dict[str, Set[WebSocket]] = {}
        self.room_code_cache: Dict[str, str] = {}
    
    async def get_room_exists(self, room_id: str, db: AsyncSession) -> bool:
        stmt = select(Room).where(Room.id == room_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def connect(self, room_id: str, websocket: WebSocket):
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = set()
            # Load initial code from cache or empty
            self.room_code_cache[room_id] = self.room_code_cache.get(room_id, "")
        
        self.active_rooms[room_id].add(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_rooms:
            self.active_rooms[room_id].discard(websocket)
            if not self.active_rooms[room_id]:
                # Cleanup empty room
                del self.active_rooms[room_id]
                self.room_code_cache.pop(room_id, None)

    async def broadcast_code(self, room_id: str, code: str, websocket: WebSocket):
        """Send code to all OTHER clients in room"""
        self.room_code_cache[room_id] = code  # Update cache
        
        if room_id in self.active_rooms:
            message = {"type": "code_sync", "code": code}
            disconnected = set()
            
            for conn in self.active_rooms[room_id]:
                if conn != websocket:  # Skip sender
                    try:
                        await conn.send_json(message)
                    except WebSocketDisconnect:
                        disconnected.add(conn)
            
            # Cleanup disconnected clients
            for conn in disconnected:
                self.active_rooms[room_id].discard(conn)

    async def get_room_code(self, room_id: str, db: AsyncSession) -> str:
        """Get latest code from DB or cache"""
        if room_id in self.room_code_cache:
            return self.room_code_cache[room_id]
        
        # Fallback to DB
        stmt = select(Room.code).where(Room.id == room_id)
        result = await db.execute(stmt)
        code = result.scalar() or ""
        self.room_code_cache[room_id] = code
        return code
    
# Global singleton instance
manager = RealtimeRoomManager()