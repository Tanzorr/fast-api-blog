from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, make_url, text
from sqlalchemy.orm import Session, sessionmaker

from database import Base, get_db, settings
from main import app

TEST_DB_NAME = f"{settings.postgres_db}_test"
TEST_DATABASE_URL = make_url(settings.database_url).set(database=TEST_DB_NAME)


def create_test_database() -> None:
    """Create the test database on the same PostgreSQL server, if it is missing."""
    # CREATE DATABASE cannot run inside a transaction, so we use AUTOCOMMIT.
    admin_engine = create_engine(settings.database_url, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        exists = conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": TEST_DB_NAME},
        )
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    admin_engine.dispose()


@pytest.fixture(scope="session")
def test_engine():
    create_test_database()
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db(test_engine) -> Iterator[Session]:
    session = sessionmaker(bind=test_engine, autoflush=False)()
    yield session
    session.close()
    # Empty every table, so the next test starts clean.
    tables = ", ".join(table.name for table in Base.metadata.sorted_tables)
    with test_engine.begin() as conn:
        conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))


@pytest.fixture
def client(db: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db
    # Not `with TestClient(app)`: that runs lifespan, which would call
    # create_all() on the development database.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def new_user(client: TestClient) -> dict:
    payload = {"email": "ann@example.com", "password": "secret-123"}
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    return {**response.json(), "password": payload["password"]}
