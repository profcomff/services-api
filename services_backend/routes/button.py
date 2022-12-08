from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db

from .models.button import ButtonCreate, ButtonUpdate, ButtonGet
from ..models.database import Button, Category

button = APIRouter()


@button.post("/", response_model=ButtonGet)
def create_button(button_inp: ButtonCreate):
    category = db.session.query(Category).filter(Category.id == button_inp.category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    button = Button(**button_inp.dict())
    db.session.add(button)
    db.session.flush()
    return button


@button.get("/", response_model=list[ButtonGet])
def get_buttons(offset: int = 0, limit: int = 100):
    return db.session.query(Button).offset(offset).limit(limit).all()


@button.get("/{button_id}", response_model=ButtonGet)
def get_button(button_id: int):
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return button


@button.delete("/{button_id}", response_model=None)
def remove_button(button_id: int):
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    db.session.delete(button)
    db.session.flush()

 
@button.patch("/{button_id}", response_model=ButtonGet)
def update_button(button_inp: ButtonUpdate, button_id: int):
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    button.category_id = button_inp.category_id or button.category_id
    button.icon = button_inp.icon or button.icon
    button.name = button_inp.name or button.name
    db.session.flush()
    return button
