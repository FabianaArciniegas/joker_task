from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from api.routes import routes
from core.config import settings
from utils.app_exception_handler import app_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting...")
    env = settings.ENV
    app.mongodb_client = AsyncIOMotorClient(settings.DB_CONNECTION)
    app.database = app.mongodb_client[settings.DB_NAME]
    print(f"Started successfully: {env}")
    yield
    print("Application closing...")
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan, exception_handlers=app_exception_handler)

for route in routes:
    app.include_router(route, prefix=settings.API_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
