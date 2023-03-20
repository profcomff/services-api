from fastapi import HTTPException, APIRouter, Depends
from fastapi_sqlalchemy import db

from auth_lib.fastapi import UnionAuth
from .models.scope import ScopeGet, ScopeCreate
from ..models.database import Scope

scope = APIRouter()


@scope.post("/", response_model=ScopeGet)
def create_scope(scope_inp: ScopeCreate, category_id: int, user=Depends(UnionAuth(['services.category.permission.create']))):
    scope = Scope(**{"name": scope_inp.name, "category_id": category_id})
    db.session.add(scope)
    db.session.flush()
    return scope


@scope.get("/", response_model=list[ScopeGet])
def get_scopes(category_id: int, offset: int = 0, limit: int = 100):
    return db.session.query(Scope).filter(category_id == Scope.category_id).offset(offset).limit(limit).all()


@scope.delete("/{scope_id}", response_model=None)
def delete_scope(category_id: int, scope_id: int, user=Depends(UnionAuth(['services.category.permission.delete']))):
    scope = db.session.query(Scope).filter(category_id == Scope.category_id).filter(Scope.id == scope_id).one_or_none()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope does not exist")
    db.session.delete(scope)
    db.session.flush()
