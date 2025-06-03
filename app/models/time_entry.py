import uuid
from sqlalchemy import Column, ForeignKey, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class DayType(enum.Enum):
    normal = "normal"
    ferie = "ferie"
    permesso = "permesso"
    malattia = "malattia"
    smartworking = "smartworking"


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, index=True, nullable=False)
    day_type = Column(Enum(DayType), default=DayType.normal, nullable=False)

    punches = relationship("Punch", back_populates="time_entry", cascade="all, delete")
    user = relationship("User", back_populates="timesheets")



