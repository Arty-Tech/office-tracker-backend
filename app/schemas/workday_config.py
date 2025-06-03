from pydantic import BaseModel
from datetime import time
from uuid import UUID
from typing import Optional

class WorkDayConfigBase(BaseModel):
    weekday: int  # 0 = Lunedì, 6 = Domenica
    start_time_1: time
    end_time_1: time
    start_time_2: Optional[time] = None
    end_time_2: Optional[time] = None

class WorkDayConfigCreate(WorkDayConfigBase):
    pass

class WorkDayConfigRead(WorkDayConfigBase):
    id: UUID

    class Config:
        orm_mode = True