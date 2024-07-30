import logging
from typing import Literal

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_sqlalchemy import db
from pydantic import Field, conint

from services_backend.models.database import Button, Category
from services_backend.schemas import Base

from .button import ButtonGet, ButtonView


logger = logging.getLogger(__name__)
category = APIRouter()


# region schemas


class CategoryCreate(Base):
    type: str = Field(description='Тип отображения категории')
    name: str = Field(description='Имя категории')
    scopes: set[str] | None = Field(description='Каким пользователям будет видна категория', default=None)


class CategoryUpdate(Base):
    order: conint(gt=0) | None = Field(description='На какую позицию перенести категорию', default=None)
    type: str | None = Field(description='Тип отображения категории', default=None)
    name: str | None = Field(description='Имя категории', default=None)
    scopes: set[str] | None = Field(description='Каким пользователям будет видна категория', default=None)


class CategoryGet(Base):
    id: int
    order: int
    type: str | None = None
    name: str | None = None
    buttons: list[ButtonGet] | None = None
    scopes: list[str] | None = None


# endregion

# region routes


@category.post("", response_model=CategoryGet)
def create_category(
    category_inp: CategoryCreate,
    user=Depends(UnionAuth(['services.category.create'])),
):
    """Создает категорию

    Необходимые scopes: `services.category.create`
    """
    logger.info(f"User {user.get('id')} triggered create_category")
    last_category = db.session.query(Category).order_by(Category.order.desc()).first()
    scopes = category_inp.scopes
    category_inp.scopes = None
    category = Category(**category_inp.model_dump(exclude_none=True))
    if scopes is not None:
        category.scopes = scopes
    if last_category:
        category.order = last_category.order + 1
    db.session.add(category)
    db.session.commit()
    return category


@category.get("", response_model=list[CategoryGet], response_model_exclude_none=True)
def get_categories(
    info: list[Literal['buttons']] = Query([]),
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показывает список категорий

    Необходимые scopes: `-`
    """
    user_id = user.get('id') if user is not None else None
    if user_id is None:
        logger.info("Unauthorised user triggered get_categories")
    else:
        logger.info(f"User {user_id} triggered get_categories")
    try:
        user_scopes = {scope["name"] for scope in user["user_scopes"]}
    except TypeError:
        user_scopes = frozenset()

    session_scopes = set([scope["name"] for scope in user["session_scopes"]] if user else [])
    filtered_categories = []
    for category in db.session.query(Category).order_by(Category.order).all():
        category_scopes = set(category.scopes)
        if (category_scopes == set()) or len(category_scopes - session_scopes) == 0:
            filtered_categories.append(category)
    if 'buttons' not in info:
        return [CategoryGet.model_validate(row).model_dump(exclude={"buttons"}) for row in filtered_categories]
    result = []
    for row in filtered_categories:
        category = {
            "id": row.id,
            "order": row.order,
            "type": row.type,
            "name": row.name,
            "scopes": row.scopes,
            "buttons": [],
        }
        for button in row.buttons:
            view = ButtonView.ACTIVE
            scopes = set()
            if button.required_scopes - user_scopes:
                view = ButtonView.BLOCKED
            else:
                scopes |= button.required_scopes
                scopes |= user_scopes & button.optional_scopes
            category["buttons"].append(
                {
                    "id": button.id,
                    "icon": button.icon,
                    "name": button.name,
                    "link": (button.link if view == ButtonView.ACTIVE else None),
                    "order": button.order,
                    "type": button.type,
                    "view": view.value,
                    "scopes": list(scopes) if view == ButtonView.ACTIVE else None,
                    "required_scopes": button.required_scopes,
                    "optional_scopes": button.optional_scopes,
                }
            )
        result.append(category)
    return result


@category.get("/{category_id}", response_model=CategoryGet, response_model_exclude_none=True)
def get_category(
    category_id: int,
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показывает категорию

    Необходимые scopes: `-`
    """
    user_id = user.get('id') if user is not None else None
    if user_id is None:
        logger.info("Unauthorised user triggered get_category")
    else:
        logger.info(f"User {user_id} triggered get_category")

    user_scopes = set([scope["name"] for scope in user["session_scopes"]] if user else [])
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category or (category.scopes and len(category.scopes - user_scopes) != 0):
        raise HTTPException(status_code=404, detail="Category does not exist")
    return {
        "id": category_id,
        "order": category.order,
        "name": category.name,
        "type": category.type,
        "scopes": category.scopes,
    }


@category.delete("/{category_id}", response_model=None)
def remove_category(
    category_id: int,
    user=Depends(UnionAuth(['services.category.delete'])),
):
    """Удаляет категорию и все кнопки в ней

    Необходимые scopes: `services.category.delete`
    """
    user_id = user.get('id') if user is not None else None
    logger.info(f"User {user_id} triggered remove_category")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    for button in db.session.query(Button).filter(Button.category_id == category_id).all():
        db.session.delete(button)
        db.session.flush()
    db.session.query(Category).filter(Category.order > category.order).update({"order": Category.order - 1})
    db.session.delete(category)
    db.session.flush()


@category.patch("/{category_id}", response_model=CategoryUpdate)
def update_category(
    category_inp: CategoryUpdate,
    category_id: int,
    user=Depends(UnionAuth(['services.category.update'])),
):
    """Обновляет категорию

    Необходимые scopes: `services.category.update`
    """

    logger.info(f"User {user.get('id')} triggered update_category")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    last_category = db.session.query(Category).order_by(Category.order.desc()).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")

    if category_inp.scopes is not None:
        category.scopes = category_inp.scopes
        db.session.flush()

    if category_inp.order and category.order != category_inp.order:
        if last_category and (category_inp.order > last_category.order):
            raise HTTPException(
                status_code=400,
                detail=f"Can`t create category with order {category_inp.order}. "
                f"Last category is {last_category.order}",
            )

        swapping_category = db.session.query(Category).filter(Category.order == category_inp.order).one()
        swapping_category.order, category.order = category.order, swapping_category.order

    query = db.session.query(Category).filter(Category.id == category_id)
    update_values = category_inp.model_dump(exclude_unset=True, exclude_none=True, exclude={'scopes': True})
    if update_values:
        query.update(update_values)
    db.session.commit()
    return category


# endregion
