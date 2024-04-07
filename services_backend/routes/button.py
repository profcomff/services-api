import logging
from enum import Enum

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from pydantic import Field, conint

from services_backend.models.database import Button, Category, Type
from services_backend.schemas import Base


logger = logging.getLogger(__name__)
button = APIRouter()
service = APIRouter()

# region schemas


class ButtonCreate(Base):
    icon: str = Field(description='Иконка кнопки')
    name: str = Field(description='Название кнопки')
    link: str = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: Type = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')
    required_scopes: set[str] | None = Field(description='Каким скоупы нужны, чтобы кнопка была доступна', default=None)
    optional_scopes: set[str] | None = Field(description='Каким скоупы желательны', default=None)


class ButtonUpdate(Base):
    category_id: int | None = Field(description='Айди категории', default=None)
    icon: str | None = Field(description='Иконка кнопки', default=None)
    name: str | None = Field(description='Название кнопки', default=None)
    order: conint(gt=0) | None = Field(description='Порядок, в котором отображаются кнопки', default=None)
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка', default=None)
    type: Type | None = Field(
        description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер', default=None
    )
    required_scopes: set[str] | None = Field(description='Каким скоупы нужны, чтобы кнопка была доступна', default=None)
    optional_scopes: set[str] | None = Field(description='Каким скоупы желательны', default=None)


class ButtonView(Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class ButtonGet(Base):
    id: int = Field(description='Айди кнопки')
    icon: str | None = Field(description='Иконка кнопки')
    name: str | None = Field(description='Название кнопки')
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка')
    order: int | None = Field(description='Порядок, в котором отображаются кнопки')
    type: Type | None = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')
    view: ButtonView | None = Field(description='Доступна ли запрашиваемая кнопка', default=None)
    required_scopes: list[str] | None = None
    optional_scopes: list[str] | None = None
    scopes: list[str] | None = Field(description='Скоупы, которые можно запросить', default=None)


class ButtonsGet(Base):
    buttons: list[ButtonGet] | None = None


# endregion


@button.post("", response_model=ButtonGet, response_model_exclude_none=True)
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
    required_scopes = button_inp.required_scopes
    optional_scopes = button_inp.optional_scopes
    button_inp.optional_scopes = None
    button_inp.required_scopes = None
    button = Button(**button_inp.model_dump(exclude_none=True))
    button.category_id = category_id
    if last_button:
        button.order = last_button.order + 1
    if required_scopes is not None:
        button.required_scopes = required_scopes
    if optional_scopes is not None:
        button.optional_scopes = optional_scopes
    db.session.add(button)
    db.session.flush()
    return button


@button.get("", response_model=ButtonsGet, response_model_exclude_unset=True)
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
    result = {"buttons": []}
    try:
        user_scopes = {scope["name"] for scope in user["user_scopes"]}
    except TypeError:
        user_scopes = frozenset()
    for button in category.buttons:
        view = ButtonView.ACTIVE
        scopes = set()
        if button.required_scopes - user_scopes:
            view = ButtonView.BLOCKED
        else:
            scopes |= button.required_scopes
            scopes |= user_scopes & button.optional_scopes
        to_add = {
            "id": button.id,
            "icon": button.icon,
            "name": button.name,
            "link": button.link,
            "order": button.order,
            "type": button.type,
            "view": view.value,
            "required_scopes": button.required_scopes,
            "optional_scopes": button.optional_scopes,
        }
        if view == ButtonView.ACTIVE:
            to_add["scopes"] = list(scopes)
        result["buttons"].append(to_add)
    return result


@button.get("/{button_id}", response_model=ButtonGet, response_model_exclude_unset=True)
def get_button(
    button_id: int,
    category_id: int,
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показать одну кнопку

    Необходимые scopes: `-`
    """
    user_id = user.get('id') if user is not None else None
    try:
        user_scopes = {scope["name"] for scope in user["user_scopes"]}
    except TypeError:
        user_scopes = frozenset()
    logger.info(f"User {user_id} triggered get_button")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    if button.category_id != category_id:
        raise HTTPException(status_code=404, detail="Button is not this category")
    view = ButtonView.ACTIVE
    scopes = set()
    if button.required_scopes - user_scopes:
        view = ButtonView.BLOCKED
    else:
        scopes |= button.required_scopes
        scopes |= user_scopes & button.optional_scopes
    result = {
        "id": button.id,
        "icon": button.icon,
        "name": button.name,
        "link": button.link,
        "order": button.order,
        "type": button.type,
        "view": view.value,
        "required_scopes": button.required_scopes,
        "optional_scopes": button.optional_scopes,
    }
    if view == ButtonView.ACTIVE:
        result["scopes"] = list(scopes)
    return result


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
    query = db.session.query(Button).filter(Button.category_id == category_id).filter(Button.id == button_id)
    button = query.one_or_none()
    last_button = (
        db.session.query(Button).filter(Button.category_id == category_id).order_by(Button.order.desc()).first()
    )
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    if not any(button_inp.model_dump().values()):
        raise HTTPException(status_code=400, detail="Empty schema")
    if button.category_id != category_id:
        raise HTTPException(status_code=404, detail="Button is not this category")

    if button_inp.required_scopes is not None:
        button.required_scopes = button_inp.required_scopes
    if button_inp.optional_scopes is not None:
        button.optional_scopes = button_inp.optional_scopes
    db.session.flush()

    if button_inp.order and button.order != button_inp.order:
        if last_button and (button_inp.order > last_button.order):
            raise HTTPException(
                status_code=400,
                detail=f"Can`t create button with order {button_inp.order}. " f"Last category is {last_button.order}",
            )
        swapping_button = (
            db.session.query(Button)
            .filter(Button.category_id == category_id)
            .filter(Button.order == button_inp.order)
            .one()
        )
        swapping_button.order, button.order = button.order, swapping_button.order
    required_scopes = button_inp.required_scopes
    optional_scopes = button_inp.optional_scopes
    button_inp.optional_scopes = None
    button_inp.required_scopes = None
    if dump := button_inp.model_dump(exclude_unset=True, exclude_none=True):
        query.update(dump)
        db.session.flush()
    if required_scopes is not None:
        button.required_scopes = required_scopes
    if optional_scopes is not None:
        button.optional_scopes = optional_scopes
    return button


@service.get("/{button_id}", response_model=ButtonGet)
def get_service(
    button_id: int,
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показать одну кнопку

    Необходимые scopes: `-`

    TODO: Переделать ручку, сделав сервис независимым от кнопки
    """
    user_id = user.get('id') if user is not None else None
    try:
        user_scopes = {scope["name"] for scope in user["user_scopes"]}
    except TypeError:
        user_scopes = frozenset()
    logger.info(f"User {user_id} triggered get_button")
    button = db.session.query(Button).filter(Button.id == button_id).one_or_none()
    if not button:
        raise HTTPException(status_code=404, detail="Button does not exist")
    view = ButtonView.ACTIVE
    scopes = set()
    if button.required_scopes - user_scopes:
        view = ButtonView.BLOCKED
    else:
        scopes |= button.required_scopes
        scopes |= user_scopes & button.optional_scopes
    result = {
        "id": button.id,
        "icon": button.icon,
        "name": button.name,
        "link": button.link,
        "order": button.order,
        "type": button.type,
        "view": view.value,
        "required_scopes": button.required_scopes,
        "optional_scopes": button.optional_scopes,
    }
    if view == ButtonView.ACTIVE:
        result["scopes"] = list(scopes)
    return result
