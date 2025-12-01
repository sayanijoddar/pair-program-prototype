# backend/app/app.py - DEPLOYMENT READY!
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers.router_room import router as rooms_router
from routers.router_ws import router as ws_router
from routers.autocomplete import router as autocomplete_router
from database.database import engine, Base
import database.models
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

 
app = FastAPI(
    title="Pair Programming Backend", 
    lifespan=lifespan,
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",   
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 
app.include_router(rooms_router, prefix="/api", tags=["rooms"])
app.include_router(ws_router, prefix="/ws", tags=["websocket"])
app.include_router(autocomplete_router, prefix="/api", tags=["autocomplete"])

 
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pair-program-backend"}


@app.get("/")
async def root():
    return {
        "message": "Pair Programming Backend ",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "rooms": "/api/rooms",
            "ws": "/ws/{room_id}",
            "autocomplete": "/api/autocomplete"
        }
    }

if __name__ == "__main__":
    import uvicorn
     
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app", 
        host=host, 
        port=port, 
        reload=os.getenv("ENV") == "development"
    )
