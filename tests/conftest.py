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


@pytest.fixture(scope='session')
def dbsession() -> Session:
    settings = get_settings()
    engine = create_engine(settings.DB_DSN, execution_options={"isolation_level": "AUTOCOMMIT"})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)