# backend/app/app.py - COMPLETE FILE (CORS FIXED!)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ CRITICAL!
from contextlib import asynccontextmanager
from routers.router_room import router as rooms_router
from routers.router_ws import router as ws_router
from routers.autocomplete import router as autocomplete_router
from database.database import engine, Base
import database.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Pair Programming Backend", lifespan=lifespan)

# ✅ CORS MIDDLEWARE - FIRST THING!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms_router)
app.include_router(ws_router)
app.include_router(autocomplete_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
