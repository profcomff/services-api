from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from .models.category import CategoryCreate, CategoryUpdate, CategoryGet
from ..models.database import Category, Button

category = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={404: {"description": "You tried, but no"}}
)


# Да, без этого говна ничего не работает, я честно пытался
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@category.post("/", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryCreate(category_id=category.category_id,
                                 type=category.type, name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()

    return db_category


@category.get("/", response_model=list[CategoryGet])
def get_categories(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


@category.get("/{category_id}", response_model=CategoryGet)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return db_category


@category.delete("/")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    delete = db.query(Category).filter(Category.id == category_id).first()
    d = db.query(Button).filter(Button.category_id == category_id).all()
    for button in d:
        db.delete(button)
        db.commit()
    db.delete(delete)
    db.commit()
    db.close()


@category.patch("/", response_model=CategoryUpdate)
def update_category(category: CategoryUpdate, db: Session = Depends(get_db)):
    db_old_category = get_category(db=db, category_id=category.id)
    if db_old_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return db.query(Category).update(category)
