from contextlib import asynccontextmanager
from contextlib import contextmanager
from typing import AsyncContextManager
from typing import ContextManager
from typing import Type, List
from typing import Self

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.settings import async_postgres_settings
from src.settings import postgres_settings


class BaseModel(DeclarativeBase):
    """Postgres base model"""

    _session: Session | None = None

    @classmethod
    def set_session(cls, session: Session) -> None:
        cls._session = session

    @classmethod
    def first(cls) -> Type[Self]:
        return cls._session.query(cls).first()

    @classmethod
    def all(cls) -> List[Type[Self]]:
        return cls._session.query(cls).all()

    @classmethod
    def fill(cls, **data) -> Self:
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj


@asynccontextmanager
async def get_async_session() -> AsyncContextManager[AsyncSession]:
    engine = create_async_engine(async_postgres_settings.get_url())
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


@contextmanager
def get_session() -> ContextManager[Session]:
    engine = create_engine(postgres_settings.get_url())
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def set_session():
    """Создать сессию"""
    engine = create_engine(postgres_settings.get_url())
    db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
    BaseModel.set_session(db_session)
    BaseModel.query = db_session.query_property()
    BaseModel.metadata.create_all(engine)
