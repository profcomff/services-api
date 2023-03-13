from fastapi import HTTPException, APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import or_

from ..settings import get_settings
from .models.category import CategoryCreate, CategoryGet, CategoryUpdate
from ..models.database import Category, Button, Scope

from auth_lib.fastapi import UnionAuth

category = APIRouter()


@category.post("/", response_model=CategoryGet, response_model_exclude_none=True)
def create_category(category_inp: CategoryCreate, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if not user:
        raise HTTPException(403, detail="Not authenticated")
    if "services.category.create" in [scope["name"] for scope in user["session_scopes"]]:
        last_category = db.session.query(Category).order_by(Category.order.desc()).first()
        category = Category(**category_inp.dict(exclude_none=True))
        if last_category:
            category.order = last_category.order + 1
        # category.scopes.append("services.category.create")
        # category.scopes.append("services.test.test1")
        db.session.add(category)
        db.session.commit()
        return category
    else:
        raise HTTPException(403, detail="Not authenticated")


@category.get("/", response_model=list[CategoryGet], response_model_exclude_none=True)
def get_categories(offset: int = 0, limit: int = 100, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL, allow_none=True))):
    if (offset < 0) or (limit < 0):
        raise HTTPException(400, detail="Offset or limit cant be negative")
    if user:
        return [
            CategoryGet.from_orm(row).dict(exclude={"buttons"})
            for row in db.session.query(Category).order_by(Category.order)
            .filter(or_(bool(db.session.query(Scope).filter(Scope.read_scope.in_([scope["name"] for scope in user["session_scopes"]])).all()), Category.scopes == None))
            .offset(offset).limit(limit).all()
        ]
    else:
        return [
            CategoryGet.from_orm(row).dict(exclude={"buttons"})
            for row in db.session.query(Category).order_by(Category.order)
            .filter(Category.scopes == None).offset(offset).limit(limit).all()
        ]


@category.get("/{category_id}", response_model=CategoryGet, response_model_exclude_none=True)
def get_category(category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if user:
        category = db.session.query(Category) \
                .filter(or_(bool(db.session.query(Scope).filter(Scope.read_scope.in_([scope["name"] for scope in user["session_scopes"]])).all()), Category.scopes == None)) \
                .filter(Category.id == category_id) \
                .one_or_none()
    else:
        category = db.session.query(Category) \
            .filter(Category.scopes == None) \
            .filter(Category.id == category_id) \
            .one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return {
        "id": category_id,
        "order": category.order,
        "name": category.name,
        "type": category.type,
        "scopes": category.scopes
    }


@category.delete("/{category_id}", response_model=None)
def remove_category(category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if not user:
        raise HTTPException(403, detail="Not authenticated")
    if "services.category.delete" in [scope["name"] for scope in user["session_scopes"]]:
        category = db.session.query(Category).filter(Category.id == category_id).one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category does not exist")
        for button in db.session.query(Button).filter(Button.category_id == category_id).all():
            db.session.delete(button)
            db.session.flush()
        db.session.query(Category).filter(Category.order > category.order).update({"order": Category.order - 1})
        db.session.delete(category)
        db.session.commit()
    else:
        raise HTTPException(403, detail="Not authenticated")


@category.patch("/{category_id}", response_model=CategoryUpdate)
def update_category(category_inp: CategoryUpdate, category_id: int, user: dict[str, str] = Depends(UnionAuth(get_settings().AUTH_URL))):
    if not user:
        raise HTTPException(403, detail="Not authenticated")
    if "services.category.update" in [scope["name"] for scope in user["session_scopes"]]:
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
    else:
        raise HTTPException(403, detail="Not authenticated")
