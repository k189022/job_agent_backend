from pydantic import BaseModel


class JobList(BaseModel):
    title: str
    company: str
    location: str
    description: str
    skills: str
    url: str

class JobDeteils(BaseModel):
    title: str
    company: str
    description: str
    skills: str