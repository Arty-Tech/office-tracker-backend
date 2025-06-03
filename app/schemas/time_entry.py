from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date, time
from typing import List
from app.models.time_entry import DayType

class PunchCreate(BaseModel):
    in_time: time
    out_time: time

    @validator('out_time')
    def check_out_after_in(cls, v, values):
        if 'in_time' in values and v <= values['in_time']:
            raise ValueError('out_time must be after in_time')
        return v

class TimeEntryCreate(BaseModel):
    date: date
    day_type: DayType
    punches: List[PunchCreate] = []
    note: str = ""

class PunchRead(BaseModel):
    timestamp: str
    is_entry: bool

class TimeEntryRead(BaseModel):
    id: UUID
    date: date
    day_type: DayType
    punches: List[PunchRead]
    ore_ordinarie: float
    ore_extra: float
    note: str

    class Config:
        orm_mode = True