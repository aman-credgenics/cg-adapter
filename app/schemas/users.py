from uuid import UUID

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(
        title="",
        description="",
    )
    contact_number: int = Field(
        title="",
        description="",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Aman",
                "contact_number": 7424995568,
            }
        }


class UserResponse(BaseModel):
    user_id: UUID = Field(
        title="user_id",
        description="",
    )
    name: str = Field(
        title="",
        description="",
    )
    contact_number: int = Field(
        title="",
        description="",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Aman",
                "contact_number": 7524995568,
            }
        }
