# app/routers/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from services.realtime_manager import manager

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    db: AsyncSession = Depends(get_db)
):
    await websocket.accept()
    
    # 1. Validate room exists
    if not await manager.get_room_exists(room_id, db):
        await websocket.close(code=4001)  # Custom close code
        return

    # 2. Connect client and send initial code
    manager.connect(room_id, websocket)
    initial_code = await manager.get_room_code(room_id, db)
    await websocket.send_json({
        "type": "init", 
        "code": initial_code
    })

    try:
        # 3. Message loop
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "code_change":
                code = data.get("code", "")
                await manager.broadcast_code(room_id, code, websocket)
                
    except WebSocketDisconnect:
        # 4. Cleanup
        manager.disconnect(room_id, websocket)
