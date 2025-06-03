from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.workday_config import WorkDayConfigCreate, WorkDayConfigRead
from app.crud.workday_config import crud_workday_config
from app.models.workday_config import WorkDayConfig

router = APIRouter(tags=["schedules"], prefix="/schedules")

@router.get("/", response_model=List[WorkDayConfigRead])
async def get_schedules(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    configs = await crud_workday_config.get_by_user(db, str(current_user.id))
    return configs

@router.post("/", response_model=WorkDayConfigRead)
async def create_or_update_schedule(
    config_in: WorkDayConfigCreate,
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    cfg = await crud_workday_config.create_or_update(db, str(current_user.id), config_in)
    return cfg

@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    config_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    # Non serve verificare se user possiede la config: è fatto dal CASCADE e FK
    await crud_workday_config.delete(db, config_id)
    return None