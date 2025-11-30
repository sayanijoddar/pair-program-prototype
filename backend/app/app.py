from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import Engine
from database.database import Base, engine
from routers.router_room import router as rooms_router
from routers.router_ws import router as ws_router      # Your WS file name
from routers.autocomplete import router as autocomplete_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    await engine.dispose()


app = FastAPI(title="Pair Programming Backend", lifespan=lifespan)

app.include_router(rooms_router)
app.include_router(ws_router)
app.include_router(autocomplete_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)