from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from monggoDB.models.common import PyObjectId


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=None, alias="_id")
    email: EmailStr
    resume: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "",
                "email": "jdoe@example.com",
                "resume": "this is example",
            }
        },
    )

class UserUpdateModel(BaseModel):
    email: Optional[EmailStr] = None
    resume: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "id": "",
                "email": "jdoe@example.com",
                "resume": "this is example",
            }
        },
    )



class UserCollection(BaseModel):
    users: List[UserModel]