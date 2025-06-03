from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workday_config import WorkDayConfig
from app.schemas.workday_config import WorkDayConfigCreate, WorkDayConfigRead
from typing import List
from uuid import UUID

class CRUDWorkDayConfig:
    async def get_by_user(self, db: AsyncSession, user_id: str) -> List[WorkDayConfig]:
        result = await db.execute(select(WorkDayConfig).where(WorkDayConfig.user_id == UUID(user_id)))
        return result.scalars().all()

    async def create_or_update(
        self, db: AsyncSession, user_id: str, config_in: WorkDayConfigCreate
    ) -> WorkDayConfig:
        # Controlla se esiste già una config per 'weekday'
        result = await db.execute(
            select(WorkDayConfig).where(
                WorkDayConfig.user_id == UUID(user_id),
                WorkDayConfig.weekday == config_in.weekday
            )
        )
        existing = result.scalars().first()
        if existing:
            existing.start_time_1 = config_in.start_time_1
            existing.end_time_1 = config_in.end_time_1
            existing.start_time_2 = config_in.start_time_2
            existing.end_time_2 = config_in.end_time_2
            db.add(existing)
            await db.commit()
            await db.refresh(existing)
            return existing
        # Altrimenti crea nuova
        new_cfg = WorkDayConfig(
            user_id=UUID(user_id),
            weekday=config_in.weekday,
            start_time_1=config_in.start_time_1,
            end_time_1=config_in.end_time_1,
            start_time_2=config_in.start_time_2,
            end_time_2=config_in.end_time_2
        )
        db.add(new_cfg)
        await db.commit()
        await db.refresh(new_cfg)
        return new_cfg

    async def delete(self, db: AsyncSession, config_id: str) -> None:
        result = await db.execute(select(WorkDayConfig).where(WorkDayConfig.id == UUID(config_id)))
        cfg = result.scalars().first()
        if cfg:
            await db.delete(cfg)
            await db.commit()

crud_workday_config = CRUDWorkDayConfig()