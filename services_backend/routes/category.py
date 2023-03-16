import logging
from typing import Literal

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_sqlalchemy import db

from ..models.database import Button, Category
from .models.category import CategoryCreate, CategoryGet, CategoryUpdate


logger = logging.getLogger(__name__)
category = APIRouter()


@category.post("/", response_model=CategoryGet)
def create_category(
    category_inp: CategoryCreate,
    user=Depends(UnionAuth(['services.category.create'])),
):
    """Создает категорию

    Необходимые scopes: `services.category.create`
    """
    logger.info(f"User {user} triggered create_category")
    last_category = db.session.query(Category).order_by(Category.order.desc()).first()
    category = Category(**category_inp.dict(exclude_none=True))
    if last_category:
        category.order = last_category.order + 1
    db.session.add(category)
    db.session.commit()
    return category


@category.get("/", response_model=list[CategoryGet], response_model_exclude_none=True)
def get_categories(
    info: list[Literal['buttons']] = Query([]),
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показывает список категорий

    Необходимые scopes: `-`
    """
    logger.info(f"User {user} triggered get_categories")
    return [
        CategoryGet.from_orm(row).dict(exclude={"buttons"} if 'buttons' not in info else {})
        for row in db.session.query(Category).order_by(Category.order).all()
    ]


@category.get("/{category_id}", response_model=CategoryGet, response_model_exclude_none=True)
def get_category(
    category_id: int,
    user=Depends(UnionAuth(allow_none=True, auto_error=False)),
):
    """Показывает категорию

    Необходимые scopes: `-`
    """
    logger.info(f"User {user} triggered get_category")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return {
        "id": category_id,
        "order": category.order,
        "name": category.name,
        "type": category.type,
    }


@category.delete("/{category_id}", response_model=None)
def remove_category(
    category_id: int,
    user=Depends(UnionAuth(['services.category.delete'])),
):
    """Удаляет категорию и все кнопки в ней

    Необходимые scopes: `services.category.delete`
    """
    logger.info(f"User {user} triggered remove_category")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    for button in db.session.query(Button).filter(Button.category_id == category_id).all():
        db.session.delete(button)
        db.session.flush()
    db.session.query(Category).filter(Category.order > category.order).update({"order": Category.order - 1})
    db.session.delete(category)
    db.session.commit()


@category.patch("/{category_id}", response_model=CategoryUpdate)
def update_category(
    category_inp: CategoryUpdate,
    category_id: int,
    user=Depends(UnionAuth(['services.category.update'])),
):
    """Обновляет категорию

    Необходимые scopes: `services.category.update`
    """
    logger.info(f"User {user} triggered update_category")
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    last_category = db.session.query(Category).order_by(Category.order.desc()).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    if not any(category_inp.dict().values()):
        raise HTTPException(status_code=400, detail="Empty schema")

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
    query.update(category_inp.dict(exclude_unset=True, exclude_none=True))
    db.session.commit()
    return category
