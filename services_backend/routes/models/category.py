from .base import Base
from .button import ButtonGet
from .scope import ScopeGet


class CategoryCreate(Base):
    type: str | None
    name: str | None


class CategoryUpdate(Base):
    order: int | None
    type: str | None
    name: str | None
    user_scope: list[str] | None


class CategoryGet(Base):
    id: int
    order: int
    type: str | None
    name: str | None
    buttons: list[ButtonGet] | None
    scopes: list[ScopeGet] | None
