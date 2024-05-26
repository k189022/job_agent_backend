
from typing import List, Optional
from pydantic import BaseModel

from monggoDB.schemas.motivationLetter import MotivationLetter
from monggoDB.schemas.user import User



class JobBase(BaseModel):
    url: str
    company: str
    title: str
    description: Optional[str] = None
    skills: Optional[str] = None
    location: Optional[str] = None

class JobCreate(JobBase):
    user_id: int

class Job(JobBase):
    id: int
    user_id: int
    user: User
    motivation_letters: List["MotivationLetter"] = []

    class Config:
        orm_mode: True
        