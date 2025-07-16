from unittest.mock import MagicMock
import pytest
from sqlalchemy import Connection

from app.storages.pg.base import engine, Session


@pytest.fixture(
    scope="session",
)
def logger() -> MagicMock:
    return MagicMock()


@pytest.fixture(scope="session")
def connection() -> Connection:
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def session(connection: Connection) -> Session:
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
