import pytest
from services_backend.models.database import Button, Category


@pytest.fixture
def db_category(dbsession):
    category = Category(name='categoty', type='some-type')
    dbsession.add(category)
    dbsession.commit()
    category = dbsession.query(Category).filter(Category.id == category.id).one_or_none()
    yield category
    for button in dbsession.query(Button).filter(Button.category_id == category.id).all():
        dbsession.delete(button)
        dbsession.flush()
    dbsession.delete(category)
    dbsession.commit()


@pytest.fixture
def db_button(dbsession, db_category):
    _button = Button(name='button', category_id=db_category.id, icon='test', link='g', type='d')
    dbsession.add(_button)
    dbsession.commit()
    _button = dbsession.query(Button).filter(Button.id == _button.id).one_or_none()
    yield _button
    if _button:
        dbsession.delete(_button)
    dbsession.commit()
