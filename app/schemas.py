from pydantic import BaseModel, Field


class Validating(BaseModel):
    text : str = Field(min_length=1)