from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from mySQL.config.db import Base



class MotivationLetter(Base):
    __tablename__ = 'motivation_letters'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    letter = Column(Text, nullable=False)

    user = relationship("User", back_populates="motivation_letters")
    job = relationship("Job", back_populates="motivation_letters")
