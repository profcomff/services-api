from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db

from .models.button import ButtonCreate, ButtonUpdate, ButtonGet
from ..models.database import Button, Category
from .category import get_category

button = APIRouter(
    tags=["button"],
    responses={200: {"description": "Ok"}}
)


@button.post("/", response_model=ButtonCreate)
def create_button(button: ButtonCreate):
    db_category = db.session.query(Category).filter(Category.id == button.category_id).one_or_none()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    db_button = Button(category_id=button.category_id, name=button.name,
                             icon=button.icon)
    db.session.add(db_button)
    db.session.flush()
    return db_button


@button.get("/", response_model=list[ButtonGet])
def get_buttons(skip: int = 0, limit: int = 100):
    return db.session.query(Button).offset(skip).limit(limit).all()


@button.get("/{button_id}", response_model=ButtonGet)
def get_button(button_id: int):
    db_button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if db_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return db_button


@button.delete("/")
def remove_button(button_id: int):
    db_button = get_button(button_id=button_id)
    if db_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    db.session.delete(db_button)
    db.session.flush()

 
@button.patch("/{button_id}", response_model=ButtonGet)
def update_button(button: ButtonUpdate, button_id: int):
    db_old_button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if db_old_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    db_old_button.category_id = button.category_id or db_old_button.category_id
    db_old_button.icon = button.icon or db_old_button.icon
    db_old_button.name = button.name or db_old_button.name
    db.session.flush()

    return db_old_button

