from fastapi import HTTPException, APIRouter, Depends
from fastapi_sqlalchemy import db

from ..settings import get_settings
from .models.button import ButtonCreate, ButtonUpdate, ButtonGet
from .models.category import CategoryGet
from ..models.database import Button, Category

from auth_lib.fastapi import UnionAuth

button = APIRouter()


@button.post("/", response_model=ButtonGet)
def create_button(button_inp: ButtonCreate, category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if not user:
        raise HTTPException(403, detail="Not authenticated")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    last_button = db.session.query(Button).order_by(Button.order.desc()).first()
    button = Button(**button_inp.dict(exclude_none=True))
    button.category_id = category_id
    if last_button:
        button.order = last_button.order + 1
    db.session.add(button)
    db.session.commit()
    return button


@button.get("/", response_model=CategoryGet)
def get_buttons(category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if user:
        category = db.session.query(Category) \
            .filter(Category.user_scope.in_(user["scopes"]) or Category.user_scope == []) \
            .filter(Category.id == category_id) \
            .one_or_none()
    else:
        category = db.session.query(Category) \
            .filter(Category.user_scope == []) \
            .filter(Category.id == category_id) \
            .one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return category


@button.get("/{button_id}", response_model=ButtonGet)
def get_button(button_id: int, category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if user:
        category = db.session.query(Category) \
            .filter(Category.user_scope.in_(user["scopes"]) or Category.user_scope == []) \
            .filter(Category.id == category_id) \
            .one_or_none()
    else:
        category = db.session.query(Category) \
            .filter(Category.user_scope == []) \
            .filter(Category.id == category_id) \
            .one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    if button.category_id != category_id:
        raise HTTPException(status_code=404, detail="Button is not this category")
    return button


@button.delete("/{button_id}", response_model=None)
def remove_button(button_id: int, category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if not user:
        raise HTTPException(403, detail="Not authenticated")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    if button.category_id != category_id:
        raise HTTPException(status_code=404, detail="Button is not in this category")
    db.session.delete(button)
    db.session.query(Button).filter(Button.order > button.order).update({"order": Button.order - 1})
    db.session.commit()


@button.patch("/{button_id}", response_model=ButtonUpdate)
def update_button(button_inp: ButtonUpdate, button_id: int, category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if not user:
        raise HTTPException(403, detail="Not authenticated")
    query = db.session.query(Button).filter(Button.id == button_id)
    button = query.one_or_none()
    last_button = (
        db.session.query(Button).filter(Button.category_id == category_id).order_by(Button.order.desc()).first()
    )
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    if not any(button_inp.dict().values()):
        raise HTTPException(status_code=400, detail="Empty schema")
    if button.category_id != category_id:
        raise HTTPException(status_code=404, detail="Button is not this category")

    if button_inp.order:
        if last_button and (button_inp.order > last_button.order + 1):
            raise HTTPException(
                status_code=400,
                detail=f"Can`t create button with order {button_inp.order}. " f"Last category is {last_button.order}",
            )
        if button_inp.order < 1:
            raise HTTPException(status_code=400, detail="Order can`t be less than 1")
        if button.order > button_inp.order:
            db.session.query(Button).filter(Button.order < button.order).update({"order": Button.order + 1})
        elif button.order < button_inp.order:
            db.session.query(Button).filter(Button.order > button.order).update({"order": Button.order - 1})

    query.update(button_inp.dict(exclude_unset=True, exclude_none=True))
    db.session.commit()
    return button
