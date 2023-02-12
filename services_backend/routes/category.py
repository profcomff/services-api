from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db

from .models.category import CategoryCreate, CategoryUpdate, CategoryGet
from ..models.database import Category, Button

category = APIRouter()


@category.post("/", response_model=CategoryGet)
def create_category(category_inp: CategoryCreate):
    last_category = db.session.query(Category).order_by(Category.order.desc()).first()
    category = Category(**category_inp.dict())
    if last_category:
        category.order = last_category.order + 1
    else:
        category.order = 1
    db.session.add(category)
    db.session.commit()
    return category


@category.get("/", response_model=list[CategoryGet])
def get_categories(offset: int = 0, limit: int = 100):
    return db.session.query(Category).order_by(Category.order).offset(offset).limit(limit).all()


@category.get("/{category_id}", response_model=CategoryGet)
def get_category(category_id: int):
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return category


@category.delete("/{category_id}", response_model=None)
def remove_category(category_id: int):
    category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    delete = db.session.query(Category).filter(Category.id == category_id).one_or_none()
    for button in db.session.query(Button).filter(Button.category_id == category_id).all():
        db.session.delete(button)
        db.session.flush()
    db.session.query(Category) \
        .filter(Category.order > category.order) \
        .update({"order": Category.order - 1})
    db.session.delete(delete)
    db.session.commit()


@category.patch("/{category_id}", response_model=CategoryUpdate)
def update_category(category_inp: CategoryUpdate, category_id: int):
    category = db.session.query(Category).filter(Category.id == category_id)
    last_category = db.session.query(Category).order_by(Category.order.desc()).first()
    if not category.one_or_none():
        raise HTTPException(status_code=404, detail="Category does not exist")
    if not any(category_inp.dict().values()):
        raise HTTPException(status_code=400, detail="Empty schema")
    if category_inp.order < 1:
        raise HTTPException(status_code=400,
                            detail="Order can`t be less than 1")
    if last_category and (category_inp.order > last_category.order):
        raise HTTPException(status_code=400, detail=f"Can`t create category with order {category_inp.order}. "
                                                    f"Last category is {last_category.order}")

    if category.one().order > category_inp.order:
        db.session.query(Category) \
            .filter(Category.order < category.one().order) \
            .update({"order": Category.order + 1})
    elif category.one().order < category_inp.order:
        db.session.query(Category) \
            .filter(Category.order > category.one().order) \
            .update({"order": Category.order - 1})

    category.update(
        category_inp.dict(exclude_unset=True)
    )
    ret = category.one()
    db.session.commit()
    return ret
