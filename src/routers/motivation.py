from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, status
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.monggoDB.config.db import motivation_collection
from src.monggoDB.models.motivationLetter import MotivationLetterModel, MotivationLetterUpdate, MotivationLetterCollection
from src.utils.supabase_clients import get_supabase_user


user_id ="75dcd09a-0264-4a3c-8a43-6871882f5ecf"

# Motivation Letter Router
motivation_letter_router = APIRouter()

@motivation_letter_router.post("/", response_description="Add new job", response_model=MotivationLetterModel, status_code=status.HTTP_201_CREATED)
# async def create_motivation(user_id, job_id, letter: MotivationLetterModel = Body(...)):
def create_motivation(letter: MotivationLetterModel = Body(...)):

    if isinstance(letter, dict):
        letter_dict = letter  # Directly use the dictionary if no model instance is available.
    else:
        letter_dict = letter.model_dump(by_alias=True, exclude=["id"])  

    print(letter_dict)

    new_letter = motivation_collection.insert_one(letter_dict)
    created_letter = motivation_collection.find_one({"_id": new_letter.inserted_id})
    return created_letter

# job_id = "6658e9c88e3b5b0c8a2b4883"
# job_id = "6658e9c88e3b5b0c8a2b4881"

@motivation_letter_router.get("/{job_id}", response_description="Get a single motivation letter", response_model=MotivationLetterCollection, status_code=status.HTTP_200_OK)
# async def get_motivation_letter(user_id:str = Depends(get_supabase_user), job_id:Optional[str]=None):
async def get_motivation_letter(user_id:str= Depends(get_supabase_user), job_id:str=None):
# async def get_motivation_letter(user_id:str= user_id, job_id:str=None):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not job_id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    letters = await motivation_collection.find({"user_id": user_id, "job_id":job_id}).to_list(100)

    if not letters:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No letters found")
    
    return MotivationLetterCollection(letters = letters)

@motivation_letter_router.put("/{letter_id}", response_description="Update motivation letter content", status_code=status.HTTP_200_OK)
async def update_motivation_letter_content(letter_id: str, update: MotivationLetterUpdate, user_id: str = Depends(get_supabase_user)):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    result = await motivation_collection.update_one(
        {"_id": ObjectId(letter_id), "user_id": user_id},
        {"$set": {"content": update.content}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motivation letter not found")

    return {"msg": "Content updated successfully"}


@motivation_letter_router.delete("/{id}", response_description="Delete a motivation letter")
async def delete_motivation_letter(id: str):
    delete_result = await motivation_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=204)
    raise HTTPException(status_code=404, detail=f"Motivation Letter {id} not found")



# 665b846d878c6c960e48586d