from sqlalchemy.orm import Session
from mySQL.models.job import Job as JobModel
from mySQL.schemas.job import JobCreate



# Job CRUD
def get_job(db: Session, job_id: int):
    return db.query(JobModel).filter(JobModel.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(JobModel).offset(skip).limit(limit).all()

def create_job(db: Session, job: JobCreate):
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

