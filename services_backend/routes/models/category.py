from pydantic import Field

from .base import Base
from .button import ButtonGet
from .scope import ScopeGet


class CategoryCreate(Base):
    type: str = Field(description='Тип отображения категории')
    name: str = Field(description='Имя категории')


class CategoryUpdate(Base):
    order: int | None
    type: str | None
    name: str | None


class CategoryGet(Base):
    id: int
    order: int
    type: str | None
    name: str | None
    buttons: list[ButtonGet] | None
    scopes: list[ScopeGet] | None
