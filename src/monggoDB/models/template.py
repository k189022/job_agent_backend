from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from src.monggoDB.models.common import PyObjectId

class TemplateModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=None, alias="_id")
    user_id:str
    content:str
    # class Config:
    #     orm_mode = True
    #     use_enum_values = True
    #     anystr_strip_whitespace = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed=True,
        orm_mode= True,
        allow_population_by_field_name = True,
        extra= "ignore",
        json_schema_extra={
            "example": {
                "id": "",
                "content": "",
                "user_id": ""
            }
        }
    )

class TemplateUpdateModel(BaseModel):
    user_id:str
    content:str
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "",
                "content": "",
                "user_id": "automaatic"
            }
        }
    )
        

class TemplateCollection(BaseModel):
    template: List[TemplateModel]
    