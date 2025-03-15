from pydantic import BaseModel, Field


class UserPutRequestInput(BaseModel):
    username: str = Field(description="Username")
    email: str = Field(description="Email")
    password: str = Field(description="Password")