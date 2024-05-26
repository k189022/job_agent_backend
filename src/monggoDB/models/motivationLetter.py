from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.monggoDB.models.common import PyObjectId


class MotivationLetterModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    content: str
    user_id: PyObjectId
    job_id: PyObjectId

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}