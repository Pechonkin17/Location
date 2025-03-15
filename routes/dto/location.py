from pydantic import BaseModel, Field


class LocationRequestInput(BaseModel):
    name: str = Field(description="Name")
    description: str = Field(description="Description")
    category: str = Field(description="Category")


class LocationSelectedRatingInput(BaseModel):
    rating: float = Field(description="Rating")