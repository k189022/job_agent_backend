from fastapi import APIRouter, Depends, HTTPException, Response, status, Body, File, UploadFile
from bson import ObjectId
from pymongo import ReturnDocument

from src.monggoDB.config.db import resume_collection
from src.monggoDB.models.resume import ResumeCollection, ResumeModel, ResumeUpdateModel
from src.utils.supabase_clients import get_supabase_user

resume_router = APIRouter()

@resume_router.post(
    "/",
    response_description="Add new resume",
    response_model=ResumeModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_resume(
    user_id: str = Depends(get_supabase_user), 
    file: UploadFile = File(...)):
    """
    Insert Resume Data
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    print("file:", file)
    print("userId: ", user_id)
    print("YESSSSS")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    try:
        # Read the file content
        content = await file.read()
        
        # Create the resume model with userId
        new_resume = ResumeModel(userId=user_id, resume=content)
        
        # Insert the resume into the collection
        new_resume_doc = await resume_collection.insert_one(new_resume.model_dump(by_alias=True, exclude=["id"]))
        created_resume = await resume_collection.find_one({"_id": new_resume_doc.inserted_id})
        return created_resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")

@resume_router.get("/", response_description="Get all resumes", response_model=ResumeCollection)
async def get_resumes(user_id: str = Depends(get_supabase_user)):
    return ResumeCollection(users=await resume_collection.find({"userId": user_id}).to_list(100))  # Ensure correct serialization

@resume_router.get(
    "/{id}",
    response_description="Get a single resume by ID",
    response_model=ResumeModel,
    response_model_by_alias=False,
)
async def get_resume_by_id(id: str, user_id: str = Depends(get_supabase_user)):
    """
    Get the record for a specific resume, looked up by `id`.
    """

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if (resume := await resume_collection.find_one({"_id": ObjectId(id), "userId": user_id})) is not None:
        return resume

    raise HTTPException(status_code=404, detail=f"Resume {id} not found")

@resume_router.put(
    "/{id}",
    response_description="Update a resume",
    response_model=ResumeModel,
    response_model_by_alias=False,
)
async def update_resume(id: str, resume: ResumeUpdateModel = Body(...), user_id: str = Depends(get_supabase_user)):

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    resume_update = {
        k: v for k, v in resume.model_dump(by_alias=True).items() if v is not None
    }

    if len(resume_update) >= 1:
        update_result = await resume_collection.find_one_and_update(
            {"_id": ObjectId(id), "userId": user_id},
            {"$set": resume_update},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Resume {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_resume := await resume_collection.find_one({"_id": ObjectId(id), "userId": user_id})) is not None:
        return existing_resume

    raise HTTPException(status_code=404, detail=f"Resume {id} not found")

@resume_router.delete("/{id}", response_description="Delete a resume")
async def delete_resume(id: str, user_id: str = Depends(get_supabase_user)):
    """
    Remove a single resume from the database.
    """

    delete_result = await resume_collection.delete_one({"_id": ObjectId(id), "userId": user_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Resume {id} not found")
