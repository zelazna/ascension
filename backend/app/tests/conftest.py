from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlmodel import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import User
from app.tests.utils import (authentication_token_from_username,
                             get_first_user_token_headers)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        await init_db(session)
        yield session
        statement = delete(User)
        await session.exec(statement)  # type: ignore
        await session.commit()


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.fixture(scope="module")
async def normal_user_token_headers(
    client: AsyncClient, db: AsyncSession
) -> dict[str, str]:
    return await authentication_token_from_username(
        client=client, username=settings.FIRST_USER, db=db
    )


@pytest.fixture()
async def first_user_token_headers(
    client: AsyncClient, db: AsyncSession
) -> dict[str, str]:
    return await get_first_user_token_headers(client=client)
