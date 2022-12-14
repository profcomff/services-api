import pytest
from services_backend.models.database import Button, Category


@pytest.fixture
def db_category(dbsession):
    _category = Category(id=1, name='categoty', type='some-type')
    dbsession.add(_category)
    dbsession.flush()
    yield _category
    query = dbsession.query(Category).filter(Category.id == _category.id)
    dbsession.delete(query.one())
    dbsession.flush()


@pytest.fixture
def db_button(dbsession, db_category):
    _button = Button(id=42, name='button', category_id=db_category.id)
    dbsession.add(_button)
    dbsession.flush()
    yield _button
    query = dbsession.query(Button).filter(Button.id == _button.id)
    dbsession.delete(query.one())
    dbsession.flush()


