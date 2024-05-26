from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import  Integer, String, Text
from mySQL.config.db import Base
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(Text, nullable=False)
    company = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    skills = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)

    user = relationship("User", back_populates="jobs")
    motivation_letters = relationship("MotivationLetter", back_populates="job")


