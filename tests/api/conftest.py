import pytest
from services_backend.models.database import Button, Category


@pytest.fixture
def db_category(dbsession):
    category = Category(id=666, name='categoty', type='some-type', order=1)
    dbsession.add(category)
    dbsession.flush()
    dbsession.commit()
    yield category
    query = dbsession.query(Category).filter(Category.id == category.id).one_or_none()
    if query:
        for button in dbsession.query(Button).filter(Button.category_id == category.id).all():
            dbsession.delete(button)
        dbsession.delete(query)
        dbsession.commit()


@pytest.fixture
def db_button(dbsession, db_category):
    _button = Button(id=42, name='button', category_id=db_category.id, order=1, icon='test', link='g', type='d')
    dbsession.add(_button)
    dbsession.commit()
    yield _button
    query = dbsession.query(Button).filter(Button.id == _button.id).one_or_none()
    if query:
        dbsession.delete(query)
        dbsession.commit()
