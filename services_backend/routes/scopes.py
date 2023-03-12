from fastapi import HTTPException, APIRouter
from fastapi_sqlalchemy import db

from .models.scope import ScopeGet, ScopeCreate, ScopeUpdate
from ..models.database import Scope

scope = APIRouter()


@scope.post("/", response_model=ScopeGet)
def create_scope(scope_inp: ScopeCreate):
    scope = Scope(**scope_inp.dict(exclude_none=True))
    db.session.add(scope)
    db.session.commit()
    return scope


@scope.get("/", response_model=list[ScopeGet])
def get_scopes(offset: int = 0, limit: int = 100):
    return db.session.query(Scope).offset(offset).limit(limit).all()


@scope.get("/{scope_id}", response_model=ScopeGet)
def get_scope(scope_id: int):
    scope = db.session.query(Scope).filter(Scope.id == scope_id).one_or_none()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope does not exist")
    return scope


@scope.delete("/{scope_id}", response_model=None)
def delete_scope(scope_id: int):
    scope = db.session.query(Scope).filter(Scope.id == scope_id).one_or_none()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope does not exist")
    db.session.delete(scope)
    db.session.commit()


@scope.patch("/{scope_id}", response_model=ScopeUpdate)
def update_scope(scope_inp: ScopeUpdate, scope_id: int):
    scope = db.session.query(Scope).filter(Scope.id == scope_id).one_or_none()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope does not exist")
    if not any(scope_inp.dict().values()):
        raise HTTPException(status_code=400, detail="Empty schema")

    query = db.session.query(Scope).filter(Scope.id == scope_id)
    query.update(scope_inp.dict(exclude_unset=True, exclude_none=True))
    db.session.commit()
    return scope