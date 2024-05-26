from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.monggoDB.config import db
from src.monggoDB.models.motivationLetter import MotivationLetterModel



# Motivation Letter Router
motivation_letter_router = APIRouter()

@motivation_letter_router.post("/", response_description="Add new motivation letter", response_model=MotivationLetterModel)
async def create_motivation_letter(motivation_letter: MotivationLetterModel):
    motivation_letter = jsonable_encoder(motivation_letter)
    new_motivation_letter = await db["motivation_letters"].insert_one(motivation_letter)
    created_motivation_letter = await db["motivation_letters"].find_one({"_id": new_motivation_letter.inserted_id})
    return JSONResponse(status_code=201, content=created_motivation_letter)

@motivation_letter_router.get("/{id}", response_description="Get a single motivation letter", response_model=MotivationLetterModel)
async def get_motivation_letter(id: str):
    if (motivation_letter := await db["motivation_letters"].find_one({"_id": ObjectId(id)})) is not None:
        return jsonable_encoder(motivation_letter)  # Ensure correct serialization
    raise HTTPException(status_code=404, detail=f"Motivation Letter {id} not found")

@motivation_letter_router.put("/{id}", response_description="Update a motivation letter", response_model=MotivationLetterModel)
async def update_motivation_letter(id: str, motivation_letter: MotivationLetterModel):
    motivation_letter = {k: v for k, v in motivation_letter.dict().items() if v is not None}
    if len(motivation_letter) >= 1:
        update_result = await db["motivation_letters"].update_one({"_id": ObjectId(id)}, {"$set": motivation_letter})
        if update_result.modified_count == 1:
            if (updated_motivation_letter := await db["motivation_letters"].find_one({"_id": ObjectId(id)})) is not None:
                return jsonable_encoder(updated_motivation_letter)  # Ensure correct serialization
    if (existing_motivation_letter := await db["motivation_letters"].find_one({"_id": ObjectId(id)})) is not None:
        return jsonable_encoder(existing_motivation_letter)  # Ensure correct serialization
    raise HTTPException(status_code=404, detail=f"Motivation Letter {id} not found")

@motivation_letter_router.delete("/{id}", response_description="Delete a motivation letter")
async def delete_motivation_letter(id: str):
    delete_result = await db["motivation_letters"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=204)
    raise HTTPException(status_code=404, detail=f"Motivation Letter {id} not found")
