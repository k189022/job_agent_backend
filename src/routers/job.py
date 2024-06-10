from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from bson import ObjectId

from src.monggoDB.config.db import jobs_collection
from src.monggoDB.models.common import PyObjectId
from src.utils.supabase_clients import get_supabase_user
from src.monggoDB.models.job import JobCollection, JobModel


# Job Router
job_router = APIRouter()

# user_id ="75dcd09a-0264-4a3c-8a43-6871882f5ecf"

@job_router.post("/", response_description="Add new job", response_model=JobModel, status_code=status.HTTP_201_CREATED)
# async def create_job(user_id:str = Depends(get_supabase_user), job: JobModel = Body(...)):
async def create_job(user_id, job: JobModel = Body(...)):
    # Check if the user_id exists
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if isinstance(job, dict):
        job_dict = job  # Directly use the dictionary if no model instance is available.
    else:
        job_dict = job.model_dump(by_alias=True, exclude=["id"])  # If it's a model instance, dump to dict.

    job_dict["user_id"] = user_id

    new_job = await jobs_collection.insert_one(job_dict)
    created_job = await jobs_collection.find_one({"_id": new_job.inserted_id})
    return created_job

user_id ="75dcd09a-0264-4a3c-8a43-6871882f5ecf"

@job_router.get("/", response_description="List all jobs for a user", response_model=JobCollection, status_code=status.HTTP_200_OK)
async def get_jobs_for_user(user_id:str = Depends(get_supabase_user)):
# async def get_jobs_for_user(user_id = user_id):

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    jobs = await jobs_collection.find({"user_id": user_id}).to_list(100)
    return JobCollection(jobs=jobs)


@job_router.delete("/{job_id}", response_description="Delete a job", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: PyObjectId, user_id: str = Depends(get_supabase_user)):
    # Find the job to verify ownership
    job = await jobs_collection.find_one({"_id": job_id, "user_id": ObjectId(user_id)})
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or you do not have permission to delete this job")
    
    delete_result = await jobs_collection.delete_one({"_id": job_id})
    
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail="Job not found")