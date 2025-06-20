import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nome = Column(String, nullable=True)
    preferences = Column(JSON, default={})

    schedules = relationship("WorkDayConfig", back_populates="user", cascade="all, delete")
    timesheets = relationship("TimeEntry", back_populates="user", cascade="all, delete")
