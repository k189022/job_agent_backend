from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mySQL.config.db import SessionLocal
from mySQL.database.job import get_job, get_jobs
from mySQL.schemas.job import JobCreate, Job

job_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@job_router.post("/", status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db=db, job=job)

@job_router.get("/{job_id}", status_code=status.HTTP_200_OK)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@job_router.get("/", status_code=status.HTTP_200_OK)
def read_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = get_jobs(db, skip=skip, limit=limit)
    return jobs





# # job_router.py

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from mySQL.models.job import Job as JobModel
# from mySQL.schemas.job import JobResponse as JobSchema
# from mySQL.config.db import SessionLocal

# job = APIRouter()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @job.get("/", status_code=status.HTTP_200_OK)
# async def read_all_jobs(db: Session = Depends(get_db)):
#     return db.query(JobModel).all()


# @job.get("/{id}", status_code=status.HTTP_200_OK)
# async def read_job_by_id(id: int, db: Session = Depends(get_db)):
#     job = db.query(JobModel).filter(JobModel.id == id).first()
#     if job is None:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return job


# @job.post("/", status_code=status.HTTP_201_CREATED)
# async def create_job(job: JobSchema, db: Session = Depends(get_db)):
#     new_job = JobModel(**job.dict())
#     db.add(new_job)
#     db.commit()
#     db.refresh(new_job)
#     return {"message": "Job created successfully"}


# @job.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
# async def update_job(id: int, job: JobSchema, db: Session = Depends(get_db)):
#     existing_job = db.query(JobModel).filter(JobModel.id == id).first()
#     if existing_job is None:
#         raise HTTPException(status_code=404, detail="Job not found")

#     for var, value in vars(job).items():
#         setattr(existing_job, var, value)

#     db.commit()
#     db.refresh(existing_job)
#     return {"message": "Job updated successfully"}


# @job.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_job(id: int, db: Session = Depends(get_db)):
#     job = db.query(JobModel).filter(JobModel.id == id).first()
#     if job is None:
#         raise HTTPException(status_code=404, detail="Job not found")
#     db.delete(job)
#     db.commit()
#     return {"message": "Job deleted successfully"}


# @job.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_job(db: Session = Depends(get_db)):
#     jobs = db.query(JobModel).all()
#     if not jobs:
#         raise HTTPException(status_code=404, detail="Job not found")
#     # Delete all jobs
#     for job in jobs:
#         db.delete(job)
    
#     # Commit the changes to the database
#     db.commit()
#     return {"message": "Job deleted successfully"}
