import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

async def init_models():
    engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        # Crea tutte le tabelle basate su Base.metadata
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())