from core.config import settings
from httpx import AsyncClient


async def test_get_access_token(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_USER,
        "password": settings.FIRST_USER_PASSWORD,
    }
    res = await client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = res.json()
    assert res.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


async def test_get_access_token_incorrect_password(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_USER,
        "password": "incorrect",
    }
    res = await client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    assert res.status_code == 400


async def test_use_access_token(
    client: AsyncClient, first_user_token_headers: dict[str, str]
) -> None:
    res = await client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=first_user_token_headers,
    )
    result = res.json()
    assert res.status_code == 200
    assert "email" in result
