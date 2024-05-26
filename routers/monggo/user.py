from fastapi import APIRouter, HTTPException, Response, status, Body
from bson import ObjectId
from pymongo import ReturnDocument

from monggoDB.config.db import users_collection
from monggoDB.models.user import UserCollection, UserModel, UserUpdateModel
# User Router
user_router = APIRouter()



@user_router.post(
        "/users/", 
        response_description="Add new user", 
        response_model=UserModel, 
        status_code=status.HTTP_201_CREATED,)
async def create_user(user: UserModel = Body(...)):
    """
    Insert Student Data
    """
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id": new_user.inserted_id})
    return created_user


@user_router.get("/users/", response_description="Get a single user", response_model=UserCollection)
async def get_users():
    return UserCollection(users= await users_collection.find().to_list(100))  # Ensure correct serialization


@user_router.get(
    "/users/{id}",
    response_description="Get a single User",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def show_user(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        student := await users_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

@user_router.put(
    "/users/{id}",
    response_description="Update a User",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def update_user(id: str, user: UserUpdateModel = Body(...)):

    user = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }

    if len(user) >= 1:
        update_result = await users_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"user {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := await users_collection.find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@user_router.delete("/users/{id}", response_description="Delete a User")
async def delete_user(id: str):
    """
    Remove a single User from the database.
    """
    delete_result = await users_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")