"""
This script is a simple example of how to use the cachetools library to cache the results of an expensive operation.
The script defines a FastAPI application with a single GET endpoint that takes an optional key query parameter.
The endpoint checks if the result for the given key is already in the cache and returns it if found.
If the result is not in the cache, the endpoint calls an expensive operation _get_expensive_resource() and stores the result in the cache before returning it.
The cache has a maximum size of 100 entries and a TTL of 60 seconds.
Also test basic authentication and verification using FastAPI.
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from cachetools import TTLCache
import asyncio
from redis import asyncio as aioredis
from contextlib import asynccontextmanager
import uuid
from backend.dependencies.auth import security, verification
from typing import Annotated


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create a cache with a maximum size of 100 entries and a TTL of 60 seconds
    cache = TTLCache(maxsize=100, ttl=60)
    app.state.cache = cache
    yield


app = FastAPI(
    title="Testing",
    description="Testing Script",
    version="0.0.1",
    terms_of_service=None,
    contact=None,
    license_info=None,
    lifespan=lifespan,
)


async def _get_expensive_resource():
    await asyncio.sleep(5)
    return True


@app.get("/")
async def get(
    request: Request, key: str, Verification: Annotated[bool, Depends(verification)]
):
    if not Verification:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cache = request.app.state.cache

    # Check if the result is already in the cache
    result = cache.get(key)
    if result is not None:
        print(f"Found it in cache for key {key}")
        return result

    result = await _get_expensive_resource()

    # Store the result in the cache
    cache[key] = result

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
