def drop_tables():
    """
    Cancella tutte le tabelle (drop all) – USO RISERVATO, solo in dev!
    """
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:p0stgr3s@db/time_tracker_db")

    import sqlalchemy as sa
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(DATABASE_URL, future=True, echo=False)
    async def _inner():
        # drop tutte le tabelle
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("✅ Tutte le tabelle sono state droppate.")

    asyncio.run(_inner())


def recreate_schema():
    """
    Fa prima drop_all poi create_all – USO RISERVATO, solo in dev!
    """
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:p0stgr3s@db/time_tracker_db")

    import sqlalchemy as sa
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(DATABASE_URL, future=True, echo=False)
    async def _inner():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Schema ricreato (drop_all + create_all).")

    asyncio.run(_inner())
