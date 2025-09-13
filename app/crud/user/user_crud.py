from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.core.security import pass_settings

from fastapi import HTTPException

class UserCRUD:
    @staticmethod
    async def get_user_existing(
        db: AsyncSession,
        username: str
    ) -> bool:
        existing_user = await db.execute(
            select(User).where(
                User.username == username
            )
        )

        if existing_user.scalar_one_or_none():
            return True
        else:
            return False

    @staticmethod
    async def get_user_by_username(
        db: AsyncSession,
        username: str
    ) -> User | None:
        user = await db.execute(
            select(User).where(
                User.username == username
            )
        )

        return user.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession, 
        user_data
    ):
        is_exists = await UserCRUD.get_user_existing(
            db=db,
            username=user_data.username
        )

        if is_exists:
            raise HTTPException(
                status_code=400,
                detail='User already registered'
            )
        
        password_str = user_data.password
        hashed_password = pass_settings.get_password_hash(password_str)

        new_user = User(
            username=user_data.username,
            hashed_password=hashed_password,
            is_active=user_data.is_active
        )

        db.add(new_user)

        try:
            await db.commit()
            await db.refresh(new_user)

            return new_user
        except Exception as e:
            await db.rollback()

            raise HTTPException(
                status_code=500,
                detail=f"Error while registering user: {str(e)}"
            )