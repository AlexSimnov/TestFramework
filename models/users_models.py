from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=8, max_length=100)
    age: int = Field(..., ge=1, le=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Username не должен содержать пробелы")
        if not re.fullmatch(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError(
                "Username должен содержать только латинские буквы, цифры и '_'"
            )
        return value

    model_config = {
        "extra": "allow",
    }


class UserResponce(UserCreate):
    id: int

    model_config = {
        "from_attributes": True,
        "extra": "allow",
    }
