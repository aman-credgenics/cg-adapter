from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.users import User
from app.schemas.users import UserResponse, UserSchema

router = APIRouter(prefix="/v1/user")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(payload: UserSchema, db_session: AsyncSession = Depends(get_db)):
    user = User(**payload.dict())
    await user.save(db_session)
    return user


@router.get("/", response_model=UserResponse)
async def find_user(
    name: str,
    db_session: AsyncSession = Depends(get_db),
):
    return await User.find(db_session, name)


@router.delete("/")
async def delete_user(name: str, db_session: AsyncSession = Depends(get_db)):
    user = await User.find(db_session, name)
    return await User.delete(user, db_session)
