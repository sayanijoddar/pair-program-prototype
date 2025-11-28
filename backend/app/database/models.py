import time
from sqlalchemy import Column, String, Text, DateTime, func
from .database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String(32), primary_key=True, index=True)
    code = Column(Text, nullable=False, default="")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=time.time(),
    )