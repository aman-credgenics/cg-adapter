import uuid

from fastapi import HTTPException, status
from sqlalchemy import Column, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, autoincrement=True)
    name = Column(String, nullable=False, primary_key=True, unique=True)
    contact_number = Column()

    @classmethod
    async def find(cls, db_session: AsyncSession, name: str):
        """

        :param db_session:
        :param name:
        :return:
        """
        stmt = select(cls).where(cls.name == name)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Record not found": f"There is no record for requested name value : {name}"},
            )
        else:
            return instance