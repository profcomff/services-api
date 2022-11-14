from sqlalchemy.orm import Session
from models import CRUD, buttons, categories
from models.database import engine


def get_button(db: Session, button_id: int):
    return db.query(buttons.Button).filter(buttons.Button.id == button_id).first()


def get_buttons(db: Session, skip: 0, limit: int = 100):
    return db.query(buttons.Button).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return db.query(categories.Category).filter(categories.Category.id == category_id).first()


def get_categories(db: Session, skip: int, limit: int):
    return db.query(categories.Category).offset(skip).limit(limit).all()


def create_button(db: Session, button: CRUD.ButtonCreate):
    db_button = buttons.Button(id=button.id, category_id=button.category_id,
                               name=button.name, icon={"src": button.icon})
    try:
        db.add(db_button)
        db.commit()
        db.refresh(db_button)
        return db_button
    except:
        print('Кнопка уже существует или неверно указан параметр категории')
    db.close()


def create_category(db: Session, category: CRUD.CategoryCreate):
    db_category = categories.Category(id=category.id, category_id=category.category_id,
                                      type=category.type, name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()
    return db_category


def delete_button(db: Session, button_id: int):
    delete = db.query(buttons.Button).filter(buttons.Button.id == button_id).first()
    try:
        db.delete(delete)
        db.commit()
    except:
        raise ValueError('Object doesn`t exist')
    db.close()


def delete_category(db: Session, category_id: int):
    delete = db.query(categories.Category).filter(categories.Category.id == category_id).first()
    try:
        db.delete(delete)
        db.commit()
    except:
        raise ValueError('Object doesn`t exist')
    db.close()


def update_button(db: Session, button_id: int, object: str, value: str):
    button = db.query(buttons.Button).filter(buttons.Button.id == button_id).first()
    if not button:
        raise ValueError('Object doesn`t exist')
    category_id = button.category_id
    if object == 'category':
        value = int(value)
        delete_button(db=Session(bind=engine), button_id=button_id)
        create_button(db=Session(bind=engine), button=CRUD.ButtonCreate(
                      id=button_id, category_id=value, name=button.name, icon=button.icon))
    elif object == 'name':
        icon = button.icon
        delete_button(db=Session(bind=engine), button_id=button_id)
        create_button(db=Session(bind=engine), button=CRUD.ButtonCreate(
            id=button_id, category_id=category_id, name=value, icon=icon))

    elif object == 'icon':
        name = button.name
        delete_button(db=Session(bind=engine), button_id=button_id)
        create_button(db=Session(bind=engine), button=CRUD.ButtonCreate(
                            id=button_id, category_id=category_id, name=name, icon=value))
    else:
        raise ValueError('Invalid object')


# ТЕСТЫ CRUD РУЧЕК (вроде работает)

# print(get_button(db=Session(bind=engine), button_id=7))
# print(get_category(db=Session(bind=engine), category_id=2))
#
# create_category(db=Session(bind=engine),
#                 category=CRUD.CategoryCreate(
#                     id=4, category_id=4, type='test', name='test'))
#
# print(get_category(db=Session(bind=engine), category_id=4))
# print(get_buttons(db=Session(bind=engine), skip=0, limit=100))
# print(get_categories(db=Session(bind=engine), skip=0, limit=100))

# create_button(db=Session(bind=engine), button=CRUD.ButtonCreate(
#     id=15, category_id=4, name='test', icon='test'))
# print(get_button(db=Session(bind=engine), button_id=15))

# delete_button(db=Session(bind=engine), button_id=15)
# print(get_button(db=Session(bind=engine), button_id=15))

# delete_category(db=Session(bind=engine), category_id=4)
# print(get_category(db=Session(bind=engine), category_id=4))
# create_button(db=Session(bind=engine), button=CRUD.ButtonCreate(
#               id=15, category_id=3, name='test', icon='test'))
# update_button(db=Session(bind=engine), button_id=15, object='category', value='3')
# print(get_button(db=Session(bind=engine), button_id=15))
