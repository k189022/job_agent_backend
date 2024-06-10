from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from src.monggoDB.models.common import PyObjectId


class MotivationLetterModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    content: Optional[str]=None
    user_id: str
    job_id: Optional[str]
    company: Optional[str]= None
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            "example": {
                "id": "",
                "content": "",
                "user_id": "",
                "job_id": "",
                "company": "",
            }
        },
    )

class MotivationLetterUpdate(BaseModel):
    content: Optional[str]=None
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            "example": {
                "content": "",
            }
        },
    )

class MotivationLetterCollection(BaseModel):
    letters: List[MotivationLetterModel]