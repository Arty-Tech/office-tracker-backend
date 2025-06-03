from datetime import date
from typing import List
from pydantic import BaseModel


class DailyDetail(BaseModel):
    date: date
    day_type: str
    punches_formatted: str
    ore_ordinarie: float
    ore_extra: float
    note: str = ""


class Summary(BaseModel):
    total_worked_days: int
    total_ore_ordinarie: float
    total_ore_extra: float
    ferie: int
    permessi: int
    malattia: int


class ReportMonth(BaseModel):
    daily_details: List[DailyDetail]
    summary: Summary
