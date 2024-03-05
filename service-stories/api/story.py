from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any


class StoryModel(BaseModel):
    id: Optional[int] = None
    title: str = Field(json_schema_extra={"example": "bitcoin price is going up soon"})
    content: Optional[str] = Field(
        default="",
        json_schema_extra={"example": "This is a very interesting article about bitcoin"},
    )
    url: Optional[str] = Field(default="", json_schema_extra={"example": "https://www.google.com"})
    poster: str = Field(json_schema_extra={"example": "123"})

    @model_validator(mode="after")
    def check_url_or_content(self) -> "StoryModel":
        if not self.url and not self.content:
            raise ValueError("Either url or content must be set.")
        return self
