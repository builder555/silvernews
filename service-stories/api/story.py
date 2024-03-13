from pydantic import BaseModel, Field, model_validator
from typing import Optional


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
    def check_url_or_content(self):
        if not self.url and not self.content:
            raise ValueError("Either url or content must be set.")
        return self


class CommentModel(BaseModel):
    id: Optional[int] = None
    content: str = Field(
        json_schema_extra={"example": "This is a very interesting article about bitcoin"}
    )
    poster: str = Field(json_schema_extra={"example": "123"})
    parent: Optional[int] = None
