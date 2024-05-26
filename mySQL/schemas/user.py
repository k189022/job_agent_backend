from typing import List, Optional
from pydantic import BaseModel

from mySQL.schemas.job import Job, MotivationLetter

class UserBase(BaseModel):
    email: str
    resume: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    jobs: List["Job"] = []
    motivation_letters: List["MotivationLetter"] = []

    class Config:
        orm_mode: True


