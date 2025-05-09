from sqlalchemy import NullPool
from core.config import settings
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from crud import UserCreate, create_user
from models import User

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), poolclass=NullPool)


# make sure all SQLModel models are imported (models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


async def init_db(session: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # This works because the models are already imported and registered from models
    # SQLModel.metadata.create_all(engine)
    stmt = await session.exec(select(User).where(User.username == settings.FIRST_USER))
    if not stmt.first():
        user_in = UserCreate(
            email="first.user@gmail.com",
            username=settings.FIRST_USER,
            password=settings.FIRST_USER_PASSWORD,
        )
        await create_user(session=session, user_create=user_in)
