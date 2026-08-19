import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


def _utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


class Adventure(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    draft = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    created_at = Column(DateTime, default=_utcnow)

    author = relationship("User", back_populates="adventures")
