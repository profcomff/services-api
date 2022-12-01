from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db

from .models.category import CategoryCreate, CategoryUpdate, CategoryGet
from ..models.database import Category, Button

category = APIRouter(
    tags=["category"],
    responses={200: {"description": "Ok"}}
)


@category.post("/", response_model=CategoryCreate)
def create_category(category: CategoryCreate):
    db_category = Category(type=category.type, name=category.name)
    db.session.add(db_category)
    return db_category


@category.get("/", response_model=list[CategoryGet])
def get_categories(skip: int = 0, limit: int = 100):
    return db.session.query(Category).offset(skip).limit(limit).all()


@category.get("/{category_id}", response_model=CategoryGet)
def get_category(category_id: int):
    db_category = db.session.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return db_category


@category.delete("/")
def remove_category(category_id: int):
    db_category = get_category(category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    delete = db.session.query(Category).filter(Category.id == category_id).first()
    d = db.session.query(Button).filter(Button.category_id == category_id).all()
    for button in d:
        db.session.delete(button)
        db.session.flush()
    db.session.delete(delete)


@category.patch("/", response_model=CategoryUpdate)
def update_category(category: CategoryUpdate):
    db_old_category = get_category(db=db, category_id=category.id)
    if db_old_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return db.session.query(Category).update(category)
