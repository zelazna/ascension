import random
import string

import crud
from core.config import settings
from httpx import AsyncClient
from models import User, UserCreate, UserUpdate
from sqlmodel.ext.asyncio.session import AsyncSession


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def create_random_user(db: AsyncSession) -> User:
    user_in_create = UserCreate(
        email=random_email(),
        password=random_lower_string(),
        username=random_lower_string(),
    )
    return await crud.create_user(session=db, user_create=user_in_create)


async def user_authentication_headers(
    *, client: AsyncClient, username: str, password: str
) -> dict[str, str]:
    data = {"username": username, "password": password}

    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def get_first_user_token_headers(client: AsyncClient) -> dict[str, str]:
    return await user_authentication_headers(
        client=client,
        username=settings.FIRST_USER,
        password=settings.FIRST_USER_PASSWORD,
    )


async def authentication_token_from_username(
    *, client: AsyncClient, username: str, db: AsyncSession
) -> dict[str, str]:
    """
    Return a valid token for the user with given username.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await crud.get_user_by_username(session=db, username=username)
    if not user:
        user_in_create = UserCreate(
            email=random_email(), username=username, password=password
        )
        user = await crud.create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = await crud.update_user(session=db, db_user=user, user_in=user_in_update)

    return await user_authentication_headers(
        client=client, username=user.username, password=password
    )
