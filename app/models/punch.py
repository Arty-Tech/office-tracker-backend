import uuid
from sqlalchemy import Column, ForeignKey, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Boolean, DateTime

from app.db.base import Base

class Punch(Base):
    __tablename__ = "punches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time_entry_id = Column(UUID(as_uuid=True), ForeignKey("time_entries.id", ondelete="CASCADE"), nullable=False)
    is_entry = Column("in_or_out", Boolean, nullable=False)  # True se ingresso, False se uscita
    timestamp = Column(DateTime(timezone=True), nullable=False)

    time_entry = relationship("TimeEntry", back_populates="punches")
