from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.monggoDB.config.db import template_collection
from src.monggoDB.models.common import PyObjectId
from src.utils.supabase_clients import get_supabase_user
from src.monggoDB.models.template import TemplateModel, TemplateCollection
from pydantic import ValidationError
from fastapi import FastAPI, Request
import json

template_router = APIRouter()

user_id ="75dcd09a-0264-4a3c-8a43-6871882f5ecf"

@template_router.post("/", response_description="Add Template", response_model=TemplateModel, status_code=status.HTTP_201_CREATED)
async def create_template(request: Request, user_id:str = Depends(get_supabase_user)):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    body_str = await request.body()
    
    try:
        # json_compatible_item_data = jsonable_encoder(request.json())
        body_dict = json.loads(body_str)
        print("Received JSON data:", body_dict)
        # template = TemplateModel(**body_dict) 
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"message": "Validation error", "details": e.errors()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    if isinstance(body_dict, dict):
        template_dict = body_dict  # Directly use the dictionary if no model instance is available.
    else:
        template_dict = TemplateModel(**body_dict) .model_dump(by_alias=True, exclude=["id"])  # If it's a model instance, dump to dict.

    template_dict["user_id"] = user_id

    new_template = await template_collection.insert_one(template_dict)
    create_template = await template_collection.find_one({"_id": new_template.inserted_id})

    return create_template

@template_router.get("/", response_description="List all jobs for a user", response_model=TemplateCollection, status_code=status.HTTP_200_OK)
# async def get_jobs_for_user(user_id:str = Depends(get_supabase_user)):
async def get_template_for_user(user_id):

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    template = await template_collection.find({"user_id": user_id}).to_list(100)
    return TemplateCollection(template=template)
