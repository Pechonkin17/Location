from pydantic import BaseModel, Field

class RegisterRequestInput(BaseModel):
    username: str = Field(description="Username")
    email: str = Field(description="Email")
    password: str = Field(description="Password")


class LoginRequestInput(BaseModel):
    email: str = Field(description="Email")
    password: str = Field(description="Password")


class ResetPasswordRequestInput(BaseModel):
    email: str = Field(description="Email")
    password: str = Field(description="Password")