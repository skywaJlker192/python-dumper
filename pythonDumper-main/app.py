from fastapi import FastAPI
from contextlib import asynccontextmanager
from repositories import init_db
from routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Api", lifespan=lifespan)
app.include_router(router)
