import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from services_backend.models.base import Base
from services_backend.routes.base import app
from services_backend.settings import get_settings


@pytest.fixture()
def client(mocker: MockerFixture):
    user_mock = mocker.patch('auth_lib.fastapi.UnionAuth.__call__')
    user_mock.return_value = {
        "session_scopes": [{"id": 0, "name": "string", "comment": "string"}],
        "user_scopes": [{"id": 0, "name": "string", "comment": "string"}],
        "indirect_groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "id": 0,
        "email": "string",
    }
    client = TestClient(app)
    return client


@pytest.fixture(scope='session')
def dbsession() -> Session:
    settings = get_settings()
    engine = create_engine(str(settings.DB_DSN), execution_options={"isolation_level": "AUTOCOMMIT"})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
