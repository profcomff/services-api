import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from pydantic import Field

from services_backend.models.database import Button, Category, Type
from services_backend.schemas import Base


logger = logging.getLogger(__name__)
button = APIRouter()

# region schemas


class ButtonCreate(Base):
    icon: str = Field(description='Иконка кнопки')
    name: str = Field(description='Название кнопки')
    link: str = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: Type = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')


class ButtonUpdate(Base):
    category_id: int | None = Field(description='Айди категории', default=None)
    icon: str | None = Field(description='Иконка кнопки', default=None)
    name: str | None = Field(description='Название кнопки', default=None)
    order: int | None = Field(description='Порядок, в котором отображаются кнопки', default=None)
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка', default=None)
    type: Type | None = Field(
        description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер', default=None
    )


class ButtonGet(Base):
    id: int = Field(description='Айди кнопки')
    icon: str | None = Field(description='Иконка кнопки')
    name: str | None = Field(description='Название кнопки')
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка')
    order: int | None = Field(description='Порядок, в котором отображаются кнопки')
    type: Type | None = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')


class ButtonsGet(Base):
    buttons: list[ButtonGet] | None = None


# endregion


@button.post("", response_model=ButtonGet)
def create_button(
    button_inp: ButtonCreate,
    category_id: int,
    user=Depends(UnionAuth(['services.button.create'])),
):
    """Создать кнопку

    Необходимые scopes: `services.button.create`
    """
    logger.info(f"User {user.get('id')} triggered create_button")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    last_button = (
        db.session.query(Button).filter(Button.category_id == category_id).order_by(Button.order.desc()).first()
    )
    button = Button(**button_inp.dict(exclude_none=True))
    button.category_id = category_id
    if last_button:
        button.order = last_button.order + 1
    db.session.add(button)
    db.session.flush()
    return button


@button.get("", response_model=ButtonsGet)
def get_buttons(
    category_id: int,
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показать все кнопки в категории

    Необходимые scopes: `-`
    """
    user_id = user.get('id') if user is not None else None
    logger.info(f"User {user_id} triggered get_buttons")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return category


@button.get("/{button_id}", response_model=ButtonGet)
def get_button(
    button_id: int,
    category_id: int,
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показать одну кнопку

    Необходимые scopes: `-`
    """
    user_id = user.get('id') if user is not None else None
    logger.info(f"User {user_id} triggered get_button")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    if button.category_id != category_id:
        raise HTTPException(status_code=404, detail="Button is not this category")
    return button


@button.delete("/{button_id}", response_model=None)
def remove_button(
    button_id: int,
    category_id: int,
    user=Depends(UnionAuth(['services.button.delete'])),
):
    """Удалить кнопку

    Необходимые scopes: `services.button.remove`
    """
    logger.info(f"User {user.get('id')} triggered create_category")
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
    db.session.flush()


@button.patch("/{button_id}", response_model=ButtonUpdate)
def update_button(
    button_inp: ButtonUpdate,
    button_id: int,
    category_id: int,
    user=Depends(UnionAuth(['services.button.update'])),
):
    """Обновить кнопку

    Необходимые scopes: `services.button.update`
    """
    logger.info(f"User {user.get('id')} triggered create_category")
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
    db.session.flush()
    return button
