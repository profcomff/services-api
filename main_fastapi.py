from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from __init__ import get_db, app
import methods
from models import CRUD


@app.post("/button/", response_model=CRUD.Button)
def create_button(button: CRUD.Button, db: Session = Depends(get_db)):
    db_button = methods.get_button(db, button_id=button.id)
    if db_button:
        raise HTTPException(status_code=409, detail='Button already exist')
    return methods.create_button(db=db, button=button)


@app.get("/button/", response_model=list[CRUD.Button])
def get_buttons(skip: int, limit: int, db: Session = Depends(get_db)):
    return methods.get_buttons(db, skip=skip, limit=limit)


@app.get("/button/{button_id}", response_model=CRUD.Button)
def get_button(button_id: int, db: Session = Depends(get_db)):
    db_button = methods.get_button(db, button_id)
    if db_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return db_button


@app.delete("/button/", response_model=CRUD.Button)
def remove_button(button_id: int, db: Session = Depends(get_db)):
    db_button = methods.get_button(db, button_id)
    if db_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return methods.delete_button(db=db, button_id=button_id)


@app.patch("/button/", response_model=CRUD.Button)
def update_button(button: CRUD.Button, db: Session = Depends(get_db)):
    db_old_button = get_button(button_id=button.id, db=db)
    if db_old_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return methods.update_button(db=db, button_id=button.id, button=button)


@app.post("/category/", response_model=CRUD.Category)
def create_category(category: CRUD.Category, db: Session = Depends(get_db)):
    db_category = methods.get_category(category_id=category.id, db=db)
    if db_category:
        raise HTTPException(status_code=409, detail="Category already exist")
    return methods.create_category(db=db, category=category)


@app.get("/category/", response_model=list[CRUD.Category])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return methods.get_categories(db, skip=skip, limit=limit)


@app.get("/category/{category_id}", response_model=CRUD.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = methods.get_category(category_id=category_id, db=db)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return db_category


@app.delete("/category/")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    db_category = methods.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return methods.delete_category(db=db, category_id=category_id)


@app.patch("/category/", response_model=CRUD.Category)
def update_category(category: CRUD.Category, db: Session = Depends(get_db)):
    db_old_category = methods.get_category(db=db, category_id=category.id)
    if db_old_category is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return methods.update_category(db=db, category_id=category.id, category=category)
