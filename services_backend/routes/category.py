import logging
from typing import Literal

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_sqlalchemy import db
from pydantic import Field

from services_backend.models.database import Button, Category, Type
from services_backend.schemas import Base


logger = logging.getLogger(__name__)
category = APIRouter()


# region schemas


class ButtonGet(Base):
    id: int = Field(description='Айди кнопки')
    icon: str | None = Field(description='Иконка кнопки')
    name: str | None = Field(description='Название кнопки')
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: Type | None = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')


class CategoryCreate(Base):
    type: str = Field(description='Тип отображения категории')
    name: str = Field(description='Имя категории')
    scopes: set[str] | None = Field(description='Каким пользователям будет видна категория')


class CategoryUpdate(Base):
    order: int | None = Field(description='На какую позицию перенести категорию')
    type: str | None = Field(description='Тип отображения категории')
    name: str | None = Field(description='Имя категории')
    scopes: set[str] | None = Field(description='Каким пользователям будет видна категория')


class CategoryGet(Base):
    id: int
    order: int
    type: str | None
    name: str | None
    buttons: list[ButtonGet] | None
    scopes: list[str] | None


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
    category = Category(**category_inp.dict(exclude_none=True))
    if last_category:
        category.order = last_category.order + 1
    db.session.add(category)
    db.session.flush()
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

    user_scopes = set([scope["name"] for scope in user["session_scopes"]] if user else [])
    filtered_categories = []
    for category in db.session.query(Category).order_by(Category.order).all():
        category_scopes = set(category.scopes)
        if (category_scopes == set()) or (user_scopes & category_scopes):
            filtered_categories.append(category)

    return [
        CategoryGet.from_orm(row).dict(exclude={"buttons"} if 'buttons' not in info else {})
        for row in filtered_categories
    ]


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
    if not category or (category.scopes and len(category.scopes - user_scopes) == 0):
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

    if category_inp.order:
        if category_inp.order < 1:
            raise HTTPException(status_code=400, detail="Order can`t be less than 1")
        if last_category and (category_inp.order > last_category.order):
            raise HTTPException(
                status_code=400,
                detail=f"Can`t create category with order {category_inp.order}. "
                f"Last category is {last_category.order}",
            )

        if category.order > category_inp.order:
            db.session.query(Category).filter(Category.order < category.order).update({"order": Category.order + 1})
        elif category.order < category_inp.order:
            db.session.query(Category).filter(Category.order > category.order).update({"order": Category.order - 1})

    query = db.session.query(Category).filter(Category.id == category_id)
    update_values = category_inp.dict(exclude_unset=True, exclude_none=True, exclude={'scopes': True})
    if update_values:
        query.update(**update_values)
    db.session.commit()
    return category


# endregion
