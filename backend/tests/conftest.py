from collections.abc import Generator

import pytest
from core.config import settings
from core.db import engine, init_db
from fastapi.testclient import TestClient
from main import app
from models import User
from sqlmodel import Session, delete

from tests.utils import authentication_token_from_username, get_first_user_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(User)
        session.exec(statement)  # type: ignore
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_username(
        client=client, username=settings.FIRST_USER, db=db
    )


@pytest.fixture(scope="module")
def first_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return get_first_user_token_headers(client=client)
