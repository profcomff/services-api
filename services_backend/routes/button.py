from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db

from .models.button import ButtonCreate, ButtonUpdate, ButtonGet
from ..models.database import Button

button = APIRouter(
    tags=["button"],
    responses={404: {"description": "You tried, but no"}}
)


@button.post("/", response_model=ButtonCreate)
def create_button(button: ButtonCreate):
    db_button = ButtonCreate(category_id=button.category_id, name=button.name,
                             icon=button.icon)
    db.session.add(db_button)
    return db_button


@button.get("/", response_model=list[ButtonGet])
def get_buttons(skip: int = 0, limit: int = 100):
    return db.session.query(Button).offset(skip).limit(limit).all()


@button.get("/{button_id}", response_model=ButtonGet)
def get_button(button_id: int):
    return db.session.query(Button).filter(Button.id == button_id).first()


@button.delete("/")
def remove_button(button_id: int):
    db_button = get_button(button_id=button_id, db=db)
    if db_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    db.session.query(Button).filter(Button.id == button_id).first()


@button.patch("/", response_model=ButtonUpdate)
def update_button(button: ButtonUpdate):
    db_old_button = get_button(button_id=button.id, db=db)
    if db_old_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return db.session.query(Button).update(button)
