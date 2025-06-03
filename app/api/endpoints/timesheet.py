from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from app.api.deps import get_db, get_current_user
from app.schemas.time_entry import TimeEntryCreate, TimeEntryRead
from app.crud.time_entry import crud_time_entry

router = APIRouter(tags=["timesheets"], prefix="/timesheets")

@router.get("/{anno}/{mese}", response_model=List[TimeEntryRead])
async def get_timesheet_month(
    anno: int, mese: int,
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    details = await crud_time_entry.get_month_entries(db, str(current_user.id), anno, mese)
    return details

@router.post("/day", response_model=TimeEntryRead)
async def create_or_update_day(
    te_in: TimeEntryCreate,
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    if te_in.day_type != te_in.day_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid day type")
    detail = await crud_time_entry.create_or_update_day(db, str(current_user.id), te_in)
    return detail

@router.delete("/day/{date_str}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_day(
    date_str: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    await crud_time_entry.delete_day(db, str(current_user.id), date_str)
    return None