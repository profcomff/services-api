import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from services_backend.routes.base import app
from services_backend.settings import get_settings
from services_backend.models.base import Base


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    return client



@pytest.fixture(scope="session")
def engine():
    return create_engine(
        get_settings().DB_DSN, execution_options={"isolation_level": "AUTOCOMMIT"}
    )


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def dbsession(engine, tables):
    connection = engine.connect()
    session = Session(bind=connection, autoflush=True)
    yield session
    session.close()
    connection.close()
