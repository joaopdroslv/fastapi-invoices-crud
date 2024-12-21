from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    class ConfigDict:
        from_attributes = True


class UserRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=255)
    last_name: str = Field(min_length=3, max_length=255)
