import crud
import pytest
from core.security import verify_password
from fastapi.encoders import jsonable_encoder
from models import User, UserCreate, UserUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from tests.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, username=random_lower_string())
    user = await crud.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


async def test_authenticate_user(db: AsyncSession) -> None:
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreate(email=random_email(), password=password, username=username)
    user = await crud.create_user(session=db, user_create=user_in)
    authenticated_user = await crud.authenticate(
        session=db, password=password, username=username
    )
    assert authenticated_user
    assert user.username == authenticated_user.username


async def test_not_authenticate_user(db: AsyncSession) -> None:
    password = random_lower_string()
    username = random_lower_string()
    user = await crud.authenticate(session=db, password=password, username=username)
    assert user is None


async def test_get_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=email, password=password, username=username)
    user = await crud.create_user(session=db, user_create=user_in)
    user_2 = await db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


async def test_update_user(db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    username = random_email()
    user_in = UserCreate(email=email, password=password, username=username)
    user = await crud.create_user(session=db, user_create=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password)
    await crud.update_user(session=db, db_user=user, user_in=user_in_update)
    user_2 = await db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
