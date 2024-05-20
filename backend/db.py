import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.settings import env_settings

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseSessionManager:
    """
    A manager for managing database sessions asynchronously using SQLAlchemy.
    """

    def __init__(self, url: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(url, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        """
        Close the database session manager.
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Context manager for getting a connection asynchronously.
        """
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Context manager for getting a session asynchronously.
        """
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(env_settings.DB_URI, {"echo": True})


async def get_db_session() -> AsyncSession:
    """
    Get an asynchronous database session.
    """
    async with sessionmanager.session() as session:
        yield session
