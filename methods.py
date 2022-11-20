from sqlalchemy.orm import Session
from models import CRUD, buttons, categories


def get_button(db: Session, button_id: int):
    return db.query(buttons.Button).filter(buttons.Button.id == button_id).first()


def get_buttons(db: Session, skip: 0, limit: int = 100):
    return db.query(buttons.Button).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return db.query(categories.Category).filter(categories.Category.id == category_id).first()


def get_categories(db: Session, skip: int, limit: int):
    return db.query(categories.Category).offset(skip).limit(limit).all()


def create_button(db: Session, button: CRUD.Button):
    db_button = buttons.Button(id=button.id, category_id=button.category_id,
                               name=button.name, icon=button.icon)
    db.add(db_button)
    db.commit()
    db.refresh(db_button)
    db.close()

    return db_button


def create_category(db: Session, category: CRUD.Category):
    db_category = categories.Category(id=category.id, category_id=category.category_id,
                                      type=category.type, name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()
    return db_category


def delete_button(db: Session, button_id: int):
    delete = db.query(buttons.Button).filter(buttons.Button.id == button_id).first()
    db.delete(delete)
    db.commit()
    db.close()
    return delete


def delete_category(db: Session, category_id: int):
    delete = db.query(categories.Category).filter(categories.Category.id == category_id).first()
    d = db.query(buttons.Button).filter(buttons.Button.category_id == category_id).all()
    for button in d:
        db.delete(button)
        db.commit()
    db.delete(delete)
    db.commit()
    db.close()

    return delete


def update_button(db: Session, button_id: int, button: CRUD.Button):
    # old_button = db.query(buttons.Button).filter(buttons.Button.id == button_id).first()
    # new_button = buttons.Button(id=button.id, category_id=button.category_id,
    #                             name=button.name, icon=button.icon)
    # delete_button(db=db, button_id=old_button.id)
    # create_button(db=db, button=new_button)

    db.query(buttons.Button).update(button)

    return button


def update_category(db: Session, category_id: int, category: CRUD.Category):
    old_category = db.query(buttons.Button).filter(buttons.Button.id == category_id).first()
    new_category = categories.Category(id=category.id, category_id=category.category_id,
                                       name=category.name, type=category.type)
    delete_category(db=db, category_id=old_category.id)
    create_category(db=db, category=new_category)

    return new_category
