from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from mySQL.config.db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    resume = Column(Text, nullable=True)

    jobs = relationship("Job", back_populates="user")
    motivation_letters = relationship("MotivationLetter", back_populates="user")