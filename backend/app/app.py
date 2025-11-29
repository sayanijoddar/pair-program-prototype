from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.router_room import router
from database.database import engine, Base
import database.models  # Registers Room model
import routers.router_ws as router_ws

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Pair Programming Backend",
    lifespan=lifespan,
)

app.include_router(router)
app.include_router(router_ws.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
