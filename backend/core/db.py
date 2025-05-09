from core.config import settings
from sqlmodel import Session, create_engine, select

from crud import UserCreate, create_user
from models import User

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # This works because the models are already imported and registered from models
    # SQLModel.metadata.create_all(engine)
    user = session.exec(
        select(User).where(User.username == settings.FIRST_USER)
    ).first()
    if not user:
        user_in = UserCreate(
            email="first.user@gmail.com",
            username=settings.FIRST_USER,
            password=settings.FIRST_USER_PASSWORD,
        )
        user = create_user(session=session, user_create=user_in)
