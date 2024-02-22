from pydantic import BaseModel, Field

from ..pyobjectid import PyObjectId


class ObjectIdDoc(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
