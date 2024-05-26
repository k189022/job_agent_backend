from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.monggoDB.models.common import PyObjectId

class ResumeModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=None, alias="_id")
    resume: Optional[bytes] = None  # Change to bytes
    user_id:str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "",
                "resume": "this is an example in binary",
                "user_id": "automaatic"
            }
        },
    )

class ResumeUpdateModel(BaseModel):
    resume: Optional[bytes] = None  # Change to bytes
    user_id: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "id": "",
                "resume": "this is an example in binary",
                "user_id": "automatic"
            }
        },
    )

class ResumeCollection(BaseModel):
    users: List[ResumeModel]
