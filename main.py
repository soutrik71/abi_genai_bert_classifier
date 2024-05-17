import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import sessionmanager, Base
from backend.routes import prediction, system_info, status_check, chat

from src.model_startup import model_startup
from contextlib import asynccontextmanager

from src.settings import (
    LoggerSettings,
)
from src.utils.logger import setup_logging
import time
from src.utils.redis_connect import _get_redis_url
from redis import asyncio as aioredis

logger = setup_logging(
    logger_name=LoggerSettings().logger_name,
    log_file="ModelApiEndpoint.log",
    log_level=LoggerSettings().log_level,
)


# Initialize the model startup context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Executing Model Startup")
    model = model_startup()
    app.state.model = model

    logger.info("Creating DB Tables")
    async with sessionmanager._engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


# Initialize API Server
app = FastAPI(
    title="ML Model",
    description="Description of the ML Model",
    version="0.0.1",
    terms_of_service=None,
    contact=None,
    license_info=None,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# @app.on_event("startup")
# async def startup_event():
#     logger.info("Creating DB Records")
#     async with sessionmanager._engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# adding time middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers in the API
app.include_router(status_check.router)
app.include_router(system_info.router)
app.include_router(chat.router)
app.include_router(prediction.router)

if __name__ == "__main__":
    # server api
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
