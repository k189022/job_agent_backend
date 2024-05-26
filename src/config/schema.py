from pydantic import BaseModel


class JobList(BaseModel):
    job_title: str
    company_name: str
    description: str
    requirements: str
    skils:str