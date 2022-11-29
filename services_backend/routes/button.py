from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .models.button import ButtonCreate, ButtonUpdate, ButtonGet
from ..models.database import Button

button = APIRouter(
    prefix="/button",
    tags=["button"],
    responses={404: {"description": "You tried, but no"}}
)

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres:123@localhost:5432/Profcom')
Base.metadata.create_all(bind=engine)


# Да, без этого говна ничего не работает, я честно пытался
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@button.post("/", response_model=ButtonCreate)
def create_button(button: ButtonCreate, db: Session = Depends(get_db)):
    db_button = ButtonCreate(category_id=button.category_id, name=button.name,
                             icon=button.icon)
    db.add(db_button)
    db.commit()
    db.refresh(db_button)
    db.close()

    return db_button


@button.get("/", response_model=list[ButtonGet])
def get_buttons(skip: int, limit: int, db: Session = Depends(get_db)):
    return db.query(Button).offset(skip).limit(limit).all()


@button.get("/{button_id}", response_model=ButtonGet)
def get_button(button_id: int, db: Session = Depends(get_db)):
    return db.query(Button).filter(Button.id == button_id).first()


@button.delete("/")
def remove_button(button_id: int, db: Session = Depends(get_db)):
    db_button = get_button(button_id=button_id, db=db)
    if db_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    delete = db.query(Button).filter(Button.id == button_id).first()
    db.delete(delete)
    db.commit()
    db.close()


@button.patch("/", response_model=ButtonUpdate)
def update_button(button: ButtonUpdate, db: Session = Depends(get_db)):
    db_old_button = get_button(button_id=button.id, db=db)
    if db_old_button is None:
        raise HTTPException(status_code=404, detail="Button does not exist")
    return db.query(Button).update(button)
