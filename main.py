"""
Main API Endpoint for the Question Classifier API.
This file initializes the FastAPI server and includes the routers for the API.
The startup event initializes the database tables and the model.

The API includes the following routers:
1. status_check: A router to check the status of the API.
2. system_info: A router to get system information.
3. chat: A router to interact with the chat records in the database.
4. prediction: A router to perform predictions using the loaded model.

The API server is started using the uvicorn library.
"""

import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.db import sessionmanager, Base
from backend.routes import prediction, system_info, status_check, chat
from src.model_startup import model_startup
from src.settings import LoggerSettings
from src.utils.logger import setup_logging
from cachetools import TTLCache

# Setup logging
logger = setup_logging(
    logger_name=LoggerSettings().logger_name,
    log_file="ModelApiEndpoint.log",
    log_level=LoggerSettings().log_level,
)


# Initialize the model startup context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the model and create the database tables on startup of the API server,
    and create a cache.
    """
    logger.info("Executing Model Startup")
    model = model_startup()
    app.state.model = model

    logger.info("Creating DB Tables")
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    logger.info(
        "Initializing cache with a maximum size of 100 entries and a TTL of 60 seconds"
    )
    app.state.cache = TTLCache(maxsize=100, ttl=60)

    yield


# Initialize API Server
app = FastAPI(
    title="Question Bert-Classifier",
    description="Question Classifier API Endpoint",
    version="0.0.1",
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


# Adding time middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add a header with the process time for each request."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.3f}"
    return response


# Include routers in the API
app.include_router(status_check.router)
app.include_router(system_info.router)
app.include_router(chat.router)
app.include_router(prediction.router)

if __name__ == "__main__":
    # Start the API server
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
