from sqlalchemy import Column, ForeignKey, SmallInteger, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
import uuid

class WorkDayConfig(Base):
    __tablename__ = "workday_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    weekday = Column(SmallInteger, nullable=False)  # 0 = Lunedì, …, 6 = Domenica
    start_time_1 = Column(Time, nullable=False)
    end_time_1 = Column(Time, nullable=False)
    start_time_2 = Column(Time, nullable=True)
    end_time_2 = Column(Time, nullable=True)

    user = relationship("User", back_populates="schedules")
