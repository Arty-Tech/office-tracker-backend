from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from pydantic import BaseModel

router = APIRouter(tags=["timer"], prefix="/timer")

class TimerPreferences(BaseModel):
    workDuration: int  # minuti
    breakDuration: int  # minuti
    soundUrl: str

@router.get("/preferences", response_model=TimerPreferences)
async def get_timer_preferences(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    prefs = current_user.preferences or {}
    return TimerPreferences(
        workDuration=prefs.get("workDuration", 25),
        breakDuration=prefs.get("breakDuration", 5),
        soundUrl=prefs.get("soundUrl", "/audio/bell.mp3")
    )

@router.post("/preferences")
async def update_timer_preferences(
    prefs_in: TimerPreferences,
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    # Aggiorna le preferenze nel JSON
    current_user.preferences.update({
        "workDuration": prefs_in.workDuration,
        "breakDuration": prefs_in.breakDuration,
        "soundUrl": prefs_in.soundUrl
    })
    db.add(current_user)
    await db.commit()
    return {"success": True}