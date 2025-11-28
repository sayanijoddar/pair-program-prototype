from pydantic import BaseModel

class RoomCreateResponse(BaseModel):
    roomId:str
    class Config:
        from_attributes = True