from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import event, text
from sqlalchemy.orm import Session, declarative_base

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async_session_maker = AsyncSessionLocal
Base = declarative_base()


@event.listens_for(Session, 'after_begin')
def set_rls_after_begin(session, transaction, connection):
    """Garante que app.condominio_id seja re-injetado a cada nova transacao
    (inclusive apos commit), mantendo o isolamento RLS sempre ativo.
    """
    condo_id = session.info.get('condominio_id')
    if condo_id and connection.dialect.name == 'postgresql':
        connection.execute(text(f"SET LOCAL app.condominio_id = '{condo_id}'"))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
