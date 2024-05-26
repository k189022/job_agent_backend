from typing import List, Optional
from pydantic import BaseModel

from mySQL.schemas.job import Job, User


class MotivationLetterBase(BaseModel):
    letter: str

class MotivationLetterCreate(MotivationLetterBase):
    user_id: int
    job_id: int

class MotivationLetter(MotivationLetterBase):
    id: int
    user_id: int
    job_id: int
    user: User
    job: Job

    class Config:
        orm_mode: True
