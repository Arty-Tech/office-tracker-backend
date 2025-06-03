from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from uuid import UUID

class CRUDUser:
    async def get(self, db: AsyncSession, user_id: str):
        result = await db.execute(select(User).where(User.id == UUID(user_id)))
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, db: AsyncSession, user_in: UserCreate, hashed_password: str):
        user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            nome=user_in.nome,
            preferences={
                "workDuration": 25,
                "breakDuration": 5,
                "soundUrl": "/audio/bell.mp3"
            }
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

crud_user = CRUDUser()