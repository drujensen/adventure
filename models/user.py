from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    inactive = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    adventures = relationship("Adventure", back_populates="author")
