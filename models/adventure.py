from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Adventure(Base):
    id = Column(Integer,primary_key = True, index=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    draft = Column(Boolean,default=False)
    author_id =  Column(Integer,ForeignKey("user.id"))
    updated_at = Column(Date)
    created_at = Column(Date)

    author = relationship("User",back_populates="adventures")
