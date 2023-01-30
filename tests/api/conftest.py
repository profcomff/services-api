import pytest
import sqlalchemy

from services_backend.models.database import Button, Category


@pytest.fixture
def db_category(dbsession):
    q = sqlalchemy.insert(Category).values(id=666, name='category', type='some-type', order=0).returning(Category)
    _category = dbsession.scalar(q)
    dbsession.flush()
    yield _category
    query = dbsession.query(Category).filter(Category.id == _category.id)
    if query.one_or_none():
        dbsession.delete(query.one())
    dbsession.flush()


@pytest.fixture
def db_button(dbsession, db_category):
    q = sqlalchemy.insert(Button).values(id=42, name='button', category_id=db_category.id, order="32").returning(Button)
    _button = dbsession.scalar(q)
    dbsession.flush()
    yield _button
    query = dbsession.query(Button).filter(Button.id == _button.id)
    if query.one_or_none():
        dbsession.delete(query.one())
    dbsession.flush()
