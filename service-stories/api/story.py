from pydantic import BaseModel, Field
from typing import Optional

class StoryModel(BaseModel):
    id: Optional[int] = None
    title: str = Field(json_schema_extra={"example":"bitcoin price is going up soon"})
    content: Optional[str] = Field(json_schema_extra={"example":"This is a very interesting article about bitcoin"})
    url: Optional[str] = Field(json_schema_extra={"example":"https://www.google.com"})
    poster: str = Field(json_schema_extra={"example":"123"})
