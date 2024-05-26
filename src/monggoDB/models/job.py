from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from bson import ObjectId

from src.monggoDB.models.common import PyObjectId

class JobModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    user_id: str
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            "example": {
                "id": "",
                "title": "optional",
                "company": "optional",
                "description": "optional",
                "skills": "optional",
                "location": "optional",
                "url": "optional",
                "user_id": "",
            }
        },
    )

class JobCollection(BaseModel):
    jobs: List[JobModel]  # Correctly annotate with a type
