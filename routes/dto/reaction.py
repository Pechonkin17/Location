from pydantic import BaseModel, Field


class ReactionRequestInput(BaseModel):
    text: str = Field(description="Text")
    like: bool = Field(description="Like")